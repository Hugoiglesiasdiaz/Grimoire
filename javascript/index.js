const list = document.getElementById('files-list');

const fileInput = document.getElementById('fileInput');

let dataTransfer = new DataTransfer();

fileInput.addEventListener('change', function () {

  for (let i = 0; i < this.files.length; i++) {
        dataTransfer.items.add(this.files[i]);
    }
    fileInput.files = dataTransfer.files;

  });

document.addEventListener("DOMContentLoaded", (event) => {
  fetch('/read-files')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data && data.archivos && Array.isArray(data.archivos)) {
        list.innerHTML = '';
        
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