import React, { useState } from 'react';
import axios from 'axios';

function UploadComponent() {
    const [files, setFiles] = useState([]);
    const [messages, setMessages] = useState([]);

    const handleFileChange = (e) => {
        setFiles(Array.from(e.target.files));
    };

    const removeFile = (index) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    const removeMessage = (index) => {
        setMessages(messages.filter((_, i) => i !== index));
    };

    const handleUpload = async (e) => {
        e.preventDefault();

        if (files.length === 0) {
            setMessages([{ type: 'error', text: 'No se seleccionó ningún archivo.' }]);
            return;
        }

        const formData = new FormData();
        files.forEach((file) => formData.append('file', file));

        try {
            const response = await axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setMessages([{ type: 'success', text: response.data.message }]);
            setFiles([]);
            // Clear input manually if needed using a ref, but resetting state drops the list preview.
            document.getElementById("file-upload-input").value = null;
        } catch (error) {
            setMessages([
                {
                    type: 'error',
                    text: error.response?.data?.error || 'Hubo un error al subir los archivos.'
                }
            ]);
        }
    };

    return (
        <div className="upload-section">
            <h3>Subir Archivo</h3>

            {messages.length > 0 && (
                <div className="flashes">
                    {messages.map((msg, index) => (
                        <div key={index} className={`flash ${msg.type}`}>
                            {msg.text}
                            <button
                                type="button"
                                className="close-btn"
                                onClick={() => removeMessage(index)}
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}

            <form onSubmit={handleUpload}>
                <input
                    id="file-upload-input"
                    type="file"
                    multiple
                    onChange={handleFileChange}
                />

                {files.length > 0 && (
                    <ul className="file-list">
                        {files.map((file, i) => (
                            <li key={i}>
                                {file.name}
                                <button
                                    type="button"
                                    className="remove-file-btn"
                                    onClick={() => removeFile(i)}
                                    title="Eliminar archivo"
                                >
                                    ×
                                </button>
                            </li>
                        ))}
                    </ul>
                )}

                <button type="submit" className="upload-submit-btn">
                    Subir
                </button>
            </form>
        </div>
    );
}

export default UploadComponent;
