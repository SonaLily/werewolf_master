import os
import random
import openai
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API keys and Pinecone environment
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index(os.getenv("PINECONE_INDEX"))
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

class WerewolfAgent:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.strategy = None
        self.history = []  # Stores actions and observations for learning

    ### Step 2: Role Recognition and Assignment ###
    def assign_role(self, role):
        """
        Assign the agent's role and set up the appropriate strategy.
        """
        self.role = role
        if self.role == "Werewolf":
            print(f"{self.name} assigned as Werewolf")
            self.strategy = self.werewolf_strategy
        elif self.role == "Villager":
            print(f"{self.name} assigned as Villager")
            self.strategy = self.villager_strategy
        else:
            raise ValueError("Role must be either 'Werewolf' or 'Villager'")

    ### Step 3: Data Handling and RAG Implementation ###
    def retrieve_strategy(self, context):
        """
        Use Pinecone to retrieve relevant historical game data based on context.
        """
        vector = self.vectorize_context(context)
        query = {"filter": {"role": self.role}}
        result = pinecone_index.query(vector=vector, filter=query)
        return result.get('matches', [])

    def vectorize_context(self, context):
        """
        Converts the game context into an embedding vector for querying Pinecone.
        """
        client = openai.OpenAI()
        response = client.embeddings.create(input=context, model=EMBEDDING_MODEL)
        return response.data[0].embedding
    
    def store_game_data(self, data):
        """
        Store game actions and observations in Pinecone for post-game learning.
        """
        # Convert the game data to a vector representation
        vector = self.vectorize_context(str(data))
        
        # Create a unique ID for this game data entry
        unique_id = str(random.randint(0, 10000))
        
        # Upsert the vector data into Pinecone
        pinecone_index.upsert([(unique_id, vector, data)])

    ### Step 4: LLM-Based Reasoning Modules ###
    def generate_response(self, prompt):
        """
        Use OpenAI's ChatCompletion to generate explanations, accusations, and defenses.
        """
        client = openai.OpenAI()  # Create a client instance
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()

    def create_prompt(self, context):
        """
        Formulate a prompt for the LLM based on the agent's role and game context.
        """
        if self.role == "Werewolf":
            return f"As a Werewolf, {self.name}, craft a deceptive statement based on: {context}"
        else:
            return f"As a Villager, {self.name}, identify suspicious players based on: {context}"

    ### Werewolf Strategy Implementation ###
    def werewolf_strategy(self, game_data):
        """
        Define the Werewolf's strategy, focusing on deception and targeting.
        """
        target_player = self.choose_target(game_data)
        deceive_message = self.create_deception(game_data)
        print(f"{self.name} (Werewolf) targets {target_player} and says: {deceive_message}")
        return target_player, deceive_message

    def choose_target(self, game_data):
        """
        Choose a target to eliminate based on game data.
        """
        potential_targets = game_data.get("players", [])
        return random.choice(potential_targets) if potential_targets else "No players found"

    def create_deception(self, game_data):
        """
        Generate a deceptive message to deflect suspicion.
        """
        deceptive_statements = [
            "I believe player X is innocent.",
            "I think the werewolf is someone who talks too little.",
            "Why are you all looking at me? I'm just a villager."
        ]
        return random.choice(deceptive_statements)

    ### Villager Strategy Implementation ###
    def villager_strategy(self, game_data):
        """
        Define the Villager's strategy, focusing on detecting suspicious behavior.
        """
        suspicious_players = self.detect_suspicion(game_data)
        print(f"{self.name} (Villager) suspects: {suspicious_players}")
        return suspicious_players

    def detect_suspicion(self, game_data):
        """
        Analyze player discussions to detect suspicious players.
        """
        suspicious_players = []
        for player, behavior in game_data.get("discussions", {}).items():
            if "hesitant" in behavior or "defensive" in behavior:
                suspicious_players.append(player)
        return suspicious_players if suspicious_players else ["No suspicious players detected"]

    ### Step 5: Game Phase Execution ###
    def night_phase(self, game_data):
        """
        Werewolf-specific night actions: choosing a target to eliminate.
        """
        if self.role == "Werewolf":
            target = self.choose_target(game_data)
            print(f"{self.name} (Werewolf) decides to target {target}")
            return target
        return None

    def day_phase(self, game_data):
        """
        Participate in day discussions, accusing or defending based on role.
        """
        context = self.create_game_context(game_data)
        response = self.generate_response(self.create_prompt(context))
        print(f"{self.name}'s response: {response}")
        return response

    def vote(self, game_data):
        """
        Cast a vote based on game analysis and role strategy.
        """
        if self.role == "Werewolf":
            return self.werewolf_vote(game_data)
        else:
            return self.villager_vote(game_data)

    def werewolf_vote(self, game_data):
        """
        Werewolf-specific voting strategy.
        """
        return random.choice([player for player in game_data.get("players", []) if player != self.name])

    def villager_vote(self, game_data):
        """
        Villager-specific voting strategy, focusing on suspicious players.
        """
        suspicious_players = self.detect_suspicion(game_data)
        return random.choice(suspicious_players) if suspicious_players else "Skip vote"

    ### Helper Functions ###
    def create_game_context(self, game_data):
        """
        Creates a textual context from game data for prompting the LLM.
        """
        return f"Players: {', '.join(game_data.get('players', []))}, Discussions: {game_data.get('discussions', {})}"

    def update_strategy(self, game_data, outcome):
        """
        Update the agent's strategy based on the game outcome.
        """
        print(f"{self.name} updating strategy based on {outcome} outcome")
        # Here you can implement logic to adjust the agent's strategy
        # based on the game outcome and data
        self.store_game_data({
            "role": self.role,
            "outcome": outcome,
            "game_data": str(game_data)  # Convert game_data to string
        })

# Example Usage
if __name__ == "__main__":
    agent = WerewolfAgent(name="AI Agent1")
    
    # Step 2: Assign a role (e.g., randomly for testing)
    agent.assign_role(random.choice(["Werewolf", "Villager"]))

    # Mock game data for testing
    game_data = {
        "players": ["Player1", "Player2", "Player3", "Player4"],
        "discussions": {
            "Player1": "defensive",
            "Player2": "neutral",
            "Player3": "hesitant",
            "Player4": "aggressive"
        }
    }

    # Step 5: Simulate game phases
    if agent.role == "Werewolf":
        agent.night_phase(game_data)  # Night action for Werewolf
    agent.day_phase(game_data)  # Day action for discussion
    vote_decision = agent.vote(game_data)  # Voting based on role
    print(f"{agent.name} votes for: {vote_decision}")

    # Step 6: Update strategy based on simulated outcome
    agent.update_strategy(game_data, outcome="Win")
