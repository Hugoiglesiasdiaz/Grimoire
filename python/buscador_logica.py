import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Cargamos variables de entorno desde .env
load_dotenv()

# Instanciamos la conexión global
try:
    elastic_user = os.getenv("ELASTIC_USER", "elastic")
    es_password = os.getenv("ELASTIC_PASSWORD", "")
    es = Elasticsearch(
        "https://localhost:9200", 
        basic_auth=(elastic_user, es_password), 
        verify_certs=False # Solo porque es local y auto-firmado
    )
except Exception as e:
    print("Advertencia: No se pudo instanciar Elasticsearch al iniciar el módulo. Verifica tus credenciales.")
    es = None

def buscar_informacion(query):
    """
    Toma la palabra a buscar (query) y retorna una lista de resultados 
    ejecutando una búsqueda avanzada y con formato en Elasticsearch.
    """
    query = query.strip()
    
    # Si la búsqueda está vacía, no devolvemos nada
    if not query:
        return []
    
    if es is None:
        return [{
            "titulo": "Error del sistema",
            "url": "#",
            "descripcion": "El cliente de Elasticsearch no está configurado correctamente."
        }]

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
        return [{
            "titulo": "Error en el Buscador",
            "url": "#",
            "descripcion": "No se pudo conectar con el motor de búsqueda local."
        }]
