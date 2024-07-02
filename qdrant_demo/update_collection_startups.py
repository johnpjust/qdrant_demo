import json
import os
import multiprocessing

from qdrant_client import QdrantClient, models
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

    with open(processed_file) as fd:
        data = json.load(fd)
        documents = data['documents']
        embeddings = data['embeddings']
        payload = data['payload']

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

    new_documents = []
    new_metadata = []
    new_embeddings = []
    for doc, meta, embed in zip(documents, payload, embeddings):
        if doc not in existing_descriptions:
            new_documents.append(doc)
            new_metadata.append(meta)
            new_embeddings.append(embed)

    if new_documents:
        num_workers = multiprocessing.cpu_count()  # Set to number of CPU cores
        client.add(
            collection_name=COLLECTION_NAME,
            documents=new_documents,
            vectors=new_embeddings,
            metadata=new_metadata,
            ids=tqdm(range(len(new_metadata))),
            parallel=num_workers,
        )


if __name__ == '__main__':
    # print(os.listdir('../'))
    processed_file = os.path.join(DATA_DIR, 'processed_data.json')
    upload_embeddings(processed_file)
