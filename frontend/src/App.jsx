import React, { useState } from 'react';
import axios from 'axios';
import { ErrorBoundary } from '@elastic/react-search-ui-views';
import {
  SearchProvider,
  WithSearch,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Facet,
  Sorting
} from "@elastic/react-search-ui";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import CustomAPIConnector from './CustomAPIConnector';
import UploadComponent from './UploadComponent';
import './App.css';

const connector = new CustomAPIConnector();

const config = {
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      title: {},
      description: {}
    },
    result_fields: {
      title: { snippet: { size: 100, fallback: true } },
      description: { snippet: { size: 100, fallback: true } },
      states: {},
      visitors: {},
      world_heritage_site: {},
      image_url: {}
    },
    facets: {
      states: { type: "value", size: 30 },
      world_heritage_site: { type: "value" }
    }
  },
  autocompleteQuery: {
    results: {
      resultsPerPage: 5,
      search_fields: {
        title: { weight: 3 }
      },
      result_fields: {
        title: { snippet: { size: 100, fallback: true } }
      }
    }
  }
};

const CustomResultView = ({ result, onClickLink }) => {
  return (
    <li className="sui-result">
      <div className="sui-result__header">
        <span
          className="sui-result__title"
          dangerouslySetInnerHTML={{ __html: result.title.snippet }}
        />
      </div>
      <div className="sui-result__body">
        <div className="sui-result__image">
          <img src={result.image_url.raw} alt={result.title.raw} />
        </div>
        <div className="sui-result__details">
          <span
            className="sui-result__description"
            dangerouslySetInnerHTML={{ __html: result.description.snippet }}
          />
          <ul className="sui-result__tags">
            <li>
              <strong>State(s):</strong> {result.states.raw.join(", ")}
            </li>
            <li>
              <strong>Visitors:</strong> {result.visitors.raw.toLocaleString()}
            </li>
            <li>
              <strong>World Heritage:</strong>{" "}
              {result.world_heritage_site.raw.toString() === "true" ? "Yes" : "No"}
            </li>
          </ul>
        </div>
      </div>
    </li>
  );
};


function App() {
  const [wasSearched, setWasSearched] = useState(false);

  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => (
          <div className="App">
            <header className="sui-header">
              <nav className="header-nav">
                <h1>Bienvenido a Grimoire</h1>
                <div className="search-box-container">
                  <SearchBox
                    autocompleteResults={{
                      titleField: "title",
                      urlField: "nps_link"
                    }}
                    autocompleteSuggestions={true}
                    debounceLength={0}
                  />
                </div>
              </nav>
            </header>

            <main className="sui-layout">
              <aside className="sui-layout-sidebar">
                <UploadComponent />
                <Sorting
                  label={"Sort by"}
                  sortOptions={[
                    { name: "Relevance", value: "", direction: "" },
                    { name: "Title", value: "title", direction: "asc" },
                    { name: "Visitors", value: "visitors", direction: "desc" }
                  ]}
                />
                <Facet
                  field="states"
                  label="States"
                  filterType="any"
                  isFilterable={true}
                />
                <Facet
                  field="world_heritage_site"
                  label="World Heritage Site"
                  view={({ options, onSelect, onRemove }) => (
                    <div className="sui-facet">
                      <div className="sui-facet__title">World Heritage Site</div>
                      <div className="sui-facet-search">
                        {options.map((option) => (
                          <label key={option.value} className="sui-multi-checkbox-facet__option-label">
                            <input
                              type="checkbox"
                              className="sui-multi-checkbox-facet__checkbox"
                              checked={option.selected}
                              onChange={() =>
                                option.selected
                                  ? onRemove(option.value)
                                  : onSelect(option.value)
                              }
                            />
                            {option.value === "true" ? "Yes" : "No"} ({option.count})
                          </label>
                        ))}
                      </div>
                    </div>
                  )}
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
