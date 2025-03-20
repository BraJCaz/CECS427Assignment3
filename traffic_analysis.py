# Brandon Cazares
# CECS 427 Sec 2
# Professor Ponce
# Due Date: 3/24/2025
# Assignment 3: Traffic Analysis
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import numpy as np
from scipy.optimize import minimize
import sys
# We read our graph first
def read_graph(file_path):
    """ This reads a directed graph from a GML file."""
    Graph = nx.read_gml(file_path)
    return Graph

# We will load our graph after that
def load_graph(file_path):
    """ We load a directed path from a GML file"""
    Graph = nx.read_gml(file_path)
    return Graph

# Next, we generate a sample gml file
def generate_sample_gml(filename="di_graph.gml"):
    """Generate a sample directed graph and save it as a GML file."""
    Graph = nx.DiGraph()  # Create a directed graph
    # These are our sample nodes of both a and b based on our di_graph.gml file
    # first sample edge
    Graph.add_edge(0, 1, a=2.0, b=1.0)
    # second sample edge
    Graph.add_edge(1, 2, a=3.0, b=2.0)
    # third sample edge
    Graph.add_edge(2, 0, a=1.5, b=0.5)

    # now, we write our gml graph file
    nx.write_gml(Graph, filename)
    print(f"Sample GML file '{filename}' generated.")

# Then we run this function manually before running the script
generate_sample_gml("digraph_file.gml")

# This is our travel time
def travel_time(Graph, flow):
    """ This computes total travel time for each edge given a flow distribution."""
    # we compute our travel time
    time = {}
    # we calculate our edges
    for edge in Graph.edges():
        # for edge a
        a = Graph[edge[0]][edge[1]]['a']
        # for edge b
        b = Graph[edge[0]][edge[1]]['b']
        # We flow on this edge
        x = flow.get(edge, 0)
        # we record our time
        time[edge] = a * x + b
    # we return our time
    return time
# We compute our travel cost next
def compute_travel_cost(flow, a, b):
    """This computes travel cost based on a polynomial function (a * x + b)"""
    return a * flow + b

# Now, we need our nash equilibrium
def nash_equilibrium(Graph, source, target, vehicles):
    """This computes Nash equilibrium where each vehicle selfishly minimizes travel time"""
    edges = list(Graph.edges(data=True))
    # our initial guess
    initial_guess = np.full(len(edges), vehicles / len(edges))

    # our objective function
    def objective(flow):
        return sum(compute_travel_cost(flow[i], edges[i][2].get('a', 1), edges[i][2].get('b', 1)) for i in range(len(edges)))

    # our constraints
    constraints = ({'type': 'eq', 'fun': lambda flow: sum(flow) - vehicles})
    # our bounds
    bounds = [(0, vehicles) for _ in range(len(edges))]

    # our result
    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

    # we return our result
    return {edges[i][:2]: result.x[i] for i in range(len(edges))}

# Next, we have our social optimum
def social_optimum(Graph, source, target, vehicles):
    """This computes our social optimal traffic distribution to minimize total system cost."""
    edges = list(Graph.edges(data=True))
    # our initial guess
    initial_guess = np.full(len(edges), vehicles / len(edges))

    # our objective function
    def objective(flow):
        return sum(flow[i] + compute_travel_cost(flow[i], edges[i][2].get('a', 1), edges[i][2].get('b', 1)) for i in range(len(edges)))

    # our constraints
    constraints = ({'type': 'eq', 'fun': lambda flow: sum(flow) - vehicles})
    # our bounds
    bounds = [(0, vehicles) for _ in edges]

    # our result
    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

    # we return our result
    return {edges[i][:2]: result.x[i] for i in range(len(edges))}

# Now, we're going to plot our graph and name it Traffic Network
def plot_graph(Graph, flows, title="Traffic Network"):
    """This plots the directed graph with edge weights"""
    # our position
    position = nx.spring_layout(Graph)

    plt.figure(figsize=(8, 10))
    # we plot our graph
    nx.draw(Graph, position, with_labels=True, node_color='lightblue', edge_color='black')
    # we label our edges
    edge_labels = {edge: f"{flows.get(edge, 0):.2f}" for edge in Graph.edges}
    # this draws our edge labels
    nx.draw_networkx_edge_labels(Graph, position, edge_labels=edge_labels)
    # our graph title
    plt.title(title)
    # we show our graph
    plt.show()

# Now, we write our main function
def main():
    parser = argparse.ArgumentParser(description="Traffic Equilibrium Analysis")
    # our input GML file
    parser.add_argument("file", type=str, help="Path to the GML file")
    # our vehicles
    parser.add_argument("vehicles", type=int, help="Number of vehicles")
    # our starting node
    parser.add_argument("start", type=int, help="Our starting node")
    # our ending node
    parser.add_argument("end", type=int, help="Our ending node")
    # our plot graph
    parser.add_argument("--plot", action="store_true", help="We plot our graph")

    # This checks for missing arguments
    if len(sys.argv) < 5:
        parser.print_help()
        sys.exit(1)

    # we test these arguments to see if they work
    try:
        args = parser.parse_args()

        # Our output command
        print(f"File: {args.file}, Vehicles: {args.vehicles}, Start: {args.start}, End: {args.end}, Plot: {args.plot}")

    # This lets us know if there are errors running our output arguments
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_help()
        sys.exit(1)

    # This loads the graph
    Graph = load_graph(args.file)

    # our equilibrium flow
    equilibrium_flow = nash_equilibrium(Graph, args.start, args.end, args.vehicles)
    # our social flow
    social_flow = social_optimum(Graph, args.start, args.end, args.vehicles)

    # Nash Equilibrium
    print("Nash Equilibrium Flows:")
    for edge, flow in equilibrium_flow.items():
        print(f"{edge}: {flow:.2f}")

    # Social Optimal
    print("Social Optimal Flows:")
    for edge, flow in social_flow.items():
        print(f"{edge}: {flow:.2f}")

    # Now we plot both graphs all together
    if args.plot:
        # This generates both graphs
        print("Both graphs are generated...")
        # Our Nash Equilibrium is plotted
        plot_graph(Graph, equilibrium_flow, "Nash Equilibrium")
        # Our Social Optimality is plotted
        plot_graph(Graph, social_flow, "Social Optimality")

if __name__ == "__main__":
    main()
