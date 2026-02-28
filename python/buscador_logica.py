import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from pathlib import Path

# Cargamos variables de entorno desde .env
load_dotenv()

# Instanciamos la conexión global
es = None
try:
    elastic_user = os.getenv("ELASTIC_USER", "elastic")
    es_password = os.getenv("ELASTIC_PASSWORD", "")
    es = Elasticsearch(
        "https://localhost:9200", 
        basic_auth=(elastic_user, es_password), 
        verify_certs=False # Solo porque es local y auto-firmado
    )
    # Verificar que realmente está conectado
    es.info()
except Exception as e:
    print(f"Advertencia: No se pudo conectar a Elasticsearch. Usará búsqueda en archivos locales. Error: {e}")
    es = None

def buscar_en_archivos_locales(query):
    """
    Búsqueda alternativa en archivos locales cuando Elasticsearch no está disponible.
    Busca el término en los nombres de archivo y contenido de texto plano.
    """
    resultados = []
    testfiles_path = Path(__file__).parent.parent / "testfiles"
    query_lower = query.lower()
    
    if not testfiles_path.exists():
        return resultados
    
    for file_path in testfiles_path.iterdir():
        if not file_path.is_file():
            continue
        
        titulo = file_path.name
        
        # Búsqueda en nombre de archivo
        if query_lower in titulo.lower():
            resultados.append({
                "titulo": titulo,
                "url": f"/ver_archivo/{titulo}",
                "descripcion": f"Encontrado en el nombre del archivo",
                "tipo": file_path.suffix[1:] if file_path.suffix else "desconocido"
            })
            continue
        
        # Para archivos de texto, buscar en el contenido
        if file_path.suffix in ['.txt', '.csv', '.md']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                    if query_lower in contenido.lower():
                        # Encontrar un fragmento del contenido
                        idx = contenido.lower().find(query_lower)
                        inicio = max(0, idx - 50)
                        fin = min(len(contenido), idx + 100)
                        fragmento = contenido[inicio:fin].strip()
                        
                        resultados.append({
                            "titulo": titulo,
                            "url": f"/ver_archivo/{titulo}",
                            "descripcion": f"... {fragmento} ...",
                            "tipo": file_path.suffix[1:] if file_path.suffix else "desconocido"
                        })
            except Exception as e:
                print(f"Error al leer {titulo}: {e}")
    
    return resultados

def buscar_informacion(query):
    """
    Toma la palabra a buscar (query) y retorna una lista de resultados 
    ejecutando una búsqueda en Elasticsearch (o fallback a búsqueda local).
    """
    query = query.strip()
    
    if not query:
        return []
    
    # Si Elasticsearch no está disponible, usar búsqueda alternativa
    if es is None:
        return buscar_en_archivos_locales(query)

    # Búsqueda profesional en Elasticsearch
    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                # Busca en title (máxima prioridad ^3), texto, etc.
                "fields": ["title^3", "fileName^2", "extractedText", "summary", "category^2", "tags"]
            }
        },
        # Highlight: devuelve los fragmentos de texto exactos donde aparece la palabra buscada
        "highlight": {
            "pre_tags": ["<mark>"],  # Puedes cambiar el tag HTML (por defecto es <em>)
            "post_tags": ["</mark>"],
            "fields": {
                "extractedText": {
                    "fragment_size": 150, # Cantidad de caracteres del fragmento
                    "number_of_fragments": 1 # Solo queremos mostrar la mejor coincidencia
                },
                "summary": {}
            }
        }
    }
    
    try:
        resultado = es.search(index="documentos_empresa", body=es_query)
        
        resultados_encontrados = []
        for hit in resultado['hits']['hits']:
            source = hit['_source']
            
            # Obtener el fragmento de texto donde hizo "match" (Highlighting)
            descripcion = ""
            
            # 1. Si la palabra apareció en el texto extraído, mostrar ese fragmento
            if 'highlight' in hit and 'extractedText' in hit['highlight']:
                descripcion = "... " + " ... ".join(hit['highlight']['extractedText']) + " ..."
            # 2. Si apareció en el resumen, mostramos ese
            elif 'highlight' in hit and 'summary' in hit['highlight']:
                descripcion = "... " + " ... ".join(hit['highlight']['summary']) + " ..."
            else:
                # 3. Si no hay highlight (ej: la encontró en el título), mostramos el primer pedacito del texto
                texto_completo = source.get('extractedText', '')
                descripcion = (texto_completo[:150] + "...") if texto_completo else "Este documento no contiene texto extraíble."

            # Preparamos el resultado para devolver a Flask
            resultados_encontrados.append({
                "titulo": source.get('fileName', 'Documento sin nombre'),
                "url": f"/ver_archivo/{source.get('fileName')}", 
                "descripcion": descripcion,
                # Podemos incluso devolver campos extra por si quisieras poner un badge de "PDF" o de "Categoría"
                "tipo": source.get('fileType', 'desconocido')
            })
            
        return resultados_encontrados
        
    except Exception as e:
        print(f"Error consultando Elasticsearch: {e}")
        # Fallback a búsqueda local si hay error
        resultados_locales = buscar_en_archivos_locales(query)
        if resultados_locales:
            return resultados_locales
        # Si nadie encuentra nada, devolver lista vacía en lugar de error
        return []
