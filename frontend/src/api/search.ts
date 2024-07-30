import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";

export type SearchRequest = {
  query: string;
  neural?: boolean;
  filters?: {
    name?: string;
    alt?: string;
    city?: string;
    document?: string;
  };
  filterType?: string;
};

export const getSearchResult = (searchRequest: SearchRequest) => {
  const params = {
    q: searchRequest.query,
    neural: searchRequest.neural,
    filters: searchRequest.filters,
    filterType: searchRequest.filterType,
  };
  return Axios().get(SEARCH_URL, { params });
};


/******************************* old code ****************************** */
// export type SearchRequest = {
//     query: string;
//     neural?: boolean;
// }
//
// export const getSearchResult = (searchRequest:SearchRequest) => {
//     const params = {
//         q: searchRequest.query,
//         neural: searchRequest.neural
//     }
//     return Axios().get(SEARCH_URL, { params });
// };
