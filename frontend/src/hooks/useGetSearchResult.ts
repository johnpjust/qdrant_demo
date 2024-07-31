import { getSearchResult } from '@/api/search';
import { StatusCodes } from 'http-status-codes';
import useMountedState from './useMountedState';

export type searchResponse = {
    result: {
        name: string;
        logo_url: string;
        alt: string;
        homepage_url: string;
        city: string;
        document: string;
        uuid: string;
    }[];
};


export const useGetSearchResult = () => {
  const [data, setData] = useMountedState<searchResponse | null>(null);
  const [error, setError] = useMountedState<string | null>(null);
  const [loading, setLoading] = useMountedState<boolean>(false);

  const getSearch = async (query: string, neural?: boolean, filters?: any, filterType?: string) => {
    try {
      setLoading(true);
      setError(null);
      const res = await getSearchResult({ query, neural, filters, filterType });

      switch (res.status) {
        case StatusCodes.OK: {
          const searchRes = res.data;
          setData(searchRes);
          break;
        }
        default: {
          setError("Failed to get Search Result");
        }
      }
    } catch {
      setError("Failed to get Search Result");
    } finally {
      setLoading(false);
    }
  };

  const resetData = () => {
    setData(null);
  };

  return { data, error, loading, getSearch, resetData };
};


/*********************************** old code ********************************/
// export const useGetSearchResult = () => {
// 	const [data, setData] = useMountedState<searchResponse | null>(null);
// 	const [error, setError] = useMountedState<string | null>(null);
// 	const [loading, setLoading] = useMountedState<boolean>(false);
//
// 	const getSearch = async (query: string,neural?:boolean) => {
// 		try {
// 			setLoading(true);
// 			setError(null);
// 			const res = await getSearchResult({ query,neural });
//
// 			switch (res.status) {
// 				case StatusCodes.OK: {
// 					const searchRes = res.data;
// 					setData(searchRes);
// 					break;
// 				}
// 				default: {
// 					setError('Failed to get Search Result');
// 				}
// 			}
// 		} catch {
// 			setError('Failed to get Search Result');
// 		} finally {
// 			setLoading(false);
// 		}
// 	};
//
// 	const resetData = () => {
// 		setData(null);
// 	};
//
// 	return { data, error, loading, getSearch, resetData };
// };
