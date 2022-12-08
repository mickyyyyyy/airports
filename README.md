# Airports #

## Problem statement ## 
An airline wants to know the minimum number of routes needed to be added in order to allow passengers to fly from a given starting airport to any other airport which they own. The airline provides a list of airports which they operate at, and a list of routes between airports which can be taken. Passengers do not care how many layover flights they have to take, they only care about being able to reach any of these given airports. This problem was found in a YouTube video from Clément Mihailescu, an ex-Google and ex-Facebook Software Engineer.

## Example Inputs ##
The airline gives us three inputs, a list of airports, a list of routes between these airports, and the nominated starting airport. An example of such inputs is given as below:

`airports = ["BGI", "CDG", "DEL", "DOH", "DSM", "EWR", "EYW", "HND", "ICN",
            "JFK", "LGA", "LHR", "ORD", "SAN", "SFO", "SIN", "TLV", "BUD"]`  
`routes = [["DSM", "ORD"],
          ["ORD", "BGI"],
          ["BGI", "LGA"],
          ["SIN", "CDG"],
          ["CDG", "SIN"],
          ["CDG", "BUD"],
          ["DEL", "DOH"],
          ["DEL", "CDG"],
          ["TLV", "DEL"],
          ["EWR", "HND"],
          ["HND", "ICN"],
          ["HND", "JFK"],
          ["ICN", "JFK"],
          ["JFK", "LGA"],
          ["EYW", "LHR"],
          ["LHR", "SFO"],
          ["SFO", "SAN"],
          ["SFO", "DSM"],
          ["SAN", "EYW"]]`  
`startingAirport = 'LGA'`  

## Instructions for Code Usage ##

### Defining an Airport ###
First, we need to define our airports, from the given input. This code has utilised Object-Oriented Programming (OOP), so each airport in this list should be use as the airport's code in the object Airport (defined with the lattitude and longitude of the airport. An example for defining an airport is given below:

`AKL = Airport('AKL', -36.848461, 174.763336)`

### Defining a Route ###
Routes are defined in a similar fashion, where we have an object called Route, which we can give a list of airport objects. An example for defining a route is given below:

`r = Route([BNE, AKL])`

Where:

`BNE = Airport('BNE', -27.469770, 153.025131)`

and `AKL` is defined as before. If the longitude and lattitude are accurate, the distance of a route (as the crow flies), can be returned using:

`r.get_distance()`

Where `r` is the defined route.

A plane object has also been created, to allow the user to determine the route time. The plane object can be defined with a speed (km/h). An example for defining a plane is given below:

`p = Plane(800)`

From here, the user can find the route time by typing the following:

`r.get_time(p)`

Where `r` is the defined route, and `p` is the plane being used.

### Defining the Graph ###
Once these lists of airport objects and route objects have been defined given the input airport and route lists, we can define a graph, where the nodes are the airports, and the edges are the routes. An example for defining a graph is given below:

`g = Graph(airports, routes)`

Where `airports` is a list of airport objects defined from the list of airports given from the airline, and `routes` is a list of route objects defined from the list of routes given from the airline.

### Removing the loops ###

The next step is to remove any loops from the graph, and aggregate all nodes contained in such a loop. The code needed to aggregate these nodes is as follows:

`g.reduce()`

Where `g` is the defined graph.

### Finding the Necessary Routes to Add ###

In order to find the necessary routes needed to be added to the given list of routes in order for someone to fly from a starting airport to any other airport in the given airport list, we use the following code:

`g.find_routes(LGA)`

Where `g` is the defined graph and `LGA` is an airport object defined from the list of airports. From the example inputs given above, we get three routes, which equate to:

`['LGA', 'EWR']`  
`['LGA', 'SFO']`  
`['LGA', 'TLV']`  
