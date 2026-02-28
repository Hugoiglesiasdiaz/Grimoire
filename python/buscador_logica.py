import os

def buscar_informacion(query):
    """
    Toma la palabra a buscar (query) y retorna una lista de resultados 
    leyendo los archivos de la carpeta 'testfiles'.
    """
    resultados_encontrados = []
    
    # 1. Limpiamos y convertimos la palabra a minúsculas
    query = query.strip().lower()
    
    # Si la búsqueda está vacía, no devolvemos nada
    if not query:
        return []
        
    # 2. Obtenemos la ruta absoluta hacia la carpeta testfiles
    # __file__ es la ruta de este archivo (ej: c:/.../python/buscador_logica.py)
    # Por lo que subimos un nivel (..) para llegar a la raíz y de ahí a testfiles
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_actual)
    ruta_testfiles = os.path.join(ruta_raiz, 'testfiles')
    
    # 3. Buscamos nombres de archivos en el directorio
    try:
        archivos = os.listdir(ruta_testfiles)
        
        for nombre_archivo in archivos:
            
            # Solo vamos a revisar archivos, no carpetas
            if os.path.isfile(os.path.join(ruta_testfiles, nombre_archivo)):
                nombre_min = nombre_archivo.lower()
                
                # ¿La palabra buscada forma parte del nombre del archivo?
                if query in nombre_min:
                    
                    # Lo preparamos para que la API lo devuelva
                    resultado_formateado = {
                        "titulo": nombre_archivo,
                        "url": f"/ver_archivo/{nombre_archivo}", # Enlace ficticio por ahora
                        "descripcion": f"Documento ubicado en la carpeta testfiles."
                    }
                    resultados_encontrados.append(resultado_formateado)
                    
    except FileNotFoundError:
        # En caso de que la carpeta testfiles no exista, devolvemos este mensaje de error "falso" en el HTML
        return [{
            "titulo": "Error en servidor",
            "url": "#",
            "descripcion": "La carpeta testfiles no existe o la ruta está mal configurada."
        }]
        
    return resultados_encontrados
