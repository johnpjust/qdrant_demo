# import os
# import pandas as pd
#
#
# from qdrant_client.models import Distance, VectorParams, PointStruct
# from qdrant_client import QdrantClient, models
# from tqdm import tqdm
#
# from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL
#
# dense_vector_name = EMBEDDINGS_MODEL.split(('/'))[-1]
# def get_existing_descriptions_and_max_id(client, collection_name, batch_size=5000):
#     existing_descriptions = set()
#     max_id = 0
#     response, _ = client.scroll(
#         collection_name=collection_name,
#         limit=batch_size,
#     )
#
#     while response:
#         for hit in response:
#             existing_descriptions.add(hit.payload[TEXT_FIELD_NAME])
#             max_id = max(max_id, int(hit.id))
#         response, _ = client.scroll(
#             collection_name=collection_name,
#             limit=batch_size,
#             offset=response[-1].id
#         )
#     return existing_descriptions, max_id
#
#
# def upload_embeddings(processed_file):
#     client = QdrantClient(
#         url=QDRANT_URL,
#         api_key=QDRANT_API_KEY,
#         prefer_grpc=False,
#     )
#
#     # Load the Parquet file into a DataFrame
#     df = pd.read_parquet(processed_file)
#     documents = df['documents'].tolist()
#     embeddings = df['embeddings'].tolist()
#     payload = df.drop(columns=['documents', 'embeddings']).to_dict(orient='records')
#
#     if not client.collection_exists(COLLECTION_NAME):
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config={dense_vector_name: VectorParams(size=384,
#                                       distance=Distance.COSINE,
#                                       hnsw_config=None,
#                                       quantization_config=models.ScalarQuantization(
#                                                         scalar=models.ScalarQuantizationConfig(
#                                                             type=models.ScalarType.INT8,
#                                                             quantile=0.99,
#                                                             always_ram=True
#                                                         )),
#                                       on_disk=True,
#                                       datatype=None,
#                                       multivector_config=None),},
#         )
#
#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name=TEXT_FIELD_NAME,
#             field_schema=models.TextIndexParams(
#                 type=models.TextIndexType.TEXT,
#                 tokenizer=models.TokenizerType.WORD,
#                 min_token_len=2,
#                 max_token_len=20,
#                 lowercase=True,
#             )
#         )
#
#     existing_descriptions, max_id = get_existing_descriptions_and_max_id(client, COLLECTION_NAME)
#
#     points = [
#           PointStruct(
#             id=max_id + i + 1,  # Generate sequential ID
#             vector={dense_vector_name: embedding},
#             payload=meta
#         )
#         for i, (doc, meta, embedding) in enumerate(zip(documents, payload, embeddings))
#         if doc not in existing_descriptions
#     ]
#
#     client.update_collection(
#         collection_name=COLLECTION_NAME,
#         optimizer_config=models.OptimizersConfigDiff(indexing_threshold=0),
#     )
#
#     # if points:
#     #     client.upload_points(
#     #         collection_name=COLLECTION_NAME,
#     #         points=tqdm(points, desc="Uploading points"),
#     #         parallel=os.cpu_count()
#     #     )
#
#     if points:
#         response = client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=tqdm(points, desc="Uploading points"),
#         )
#
#         if response.status == 'ok':
#             print("Points uploaded successfully.")
#         else:
#             print(f"Failed to upload points: {response}")
#
#         client.update_collection(
#             collection_name="COLLECTION_NAME",
#             optimizer_config=models.OptimizersConfigDiff(indexing_threshold=20000),
#         )
#
#
# if __name__ == '__main__':
#     processed_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
#     upload_embeddings(processed_file_)

################################
# import os
# import pandas as pd
# from qdrant_client.models import Distance, VectorParams, PointStruct
# from qdrant_client import QdrantClient, models
# from tqdm import tqdm
#
# from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL
#
# dense_vector_name = EMBEDDINGS_MODEL.split(('/'))[-1]
#
# def get_existing_descriptions_and_max_id(client, collection_name, batch_size=5000):
#     existing_descriptions = set()
#     max_id = 0
#     response, _ = client.scroll(
#         collection_name=collection_name,
#         limit=batch_size,
#     )
#
#     while response:
#         for hit in response:
#             existing_descriptions.add(hit.payload[TEXT_FIELD_NAME])
#             max_id = max(max_id, int(hit.id))
#         response, _ = client.scroll(
#             collection_name=collection_name,
#             limit=batch_size,
#             offset=response[-1].id
#         )
#     return existing_descriptions, max_id
#
# def upload_embeddings(processed_file):
#     client = QdrantClient(
#         url=QDRANT_URL,
#         api_key=QDRANT_API_KEY,
#         prefer_grpc=False,
#     )
#
#     # Load the Parquet file into a DataFrame
#     df = pd.read_parquet(processed_file)
#     documents = df['documents'].tolist()
#     embeddings = df['embeddings'].tolist()
#     payload = df.drop(columns=['documents', 'embeddings']).to_dict(orient='records')
#
#     if not client.collection_exists(COLLECTION_NAME):
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config={
#                 dense_vector_name: VectorParams(size=384,
#                                                 distance=Distance.COSINE,
#                                                 hnsw_config=None,
#                                                 quantization_config=models.ScalarQuantization(
#                                                     scalar=models.ScalarQuantizationConfig(
#                                                         type=models.ScalarType.INT8,
#                                                         quantile=0.99,
#                                                         always_ram=True
#                                                     )),
#                                                 on_disk=True,
#                                                 datatype=None,
#                                                 multivector_config=None),
#             },
#         )
#
#         client.create_payload_index(
#             collection_name=COLLECTION_NAME,
#             field_name=TEXT_FIELD_NAME,
#             field_schema=models.TextIndexParams(
#                 type=models.TextIndexType.TEXT,
#                 tokenizer=models.TokenizerType.WORD,
#                 min_token_len=2,
#                 max_token_len=20,
#                 lowercase=True,
#             )
#         )
#
#     existing_descriptions, max_id = get_existing_descriptions_and_max_id(client, COLLECTION_NAME)
#
#     points = [
#         PointStruct(
#             id=max_id + i + 1,  # Generate sequential ID
#             vector={dense_vector_name: embedding},
#             payload=meta
#         )
#         for i, (doc, meta, embedding) in enumerate(zip(documents, payload, embeddings))
#         if doc not in existing_descriptions
#     ]
#
#     client.update_collection(
#         collection_name=COLLECTION_NAME,
#         optimizer_config=models.OptimizersConfigDiff(indexing_threshold=0),
#     )
#
#     if points:
#         # Use list comprehension to create a progress bar compatible list of points
#         points_with_progress = [point for point in tqdm(points, desc="Uploading points")]
#
#         response = client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=points_with_progress,
#         )
#
#         if response.status == models.UpdateStatus.COMPLETED:
#             print("Points uploaded successfully.")
#         else:
#             print(f"Failed to upload points: {response}")
#
#         client.update_collection(
#             collection_name=COLLECTION_NAME,
#             optimizer_config=models.OptimizersConfigDiff(indexing_threshold=1),
#         )
#
# if __name__ == '__main__':
#     processed_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
#     upload_embeddings(processed_file_)


#############################################
import os
import pandas as pd
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL

dense_vector_name = EMBEDDINGS_MODEL.split(('/'))[-1]


def get_existing_descriptions_and_max_id(client, collection_name, batch_size=5000):
    existing_descriptions = set()
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
                existing_descriptions.add(hit.payload[TEXT_FIELD_NAME])
            else:
                print(f"Missing field '{TEXT_FIELD_NAME}' in payload: {hit.payload}")
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
    return existing_descriptions, max_id


def upload_embeddings(processed_file):
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    # Load the Parquet file into a DataFrame
    df = pd.read_parquet(processed_file)
    print("DataFrame loaded from Parquet file:")
    print(df.head())  # Print the first few rows for inspection

    documents = df['documents'].tolist()
    embeddings = df['embeddings'].tolist()
    payload = df.drop(columns=['documents', 'embeddings']).to_dict(orient='records')

    # Verify that 'document' field is present in the DataFrame
    if 'documents' not in df.columns:
        print("Error: 'documents' column is missing in the DataFrame")
        return

    # Debugging: Check the payload structure before and after adding 'document' field
    print("Sample payload before adding 'document' field:")
    print(payload[0] if payload else "No payload data")

    # Add 'document' field to each payload
    for i, doc in enumerate(documents):
        payload[i]['document'] = doc

    print("Sample payload after adding 'document' field:")
    print(payload[0] if payload else "No payload data")

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                dense_vector_name: VectorParams(size=384,  # Ensure this matches the actual vector size
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
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=20,
                lowercase=True,
            )
        )

    existing_descriptions, max_id = get_existing_descriptions_and_max_id(client, COLLECTION_NAME)
    print(f"Existing descriptions count: {len(existing_descriptions)}")
    print(f"Max ID: {max_id}")

    points = [
        PointStruct(
            id=max_id + i + 1,  # Generate sequential ID
            vector={dense_vector_name: embedding},
            payload=meta
        )
        for i, (doc, meta, embedding) in enumerate(zip(documents, payload, embeddings))
        if doc not in existing_descriptions  # Use `doc` directly here as it should be part of the documents list
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
