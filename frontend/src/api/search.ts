import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";

export type SearchRequest = {
    query: string;
    neural?: boolean;
    numResults?: number; // Add numResults parameter
}

export const getSearchResult = (searchRequest: SearchRequest) => {
    const params = {
        q: searchRequest.query,
        neural: searchRequest.neural,
        n_limit: searchRequest.numResults, // Pass numResults as n_limit
    }
    return Axios().get(SEARCH_URL, { params });
};
