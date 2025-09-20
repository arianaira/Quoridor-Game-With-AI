<p align="center"><h1 align="center">QUORIDOR-GAME-WITH-AI</h1></p>
<p align="center">
  <em><code> Play the classic strategy game Quoridor against a smart AI in your terminal.</code></em>
</p>

<br>

---
##  Overview

Quoridor is a two-player game where the objective is to be the first to move your pawn to the opposite side of the board. On each turn, a player can choose one of two actions:

1. Move their pawn one space (horizontally or vertically).

2. Place a wall to obstruct the path of the opponent.

A key rule is that a wall cannot be placed if it completely blocks the last remaining path for either player to their goal line. Each player has a limited number of walls (10 in this implementation).

## Implementation Details
The project is structured into two main components: the game environment and the agents.

1. Game Environment (QuoridorEnv)
The QuoridorEnv class manages the entire game. Its key responsibilities include:

   - State Management: Tracks pawn positions, remaining walls for each player, and the locations of all placed walls.

   - Game Logic: Contains functions to determine all valid moves and valid wall placements at any given state.

   - Rule Enforcement: Ensures that no move is illegal. Crucially, it uses a Breadth-First Search (BFS) algorithm (is_path_available) to verify that placing a wall does not illegally trap a player.

   - Rendering: Draws the current state of the game board in the console.

2. AI Agent (AI)
The AI's decision-making is driven by the Minimax algorithm with Alpha-Beta Pruning. This is an adversarial search algorithm designed for two-player, zero-sum games.

   1. Search: The algorithm explores a tree of possible future moves up to a certain depth (dep_limit) to find the optimal action. Alpha-beta pruning is used to significantly reduce the number of nodes evaluated in the search tree, making the process more efficient.

   2. Heuristic Evaluation Function: When the search reaches its depth limit without finding a terminal (win/loss) state, it uses a heuristic evaluation function (eval) to score the board position. The score is calculated as:
   **Score** = (Opponent's Shortest Path - AI's Shortest Path) + (AI's Walls - Opponent's Walls)
- The AI aims to maximize this score by minimizing its own path to the goal while maximizing the opponent's path.
- The number of remaining walls is used as a tie-breaker and to encourage preserving resources.
- Shortest paths are calculated using a Breadth-First Search (BFS) on the current board state.

##  How To Play
Run the main script from your terminal.

The game board will be displayed, showing the AI's position ('X') and the player's position ('●').

When it's your turn, you will be prompted to enter an action in one of the following formats:

- To move your pawn: ('MOVE', (row, col))

- To place a horizontal wall: ('HWALL', ((row, col), (row, col+1)))

- To place a vertical wall: ('VWALL', ((row, col), (row+1, col)))

For example, to move to the space at row 5, column 3, you would type:

('MOVE', (5, 3))
The game ends when one player's pawn reaches the opposite side of the board.



##  Project Structure

```sh
└── Quoridor-Game-With-AI/
    ├── README.md
    ├── __pycache__
    │   ├── Env.cpython-311.pyc
    │   └── agent.cpython-311.pyc
    ├── agent.py
    └── main.py
```


---
##  Getting Started

###  Prerequisites

Before getting started with Quoridor-Game-With-AI, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python


###  Installation

Install Quoridor-Game-With-AI using one of the following methods:

**Build from source:**

1. Clone the Quoridor-Game-With-AI repository:
```sh
❯ git clone https://github.com/arianaira/Quoridor-Game-With-AI
```

2. Navigate to the project directory:
```sh
❯ cd Quoridor-Game-With-AI
```
3. Run the environment (main.py)

---
