async function buscar(event) {
    event.preventDefault();

    const searchBox = document.getElementById('search-box');
    const query = searchBox.value.trim();
    const resultadosDiv = document.getElementById('resultados');

    if (query !== '') {
        console.log('Buscando en API local:', query);
        resultadosDiv.innerHTML = '<p>Buscando...</p>';

        try {
            const response = await fetch(`/api/buscar?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            resultadosDiv.innerHTML = '';

            if (data.length === 0) {
                resultadosDiv.innerHTML = '<p>No se encontraron resultados.</p>';
            } else {
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'resultado-item';

                    const h3 = document.createElement('h3');
                    h3.className = 'resultado-titulo';
                    
                    const a = document.createElement('a');
                    a.href = item.url;
                    a.textContent = item.titulo;
                    h3.appendChild(a);

                    const p = document.createElement('p');
                    p.className = 'resultado-descripcion';
                    p.textContent = item.descripcion;

                    div.appendChild(h3);
                    div.appendChild(p);
                    resultadosDiv.appendChild(div);
                });
            }
        } catch (error) {
            console.error('Error al realizar la búsqueda:', error);
            const errorMessage = document.createElement('p');
            errorMessage.style.color = 'red';
            errorMessage.textContent = 'Ocurrió un error al contactar al servidor.';
            resultadosDiv.appendChild(errorMessage);
        }
    } else {
        const errorMessageOut = document.createElement('p');
        errorMessageOut.textContent = 'Por favor, escribe algo para buscar.';
        errorMessageOut.style.color = 'red';
        resultadosDiv.appendChild(errorMessageOut);
    }
}