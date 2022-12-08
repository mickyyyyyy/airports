import math
import random

RADIUS = 6371 # Radius of the Earth (km)
REFERENCE_ROUTE = 0 # Reference index of the route to use
REFERENCE_AIRPORT = 0 # Reference index of the airport to use
REFERENCE_NODE = 0 # Reference index of the node to use
STOPS_IN_ROUTE = 2 # Number of airports in a route

# Problem statement: The airline wants to know the minimum number of routes
#                    needed to be added in order to allow passengers to fly from
#                    the starting airport to any other airport (can be
#                    indirect).

# Solution:
# 1. Create a directed graph. (DONE)
# 2. Group cycles into aggregate of airports (multiple airports per node). (DONE)
# 3. Find (number of) nodes with no directed edges leading into them (DONE)
#    (route is then from startingAirport to first airport in such a node).

# Example inputs:

## airports = ["BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN",
##             "JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"]
## routes = [["DSM", "ORD"],
##           ["ORD", "BGI"],
##           ["BGI", "LGA"],
##           ["SIN", "CDG"],
##           ["CDG", "SIN"],
##           ["CDG", "BUD"],
##           ["DEL", "DOH"],
##           ["DEL", "CDG"],
##           ["TLV", "DEL"],
##           ["EWR", "HND"],
##           ["HND", "ICN"],
##           ["HND", "JFK"],
##           ["ICN", "JFK"],
##           ["JFK", "LGA"],
##           ["EYW", "LHR"],
##           ["LHR", "SFO"],
##           ["SFO", "SAN"],
##           ["SFO", "DSM"],
##           ["SAN", "EYW"]]
## startingAirport = 'LGA'


class Airport :
    """Represents an airport.
    """
    
    def __init__(self, code, lattitude, longitude) :
        """Constructs an airport object.

        Parameters:
            code (str) -> the airport's code.
            lattitude (int) -> the lattitude of the airport (degrees).
            longitude (int) -> the longitude of the airport (degrees).
        """
        self.code = code
        self.lattitude = lattitude
        self.longitude = longitude

    def get_lattitude(self) :
        """Returns the lattitude of the airport's location.
        """
        return self.lattitude

    def get_longitude(self) :
        """Returns the longitude of the airport's location.
        """
        return self.longitude

    def get_distance(self, airport) :
        """Returns the shortest flight path (in km) from this airport to the
        given airport."""

        # Get the lattitudes and longitudes in radians
        thisLattitude = self.get_lattitude() * math.pi / 180
        thisLongitude = self.get_longitude() * math.pi / 180
        otherLattitude = airport.get_lattitude() * math.pi / 180
        otherLongitude = airport.get_longitude() * math.pi / 180

        # Calculate the Haversine
        a = math.sin((thisLattitude - otherLattitude) / 2) ** 2 + \
            math.cos(thisLattitude) * math.cos(otherLattitude) * \
            math.sin((thisLongitude - otherLongitude) / 2) ** 2

        arcAngle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Return the arc distance
        return RADIUS * arcAngle

    def copy(self) :
        """Creates a shallow copy of the airport.
        """
        return Airport(self.code.copy(), self.lattitude, self.longitude)

    
class Plane :
    """Represents a plane.
    """

    def __init__(self, speed) :
        """Constructs a plane object.

        Parameters:
            speed (int) -> the speed of the plane (km/h).
        """
        self.speed = speed

    def get_speed(self) :
        """Returns the speed of the plane.
        """
        return self.speed


class Route :
    """Represents a route a plane can take.
    """

    def __init__(self, airports) :
        """Constructs a route object.

        Parameters:
            airports (List<Airport>) -> the airports involved in the route.
        """
        self.airports = airports
        self.distance = 0
        lastAirport = None
        for airport in self.airports :
            if lastAirport is not None :
                self.distance += airport.get_distance(lastAirport)

            lastAirport = airport

    def get_airports(self) :
        """Returns the airports involved in the route.
        """
        return self.airports

    def get_distance(self) :
        """Returns the distance of the route.
        """
        return self.distance

    def get_time(self, plane) :
        """Returns the time it will take from take off to landing.

        Parameters:
            plane (Plane) -> the plane to be used.
        """
        return self.distance / plane.get_speed()


class Node :
    """Represents a node in the graph representing the airports.
    """

    def __init__(self, airport) :
        """Constructs a node object.

        Parameters:
            airport (Airport) -> the airport associated with this node.
        """
        self.airports = {airport}
        self.heads = set()
        self.tails = set()

    def get_airports(self) :
        """Returns the airports associated with this node.
        """
        return self.airports.copy()

    def add_airport(self, airport) :
        """Adds an airport to the node.

        Parameters:
            airport (Airport) -> the airport to add.
        """
        if airport not in self.airports :
            self.airports.add(airport)

    def add_airports(self, airports) :
        """Adds multiple airports to the node.

        Parameters:
            airports (Set<Airport>) -> the airports to add.
        """
        for airport in airports :
            self.add_airport(airport)

    def get_heads(self) :
        """Returns the nodes on incoming edges of this node.
        """
        return self.heads.copy()

    def add_head(self, node) :
        """Adds a node as an incoming edge of this node.

        Parameters:
            node (Node) -> the node to add.
        """
        if node not in self.heads :
            self.heads.add(node)

    def remove_head(self, node) :
        """Removes a node as an incoming edge of this node.

        Parameters:
            node (Node) -> the node to remove.
        """
        if node in self.heads :
            self.heads.remove(node)

    def get_tails(self) :
        """Returns the nodes on outgoing edges of this node.
        """
        return self.tails.copy()

    def add_tail(self, node) :
        """Adds a node as an outgoing edge of this node.

        Parameters:
            node (Node) -> the node to add.
        """
        if node not in self.tails :
            self.tails.add(node)

    def remove_tail(self, node) :
        """Removes a node as an outgoing edge of this node.

        Parameters:
            node (Node) -> the node to remove.
        """
        if node in self.tails :
            self.tails.remove(node)

    def copy(self) :
        """Creates a shallow copy of the node.
        """
        return Node([airport.copy for airport in self.airports.copy()])

    
