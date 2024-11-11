import random
from GameStateController import GameStateController
from WerewolfPlayer import Werewolf, Villager, WerewolfPlayer

class WerewolfGame:
    def __init__(self):
        # Initialize players and roles
        self.game_state = GameStateController([])
        self.players = []
        self.create_players()
        self.assign_roles()

    def create_players(self):
        # Create player names
        player_names = [f"Player {i+1}" for i in range(12)]
        roles = ["Werewolf"] * 3 + ["Villager"] * 9
        random.shuffle(roles)

        for name, role in zip(player_names, roles):
            if role == "Werewolf":
                player = Werewolf(name, self.game_state)
            else:
                player = Villager(name, self.game_state)
            self.players.append(player)
            self.game_state.players[name] = player
            print(f"{name} has been assigned the role of {role}.")

    def assign_roles(self):
        # Reveal all roles to werewolves
        werewolves = [player for player in self.players if player.role == "Werewolf"]
        for werewolf in werewolves:
            print(f"{werewolf.name} knows the roles of all players.")
            for player in self.players:
                print(f"  - {player.name}: {player.role}")

    def play_game(self):
        while not self.check_win_conditions():
            self.night_phase()
            if self.check_win_conditions():
                break
            self.day_phase()

    def night_phase(self):
        print("\n--- Night Phase ---")
        self.game_state.update_phase("night")
        werewolves = [player for player in self.players if player.role == "Werewolf" and player.status == "alive"]

        # Track possible targets and vote counts
        possible_targets = [player for player in self.players if player.role != "Werewolf" and player.status == "alive"]
        target_votes = {}

        if possible_targets:
            # Step 1: Werewolves discuss potential targets
            for werewolf in werewolves:
                target = werewolf.werewolf_night_discussion(possible_targets)
                print(f"{werewolf.name} discusses targeting {target.name}.")

            # Step 2: Werewolves vote on a target to eliminate
            for werewolf in werewolves:
                target = werewolf.werewolf_night_vote(possible_targets)
                target_name = target.name
                target_votes[target_name] = target_votes.get(target_name, 0) + 1

            # Determine and execute elimination on the most-voted target
            most_voted_target = max(target_votes, key=target_votes.get)
            print(f"Target chosen for elimination: {most_voted_target} with {target_votes[most_voted_target]} votes.")
            werewolves[0].perform_night_action(most_voted_target)

    def day_phase(self):
        print("\n--- Day Phase ---")
        self.game_state.update_phase("day")
        alive_players = [player for player in self.players if player.status == "alive"]

        print(f"Alive players at start of day phase: {[p.name for p in alive_players]}")
        
        # Reset votes at the beginning of each day phase
        self.game_state.reset_votes()

        possible_suspects = alive_players  # All alive players can be suspects
        day_votes = {}

        # Step 1: All players discuss potential suspects
        for player in alive_players:
            if player.role == "Villager":
                suspect = player.villager_day_discussion(possible_suspects)
                print(f"{player.name} (Villager) discusses suspicion about {suspect.name}.")
            elif player.role == "Werewolf":
                suspect = player.werewolf_day_discussion(possible_suspects)
                print(f"{player.name} (Werewolf) discusses suspicion about {suspect.name}.")

        # Step 2: All players vote based on discussion
        for player in alive_players:
            if player.role == "Villager":
                suspect = player.villager_day_vote(possible_suspects)
            elif player.role == "Werewolf":
                suspect = player.werewolf_day_vote(possible_suspects)
            
            # Ensure suspect is a single WerewolfPlayer object
            if isinstance(suspect, WerewolfPlayer):
                suspect_name = suspect.name
                day_votes[suspect_name] = day_votes.get(suspect_name, 0) + 1
            else:
                print(f"Error: {player.name} did not select a valid suspect.")

        print("Votes recorded for the day phase:", day_votes)

        # Use GameStateController to tally votes and eliminate the player with the highest votes
        most_voted_player = max(day_votes, key=day_votes.get)
        print(f"Player chosen for elimination during the day: {most_voted_player} with {day_votes[most_voted_player]} votes.")
        self.game_state.eliminate_player(most_voted_player)

    def check_win_conditions(self):
        alive_players = self.game_state.get_alive_players()
        werewolves = [player for player in alive_players if player.role == "Werewolf"]
        villagers = [player for player in alive_players if player.role == "Villager"]

        if not werewolves:
            print("Villagers win! All werewolves have been eliminated.")
            return True
        elif len(werewolves) >= len(villagers):
            print("Werewolves win! They outnumber the villagers.")
            return True
        return False

# Start the game
game = WerewolfGame()
game.play_game()
