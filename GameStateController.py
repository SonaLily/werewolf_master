import random

class GameStateController:
    def __init__(self, players):
        # Initialize players and store them in a dictionary
        self.players = {player.name: player for player in players}
        self.phase = "day"  # 'day' or 'night'
        self.round_number = 1
        self.accusations = []
        self.votes = {}
        self.eliminated_players = []

    def update_phase(self, new_phase):
        """
        Update the current phase of the game (day or night).
        """
        self.phase = new_phase
        self.votes.clear()  # Clear votes at the start of a new phase
        print(f"Game phase updated to: {self.phase}")

    def record_accusation(self, accuser, accused):
        """
        Record an accusation made by a player.
        """
        if self.phase == "day" and self.players[accuser].status == "alive":
            self.accusations.append((accuser, accused))
            print(f"{accuser} accuses {accused}")

    def record_vote(self, voter, target):
        """
        Record a vote cast by a player.
        """
        if self.phase == "day" and self.players[voter].status == "alive":
            self.votes[target] = self.votes.get(target, 0) + 1
            print(f"{voter} votes for {target}")

    def tally_votes_and_eliminate(self):
        """
        Tallies votes at the end of the day phase and eliminates the player with the most votes.
        If there is a tie, initiates a revote until the tie is broken.
        """
        if self.phase == "day" and self.votes:
            vote_counts = {}
            for target in self.votes.values():
                vote_counts[target] = vote_counts.get(target, 0) + 1
            
            max_votes = max(vote_counts.values())
            players_with_max_votes = [player for player, votes in vote_counts.items() if votes == max_votes]
            
            if len(players_with_max_votes) == 1:
                eliminated_player = players_with_max_votes[0]
                self.players[eliminated_player].status = "eliminated"
                print(f"{eliminated_player} has been eliminated.")
            else:
                print("There was a tie. A revote is needed.")
                # Implement revote logic here
        else:
            print("No votes recorded or incorrect phase for elimination.")

    def conduct_revote(self, tied_players):
        """
        Conducts a revote among the players involved in a tie.
        Only the tied players are valid targets for this revote.
        """
        print("Revote in progress among tied players...")
        for player_name, player in self.players.items():
            if player.status == "alive":
                # For simplicity, we'll simulate a random choice among tied players
                chosen_player = random.choice(tied_players)
                self.record_vote(player_name, chosen_player)
                print(f"{player_name} revotes for {chosen_player}.")

    def eliminate_player(self, player_name):
        """
        Eliminate a player from the game and update game state.
        """
        if player_name in self.players and self.players[player_name].status == "alive":
            player = self.players[player_name]
            player.eliminate()
            self.eliminated_players.append(player_name)
            print(f"{player_name} has been eliminated.")

    def get_alive_players(self):
        """
        Returns a list of players who are still alive.
        """
        return [player for player in self.players.values() if player.status == "alive"]
    

    def reset_votes(self):
        self.votes = {}
