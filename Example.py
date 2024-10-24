# %%
import heapq
import math

# %%
class Policy:
  def __init__(self, strategy, pending):
    self.strategy = strategy  # tile-action map
    # self.closed = closed # tiles closed and their g values
    
    # Pending are tiles reached that have not been mapped to an action yet
    self.pending = pending # tiles pending and their g values

    self.best_ancestors = dict()
    self.worst_ancestors = dict()
    
    # self.best_f = 0  # Total cost (f = g + h)
    # self.worst_f = 0  # Total cost (f = g + h)

    self.closed = False
    self.cyclic = False
    self.proper = False

  def copy(self):
    new_policy = Policy(dict(),set())
    new_policy.strategy = self.strategy.copy()
    new_policy.pending = self.pending.copy()
    new_policy.best_ancestors = self.best_ancestors.copy()
    new_policy.worst_ancestors = self.worst_ancestors.copy()
    new_policy.closed = self.closed
    new_policy.cyclic = self.cyclic
    new_policy.proper = self.proper

    return new_policy

  def __lt__(self, other):
    # if self.best_f < other.best_f:
    #   return True
    # elif self.best_f == other.best_f:
    #   return self.worst_f < other.worst_f
    # else:
    #     return False
    return True
    
  def __eq__(self, other):
    if isinstance(other, Policy):
        return self.strategy == other.strategy
    return False
  
  def get_best_g(self, tile, init):
        current = tile
        g = 0
        # while current != init:
        #     current = self.best_ancestors.get(current,None)
        #     if current is None:
        #         return math.inf
        #     if current == tile:
        #         return math.inf
          
        while current is not None:
            current = self.best_ancestors.get(current,None)
            g+=1
        return g-1

  def get_worst_g(self,tile, init):
      ancestors = set()
      ancestors.add(tile)
      
      current = tile
      g = 0
      while current != None: # reaches the initial state
          current = self.worst_ancestors.get(current,None)
        #   if current is None:
        #       return math.inf
          if current in ancestors:
              return math.inf
          g+=1
          ancestors.add(current)
      return g-1
    
  def check_for_cycles(self, init, board):
    if not self.cyclic:
        frontier = {init:[]}
        while frontier:
            tile,ancestors = frontier.popitem()
            action = self.strategy.get(tile, None)
            if action is not None:
                reached_tiles = get_successor_states(tile,action,board)
                for reached_tile in reached_tiles:
                    if reached_tile in ancestors:
                        self.cyclic = True
                        return self.cyclic
                    new_ancestors = ancestors.copy()
                    new_ancestors.append(tile)
                    frontier[reached_tile] = new_ancestors
        
    return self.cyclic
  
  def is_proper(self, init, goal, board):
    if not self.proper:
        goal_trajectories = list()
        frontier = {init:[]}
        cycle_roots = set()
        while frontier:
            tile,ancestors = frontier.popitem()
            action = self.strategy.get(tile, None)
            if action is None:
                return self.proper
            else:
                reached_tiles = get_successor_states(tile,action,board)
                for reached_tile in reached_tiles:
                    if reached_tile in ancestors:
                        cycle_roots.add(reached_tile)
                    elif reached_tile == goal:
                        goal_trajectories.append(ancestors)
                    else:
                        new_ancestors = ancestors.copy()
                        new_ancestors.append(tile)
                        frontier[reached_tile] = new_ancestors
        # Every cycle root must be goal reaching
        for root in cycle_roots:
            goal_reaching = False
            for trajectory in goal_trajectories:
                if root in trajectory:
                    goal_reaching = True
                    break
            if not goal_reaching:
                return self.proper
        
        self.proper = True
    return self.proper

  def is_closed(self):
    if not self.closed:
        self.closed = len(self.pending) == 0
    return self.closed


