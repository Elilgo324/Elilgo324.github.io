import itertools

import pulp


def held_karp(graph):
    """
    Calculates the TSP tour of the points on the graph using the Held-Karp algorithm.

    Args:
    - graph: NetworkX graph representing the distances between points.

    Returns:
    - List: TSP tour of the points.
    """
    n = len(graph)
    num_sets = 2 ** n

    # Initialize the memoization table
    memo = {}
    for k in range(1, n):
        memo[(1 << k, k)] = (graph[0][k], 0)

    # Iterate over all subset sizes
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                min_dist = float('inf')
                min_prev = None
                for m in subset:
                    if m == k:
                        continue
                    dist, _ = memo[(prev, m)]
                    if dist + graph[m][k] < min_dist:
                        min_dist = dist + graph[m][k]
                        min_prev = m
                memo[(bits, k)] = (min_dist, min_prev)

    # Find the minimum tour length
    bits = (2 ** n - 1) - 1
    min_dist = float('inf')
    last = None
    for k in range(1, n):
        dist, prev = memo[(bits, k)]
        if dist + graph[k][0] < min_dist:
            min_dist = dist + graph[k][0]
            last = k

    # Reconstruct the tour
    tour = [0]
    bits = (2 ** n - 1) - 1
    while last is not None:
        tour.append(last)
        prev = memo[(bits, last)][1]
        bits &= ~(1 << last)
        last = prev

    return tour

def tsp_ilp(points):
    num_points = len(points)

    # Create a binary variable for each possible edge
    edges = [(i, j) for i in range(num_points) for j in range(num_points) if i != j]
    x = pulp.LpVariable.dicts("x", edges, cat='Binary')

    # Create the ILP problem
    tsp_ilp_problem = pulp.LpProblem("TSP_ILP", pulp.LpMinimize)

    # Objective function: minimize total distance
    tsp_ilp_problem += pulp.lpSum(x[i, j] * distance(points[i], points[j]) for i, j in edges)

    # Constraints: every point is visited exactly once
    for i in range(num_points):
        tsp_ilp_problem += pulp.lpSum(x[i, j] for j in range(num_points) if i != j) == 1
        tsp_ilp_problem += pulp.lpSum(x[j, i] for j in range(num_points) if i != j) == 1

    # Solve the ILP problem
    tsp_ilp_problem.solve()

    # Extract the solution
    solution = [(i, j) for i, j in edges if pulp.value(x[i, j]) == 1]

    return solution


def distance(point1, point2):
    # Function to calculate Euclidean distance between two points
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


# Example usage:
points = [(0, 0), (1, 3), (2, 2), (4, 4)]
solution = tsp_ilp(points)
print("TSP solution:", solution)

import networkx as nx


def tsp_christofides(points):
    # Create a complete graph with points as nodes
    G = nx.Graph()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2) ** 0.5
            G.add_edge(i, j, weight=distance)

    # Find the approximate TSP tour using the Christofides algorithm
    tsp_tour = nx.approximation.traveling_salesman.christofides(G)

    # Calculate the total tour length
    tour_length = sum(G[tsp_tour[i]][tsp_tour[i + 1]]['weight'] for i in range(len(tsp_tour) - 1))
    tour_length += G[tsp_tour[-1]][tsp_tour[0]]['weight']  # Add the last edge

    return tsp_tour, tour_length


# Example usage:
points = [(0, 0), (1, 3), (2, 2), (4, 4)]
tsp_tour, tour_length = tsp_christofides(points)
print("TSP tour:", tsp_tour)
print("Total tour length:", tour_length)


