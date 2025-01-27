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
        
    def max_value(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth, dep_limit):
        if (self.is_terminal(opponent_loc)): 
            return (self.utility(), None)
        if (depth == dep_limit):
            return self.eval(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls) , None
        best_v = float('-inf')
        valids = get_valid_action(placed_walls, ai_loc[0], ai_loc[1])
        # print("1 valid actions", valids)
        for a in valids:
            #print(a)
            if a[0] == 'MOVE':
                ai_loc = a[1]
            elif a[0] == "HWALL" or a[0] == "VWALL":
                placed_walls.append(a)
                ai_rem_walls -= 1
            v2, a2 = self.min_value(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth+1, dep_limit)
            if v2 > best_v:
                best_v, move = v2, a
        return best_v, move

    def min_value(self, get_valid_action, placed_walls,  ai_loc, ai_rem_walls, opponent_loc,opponent_rem_walls, depth, dep_limit):
        if (self.is_terminal( opponent_loc)): 
            return (self.utility(), None)
        if (depth == dep_limit):
            return self.eval(get_valid_action, placed_walls, opponent_loc, opponent_rem_walls) 
        best_v = float('inf')
        valids = get_valid_action(placed_walls, opponent_loc[0], opponent_loc[1])
        
        for a in valids:
            if a[0] == 'MOVE':
                opponent_loc = a[1]
            elif a[0] == "HWALL" or a[0] == "VWALL":
                placed_walls.append(a)
                opponent_rem_walls -= 1
            #print(a)
            v2, a2 = self.max_value(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls, depth+1, dep_limit)
            if v2 < best_v:
                best_v, move = v2, a
        return best_v, move

    def utility(self):
        return 1000 * (self.position[0])/6
        # scaling u between 0 and 1000

    def eval(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls):
        res=  self.find_shortest_path_to_max_win(get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls)
        print('eval result ', res)
        return res

    def find_shortest_path_to_max_win(self, get_valid_action, placed_walls, ai_loc, ai_rem_walls, opponent_loc, opponent_rem_walls):
        pos_cop = ai_loc
        rem_wall_cop = ai_rem_walls
        root = {'walls': placed_walls, 'opp_loc':opponent_loc,'opp_rem_wall': opponent_rem_walls,
                'ai_pos': pos_cop, 'ai_rem_wall': rem_wall_cop, 'last_turn':'human', 'path_len': 0}
        queue = [root]
        finish_not = True
        while len(queue) > 0:
            cur_node = queue.pop(0)
            if(cur_node['ai_pos'][0] == 6): #win
                print('pp', cur_node['path_len'])
                finish_not = False
                return cur_node['path_len']
            
           
            #if(cur_node['last_turn']=='human'):
            if finish_not:
                placed_walls_inAImind = cur_node['walls']
                valid_actions = get_valid_action(cur_node['walls'], cur_node['ai_pos'][0], cur_node['ai_pos'][1])
                for act in valid_actions:
                        
                        if (act[0]!='MOVE'):
                            continue
                        print(act)
                        
                        placed_walls_inAImind = cur_node['walls']
                        placed_walls_inAImind, pos, rem_walls = self.update_state( cur_node['ai_pos'], act, placed_walls_inAImind, cur_node['ai_rem_wall'])

                        new_state =  {'walls': placed_walls_inAImind, 'opp_loc':cur_node['opp_loc'],
                                      'opp_rem_wall': cur_node['opp_rem_wall'], 'ai_pos': pos, 
                                      'ai_rem_wall': rem_walls, 'last_turn':'ai', 'path_len': cur_node['path_len']+1}
                        queue.append(new_state)
                        print(new_state)
            
            # if(cur_node['last_turn']=='ai'):
            #     placed_walls_inAImind = cur_node['walls']
            #     valid_ac = get_valid_action(cur_node['walls'], cur_node['opp_loc'][0], cur_node['opp_loc'][1])
            #     for act in valid_ac:
                        
            #             placed_walls_inAImind = cur_node['walls']

            #             placed_walls_inAImind, pos, rem_walls = self.update_state(cur_node['opp_loc'], act, placed_walls_inAImind, cur_node['opp_rem_wall'])

            #             new_state =  {'walls': placed_walls_inAImind, 'opp_loc':pos ,'opp_rem_wall': rem_walls,
            #                           'ai_pos': cur_node['ai_pos'], 'ai_rem_wall': cur_node['ai_rem_wall'],
            #                           'last_turn':'human', 'path_len': cur_node['path_len']+1}
                        
            #             queue.append(new_state)
            #             #print(new_state)
  

    def update_state(self, agent_loc, action, placed_walls_inAImind, agent_remaining_walls):
        #pos = self.position
        pos = agent_loc
        walls = placed_walls_inAImind.copy()
        if action[0] == "MOVE":
            pos = action[1]
        elif action[0] == "HWALL" or action[0] == "VWALL":
            walls.append(action)
            agent_remaining_walls = agent_remaining_walls - 1

        return (walls, pos, agent_remaining_walls)


    def is_terminal(self,  opponent_loc):
        """Determine if the current state is terminal (end of game)."""
        if (self.position[0]==6):
            return True
        elif (opponent_loc[0] == 0):
            return True
        else:
            return False


        
    def action(self, get_valid_actions, placed_walls, opponent_loc, opponent_rem_walls, depth, dep_limit):
        value, move = self.max_value(get_valid_actions, placed_walls, self.position, self.remaining_walls, opponent_loc, opponent_rem_walls, depth, dep_limit)
        print(move)
        return move
       # it should get percept and recall minimax and return the selected output
    
                
                
   