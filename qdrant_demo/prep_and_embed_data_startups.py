import os
import pandas as pd
from fastembed import TextEmbedding
from qdrant_demo.config import DATA_DIR, EMBEDDINGS_MODEL


def prepare_embeddings(input_file, output_file):
    model = TextEmbedding(EMBEDDINGS_MODEL, cache_dir='./local_cache/')  # Initialize the FastEmbed model

    # Load the JSON data into a pandas DataFrame
    df = pd.read_json(input_file, lines=True)

    # TODO delete this part after testing
    df = df.iloc[:1000, :]

    # Extract descriptions for embedding and clean up the DataFrame
    documents = df['description'].tolist()
    df = df.drop(columns=['description'])
    df = df.rename(columns={'images': 'logo_url', 'link': 'homepage_url'})

    # FastEmbed handles parallelism internally, so just pass the documents
    embeddings_generator = model.embed(documents)
    embeddings = list(embeddings_generator)

    # Convert embeddings from ndarray to list
    embeddings = [embedding.tolist() for embedding in embeddings]

    # Add documents and embeddings to the DataFrame
    df['documents'] = documents
    df['embeddings'] = embeddings

    # Save DataFrame to Parquet
    df.to_parquet(output_file, index=False)


if __name__ == '__main__':
    input_file_ = os.path.join(DATA_DIR, 'startups_demo.json')
    output_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
    prepare_embeddings(input_file_, output_file_)
