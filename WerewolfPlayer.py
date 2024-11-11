import random

class WerewolfPlayer:
    def __init__(self, name, role="Villager", game_state=None):
        self.name = name
        self.role = role  # Role can be "Villager", "Werewolf", etc.
        self.status = "alive"  # "alive" or "eliminated"
        self.game_state = game_state  # Reference to the game state controller

    def perform_night_discussion(self, possible_targets):
        """
        Placeholder for night discussion, to be overridden by subclasses.
        """
        pass

    def perform_night_vote(self, target_name):
        """
        Placeholder for night voting, to be overridden by subclasses.
        """
        pass

    def perform_night_action(self, target_name=None):
        """
        Placeholder method to execute a final night action, if applicable.
        """
        pass

    def perform_day_discussion(self, possible_suspects):
        """
        Placeholder for day discussion, to be overridden by subclasses.
        """
        pass

    def perform_day_vote(self, suspect_name):
        """
        Placeholder for day voting, to be overridden by subclasses.
        """
        pass

    def perform_day_action(self, possible_suspects):
        """
        Placeholder for performing all day actions, to be overridden by subclasses.
        """
        pass

    def eliminate(self):
        """
        Eliminates the player from the game and reveals their role.
        """
        self.status = "eliminated"
        print(f"{self.name} has been eliminated. They were a {self.role}.")


class Werewolf(WerewolfPlayer):
    def __init__(self, name, game_state):
        super().__init__(name, role="Werewolf", game_state=game_state)
    
    def werewolf_night_discussion(self, possible_targets):
        """
        Discuss with other werewolves and choose a target for elimination.
        """
        if self.status == "alive":
            target = possible_targets[0]  # Simple example selection
            print(f"{self.name} discusses targeting {target.name}.")
            return target

    def werewolf_night_vote(self, possible_targets):
        # Choose a single target instead of returning the whole list
        return random.choice(possible_targets)

    def werewolf_day_discussion(self, possible_suspects):
        """
        Werewolf's day discussion to avoid suspicion and deflect onto villagers.
        """
        if self.status == "alive":
            # Example logic to deflect suspicion
            suspect = possible_suspects[0]  # Placeholder for the first suspect in list
            print(f"{self.name} (Werewolf) discusses and subtly accuses {suspect.name} during the day.")
            return suspect  # Returns the suspected player's name to deflect attention

    def werewolf_day_vote(self, suspect_names):
        """
        Werewolf votes during the day phase to influence the elimination.
        """
        if self.status == "alive":
            suspect_name=random.choice(suspect_names)
            print(f"{self.name} votes for {suspect_name} during the day phase.")
            return suspect_name  # Returns the suspect's name for voting

    def perform_night_action(self, target_name):
        """
        Execute the final elimination action after discussion and voting.
        """
        if self.status == "alive" and self.game_state:
            print(f"{self.name} (Werewolf) executes the elimination of {target_name}.")
            self.game_state.eliminate_player(target_name)


class Villager(WerewolfPlayer):
    def __init__(self, name, game_state):
        super().__init__(name, role="Villager", game_state=game_state)

    def villager_day_discussion(self, possible_suspects):
        """
        Villager's day discussion to identify potential werewolves.
        """
        if self.status == "alive":
            suspect = possible_suspects[0]  # Placeholder for the first suspect
            print(f"{self.name} (Villager) discusses suspicions about {suspect.name}.")
            return suspect

    def villager_day_vote(self, suspect_name):
        """
        Villager votes during the day phase to eliminate a suspected werewolf.
        """
        if self.status == "alive":
            print(f"{self.name} votes to eliminate {suspect_name} during the day phase.")
            return suspect_name

    def perform_day_action(self, possible_suspects):
        """
        Perform all day actions for the villager: discuss and vote.
        """
        if self.status == "alive":
            # Step 1: Discuss and choose a suspect
            suspect = self.villager_day_discussion(possible_suspects)
            # Step 2: Vote for the chosen suspect
            self.villager_day_vote(suspect.name)