class Graph :
    """Represents a graph of the airports and their available routes.
    """

    def __init__(self, airports, routes) :
        """Constructs a graph object.

        Parameters:
            airports (List<Airport>) -> the airports available.
            routes (List<Route>) -> the routes available.
        """
        self.nodes = set()
        self.head = self.get_node(routes[REFERENCE_ROUTE].get_airports()
                                  [REFERENCE_AIRPORT])

        for route in routes :
            for routePos, airport in enumerate(route.get_airports()) :

                # Get associated node of airport
                node = self.get_node(airport)

                # Deal with inbound flights
                if routePos > 0 :
                    fromNode = self.get_node(route.get_airports()[routePos - 1])
                    fromNode.add_tail(node)
                    node.add_head(fromNode)

                # Deal with outbound flights
                if routePos < len(route.get_airports()) - 1 :
                    toNode = self.get_node(route.get_airports()[routePos + 1])
                    toNode.add_head(node)
                    node.add_tail(toNode)

    def get_node(self, airport) :
        """Returns the existing node associated with the airport or a new node.

        Parameters:
            airport (Airport) -> the airport to search for.
        """
        
        # Check if this airport is already contained in a node
        for node in self.nodes :
            if airport in node.get_airports() :
                return node

        # Create a new node
        node = Node(airport)
        self.add_node(node)
        return node

    def add_node(self, node) :
        """Adds the given node to the set of nodes associated with this graph.

        Parameters:
            node (Node) -> the node to add.
        """
        if node not in self.nodes :
            self.nodes.add(node)

    def reduce(self) :
        """Makes the graph acyclic.
        """

        # Keeps track of which node we are investigating
        index = 0
        while index < len(self.nodes) :
            node = list(self.nodes)[index]
            index += 1

            # Allows for backtracking to identify nodes in loop
            paths = {node : None}

            # Possible loop
            if len(node.get_tails()) and len(node.get_heads()) :

                # Set up data structures to keep track of exploration of nodes
                unexplored = []
                explored = set()

                # Add the nodes from outbound edges of this node to explore
                for tail in node.get_tails() :
                    unexplored.append(tail)
                    paths[tail] = node

                # Perform DFS on node with the goal of the same node
                while unexplored :

                    # Check the next node
                    currNode = unexplored.pop()
                   
                    for tail in currNode.get_tails() :

                        # Update path
                        paths[tail] = currNode
                        explored.add(currNode)

                        # Loop found
                        if tail == node :
                            self.condense_nodes(paths, tail)

                            # Reset index -> ensures condensation doesn't impact
                            # past nodes
                            index = 0

                        # Keep searching
                        elif tail not in explored and tail not in unexplored :
                            unexplored.append(tail)

    def condense_nodes(self, paths, refNode) :
        """Condense nodes into a singular node.

        Parameters:
            paths (Dict<Node:Path>) -> the last path for each node.
            refNode (Node) -> the current node
        """

        # Find the nodes from the last path
        nodes = []

        currNode = paths[refNode]

        # Keep backtracking until we reach a node which shares at least one
        # airport with the reference node
        while len(currNode.airports.difference(refNode.airports)) == \
              len(currNode.airports) :
            if currNode not in nodes :
                nodes.append(currNode)
            currNode = paths[currNode]
        
        for node in nodes :

            # Add airports not already contained in the reference node
            refNode.add_airports(node.get_airports().difference(
                    refNode.get_airports()))

            # Add incoming edges
            for head in node.get_heads() :
                if len(head.airports.difference(refNode.airports)) == \
                   len(head.airports) and head not in nodes and \
                   head not in refNode.get_heads() :
                    refNode.add_head(head)

            # Add outgoing edges
            for tail in node.get_tails() :
                if len(tail.airports.difference(refNode.airports)) == \
                   len(tail.airports) and tail not in nodes and \
                   tail not in refNode.get_tails() :
                    refNode.add_tail(tail)

            # Remove the node -> details added to aggregated node
            self.nodes.remove(node)    

        # Remove links to nodes in loop
        for head in refNode.get_heads().copy() :
            if head in nodes or head == refNode :
                refNode.remove_head(head)

        for tail in refNode.get_tails().copy() :
            if tail in nodes or tail == refNode :
                refNode.remove_tail(tail)

    def find_routes(self, startingAirport) :
        """Determines the routes needed to be added for someone to fly from a
        given airport to every other airport.

        startingAirport (Airport) -> the starting airport.
        """
        routes = []
        for node in self.nodes :
            
            # Only need to consider airports/aggregates of airports with no
            # inbound flights
            if not node.get_heads() :
                route = Route([startingAirport, random.choice(tuple(node.airports))])
                routes.append(route)

        return routes
