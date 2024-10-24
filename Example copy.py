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
      while current != init:
          current = self.best_ancestors.get(current,None)
          if current is None:
              return math.inf
          if current == tile:
              return math.inf
          g+=1
      return g

  def get_worst_g(self,tile, init):
      ancestors = set()
      ancestors.add(tile)
      
      current = tile
      g = 0
      while current != init:
          current = self.worst_ancestors.get(current,None)
          if current is None:
              return math.inf
          if current in ancestors:
              return math.inf
          g+=1
          ancestors.add(current)
      return g
    
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
        heapq.heappush(prio_list, (policy.get_best_g(tile,init)+heuristic(tile,goal),tile))
    g,tile = heapq.heappop(prio_list)
    policy.pending.remove(tile)
    
    # 2: pop a random pending state
    # tile = policy.pending.pop()

    return tile

# BRUTE FORCE: generate all pi-trajectories
def update_g_brute(policy, tile, reached_tiles):
    all_new = True
    for reached_tile in reached_tiles:
        # First time reaching the state
        # tile is the best and worst ancestor
        if policy.best_ancestors.get(reached_tile,None) is None:
            policy.best_ancestors[reached_tile] = tile
            policy.worst_ancestors[reached_tile] = tile
        # Not the first time
        else:
            all_new = False
    if all_new:
        return
    
    # ELSE: Update g
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
                    cycles.append(ancestors[ancestors.index(reached_tile):])
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
    if len(cycles) != 0:
        policy.cyclic = True

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

def update_g_values():
    pass


def extend_policy(current_policy, tile, action):
    new_policy = current_policy.copy()
    new_policy.strategy[tile] = action

    # Compute the tiles reached with the new action
    reached_tiles = get_successor_states(tile, action, board)
    # Update the g-values (ancestors) of the reached states 
    update_g_brute(new_policy,tile, reached_tiles) # ACCURATE BUT COSTLY
    # update_g_incremental(new_policy,tile,reached_tiles) # CHEAP, BUT CAN UNDERAPPROXIMATE THE WORST G

    # Compute pending tiles for the new policy
    new_pending = [tile for tile in reached_tiles if tile != goal and new_policy.strategy.get(tile,None) is None]
    new_policy.pending.update(new_pending)

    return new_policy

def compute_f_value(policy):
    if policy.is_closed():
        f_best = policy.get_best_g(goal,init)
        if policy.cyclic:
            f_worst = math.inf
        else:
            f_worst = policy.get_worst_g(goal,init)
    else:
        if policy.best_ancestors.get(goal, None) is not None:
            f_best = policy.get_best_g(goal,init)
        else:
            f_best = min([policy.get_best_g(pending_tile, init) + heuristic(pending_tile,goal) for pending_tile in policy.pending])

        if policy.cyclic:
            f_worst = math.inf
        else:
            f_worst = max([policy.get_worst_g(pending_tile, init) + heuristic(pending_tile,goal) for pending_tile in policy.pending])

    return f_best, f_worst


# %%
def heuristic(current, goal):
    # Blind
    return 0

# %%
def get_applicable_actions(tile, board):

    #deadend
    if tile == 'I':
        return ['I-action']
    if tile == 'A':
        return ['A-action']
    if tile == 'B':
        return ['B-action']
    if tile == 'C':
        return ['C-action']
    if tile == 'D':
        return ['D-action']

    return []

# %%
def get_successor_states(tile,action,board):
    successors = set()

    match action:
        case 'I-action':
            successors.add('A')
            successors.add('B')
        case 'A-action':
            successors.add('C')
            successors.add('G')
        case 'B-action':
            successors.add('D')
        case 'C-action':
            successors.add('I')
        case 'D-action':
            successors.add('G')

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

    repeated = 0
    # Loop until the open list is empty
    while open_list:
        # Get the policy with the lowest f value
        f_value, current_policy = heapq.heappop(open_list)

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
            f_best, f_worst = compute_f_value(new_policy)

            # Uncomment to discard cyclic policies
            # if new_policy.cyclic:
            #     continue

            # Add the child to the open list
            heapq.heappush(open_list, ((f_best,f_worst),new_policy)) # BEST then WORST
            # heapq.heappush(open_list, ((f_worst,f_best),new_policy)) # WORST then BEST

    print(len(closed_list))
    return None  # No policy found

# %%

board = []

init = 'I'
goal = 'G'

# %%
solution = a_star(board, init, goal)
pass