import json
from pathlib import Path

def read_files():

    testfiles_path = Path(__file__).parent.parent / "testfiles"
    files_list = []
    
    if not testfiles_path.exists():
        return json.dumps({"error": "La carpeta testfiles no existe", "files": []})
    
    for file_path in testfiles_path.iterdir():
        if file_path.is_file():
            file_info = {
                "nombre": file_path.name,
                "tamaño_bytes": file_path.stat().st_size,
                "tamaño_kb": round(file_path.stat().st_size / 1024, 2),
                "extensión": file_path.suffix,
                "ruta": str(file_path)
            }
            files_list.append(file_info)
    
    result = {
        "total_archivos": len(files_list),
        "archivos": sorted(files_list, key=lambda x: x["nombre"])
    }
    
    return json.dumps(result, indent=2, ensure_ascii=False)
