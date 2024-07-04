import os
import multiprocessing
import pandas as pd

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME


def get_existing_descriptions(client, collection_name, batch_size=5000):
    existing_descriptions = set()
    response, _ = client.scroll(
        collection_name=collection_name,
        limit=batch_size,
    )

    while response:
        existing_descriptions.update(hit.payload[TEXT_FIELD_NAME] for hit in response)
        response, _ = client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=response[-1].id
        )
    return existing_descriptions


def upload_embeddings(processed_file):
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    # Load the Parquet file into a DataFrame
    df = pd.read_parquet(processed_file)
    documents = df['documents'].tolist()
    embeddings = df['embeddings'].tolist()
    payload = df.drop(columns=['documents', 'embeddings']).to_dict(orient='records')

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params(on_disk=True),
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True
                )
            )
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=TEXT_FIELD_NAME,
            field_schema=models.TextIndexParams(
                type=models.TextIndexType.TEXT,
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=20,
                lowercase=True,
            )
        )

    existing_descriptions = get_existing_descriptions(client, COLLECTION_NAME)

    points = [
        PointStruct(
            vector=embedding,
            payload=meta
        )
        for doc, meta, embedding in zip(documents, payload, embeddings)
        if doc not in existing_descriptions
    ]

    if points:
        client.upload_points(
            collection_name=COLLECTION_NAME,
            points=tqdm(points, desc="Uploading points")
        )


if __name__ == '__main__':
    processed_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
    upload_embeddings(processed_file_)