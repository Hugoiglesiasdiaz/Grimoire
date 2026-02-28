import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Instanciar entorno
elastic_user = os.getenv("ELASTIC_USER", "elastic")
es_password = os.getenv("ELASTIC_PASSWORD", "bJFeJexM3flXhJVfZEPX")

# Conexión profesional usando el usuario y contraseña del archivo .env
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(elastic_user, es_password),
    verify_certs=False # Solo falso en local porque el certificado es auto-firmado
)

index_name = "documentos_empresa"

# Mapeo estricto profesional con los campos definidos por el usuario
mapping = {
    "mappings": {
        "properties": {
            # 1. Metadata básica (obligatoria)
            "id": { "type": "long" },
            "title": { "type": "text", "analyzer": "standard" }, # Título separado por palabras para el buscador
            "fileName": { "type": "keyword" }, # keyword = no se separa en palabras, exacto
            "originalFileName": { "type": "keyword" },
            "fileType": { "type": "keyword" }, # pdf, xlsx
            "fileSize": { "type": "long" },
            "uploadDate": { "type": "date" },
            "filePath": { "type": "keyword" }, # ruta en servidor
            
            # 2. Información de extracción de texto
            # Text = se analiza, se divide en palabras, se quitan plurales, etc.
            "extractedText": { "type": "text", "analyzer": "standard" },
            "textLength": { "type": "integer" },
            
            # 3. Datos generados por IA (MUY IMPORTANTE)
            "summary": { "type": "text", "analyzer": "standard" },
            "category": { "type": "keyword" },
            "tags": { "type": "keyword" }, # Para JSON de strings (tags), keyword funciona perfecto (será una lista)
            "aiProcessed": { "type": "boolean" },
            "aiProcessedDate": { "type": "date" }
        }
    }
}

# Recreamos el índice con sus nuevas reglas (Borra el viejo si existe)
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Índice antiguo '{index_name}' eliminado para aplicar los cambios.")

es.indices.create(index=index_name, body=mapping)
print(f"Índice nuevo '{index_name}' creado con éxito.")
