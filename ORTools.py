"""Vehicles Routing Problem (VRP) with Time Windows."""
import math

import pandas
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time

def create_data_model(df, clusters, depot):
    """Stores the data for the problem."""
    if (clusters == 1 and  depot.iloc[0]['cluster'] != df.iloc[0]['cluster']):
        df = pandas.concat([depot, df])
    data = {}
    data['time_matrix'] = []
    for r in range(0, df.shape[0]):
        data['time_matrix'].append([])
        for c in range(0, df.shape[0]):
            data['time_matrix'][r].append(int(distBetween(df.iloc[r]['XCord'], df.iloc[r]['YCord'], df.iloc[c]['XCord'], df.iloc[c]['YCord']) *
                                              (df.iloc[r]['Demand'] + df.iloc[c]['Demand'])/20))

    data['time_windows'] = []
    for i in range(0, df.shape[0]):
        data['time_windows'].append((int(df.iloc[i]['ReadyTime']/60), int(df.iloc[i]['DueDate']) * 60))
    data['num_vehicles'] = clusters
    data['depot'] = 0
    data['customerNum'] = []
    for i in range(0, df.shape[0]):
        data['customerNum'].append(df.iloc[i].Customer)
    return data

def distBetween(x0, y0, x1, y1):
    return math.sqrt(math.pow(x1-x0, 2) + math.pow((y1-y0), 2))

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    route = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
            route.append((data['customerNum'][manager.IndexToNode(index)], solution.Min(time_var)))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        route.append((data['customerNum'][manager.IndexToNode(index)], solution.Min(time_var)))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        # print(plan_output)
        total_time += solution.Min(time_var)
    # print('Total time of all routes: {}min'.format(total_time))
    return route, total_time


def main(df, clusters, depot):
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model(df, clusters, depot)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        3000,  # allow waiting time
        3000,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution)



if __name__ == '__main__':
    main()