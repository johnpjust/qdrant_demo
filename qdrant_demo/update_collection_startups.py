import os
import pandas as pd
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL

dense_vector_name = 'fast-' + str.lower(EMBEDDINGS_MODEL.split(('/'))[-1])

def get_existing_entries(client, collection_name, batch_size=5000):
    existing_entries = set()
    max_id = 0
    response, next_offset = client.scroll(
        collection_name=collection_name,
        limit=batch_size,
    )

    while response:
        print(f"Scroll response: {len(response)} hits")
        for hit in response:
            print(f"Processing hit: {hit.id}")
            if TEXT_FIELD_NAME in hit.payload:
                entry_key = (hit.payload.get('name'), hit.payload.get('logo_url'), hit.payload.get('homepage_url'))
                existing_entries.add(entry_key)
            else:
                print(f"Missing fields in payload: {hit.payload}")
            max_id = max(max_id, int(hit.id))

        if next_offset is None:
            break  # No more results to process

        try:
            response, next_offset = client.scroll(
                collection_name=collection_name,
                limit=batch_size,
                offset=next_offset
            )
        except Exception as e:
            print(f"Error during scroll: {e}")
            break
    return existing_entries, max_id

def upload_embeddings(processed_file):
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    # Load the Parquet file into a DataFrame
    df = pd.read_parquet(processed_file)
    print("DataFrame loaded from Parquet file:")
    # print(df.head())  # Print the first few rows for inspection

    embeddings = df['embeddings'].tolist()
    df = df.rename(columns={'documents':'document'})
    payload = df.drop(columns=['embeddings']).to_dict(orient='records')

    # TODO: use sparse vectors or hybrid search: https://qdrant.tech/documentation/tutorials/hybrid-search-fastembed/
    # TODO: decide if we should use multiple vector embeddings (e.g. for job titles and questions separately)
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            sparse_vectors_config={},
            vectors_config={
                dense_vector_name: VectorParams(size=len(embeddings[0]),  # Ensure this matches the actual vector size
                                                distance=Distance.COSINE,
                                                hnsw_config=None,
                                                quantization_config=models.ScalarQuantization(
                                                    scalar=models.ScalarQuantizationConfig(
                                                        type=models.ScalarType.INT8,
                                                        quantile=0.99,
                                                        always_ram=True
                                                    )),
                                                on_disk=True,
                                                datatype=None,
                                                multivector_config=None),
            },
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=TEXT_FIELD_NAME,
            field_schema=models.TextIndexParams(
                type=models.TextIndexType.TEXT,
                tokenizer=models.TokenizerType.PREFIX,
                min_token_len=2,
                max_token_len=20,
                lowercase=True,
            )
        )

        #TODO: create payload indexes for date and job title

    existing_entries, max_id = get_existing_entries(client, COLLECTION_NAME)
    print(f"Existing entries count: {len(existing_entries)}")
    print(f"Max ID: {max_id}")

    # TODO: use sparse vectors --> https://qdrant.tech/articles/sparse-vectors/

    points = [
        PointStruct(
            id=max_id + i + 1,  # Generate sequential ID
            vector={dense_vector_name: embedding},
            payload=meta
        )
        for i, (meta, embedding) in enumerate(zip(payload, embeddings))
        if (meta['name'], meta['logo_url'], meta['homepage_url']) not in existing_entries
    ]

    client.update_collection(
        collection_name=COLLECTION_NAME,
        optimizer_config=models.OptimizersConfigDiff(indexing_threshold=0),
    )

    if points:
        # Use list comprehension to create a progress bar compatible list of points
        points_with_progress = [point for point in tqdm(points, desc="Uploading points")]

        response = client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_with_progress,
        )

        # Check for completion status explicitly
        if response.status == models.UpdateStatus.COMPLETED:
            print("Points uploaded successfully.")
        else:
            print(f"Failed to upload points: {response}")

        # Force indexing after upserting points
        client.update_collection(
            collection_name=COLLECTION_NAME,
            optimizer_config=models.OptimizersConfigDiff(indexing_threshold=1),
        )

        print("Collection update completed.")

if __name__ == '__main__':
    processed_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
    upload_embeddings(processed_file_)