def select_pending_state(policy):
    # 1: Expanding lower g first
    prio_list = []
    for tile in policy.pending:
        heapq.heappush(prio_list, (policy.get_best_g(tile,init)+manhattan(tile,goal),tile))
    g,tile = heapq.heappop(prio_list)
    policy.pending.remove(tile)
    
    # 2: pop a random pending state
    # tile = policy.pending.pop()

    # 3: Extend non-infinity g first
    # non_inf_pending = set([tile for tile in policy.pending if policy.get_worst_g(tile,init) < math.inf])
    # inf_pending = set([tile for tile in policy.pending if policy.get_worst_g(tile,init) == math.inf])

    # if len(inf_pending) > 0:
    #     pass

    # if len(non_inf_pending) > 0:
    #     # tile = non_inf_pending.pop()
    #     prio_list = []
    #     for tile in non_inf_pending:
    #         heapq.heappush(prio_list, (-(policy.get_worst_g(tile,init)-manhattan(tile,goal)),tile))
    #     g,tile = heapq.heappop(prio_list)
    # else:
    #     print(len(inf_pending))
    #     tile = inf_pending.pop()
    # policy.pending.remove(tile)

    # 4: establish bounds
    # prio_list = []
    # if policy.best_ancestors.get(goal,None) is None:
    #     for tile in policy.pending:
    #         heapq.heappush(prio_list, (policy.get_best_g(tile,init)+manhattan(tile,goal),tile))
    # else:
    #     for tile in policy.pending:
    #         heapq.heappush(prio_list, (-(policy.get_best_g(tile,init)+manhattan(tile,goal)),tile))
    # g,tile = heapq.heappop(prio_list)
    # policy.pending.remove(tile)

    return tile

# BRUTE FORCE: generate all pi-trajectories
def update_g_values(policy, tile, reached_tiles):
    all_new = True
    for reached_tile in reached_tiles:
        # First time reaching the state
        # tile is the best and worst ancestor
        if policy.best_ancestors.get(reached_tile,None) is None:
            if reached_tile != init:
                policy.best_ancestors[reached_tile] = tile
            policy.worst_ancestors[reached_tile] = tile
        # Not the first time
        else:
            all_new = False
    
    if not all_new:
        update_g_brute(policy)


def update_g_brute(policy):   
    # BRUTE FORCE: Compute al pi-trajectories

    trajectories = list()
    cycles = list()
    frontier = {init:[]}
    while frontier:
        tile,ancestors = frontier.popitem()
        action = policy.strategy.get(tile, None)
        if action is None: #State has no action assigned: end of trajectory
            trajectories.append(ancestors)
        else: # State has action assigned
            reached_tiles = get_successor_states(tile,action,board)
            for reached_tile in reached_tiles:
                if reached_tile in ancestors: # Cycle
                    cycles.append(ancestors[ancestors.index(reached_tile):]+[tile])
                    pass
                else: # Not a cycle
                    if policy.get_worst_g(tile,init) > policy.get_worst_g(policy.worst_ancestors[reached_tile],init):
                        policy.worst_ancestors[reached_tile] = tile
                    if policy.get_best_g(tile,init) < policy.get_best_g(policy.best_ancestors[reached_tile],init):
                        policy.best_ancestors[reached_tile] = tile
                    # Extend trajectory
                    new_ancestors = ancestors.copy()
                    new_ancestors.append(tile)
                    frontier[reached_tile] = new_ancestors
    for cycle in cycles:
        for tile in cycle:
            action = policy.strategy.get(tile, None)
            reached_tiles = get_successor_states(tile,action,board)
            for reached_tile in reached_tiles:
                policy.worst_ancestors[reached_tile] = tile
    if len(cycles) > 0:
        policy.cyclic = True

    #DEBUG
    if not policy.cyclic:
        for tile in policy.pending:
            if policy.get_worst_g(tile, init) == math.inf:
                pass

# THIS METHOD SEEMS TO UNDERAPPROXIMATE THE WORST G
def update_g_incremental(policy, tile, reached_tiles):
    for reached_tile in reached_tiles:
        # First time reaching the state
        # tile is the best and worst ancestor
        if policy.best_ancestors.get(reached_tile,None) is None:
            policy.best_ancestors[reached_tile] = tile
            policy.worst_ancestors[reached_tile] = tile
        # Not the first time: Update g s
        else:
            # new path is less costly
            if policy.get_best_g(tile,init) < policy.get_best_g(policy.best_ancestors[reached_tile],init):
                policy.best_ancestors[reached_tile] = tile
            # new path is more costly
            if policy.get_worst_g(tile,init) > policy.get_worst_g(policy.worst_ancestors[reached_tile],init):
                policy.worst_ancestors[reached_tile] = tile
                # new worst g indicates possible cycle
                policy.check_for_cycles(init, board)



