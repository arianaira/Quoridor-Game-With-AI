import ast
import math

class Agent():
    def __init__(self, position, symbol = "\u2B24", remaining_walls = 10):
        self.position = position  # (row, col)
        self.symbol = symbol
        self.remaining_walls = remaining_walls

    def action(self):
        pass
    
        
class Player(Agent):
    def __init__(self, position, symbol = "\u2B24", remaining_walls = 10):
        super().__init__(position, symbol, remaining_walls)
        self.id = 1
    
    def action(self, get_valid_moves, get_valid_walls, walls):
        print("Write the action you want to take in this format: \n ('MOVE', (row, col)) or ('HWALL', ((row, col), (row, col+1))) or ('VWALL', ((row, col), (row+1, col)))")
        try:
            p_action = ast.literal_eval(input())

            # Validate the 'MOVE' action
            if p_action[0] == 'MOVE' and isinstance(p_action[1], tuple) and len(p_action[1]) == 2:
                if all(isinstance(coord, int) for coord in p_action[1]):
                    if p_action in get_valid_moves():
                        return p_action
            
            # Validate the 'HWALL' and 'VWALL' actions
            elif p_action[0] in ('HWALL', 'VWALL') and isinstance(p_action[1], tuple) and len(p_action[1]) == 2:
                if all(isinstance(coord, tuple) and len(coord) == 2 and all(isinstance(x, int) for x in coord) for coord in p_action[1]):
                    hors, vers = get_valid_walls(walls)
                    if p_action[0] == "HWALL" and p_action[1] in hors:
                        return p_action
                    if p_action[0] == "VWALL" and p_action[1] in vers:
                        return p_action
            
            print("Invalid action format. Please try again.")
            return self.action()  # Retry for invalid input

        except (ValueError, SyntaxError):
            print("Invalid input. Please use the correct format.")
            return self.action()  # Retry
        
class AI(Agent):
    def __init__(self, position, symbol = "\u2B24", remaining_walls = 10):
        super().__init__(position, symbol, remaining_walls)
        self.id = 0
        
    def simulate_state(self, get_state):
        pass
    

    def minimax(self, state, depth, is_maximizing, get_valid_actions, evaluate_state, get_state):
        """
        Minimax algorithm for decision-making in a two-player game.

        Args:
            state: The current state of the game.
            depth: The maximum depth for the minimax search.
            is_maximizing: A boolean indicating whether the current layer is maximizing.
            get_valid_actions: A function that returns valid actions for the given state and player.
            evaluate_state: A function that evaluates the given state and returns a score.
            
        Returns:
            The best action for the player and its evaluation score.
            """
        if depth == 0 or self.is_terminal(state):
            return None, evaluate_state(state)  # No action, just the score

        best_action = None
        
        selected_actions = []
        root = Simulated_state(get_state)
        children = []
        valid_actions = get_valid_actions(self, self.walls_placed, self.ai_position[0], self.ai_position[1])
        for action in valid_actions:
            children.append(root.create_child(action))
        
        
        if is_maximizing:
            max_eval = -math.inf
            for action in get_valid_actions(state, is_maximizing):
                new_state = self.apply_action(state, action, is_maximizing)
                _, eval_score = self.minimax(new_state, depth - 1, False, get_valid_actions, evaluate_state)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_action = action
            return best_action, max_eval
        else:
            min_eval = math.inf
            for action in get_valid_actions(state, is_maximizing):
                new_state = self.apply_action(state, action, is_maximizing)
                _, eval_score = self.minimax(new_state, depth - 1, True, get_valid_actions, evaluate_state)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_action = action
            return best_action, min_eval

    # Helper Functions:
    def is_terminal(state):
        """Determine if the current state is terminal (end of game)."""
        # Replace with actual terminal condition logic
        return False

    def apply_action(state, action, is_maximizing):
        """Apply an action to the state and return the new state."""
        # Deep copy the state and modify based on the action
        # Replace with actual game logic
        new_state = state.copy()
        if action[0] == 'MOVE':
            new_state['players'][0 if is_maximizing else 1]['position'] = action[1]
        elif action[0] in ('HWALL', 'VWALL'):
            new_state['walls'].append(action[1])
            new_state['players'][0 if is_maximizing else 1]['remaining_walls'] -= 1
        return new_state

        
    def action(self):
        pass # it should get percept and recall minimax and return the selected output
    
class Simulated_state():
    def __init__(self, get_state):
        self.player_position, self.ai_position, self.player_remaining_walls, self.ai_remaining_walls, self.walls_placed = get_state()
        
    def expland(self, get_valid_actions):
        pass
        
                
                
    def update_state(self, action):
        if action[0] == "MOVE":
            self.ai_position = action[1]
        elif action[0] == "HWALL" or action[0] == "VWALL":
            self.walls_placed.append(action)
            self.player.remaining_walls -= 1
        self.current_player = 1 