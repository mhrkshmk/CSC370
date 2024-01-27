# Methods for checking whether an execution schedule is serialisable.

from Schedule import *


# Takes as input a Schedule of IOOperations and returns the lexicographically
# smallest serial SimpleSchedule that is conflict-equivalent to it. If the provided
# schedule is not conflict-serialisable, then this methods returns None (i.e., the python
# built-in type that represents a null value) 
def to_serial( schedule):


    # Solving using the topological sort
    # Implement me!
    g = dict(list()) # The graph that represents the graph.

    # To create an empty list mapped to each transaction_id.
    for op in schedule.operations:
        g[op.transaction_id] = []

    # We create a directed edge between transaction_id u and transaction_id v,
    # iff they have different transaction ids and the same database_element
    #  and atleast one of the operations is WRITE.
    for i, u in enumerate(schedule.operations):
        for j in range(i + 1, len(schedule.operations)):
            v = schedule.operations[j]
            if u.transaction_id != v.transaction_id and u.database_element == v.database_element and (u.operation == "WRITE" or v.operation == "WRITE"):
                g[u.transaction_id].append(v.transaction_id)

    # Topological Sort:
    in_deg = dict() # A dictionary that keeps track how many edges come in to each vertex.

    # To initiate a 0 value for each in_deg.
    for u in g:
        in_deg[u] = 0
    # Calculatiing the value of in_deg for g.
    for u in g:
        for v in g[u]:
            if v in in_deg:
                in_deg[v] += 1

    unreachable = [] # The vertices that don't have any edges arriving at them.

    # We add the vertices with in_deg value of 0 to the list.
    for u in g:
        if in_deg[u] == 0:
            unreachable.append(u)

    unreachable = sorted(unreachable) # We sort it so that the final answer will be lexicographically smallest.

    topol = [] # The list for the finalized topol sort.and

    # In this while loop, we add the smallest unreachable vertex
    # to the topol list, and then we delete the edges connected to it,
    # therefor we take 1 from each vertices' in_deg that were connected to it.
    while unreachable:
        u = unreachable.pop(0)
        topol.append(u)
        for v in g[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                unreachable.append(v)

    # If the number of vertices in topol and g don't match, means that topol doesn't have all the vertices,
    # so it has a cycle, therefor a conflict-free schedule doesn't exist.
    if len(topol) != len(g):
        return None # We return None if it's non-serialisable.

    # If the topol sort is found, we return a SimpleSchedule created from the topol list.
    else:
        topol_schedule = SimpleSchedule(topol)
        return topol_schedule