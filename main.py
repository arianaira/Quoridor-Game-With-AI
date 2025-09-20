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
        self.walls_placed = []    # a list of tuples like ('Hwall/Vwall', ((x,y),(x+1,y)))
        
    def get_state(self):
        return self.player.position, self.ai.position, self.player.remaining_walls, self.ai.remaining_walls, self.walls_placed
        
    def get_valid_actions(self, walls_placed, r, c, rem_walls):
        # moves
        valid_actions = self.get_valid_moves(walls_placed, r, c)
        
        # wall placement
        hors, vers = self.get_valid_walls(rem_walls, walls_placed)
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
    
    def get_valid_walls(self, rem_walls, walls_placed):
        if rem_walls <= 0:
            return [], []
        
        # Precompute existing wall positions
        existing_h = set()
        existing_v = set()
        for wall in walls_placed:
            if wall[0] == "HWALL":
                existing_h.add(wall[1][0])
            elif wall[0] == "VWALL":
                existing_v.add(wall[1][0])

        hors = []
        # Check horizontal walls
        for i in range(6):
            for j in range(6):
                # Check horizontal wall at ((i,j), (i,j+1))
                # Check overlaps with existing horizontal walls
                if (i, j) in existing_h or (i, j-1) in existing_h:
                    continue
                if (i, j+1) in existing_h:
                    continue
                # Check overlaps with vertical walls
                vertical_conflict = False
                # Check if any vertical wall covers (i,j) or (i,j+1)
                if ((i-1, j) in existing_v or (i, j) in existing_v or 
                    (i-1, j+1) in existing_v or (i, j+1) in existing_v):
                    vertical_conflict = True
                if vertical_conflict:
                    continue
                
                # Temporarily add wall and check paths
                temp_walls = walls_placed.copy()
                temp_walls.append(("HWALL", ((i,j), (i,j+1))))
                ai_path = self.is_path_available(self.ai.position, 6, temp_walls)
                player_path = self.is_path_available(self.player.position, 0, temp_walls)
                if ai_path and player_path:
                    hors.append(((i,j), (i,j+1)))

        vers = []
        # Check vertical walls
        for j in range(6):
            for i in range(6):
                # Check vertical wall at ((i,j), (i+1,j))
                # Check overlaps with existing vertical walls
                if (i, j) in existing_v or (i-1, j) in existing_v:
                    continue
                if (i+1, j) in existing_v:
                    continue
                # Check overlaps with horizontal walls
                horizontal_conflict = False
                # Check if any horizontal wall covers (i,j) or (i+1,j)
                if ((i, j) in existing_h or (i, j-1) in existing_h or 
                    (i+1, j) in existing_h or (i+1, j-1) in existing_h):
                    horizontal_conflict = True
                if horizontal_conflict:
                    continue
                
                # Temporarily add wall and check paths
                temp_walls = walls_placed.copy()
                temp_walls.append(("VWALL", ((i,j), (i+1,j))))
                ai_path = self.is_path_available(self.ai.position, 6, temp_walls)
                player_path = self.is_path_available(self.player.position, 0, temp_walls)
                if ai_path and player_path:
                    vers.append(((i,j), (i+1,j)))

        return hors, vers


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
                self.ai.remaining_walls -= 1
            self.current_player = 1 
        self.render()
    
    
    def goal_test(self):
        if self.player.position[0] == 0:
            return True, 1
        elif self.ai.position[0] == 6:
            return True, 0
        return False, None    
        
    def is_path_available(self, start_pos, target_row, walls_placed):
        # Preprocess walls into sets
        horizontal = set()
        vertical = set()
        for wall in walls_placed:
            if wall[0] == "HWALL":
                pos = wall[1][0]
                horizontal.add(pos)
            elif wall[0] == "VWALL":
                pos = wall[1][0]
                vertical.add(pos)
        
        from collections import deque
        visited = set()
        queue = deque([(start_pos[0], start_pos[1])])
        visited.add((start_pos[0], start_pos[1]))
        board_size = self.board_size

        while queue:
            r, c = queue.popleft()
            if r == target_row:
                return True

            # Up
            if r > 0:
                blocked = (r-1, c) in horizontal or (r-1, c-1) in horizontal
                if not blocked and (r-1, c) not in visited:
                    visited.add((r-1, c))
                    queue.append((r-1, c))
            # Down
            if r < board_size - 1:
                blocked = (r, c) in horizontal or (r, c-1) in horizontal
                if not blocked and (r+1, c) not in visited:
                    visited.add((r+1, c))
                    queue.append((r+1, c))
            # Left
            if c > 0:
                blocked = (r, c-1) in vertical or (r-1, c-1) in vertical
                if not blocked and (r, c-1) not in visited:
                    visited.add((r, c-1))
                    queue.append((r, c-1))
            # Right
            if c < board_size - 1:
                blocked = (r, c) in vertical or (r-1, c) in vertical
                if not blocked and (r, c+1) not in visited:
                    visited.add((r, c+1))
                    queue.append((r, c+1))
        return False

    from functools import lru_cache


    @lru_cache(maxsize=1024)
    def cached_path_check(self, ai_pos, player_pos, walls_tuple):
        # Convert walls list to tuple for hashing
        return (
            self.is_path_available(ai_pos, 6, list(walls_tuple)),
            self.is_path_available(player_pos, 0, list(walls_tuple))
        )

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
            p_action = ai.action(env.get_valid_actions, env.walls_placed, player.position,  player.remaining_walls, 0, 2)
        env.update_state(p_action, env.current_player)  # change turns for next iter
        end, winner = env.goal_test()
        # end = True
    
    if winner == 1:
        print("Congratulation player, you beat the AI!")
    elif winner == 0:
        print("AI won, better luck next time!")
