const list = document.getElementById('list');

document.addEventListener("DOMContentLoaded", (event) => {
  // Usar fetch para obtener la lista de archivos
  fetch('/read-files')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Verificar que la respuesta contiene archivos
      if (data && data.archivos && Array.isArray(data.archivos)) {
        // Limpiar la lista anterior (si existe)
        list.innerHTML = '';
        
        // Iterar sobre cada archivo y crear un elemento de lista
        data.archivos.forEach(function(archivo) {
          const elementoLista = document.createElement('li');
          elementoLista.textContent = archivo.nombre;
          elementoLista.title = `${archivo.tamaño_kb} KB`; // Mostrar tamaño al pasar el mouse
          list.appendChild(elementoLista);
        });
        
        console.log(`Se cargaron ${data.total_archivos} archivos`);
      } else {
        console.error('Respuesta JSON no válida o sin archivos');
      }
    })
    .catch(error => {
      console.error('Error al cargar los archivos:', error);
      const errorLi = document.createElement('li');
      errorLi.textContent = 'Error al cargar los archivos: ' + error.message;
      list.appendChild(errorLi);
    });
});