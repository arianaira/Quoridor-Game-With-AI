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
    def __init__(self, position, symbol = "\u2B24", remaining_walls = 10, max=True):
        super().__init__(position, symbol, remaining_walls)
        self.id = 0
        self.max= True
        
    def max_value(self, get_valid_action, placed_walls, opponent_loc,opponent_rem_walls, depth, dep_limit):
        if (self.is_terminal(opponent_loc)): 
            return (self.utility(), None)
        if (depth == dep_limit):
            return self.eval(get_valid_action, placed_walls, opponent_loc, opponent_rem_walls) 
        best_v = float('-inf')
        for a in get_valid_action():
            v2, a2 = self.min_value(get_valid_action, placed_walls, opponent_loc, depth-1, dep_limit)
            if v2 > best_v:
                best_v, move = v2, a
        return best_v, move

    def min_value(self, get_valid_action, placed_walls, opponent_loc,opponent_rem_walls, depth, dep_limit):
        if (self.is_terminal( opponent_loc)): 
            return (self.utility(), None)
        if (depth == dep_limit):
            return self.eval(get_valid_action, placed_walls, opponent_loc, opponent_rem_walls) 
        best_v = float('inf')
        for a in get_valid_action():
            v2, a2 = self.max_value(get_valid_action, placed_walls, opponent_loc, depth-1, dep_limit)
            if v2 < best_v:
                best_v, move = v2, a
        return best_v, move

    def utility(self):
        return 1000 * (self.position[0])/6
        # scaling u between 0 and 1000

    def eval(self, get_valid_action, placed_walls, opponent_loc, opponent_rem_walls):
        return self.find_shortest_path_to_max_win(get_valid_action, placed_walls, opponent_loc, opponent_rem_walls)


    def find_shortest_path_to_max_win(self, get_valid_action, placed_walls, opponent_loc, opponent_rem_walls):

        root = {'walls': placed_walls, 'opp_loc':opponent_loc,'opp_rem_wall': opponent_rem_walls,
                'ai_pos': self.position.copy(), 'ai_rem_wall': self.remaining_walls.copy(), 'last_turn':'human', 'path_len': 0}
        queue = [root]

        while len(queue) > 0:
            cur_node = queue.pop(0)
            if(cur_node['ai_pos'][0] == 6): #win
                return cur_node['path_len']
            
            placed_walls_inAImind = cur_node['walls']


            if(cur_node['last_turn']=='human'):
                for act in get_valid_action(cur_node['walls'], cur_node['ai_pos'][0], cur_node['ai_pos'][1]):
                        placed_walls_inAImind, pos, rem_walls = self.update_state(act, placed_walls_inAImind, cur_node['ai_rem_walls'])

                        new_state =  {'walls': placed_walls_inAImind, 'opp_loc':cur_node['opp_loc'],
                                      'opp_rem_wall': cur_node['opp_rem_walls'], 'ai_pos': pos, 
                                      'ai_rem_wall': rem_walls, 'last_turn':'ai', 'path_len': cur_node['path_len']+1}
            
            if(cur_node['last_turn']=='ai'):
                for act in get_valid_action(cur_node['walls'], cur_node['opp_loc'][0], cur_node['opp_loc'][1]):
                        placed_walls_inAImind, pos, rem_walls = self.update_state(act, placed_walls_inAImind, cur_node['opp_rem_walls'])

                        new_state =  {'walls': placed_walls_inAImind, 'opp_loc':pos ,'opp_rem_wall': rem_walls,
                                      'ai_pos': cur_node['ai_pos'], 'ai_rem_wall': cur_node['ai_rem_walls'],
                                      'last_turn':'human', 'path_len': cur_node['path_len']+1}
       
            queue.append(new_state)


    def update_state(self, action, placed_walls_inAImind, remaining_walls):
        if action[0] == "MOVE":
            pos = action[1]
        elif action[0] == "HWALL" or action[0] == "VWALL":
            placed_walls_inAImind.append(action)
            rem_walls = remaining_walls - 1

        return (placed_walls_inAImind, pos, rem_walls)


    def is_terminal(self,  opponent_loc):
        """Determine if the current state is terminal (end of game)."""
        if (self.position[0]==6):
            return True
        elif (opponent_loc[0] == 0):
            return True
        else:
            return False


        
    def action(self, get_valid_actions, placed_walls, opponent_loc, depth, dep_limit):
        value, move = self.max_value(get_valid_actions, placed_walls, opponent_loc, depth, dep_limit)
        return move
       # it should get percept and recall minimax and return the selected output
    
                
                
   