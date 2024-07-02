import json
import os
from fastembed import TextEmbedding
from qdrant_demo.config import DATA_DIR

def prepare_embeddings(input_file, output_file):
    model = TextEmbedding()  # Initialize the FastEmbed model
    documents = []
    payload = []

    with open(input_file) as fd:
        for line in fd:
            obj = json.loads(line)
            documents.append(obj.pop('description'))
            obj["logo_url"] = obj.pop("images")
            obj["homepage_url"] = obj.pop("link")
            payload.append(obj)

    # FastEmbed handles parallelism internally, so just pass the documents
    embeddings_generator = model.embed(documents)
    embeddings = list(embeddings_generator)

    # Save processed data
    with open(output_file, 'w') as out_fd:
        json.dump({'documents': documents, 'embeddings': embeddings, 'payload': payload}, out_fd)

if __name__ == '__main__':
    input_file = os.path.join(DATA_DIR, 'startups_demo.json')
    output_file = os.path.join(DATA_DIR, 'processed_data.json')
    prepare_embeddings(input_file, output_file)
