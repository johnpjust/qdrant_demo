import time
from typing import List, Dict, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter
from qdrant_demo.config import QDRANT_URL, QDRANT_API_KEY, EMBEDDINGS_MODEL

# from qdrant_client.models import SearchParams, QuantizationSearchParams
# from fastembed import TextEmbedding
# model = TextEmbedding(EMBEDDINGS_MODEL)  # Initialize the FastEmbed model
# dense_vector_name = 'fast-' + str.lower(EMBEDDINGS_MODEL.split(('/'))[-1])


class NeuralSearcher:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)
        self.qdrant_client.set_model(EMBEDDINGS_MODEL, cache_dir='./local_cache/')

    def search(self, text: str, filter_: Optional[dict] = None, n_limit=5) -> List[dict]:
        start_time = time.time()
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=Filter(**filter_) if filter_ else None,
            limit=n_limit
        )
        print(f"Search took {time.time() - start_time} seconds")
        return [hit.metadata for hit in hits]


    # def search2(self, text: str, filter_: dict = None, n_limit=5) -> List[dict]:
    #     start_time = time.time()
    #     hits = self.qdrant_client.search(
    #         collection_name=self.collection_name,
    #         query_vector={dense_vector_name: list(model.embed([text]))[0]},
    #         query_filter=Filter(**filter_) if filter_ else None,
    #         search_params=SearchParams(hnsw_df=128, exact=False,
    #                                    quantization=QuantizationSearchParams(rescore=False, oversampling=1.0)),
    #         limit=n_limit
    #     )
    #     print(f"Search took {time.time() - start_time} seconds")
    #     return [hit.metadata for hit in hits]
