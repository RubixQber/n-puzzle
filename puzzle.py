import math
"""
@author Joshua Lowe
This program uses 3 different search methods to find solutions to n-puzzles.
BidirectionalSearch works fairly well up until 30-move solutions. BFS and DFS
are much less time efficient, and work well until 15-20 move solutions.
"""

# This method takes in a file, checks for errors, and 
def loadfromfile(filepath):
    f = open(filepath, "r")
    try:
        n = int(f.readline())
        matrix = f.read()
        array = [line.split("\t") for line in matrix.strip().split("\n")]
        formed = len(array) == n and all([len(line) == n for line in array])
        checker = [str(x) for x in range(1, int(math.pow(n, 2)))] + ["*"]
        gamestate = split_breaks_and_tabs(matrix)
        assert formed and sorted(gamestate) == sorted(checker)
        return gamestate
    except:
        print("Something is wrong with your input file.")

def split_breaks_and_tabs(string):
    x = string.strip().replace("\n", " ").replace("\t", " ")
    return x.split(" ")

def ComputeNeighbors(state):
    n = int(math.sqrt(len(state)))
    loc = state.index("*")
    newstates = []
    if loc % n != 0:
        newstates.append(swap(state, loc, loc - 1))
    if loc % n != n - 1:
        newstates.append(swap(state, loc, loc + 1))
    if loc >= n:
        newstates.append(swap(state, loc, loc - n))
    if loc <= math.pow(n, 2) - n - 1:
        newstates.append(swap(state, loc, loc + n))
    return newstates

def swap(state, index1, index2):
    copy = list(state[:])
    temp = copy[index1]
    copy[index1] = copy[index2]
    copy[index2] = temp
    return (copy[index1], tuple(copy))

def IsGoal(state):
    return state == tuple([str(x) for x in range(1, len(state))] + ["*"])

def BFS(state):
    return directional_search(state, 0)

def DFS(state):
    return directional_search(state, -1)

def directional_search(state, direction):
    state = tuple([None, tuple(state)])
    frontier = [state]
    discovered = set(state)
    parents = {state[1]: None}
    while frontier:
        current_state = frontier.pop(direction)
        discovered.add(current_state[1])
        if IsGoal(current_state[1]):
            return parent_search(parents, current_state)
        for neighbor in ComputeNeighbors(current_state[1]):
            if neighbor[1] not in discovered:
                frontier.append(neighbor)
                discovered.add(neighbor[1])
                parents[neighbor[1]] = (neighbor[0], current_state[1])
    return None

def parent_search(parents, current_state):
    list = []
    while parents[current_state[1]]:
        list = [parents[current_state[1]][0]] + list
        current_state = parents[current_state[1]]
    return list

def BidirectionalSearch(state):
    goal = [str(x) for x in range(1, len(state))] + ["*"]
    goal = tuple([None, tuple(goal)])
    state = tuple([None, tuple(state)])
    frontier = [state]
    backtier = [goal]
    front_discovered = set(state)
    back_discovered = set(goal)
    front_parents = {state[1]: None}
    back_parents = {goal[1]: None}
    while frontier or backtier:
        current_state = frontier.pop(0)
        front_discovered.add(current_state[1])
        if current_state[1] in back_discovered:
            return parent_search(front_parents, current_state) + parent_search(back_parents, current_state)[::-1]
        for neighbor in ComputeNeighbors(current_state[1]):
            if neighbor[1] not in front_discovered:
                frontier.append(neighbor)
                front_discovered.add(neighbor[1])
                front_parents[neighbor[1]] = (neighbor[0], current_state[1])

        current_state = backtier.pop(0)
        back_discovered.add(current_state[1])
        if current_state[1] in front_discovered:
            return parent_search(front_parents, current_state) + parent_search(back_parents, current_state)[::-1]
        for neighbor in ComputeNeighbors(current_state[1]):
            if neighbor[1] not in back_discovered:
                backtier.append(neighbor)
                back_discovered.add(neighbor[1])
                back_parents[neighbor[1]] = (neighbor[0], current_state[1])
    return None
def main():
    state = loadfromfile("gamestate.txt")
    print(BidirectionalSearch(state))
main()
