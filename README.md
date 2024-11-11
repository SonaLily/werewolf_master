# Werewolf AI Agent Master

## Overview
A Python implementation of the Werewolf (Mafia) game with AI agents. This project simulates the classic social deduction game where players are divided into Villagers and Werewolves, featuring AI-driven decision making and game state management.

## Key Components

### 1. Game State Controller (`GameStateController.py`)
Manages the game's state and player interactions:
```python
class GameStateController:
    def __init__(self, players):
        self.players = {}  # Player registry
        self.current_phase = "day"
        self.votes = {}    # Vote tracking
```
- Tracks player status (alive/dead)
- Manages game phases (day/night)
- Handles voting system
- Maintains game history

### 2. Main Game Engine (`playWereWolf.py`)
Implements core game logic and flow:
```python
class WerewolfGame:
    def __init__(self):
        self.game_state = GameStateController([])
        self.players = []
```
Key features:
- Player creation and role assignment
- Day/night phase management
- Vote processing
- Win condition checking

## Setup and Usage

### Prerequisites
- Python 3.10+
- Required packages:
  - random
  - typing

### Running the Game
```bash
python playWereWolf.py
```

## Game Flow

### 1. Initialization
- Creates 12 players
- Assigns roles (3 Werewolves, 9 Villagers)
- Reveals werewolf identities to other werewolves

### 2. Game Phases

#### Night Phase
- Werewolves choose a target
- Werewolves discuss and vote
- Target elimination

#### Day Phase
- All players discuss
- Players vote for suspicious players
- Most voted player is eliminated

### 3. Win Conditions
- Werewolves win: When werewolves equal or outnumber villagers
- Villagers win: When all werewolves are eliminated

## Example Game Output
```
Player 1 has been assigned the role of Werewolf.
Player 2 has been assigned the role of Villager.
...
--- Night Phase ---
Player 1 discusses targeting Player 5.
...
--- Day Phase ---
Player 2 (Villager) discusses suspicion about Player 1.
```

## Future Improvements
- [ ] Add more sophisticated AI decision making
- [ ] Implement special roles (Seer, Doctor, etc.)
- [ ] Add game logging and replay functionality
- [ ] Create a web interface

## Contributing
Contributions are welcome! Please feel free to submit pull requests.

## License
[Your chosen license]