def extend_policy(current_policy, tile, action):
    new_policy = current_policy.copy()
    new_policy.strategy[tile] = action

    # Compute the tiles reached with the new action
    reached_tiles = get_successor_states(tile, action, board)
    # Update the g-values (ancestors) of the reached states 
    update_g_values(new_policy,tile, reached_tiles) # ACCURATE BUT COSTLY
    # update_g_incremental(new_policy,tile,reached_tiles) # CHEAP, BUT CAN UNDERAPPROXIMATE THE WORST G

    # Compute pending tiles for the new policy
    new_pending = [tile for tile in reached_tiles if tile != goal and new_policy.strategy.get(tile,None) is None]
    new_policy.pending.update(new_pending)

    return new_policy

def compute_f_value(policy):
    # if policy.is_closed():
    #     f_best = policy.get_best_g(goal,init)
    #     if policy.cyclic:
    #         f_worst = math.inf
    #     else:
    #         f_worst = policy.get_worst_g(goal,init)
    # else:
    #     if policy.best_ancestors.get(goal, None) is not None:
    #         f_best = policy.get_best_g(goal,init)
    #     else:
    #         f_best = min([policy.get_best_g(pending_tile, init) + manhattan(pending_tile,goal) for pending_tile in policy.pending])

    #     if policy.cyclic:
    #         f_worst = math.inf
    #     else:
    #         f_worst = max([policy.get_worst_g(pending_tile, init) + manhattan(pending_tile,goal) for pending_tile in policy.pending])

    Out = policy.pending.copy()
    if policy.best_ancestors.get(goal, None) is not None: # This is for policies that already reach the goal
        Out.add(goal)
    f_best = min([policy.get_best_g(tile, init) + manhattan(tile,goal) for tile in Out], default=math.inf)
    f_worst = max([policy.get_worst_g(tile, init) + manhattan(tile,goal) for tile in Out], default=math.inf)
    # f_close = len(policy.pending)
    # h_vector = sorted([manhattan(tile, goal) for tile in policy.pending])
    # if len(h_vector) > 0:
    #     f_close = max([h_vector[i] + i for i in range(len(h_vector))])
    # else:
    #     f_close = 0


    f_close = 0

    return f_best, f_worst, f_close


# %%
def manhattan(current, goal):
    # Use Manhattan distance as heuristic
    # Slightly modified to account for double movement (slips)
    return math.ceil(abs(current[0] - goal[0])/2) + math.ceil(abs(current[1] - goal[1])/2)

# %%
def get_applicable_actions(tile, board):
    applicable_actions = []
    rows = len(board)
    columns = len(board[0])
    tile_column = tile[0]
    tile_row = tile[1]

    #deadend
    if board[tile_column][tile_row] == 'H':
        return applicable_actions

    #right
    if tile_column < columns-1 and board[tile_column+1][tile_row] != 'O':
        applicable_actions += ['R']
    #left
    if tile_column > 0 and board[tile_column-1][tile_row] != 'O':
        applicable_actions += ['L']
    #up
    if tile_row < rows-1 and board[tile_column][tile_row+1] != 'O':
        applicable_actions += ['U']
    #down
    if tile_row > 0 and board[tile_column][tile_row-1] != 'O':
        applicable_actions += ['D']

    return applicable_actions

# %%
def get_successor_states(tile,action,board):
    successors = set()

    rows = len(board)
    columns = len(board[0])
    tile_column = tile[0]
    tile_row = tile[1]

    if board[tile_column][tile_row] == 'H':
        return successors

    match action:
        case 'R':
            successors.add((tile_column+1,tile_row))
            if tile_column < columns-2 and board[tile_column+1][tile_row] != 'H' and board[tile_column+2][tile_row] != 'O':
                successors.add((tile_column+2,tile_row))
        case 'L':
            successors.add((tile_column-1,tile_row))
            if tile_column > 1 and board[tile_column-1][tile_row] != 'H' and board[tile_column-2][tile_row] != 'O':
                successors.add((tile_column-2,tile_row))
        case 'U':
            successors.add((tile_column,tile_row+1))
            if tile_row < rows-2 and board[tile_column][tile_row+1] != 'H' and board[tile_column][tile_row+2] != 'O':
                successors.add((tile_column,tile_row+2))
        case 'D':
            successors.add((tile_column,tile_row-1))
            if tile_row > 1 and board[tile_column][tile_row-1] != 'H' and board[tile_column][tile_row-2] != 'O':
                successors.add((tile_column,tile_row-2))


    return successors

