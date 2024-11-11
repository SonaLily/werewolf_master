import pandas as pd
import openai
from openai import OpenAI
#import pinecone
import os
from tqdm import tqdm
import tiktoken
from typing import List
import time
import backoff

# ... existing imports ...
from pinecone import Pinecone
client = OpenAI(api_key="sk-_o3neNiIzGWa9BPUT6vkuhxLZozSBiBCa_DTjotDDhT3BlbkFJDogw-hVOCYyDoiV_6TRc_AQ-SIf6-rOT4_ctHsiBwA")

# Initialize Pinecone with environment
pc = Pinecone(
    api_key="f6199930-f9c2-49bb-8149-6359691c9229",
    environment="us-east-1"
)

# ... rest of your code ...

# Set up OpenAI API
#openai.api_key = "sk-_o3neNiIzGWa9BPUT6vkuhxLZozSBiBCa_DTjotDDhT3BlbkFJDogw-hVOCYyDoiV_6TRc_AQ-SIf6-rOT4_ctHsiBwA"

# Set up Pinecone
#pinecone.init(api_key="f6199930-f9c2-49bb-8149-6359691c9229", environment="us-east-1")
index_name = "werewolf-data2"
DIMENSION = 1536  # Adjust this to match your vector dimension
# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=DIMENSION,
        metric='cosine',
        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
    )

index = pc.Index(index_name)
# Path to the directory containing CSV files
# csv_directory = r"C:\Projects\were\train_batchs"
csv_directory = r"/home/bearu/projects/werewolfTrainData"
#werewolf_train_csv_directory


@backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=8)
def get_embedding(text):
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except openai.RateLimitError as e:
        print(f"Rate limit reached. Waiting for 20 seconds before retrying...")
        time.sleep(20)
        return get_embedding(text)  # Retry after waiting
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# def estimate_tokens(text):
#     """Estimate the number of tokens in a piece of text."""
#     return len(text.split())  # A rough estimate, can be adjusted if needed

# def process_file(filepath, token_limit=8000):
#     df = pd.read_csv(filepath)
    
#     batch = []
#     current_token_count = 0
#     ids = []
#     embeddings = []
#     metadata = []
    
#     for i, row in df.iterrows():
#         text = row['content']  # Adjust column name if necessary
#         token_count = estimate_tokens(text)
        
#         # If adding this text exceeds the token limit, process the current batch
#         if current_token_count + token_count > token_limit:
#             to_upsert = list(zip(ids, embeddings, metadata))
#             index.upsert(vectors=to_upsert)
            
#             # Reset for the next batch
#             batch = []
#             ids = []
#             embeddings = []
#             metadata = []
#             current_token_count = 0
        
#         # Add this row's data to the batch
#         embedding = get_embedding(text)
        
#         ids.append(str(row.name))
#         embeddings.append(embedding)
#         metadata.append({
#             'text': text,
#             'scum': row['scum'], 
#             'game_id': row['game_id'], 
#             'slot_id': row['slot_id'],
#             'author': row['author'],
#             # Add any other metadata fields you want to include
#         })
        
#         current_token_count += token_count

    # Process any remaining rows in the last batch
   

def estimate_tokens(text):
    """Estimate the number of tokens in a piece of text."""
    return len(text.split())  # Rough estimate, adjust if necessary

def split_text(text, max_tokens=2000):
    """Splits text into chunks that fit within the token limit."""
    words = text.split()
    chunks = []
    while len(words) > max_tokens:
        chunks.append(" ".join(words[:max_tokens]))
        words = words[max_tokens:]
    chunks.append(" ".join(words))  # Remaining words in last chunk
    return chunks

def process_file(filepath, token_limit=8000, chunk_token_limit=2000):
    df = pd.read_csv(filepath)
    
    batch = []
    current_token_count = 0
    ids = []
    embeddings = []
    metadata = []
    
    for i, row in df.iterrows():
        text = row['content']  # Adjust column name if necessary
        text_chunks = split_text(text, max_tokens=chunk_token_limit)
        
        for chunk in text_chunks:
            token_count = estimate_tokens(chunk)
            
            # If adding this chunk exceeds the token limit, process the current batch
            if current_token_count + token_count > token_limit:
                to_upsert = list(zip(ids, embeddings, metadata))
                index.upsert(vectors=to_upsert)
                
                # Reset for the next batch
                ids = []
                embeddings = []
                metadata = []
                current_token_count = 0
            
            # Get the embedding for this chunk of text
            embedding = get_embedding(chunk)  # Ensure this fits token limit

            ids.append(str(row.name))  # Using row index as ID, adjust as needed
            embeddings.append(embedding)
            metadata.append({
                'text': chunk,  # Save chunk, not full text
                'scum': row['scum'], 
                'game_id': row['game_id'], 
                'slot_id': row['slot_id'],
                'author': row['author'],
                # Add any other metadata fields you want to include
            })
            
            current_token_count += token_count

    # Process any remaining rows in the last batch
    if ids:
        to_upsert = list(zip(ids, embeddings, metadata))
        index.upsert(vectors=to_upsert)


# Function to process and upsert a single CSV file
# def process_file(filepath):
#     df = pd.read_csv(filepath)
    
#     batch_size = 100
#     for i in range(0, len(df), batch_size):
#         batch = df.iloc[i:i+batch_size]
        
#         ids = []
#         embeddings = []
#         metadata = []
        
#         for _, row in batch.iterrows():
#             text = row['content']  # Adjust column name if necessary
#             embedding = get_embedding(text)
            
#             ids.append(str(row.name))
#             embeddings.append(embedding)
#             metadata.append({
#                 'text': text,
#                 'scum': row['scum'], 
#                 'game_id': row['game_id'], 
#                 'slot_id': row['slot_id'],
#                 'author': row['author'],

#                 # Add any other metadata fields you want to include
#             })
        
#         to_upsert = list(zip(ids, embeddings, metadata))
#         index.upsert(vectors=to_upsert)

# Process all CSV files in the specified directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

for file in tqdm(csv_files, desc="Processing files"):
    full_path = os.path.join(csv_directory, file)
    process_file(full_path)

print("All files processed and inserted into Pinecone.")
