import sys
from typing import Tuple, List, Optional
from agent import AI, Player 

class QuoridorEnv:
    def __init__(self,player, ai, board_size: int = 7, initial_walls: int = 10):
        self.board_size = board_size
        self.walls_left = [initial_walls, initial_walls]
        self.current_player = 1  #0 is for ai and 1 for human player
        self.player = player
        self.ai = ai     
        self.walls_placed = []    # alist of tuples like ('Hwall/Vwall', ((x,y),(x+1,y)))
        
    def get_state(self):
        return self.player.position, self.ai.position, self.player.remaining_walls, self.ai.remaining_walls, self.walls_placed
        
    def get_valid_actions(self, walls_placed, r, c):
        # moves
        valid_actions = self.get_valid_moves(walls_placed, r, c)
        
        # wall placement
        hors, vers = self.get_valid_walls(walls_placed)
        for wall in hors:
            valid_actions.append(("HWALL", wall))
        for wall in vers:
            valid_actions.append(("VWALL", wall))
        return valid_actions   # a list of tuples ('hwall/vwall', ((ij), (ij))) or ('move', (ij))
    
        
    def get_valid_moves(self, walls_placed, r, c):
        valid_actions = []
        
        # Up
        valid = True
        for wall in walls_placed:
            if wall[0] == "HWALL" and (r - 1, c) in wall[1]:
                valid = False
                break
        if r > 0 and valid:  
            valid_actions.append(("MOVE", (r-1, c)))
            
        # Down
        valid = True
        for wall in walls_placed:
            if wall[0] == "HWALL" and (r, c) in wall[1]:
                valid = False
                break
        if r < 6 and valid:
            valid_actions.append(("MOVE", (r+1, c)))
            
        # Left
        valid = True
        for wall in walls_placed:
            if wall[0] == "VWALL" and (r, c - 1) in wall[1]:
                valid = False
                break
        if c > 0 and valid:
            valid_actions.append(("MOVE", (r, c-1)))
            
        # Right
        valid = True
        for wall in walls_placed:
            if wall[0] == "VWALL" and (r, c) in wall[1]:
                valid = False
                break
        if c < 6 and valid:
            valid_actions.append(("MOVE", (r, c+1)))
        return valid_actions
    
      
    def get_valid_walls(self, walls_placed):
        hors = []
        for i in range(0, 6):
            for j in range(0, 6):
                new = ((i, j), (i, j+1)) #new wall to be checked
                is_occupied = False
                for wall in walls_placed:
                    if wall[0] == "HWALL" and (new[0] in wall[1] or new[1] in wall[1]):
                        is_occupied = True
                        break
                if not is_occupied:
                    hors.append(new)
                
        vers = []
        for j in range(0, 6):
            for i in range(0, 6):
                new = ((i, j), (i+1, j))
                is_occupied = False
                for wall in walls_placed:
                    if wall[0] == "VWALL" and (new[0] in wall[1] or new[1] in wall[1]):
                        is_occupied =True
                        break
                if not is_occupied:
                    vers.append(new)
                    
        return hors, vers # each is a list of tuples of ((i,j), (i',j'))

    def update_state(self, action, id):
        # only valid actions are passed to this function
        print("id", id)
        print(action[0])
        if id == 1:
            if action[0] == "MOVE":
                self.player.position = action[1]
            elif action[0] == "HWALL" or action[0] == "VWALL":
                self.walls_placed.append(action)
                self.player.remaining_walls -= 1
            self.current_player = 0         
        elif id == 0:
            if action[0] == "MOVE":
                self.ai.position = action[1]
            elif action[0] == "HWALL" or action[0] == "VWALL":
                self.walls_placed.append(action)
                self.player.remaining_walls -= 1
            self.current_player = 1 
        self.render()
    
    
    def goal_test(self):
        if self.player.position[0] == 0:
            return True, 1
        elif self.ai.position[0] == 6:
            return True, 0
        return False, None    
      
            
    def render(self, stream=sys.stdout):
        print("    " + " ".join([f"{c:^3}" for c in range(self.board_size)]), file=stream)
        print("    -----" + "---" * self.board_size, file=stream)

        for r in range(self.board_size):
            row_str = f"{r:2d} |"
            for c in range(self.board_size):
                # Check if there's a player at (r, c)
                if (r, c) == self.player.position:
                    cell_symbol = self.player.symbol
                elif (r, c) == self.ai.position:
                    cell_symbol = self.ai.symbol
                else:
                    cell_symbol = "."
                row_str += f" {cell_symbol} "
                
                # Check if there's a vertical wall to the right of (r, c)
                value = True
                if c < self.board_size - 1:
                    for wall in self.walls_placed:
                        if wall[0] == "VWALL" and (r, c) in wall[1]:
                            row_str += "|"
                            value = False
                            break
                    if value:
                        row_str += " "
            print(row_str, file=stream)

            # Print horizontal walls row, if not the last row
            if r < self.board_size - 1:
                hwall_str = "     "
                for c in range(self.board_size):
                    value = True
                    for wall in self.walls_placed:
                        if wall[0] == "HWALL" and (r, c) in wall[1]:
                            hwall_str += "----"
                            value = False
                            break
                    if value:
                        hwall_str += "    "
                print(hwall_str, file=stream)
        print("", file=stream) 


if __name__ == "__main__":
    ai = AI(position = (0, 3), symbol = "X")
    player = Player(position = (6, 3))
    env = QuoridorEnv(player, ai, board_size=7, initial_walls=10)
    env.render()
    
    end = False # false as long as the game is going on
    while not end:
        p_action = None
        print("remaining walls for player:", env.player.remaining_walls, "\nremaining walls for AI:", env.ai.remaining_walls)
        print(env.current_player)
        if env.current_player == 1:
            p_action = player.action(env.get_valid_moves, env.get_valid_walls, env.walls_placed)
        elif env.current_player == 0:
            p_action = ai.action(env.get_valid_actions, env.walls_placed, player.position,  player.remaining_walls, 10, 2)
        env.update_state(p_action, env.current_player)  # change turns for next iter
        end, winner = env.goal_test()
        # end = True
    
    if winner == 1:
        print("Congratulation player, you beat the AI!")
    elif winner == 0:
        print("AI won, better luck next time!")