# %%
def a_star(board, init, goal):
    # Create start and end node

    # Initialize open and closed list
    open_list = []
    closed_list = set()
    
    # Generate empty policy
    empty_policy = Policy(dict(),{init})
    # Push the empty policy onto the open list
    heapq.heappush(open_list, ((0,0), empty_policy))

    pareto_frontier = []
    pareto_f = (math.inf, math.inf)
    repeated = 0
    # Loop until the open list is empty
    while open_list:
        # Get the policy with the lowest f value
        f_value, current_policy = heapq.heappop(open_list)

        # Pruning non-Pareto solutions
        if f_value[0] >= pareto_f[0] and f_value[1] >= pareto_f[1]:
            continue

        # CLOSED LIST SEEMS UNNECESSARY
        hashable_strategy = frozenset(current_policy.strategy.items())
        if hashable_strategy in closed_list:
            repeated += 1
            pass # Add a breakpoint here to see hits
        closed_list.add(hashable_strategy)
        

        # Check if the policy is closed
        if current_policy.is_closed():
            # If closed and proper, it is a solution
            if current_policy.is_proper(init, goal, board):
                # f_best, f_worst = compute_f_value(current_policy)
                pareto_frontier += [current_policy]
                pareto_f = (f_value[0], f_value[1])
                continue # Uncomment and add breakpoint to see all solutions
                return current_policy
            # If closed but not proper, not a solution
            else:
                continue

        # Select a state from Out~(current_policy)
        tile = select_pending_state(current_policy)

        applicable_actions = get_applicable_actions(tile, board)
        for action in applicable_actions:
            # Create new_policy by extending current_policy
            # Extension: map tile to action
            new_policy = extend_policy(current_policy, tile, action)

            # Calculate new_policy's f-value
            f_best, f_worst, f_close = compute_f_value(new_policy)

            # Uncomment to discard cyclic policies
            if new_policy.cyclic:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, ((f_best,f_worst, f_close),new_policy)) # BEST then WORST
            # heapq.heappush(open_list, ((f_worst,f_best, f_close),new_policy)) # WORST then BEST

    print(len(closed_list))
    return None  # No policy found

# %%
rows = 6
columns = 6

# 'F' = frozen tile, # 'O' = obstacle, # 'H' = hole
board = [['F'for i in range(rows)] for j in range(columns) ]

board[4][5] = 'H'
board[1][4] = 'H'
board[4][3] = 'H'
board[4][1] = 'H'
board[1][1] = 'O'
board[2][1] = 'O'

init = (0,5)
goal = (5,5)

# %%
# solution = a_star(board, init, goal)
# pass

strategy1 = {
    (0,5): "R",
    (2,5): "D",
    (1,5): "R",
    (2,4): "R",
    (3,4): "R",
    (5,4): "U",
    (2,3): "D",
    (2,2): "R",
    (4,2): "R",
    (3,2): "R",
    (5,2): "U",
    (5,3): "U",
    (4,4): "R",
    (3,5): "D",
    (3,3): "U",
}

strategy2 = {
    (0,5) : "R",
    (1,5) : "R",
    (2,5) : "D",
    (2,4) : "D",
    (3,5) : "D",
    (3,4) : "R",
    (5,4) : "U",
    (2,2) : "R",
    (3,2) : "R",
    (5,2) : "U",
    (4,2) : "R",
    (5,3) : "U",
    (4,4) : "R",
    (2,3) : "D",
    (3,3) : "U"
}

pi = Policy(dict(), {(0,5)})

while len(pi.pending) != 0:
    tile = pi.pending.pop()
    pi = extend_policy(pi, tile, strategy2[tile])

f_score = compute_f_value(pi)
pass