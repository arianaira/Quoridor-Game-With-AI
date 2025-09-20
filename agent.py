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
        # walls is the walls placed so far
        print("Write the action you want to take in this format: \n ('MOVE', (row, col)) or ('HWALL', ((row, col), (row, col+1))) or ('VWALL', ((row, col), (row+1, col)))")
        try:
            p_action = ast.literal_eval(input())

            # Validate the 'MOVE' action
            if p_action[0] == 'MOVE' and isinstance(p_action[1], tuple) and len(p_action[1]) == 2:
                if all(isinstance(coord, int) for coord in p_action[1]):
                    valids = get_valid_moves(walls, self.position[0], self.position[1])
                    if p_action in valids:
                        return p_action
            
            # Validate the 'HWALL' and 'VWALL' actions
            elif p_action[0] in ('HWALL', 'VWALL') and isinstance(p_action[1], tuple) and len(p_action[1]) == 2:
                if all(isinstance(coord, tuple) and len(coord) == 2 and all(isinstance(x, int) for x in coord) for coord in p_action[1]):
                    hors, vers = get_valid_walls(self.remaining_walls, walls)
                    if p_action[0] == "HWALL" and p_action[1] in hors:
                        return p_action
                    if p_action[0] == "VWALL" and p_action[1] in vers:
                        return p_action
            
            print("Invalid action format. Please try again.")
            return self.action(get_valid_moves, get_valid_walls, walls)  # Retry for invalid input

        except (ValueError, SyntaxError):
            print("Invalid input. Please use the correct format.")
            return self.action(get_valid_moves, get_valid_walls, walls)  # Retry
        
