import axios from 'axios';

class CustomAPIConnector {
    async onSearch(state, queryConfig) {
        const { searchTerm, filters, current, resultsPerPage, sortList } = state;

        try {
            const response = await axios.post('/api/search', {
                searchTerm,
                filters,
                current,
                resultsPerPage,
                sort: sortList,
            });

            return {
                results: response.data.results,
                totalPages: response.data.meta.page.total_pages,
                totalResults: response.data.meta.page.total_results,
                facets: response.data.facets
            };
        } catch (error) {
            console.error("Search error:", error);
            return {
                results: [],
                totalPages: 0,
                totalResults: 0,
                facets: {}
            };
        }
    }

    async onAutocomplete(state, queryConfig) {
        // Basic implementation that just uses onSearch for simplicity
        const searchResponse = await this.onSearch(state, queryConfig);
        return {
            autocompletedResults: searchResponse.results
        };
    }
}

export default CustomAPIConnector;
