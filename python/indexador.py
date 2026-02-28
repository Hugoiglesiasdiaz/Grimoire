import os
from datetime import datetime
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import fitz  # PyMuPDF para leer archivos PDF

# Cargar variables de entorno
load_dotenv()
elastic_user = os.getenv("ELASTIC_USER", "elastic")
es_password = os.getenv("ELASTIC_PASSWORD", "")

# Conexión local a Elasticsearch (igual que en setup_indice)
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(elastic_user, es_password),
    verify_certs=False
)

def indexar_archivos_test():
    print("Iniciando indexación de archivos de prueba...")
    
    # Buscamos la carpeta testfiles (subimos un nivel desde la carpeta python)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    testfiles_dir = os.path.join(directorio_actual, '..', 'testfiles')
    
    # Comprobamos que el directorio exista
    if not os.path.exists(testfiles_dir):
        print(f"Error: No se encuentra el directorio {testfiles_dir}")
        return

    archivos = os.listdir(testfiles_dir)
    index_name = "documentos_empresa"
    
    for i, file_name in enumerate(archivos, start=1):
        file_path = os.path.join(testfiles_dir, file_name)
        
        # Ignoramos si es un directorio
        if not os.path.isfile(file_path):
            continue
            
        # 1. Metadata básica (obligatoria)
        file_size = os.path.getsize(file_path)
        file_extension = file_name.split('.')[-1].lower() if '.' in file_name else 'desconocido'
        
        # Generar un "Titulo" limpio que la gente sí pueda buscar 
        nombre_sin_ext = file_name.rsplit('.', 1)[0] if '.' in file_name else file_name
        titulo_limpio = nombre_sin_ext.replace('_', ' ').replace('-', ' ')
        
        # 2. Información de extracción de texto
        # Por defecto, ponemos este texto por si es un archivo que no sabemos leer (ej. imágenes, excels sin instalar nada aún)
        extracted_text = f"Contenido indexado automáticamente de: {file_name}. (Lectura simulada para test)."
        
        if file_extension in ['txt', 'csv']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read(50000)
            except Exception as e:
                print(f"No se pudo leer {file_name} como texto: {e}")
                
        elif file_extension == 'pdf':
            try:
                pdf_doc = fitz.open(file_path)
                texto_paginas = []
                for pagina in pdf_doc:
                    # Extraer texto de cada página
                    texto_paginas.append(pagina.get_text())
                
                texto_unido = "\n".join(texto_paginas)
                if texto_unido.strip(): # Si logramos extraer texto real
                    extracted_text = texto_unido
                
                pdf_doc.close()
            except Exception as e:
                print(f"Error extrayendo datos del PDF {file_name}: {e}")
                
        text_length = len(extracted_text)
        
        # 3. Construimos el documento con TODOS los campos de la tabla que definimos en el mapping
        documento = {
            "id": i,
            "title": titulo_limpio,
            "fileName": file_name,
            "originalFileName": file_name,
            "fileType": file_extension,
            "fileSize": file_size,
            "uploadDate": datetime.now().isoformat(),
            "filePath": f"/testfiles/{file_name}",
            
            "extractedText": extracted_text,
            "textLength": text_length,
            
            # Datos simulados de IA
            "summary": f"Resumen IA para {file_name}: Un documento vital sobre desarrollo tecnológico y facturación.",
            "category": "Operaciones",
            "tags": ["empresarial", file_extension, "2024"],
            "aiProcessed": True,
            "aiProcessedDate": datetime.now().isoformat()
        }
        
        try:
            # Enviamos el documento a Elasticsearch usando el nombre del archivo como ID único
            # Esto evita duplicados: si ya existe, lo actualiza ('updated'), si no, lo crea ('created').
            resp = es.index(index=index_name, id=file_name, document=documento)
            print(f"OK [{i}/{len(archivos)}] {file_name} -> {resp['result']}")
        except Exception as e:
            print(f"ERROR al indexar {file_name}: {e}")

    print("Proceso finalizado.")

if __name__ == "__main__":
    indexar_archivos_test()