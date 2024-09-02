import os
import pandas as pd
from fastembed import TextEmbedding, SparseTextEmbedding
from qdrant_demo.config import DATA_DIR, EMBEDDINGS_MODEL_QUESTIONS, EMBEDDINGS_MODEL_JOB_TITLES
import time

def prepare_embeddings(input_file, output_file):
    model_questions = TextEmbedding(EMBEDDINGS_MODEL_QUESTIONS, cache_dir='./local_cache/')  # Initialize the FastEmbed model
    model_job_titles = TextEmbedding(EMBEDDINGS_MODEL_JOB_TITLES, cache_dir='./local_cache/')  # Initialize the FastEmbed model
    model_sparse_titles = SparseTextEmbedding(SparseTextEmbedding.list_supported_models()[0]["model"], cache_dir='./local_cache/')

    # Load the JSON data into a pandas DataFrame
    df = pd.read_csv(input_file, encoding='latin1', sep='\t', low_memory=False)

    '''
    Columns:
    'Date', 'Job_Title', 'Company', 'Question', 'Candidate_Info', 'Ratings', 'Application_Details', 'Interview_Process'
    '''

    # TODO delete this part after testing
    df = df.iloc[0:100, :]

    # Extract descriptions for embedding and clean up the DataFrame
    questions = df['Question'].tolist()
    titles = df['Job_Title'].tolist()
    # TODO leave title as "description" throughout (fix in the update collection code as well)

    # FastEmbed handles parallelism internally, so just pass the documents
    question_embeddings_generator = model_questions.embed(questions, parallel=None)
    start_time = time.time()
    question_embeddings = list(question_embeddings_generator)
    print(time.time() - start_time)

    title_embeddings_generator = model_job_titles.embed(titles, parallel=None)
    start_time = time.time()
    title_embeddings = list(title_embeddings_generator)
    print(time.time() - start_time)

    title_embeddings_generator_sparse = model_sparse_titles.embed(titles, parallel=None)
    title_embeddings_sparse = list(title_embeddings_generator_sparse)

    # Convert embeddings from ndarray to list
    question_embeddings = [embedding.tolist() for embedding in question_embeddings]
    title_embeddings = [embedding.tolist() for embedding in title_embeddings]
    title_embeddings_sparse = [embedding.tolist() for embedding in title_embeddings_sparse]

    # Add documents and embeddings to the DataFrame
    df['question_embeddings'] = question_embeddings
    df['title_embeddings'] = title_embeddings
    df['title_embeddings_sparse'] = title_embeddings_sparse

    # Save DataFrame to Parquet
    df.to_parquet(output_file, index=False)


if __name__ == '__main__':
    input_file_ = os.path.join(DATA_DIR, 'all_interviews_concatenated.csv')
    output_file_ = os.path.join(DATA_DIR, 'processed_data.parquet')
    prepare_embeddings(input_file_, output_file_)
