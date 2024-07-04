import os
import multiprocessing
import pandas as pd

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME

def get_existing_descriptions_and_max_id(client, collection_name, batch_size=5000):
    existing_descriptions = set()
    max_id = 0
    response, _ = client.scroll(
        collection_name=collection_name,
        limit=batch_size,
    )

    while response:
        for hit in response:
            existing_descriptions.add(hit.payload[TEXT_FIELD_NAME])
            max_id = max(max_id, int(hit.id))
        response, _ = client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=response[-1].id
        )
    return existing_descriptions, max_id

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

    existing_descriptions, max_id = get_existing_descriptions_and_max_id(client, COLLECTION_NAME)

    points = [
        PointStruct(
            id=max_id + i + 1,  # Generate sequential ID
            vector=embedding,
            payload=meta
        )
        for i, (doc, meta, embedding) in enumerate(zip(documents, payload, embeddings))
        if doc not in existing_descriptions
    ]

    # if points:
    #     client.upload_points(
    #         collection_name=COLLECTION_NAME,
    #         points=tqdm(points, desc="Uploading points")
    #     )

    if points:
        successful_uploads = 0
        for point in tqdm(points, desc="Uploading points"):
            try:
                response = client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=[point]
                )
                if response.status == 'ok':
                    successful_uploads += 1
            except Exception as e:
                print(f"Failed to upload point {point.id}: {e}")

        print(f"Successfully uploaded {successful_uploads}/{len(points)} points")

if __name__ == '__main__':
    processed_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
    upload_embeddings(processed_file_)
