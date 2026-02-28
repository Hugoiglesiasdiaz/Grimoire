# Grimoire - Aplicación Web en Python

Una aplicación web simple construida con Flask.

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar la aplicación:

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Estructura del Proyecto

```
Grimoire/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias del proyecto
├── templates/          # Plantillas HTML
│   ├── index.html
│   └── about.html
├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   └── style.css
└── README.md          # Este archivo
```

## Rutas Disponibles

- `/` - Página de inicio
- `/about` - Página acerca de

## Elastic Search

- Usuario y contraseña en .env.
- Descargar elastic search en https://www.elastic.co/downloads/elasticsearch
- Descomprimir y ejecutar el archivo binario carpeta bin.
- Apuntar contraseña que genere,aparece solo en la primera ejecución.
- Luego en el .venv del proyecto ejecutar: python setup_indice.py
- Inicializa el indice en elastic search.
- Luego en el .venv del proyecto ejecutar: python indexador.py
- Inicializa la indexación de archivos de prueba.
- Luego en el .venv del proyecto ejecutar: python app.py
- Inicia la aplicación web.