import React from 'react';
import {
  SearchProvider,
  WithSearch,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting
} from "@elastic/react-search-ui";
import { ErrorBoundary } from '@elastic/react-search-ui-views';
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import CustomAPIConnector from './CustomAPIConnector';
import UploadComponent from './UploadComponent';
import './App.css';

const connector = new CustomAPIConnector();

const config = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  searchQuery: {
    search_fields: {
      fileName: {},
      extractedText: {},
      summary: {}
    },
    result_fields: {
      fileName: { snippet: { size: 100, fallback: true } },
      summary: { snippet: { size: 200, fallback: true } },
      fileType: {},
      fileSize: {},
      uploadDate: {},
      category: {}
    }
  }
};

const formatBytes = (bytes) => {
  if (!bytes || bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const getFileIcon = (type) => {
  const icons = {
    pdf: '📄',
    xlsx: '📊',
    xls: '📊',
    docx: '📝',
    doc: '📝',
    png: '🖼️',
    jpg: '🖼️',
    jpeg: '🖼️',
    txt: '📃',
    csv: '📊',
  };
  return icons[type?.toLowerCase()] || '📁';
};

const CustomResultView = ({ result }) => {
  const fileType = result.fileType?.raw || '';
  const fileName = result.fileName?.raw || '';
  const summary = result.summary?.snippet || result.summary?.raw || '';
  const uploadDate = result.uploadDate?.raw ? new Date(result.uploadDate.raw).toLocaleDateString('es-ES') : '';
  const fileSize = formatBytes(result.fileSize?.raw);

  return (
    <li className="sui-result">
      <div className="sui-result__header">
        <span className="file-icon">{getFileIcon(fileType)}</span>
        <span
          className="sui-result__title"
          dangerouslySetInnerHTML={{ __html: result.fileName?.snippet || fileName }}
        />
        <span className="file-type-badge">{fileType.toUpperCase()}</span>
      </div>
      <div className="sui-result__body">
        <div className="sui-result__details">
          {summary && (
            <span
              className="sui-result__description"
              dangerouslySetInnerHTML={{ __html: summary }}
            />
          )}
          <ul className="sui-result__tags">
            {fileSize && <li><strong>Tamaño:</strong> {fileSize}</li>}
            {uploadDate && <li><strong>Subido:</strong> {uploadDate}</li>}
          </ul>
        </div>
      </div>
      <div className="sui-result__actions">
        <a
          href={`/files/${fileName}`}
          target="_blank"
          rel="noopener noreferrer"
          className="sui-download-btn"
        >
          ↓ Descargar
        </a>
      </div>
    </li>
  );
};

function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => (
          <div className="App">
            <header className="sui-header">
              <nav className="header-nav">
                <h1>Bienvenido a Grimoire</h1>
                <div className="search-box-container">
                  <SearchBox debounceLength={300} />
                </div>
              </nav>
            </header>

            <main className="sui-layout">
              <aside className="sui-layout-sidebar">
                <UploadComponent />
                <Sorting
                  label={"Ordenar por"}
                  sortOptions={[
                    { name: "Relevancia", value: "", direction: "" },
                    { name: "Título (A-Z)", value: "title", direction: "asc" },
                    { name: "Título (Z-A)", value: "title", direction: "desc" },
                    { name: "Fecha (Reciente)", value: "uploadDate", direction: "desc" },
                    { name: "Fecha (Antigua)", value: "uploadDate", direction: "asc" }
                  ]}
                />
              </aside>

              <div className="sui-layout-body">
                <ErrorBoundary>
                  <div className="sui-layout-header">
                    <div className="sui-layout-header__inner">
                      <PagingInfo />
                      <ResultsPerPage />
                    </div>
                  </div>
                  <div className="sui-layout-body__inner">
                    <Results resultView={CustomResultView} />
                  </div>
                  <div className="sui-layout-pagination">
                    <Paging />
                  </div>
                </ErrorBoundary>
              </div>
            </main>
          </div>
        )}
      </WithSearch>
    </SearchProvider>
  );
}

export default App;
