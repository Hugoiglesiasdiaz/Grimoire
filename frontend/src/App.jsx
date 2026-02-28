import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [flashMessages, setFlashMessages] = useState([]);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...selectedFiles]);
    e.target.value = null; // Reset input
  };

  const removeFile = (indexToRemove) => {
    setFiles((prev) => prev.filter((_, index) => index !== indexToRemove));
  };

  const removeFlashMessage = (indexToRemove) => {
    setFlashMessages((prev) => prev.filter((_, index) => index !== indexToRemove));
  };

  const addFlashMessage = (message, type) => {
    setFlashMessages((prev) => [...prev, { message, type }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      addFlashMessage('Error: No se seleccionó ningún archivo.', 'error');
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('file', file);
    });

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      addFlashMessage(response.data.message, 'success');
      setFiles([]); // Clear files on success
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        addFlashMessage(error.response.data.error, 'error');
      } else {
        addFlashMessage('Error al intentar subir los archivos.', 'error');
      }
    }
  };

  return (
    <>
      <header>
        <nav>
          <h1>Grimoire</h1>
          <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/about">Acerca de</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <div className="page-layout">
          <div className="container main-content">
            {flashMessages.length > 0 && (
              <div className="flashes">
                {flashMessages.map((msg, index) => (
                  <div key={index} className={`flash ${msg.type}`}>
                    <span>{msg.message}</span>
                    <button
                      type="button"
                      className="close-btn"
                      onClick={() => removeFlashMessage(index)}
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>
            )}

            <h2>Bienvenido a Grimoire</h2>
            <p>Esta es una aplicación web impulsada por React servida mediante Flask.</p>
          </div>

          <aside className="upload-sidebar">
            <div className="upload-section">
              <h3>Subir Archivos</h3>
              <form onSubmit={handleSubmit}>
                <input
                  type="file"
                  multiple
                  onChange={handleFileChange}
                />
                <ul className="file-list">
                  {files.map((file, index) => (
                    <li key={index}>
                      <span>{file.name}</span>
                      <button
                        type="button"
                        className="remove-file-btn"
                        onClick={() => removeFile(index)}
                      >
                        &times;
                      </button>
                    </li>
                  ))}
                </ul>
                <button type="submit">Subir</button>
              </form>
            </div>
          </aside>
        </div>
      </main>

      <footer>
        <p>&copy; 2026 Grimoire. Todos los derechos reservados.</p>
      </footer>
    </>
  );
}

export default App;
