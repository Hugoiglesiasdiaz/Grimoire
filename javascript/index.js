const list = document.getElementById('files-list');

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
        data.archivos.forEach(function(archivo, index) {
          const elementoLinea = document.createElement('li');
          const elementoLista = document.createElement('div');
          elementoLista.textContent = archivo.nombre;
          elementoLista.title = `${archivo.tamaño_kb} KB`;
          elementoLista.id = 'archivo-item-archivo' + index;

          const infoElementoLista = document.createElement('div');
          infoElementoLista.textContent = `${archivo.tamaño_kb} KB \r\n ${archivo.fecha_modificacion} \r\n ${archivo.tipo} \r\n ${archivo.ruta}`;
          infoElementoLista.style.display = 'none';
          infoElementoLista.className = "archivo-info";

          infoElementoLista.id = 'archivo-info-archivo' + index;
          

          elementoLinea.appendChild(elementoLista);
          elementoLinea.appendChild(infoElementoLista);
          list.appendChild(elementoLinea);


          elementoLista.onmouseover = function() {
            infoElementoLista.style.display = 'block';
          };
          elementoLista.onmouseout = function() {
            infoElementoLista.style.display = 'none';
          };
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