class AI(Agent):
    def __init__(self, position, symbol="\u2B24", remaining_walls=10, max=True):
        super().__init__(position, symbol, remaining_walls)
        self.id = 0
        self.max = True

    def action(self, get_valid_actions, placed_walls, opponent_loc, opponent_rem_walls, depth, dep_limit=3):
        # Reduced depth limit from default 6 to 3
        value, move = self.max_value_ab(
            get_valid_actions, placed_walls, self.position, self.remaining_walls,
            opponent_loc, opponent_rem_walls, depth, dep_limit, alpha=-math.inf, beta=math.inf
        )
        return move
    

    
    def max_value_ab(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth, dep_limit, alpha, beta):
        if self.is_terminal(ai_loc, opponent_loc):
            return (self.utility(ai_loc, opponent_loc), None)
        if depth == dep_limit:
            eval_res = self.eval(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
            return (eval_res, None)
        best_v = float('-inf')
        move = None
        valids = get_valid_action(placed_walls, ai_loc[0], ai_loc[1], ai_rem_walls)
        for a in valids:
            new_ai_loc = ai_loc
            new_ai_rem = ai_rem_walls
            new_walls = placed_walls.copy()
            if a[0] == 'MOVE':
                new_ai_loc = a[1]
            elif a[0] in ("HWALL", "VWALL"):
                new_walls.append(a)
                new_ai_rem -= 1
            v2, a2 = self.min_value_ab(
                get_valid_action, new_walls, new_ai_loc, new_ai_rem,
                opponent_loc, opponent_rem_walls, depth + 1, dep_limit, alpha, beta
            )
            if v2 > best_v:
                best_v, move = v2, a
                alpha = max(alpha, best_v)
            if best_v >= beta:
                break  # Prune remaining branches
        return (best_v, move)
    
    def min_value_ab(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth, dep_limit, alpha, beta):
        if self.is_terminal(ai_loc, opponent_loc):
            return (self.utility(ai_loc, opponent_loc), None)
        if depth == dep_limit:
            eval_res = self.eval(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
            return (eval_res, None)
        best_v = float('inf')
        move = None
        valids = get_valid_action(placed_walls, opponent_loc[0], opponent_loc[1], opponent_rem_walls)
        for a in valids:
            new_opp_loc = opponent_loc
            new_opp_rem = opponent_rem_walls
            new_walls = placed_walls.copy()
            if a[0] == 'MOVE':
                new_opp_loc = a[1]
            elif a[0] in ("HWALL", "VWALL"):
                new_walls.append(a)
                new_opp_rem -= 1
            v2, a2 = self.max_value_ab(
                get_valid_action, new_walls, ai_loc, ai_rem_walls,
                new_opp_loc, new_opp_rem, depth + 1, dep_limit, alpha, beta
            )
            if v2 < best_v:
                best_v, move = v2, a
                beta = min(beta, best_v)
            if best_v <= alpha:
                break  # Prune remaining branches
        return (best_v, move)

    def max_value(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth, dep_limit):
        if self.is_terminal(ai_loc, opponent_loc):
            return (self.utility(ai_loc, opponent_loc), None)
        if depth == dep_limit:
            eval_res = self.eval(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
            return (eval_res, None)
        best_v = float('-inf')
        move = None  # Initialize move
        valids = get_valid_action(placed_walls, ai_loc[0], ai_loc[1], ai_rem_walls)
        for a in valids:
            new_ai_loc = ai_loc
            new_ai_rem = ai_rem_walls
            new_walls = placed_walls.copy()
            if a[0] == 'MOVE':
                new_ai_loc = a[1]
            elif a[0] in ("HWALL", "VWALL"):
                new_walls = new_walls + [a]
                new_ai_rem -= 1
            v2, a2 = self.min_value(get_valid_action, new_walls, new_ai_loc, new_ai_rem, opponent_loc, opponent_rem_walls, depth+1, dep_limit)
            if v2 > best_v:
                best_v, move = v2, a
        return best_v, move

    def min_value(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth, dep_limit):
        if self.is_terminal(ai_loc, opponent_loc):
            return (self.utility(ai_loc, opponent_loc), None)
        if depth == dep_limit:
            eval_res = self.eval(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
            return (eval_res, None)
        best_v = float('inf')
        move = None  # Initialize move
        valids = get_valid_action(placed_walls, opponent_loc[0], opponent_loc[1], opponent_rem_walls)
        for a in valids:
            new_opp_loc = opponent_loc
            new_opp_rem = opponent_rem_walls
            new_walls = placed_walls.copy()
            if a[0] == 'MOVE':
                new_opp_loc = a[1]
            elif a[0] in ("HWALL", "VWALL"):
                new_walls = new_walls + [a]
                new_opp_rem -= 1
            v2, a2 = self.max_value(get_valid_action, new_walls, ai_loc, ai_rem_walls, new_opp_loc, new_opp_rem, depth+1, dep_limit)
            if v2 < best_v:
                best_v, move = v2, a
        return best_v, move

    def utility(self, ai_loc, opponent_loc):
        if ai_loc[0] == 6:
            return 1000  # AI wins
        elif opponent_loc[0] == 0:
            return -1000  # Opponent wins
        return 0

    def eval(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls):
        ai_path = self.find_shortest_path_to_max_win(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
        opp_path = self.find_shortest_path_to_min_win(get_valid_action, placed_walls, opponent_loc, opponent_rem_walls)
        return 1000 + opp_path - ai_path + ai_rem_walls - opponent_rem_walls  # Higher value if AI is closer to goal

    def find_shortest_path_to_max_win(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls):
        from collections import deque
        visited = set()
        queue = deque([(ai_loc, 0)])
        visited.add(ai_loc)
        initial_walls = placed_walls.copy()

        while queue:
            current_pos, path_len = queue.popleft()
            if current_pos[0] == 6:
                return path_len
            valid_actions = get_valid_action(initial_walls, current_pos[0], current_pos[1], ai_rem_walls)
            move_actions = [action[1] for action in valid_actions if action[0] == 'MOVE']
            for new_pos in move_actions:
                if new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path_len + 1))
        return float('inf')

    def find_shortest_path_to_min_win(self, get_valid_action, placed_walls, opponent_loc, opponent_rem_walls):
        from collections import deque
        visited = set()
        queue = deque([(opponent_loc, 0)])
        visited.add(opponent_loc)
        initial_walls = placed_walls.copy()

        while queue:
            current_pos, path_len = queue.popleft()
            if current_pos[0] == 0:
                return path_len
            valid_actions = get_valid_action(initial_walls, current_pos[0], current_pos[1], opponent_rem_walls)
            move_actions = [action[1] for action in valid_actions if action[0] == 'MOVE']
            for new_pos in move_actions:
                if new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path_len + 1))
        return float('inf')

    def is_terminal(self, ai_loc, opponent_loc):
        return ai_loc[0] == 6 or opponent_loc[0] == 0
