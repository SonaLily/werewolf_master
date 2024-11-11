import os
import random
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API keys and Pinecone environment
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
#pinecone_index = pc.Index(os.getenv("PINECONE_INDEX"))

# Define index parameters
index_name = "werewolf-game-data"
dimension = 1536  # Dimension of your OpenAI embeddings
metric = "cosine"
spec = ServerlessSpec(
    cloud="aws",
    region="us-west-2"
)

# Define metadata configuration
metadata_config = {
    "indexed": [
        "game_id",
        "player_role",
        "game_phase",
        "day_number",
        "action_type",
        "target_player"
    ]
}

# Create the index if it doesn't exist
if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric=metric,
        spec=spec
    
    )
    print(f"Created new Pinecone index: {index_name}")
else:
    print(f"Pinecone index {index_name} already exists")

# Connect to the index
index = pc.Index(index_name)
