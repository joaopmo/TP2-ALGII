import numpy as np
import networkx as nx


# TSP com algoritmo twice-around-the-tree
def tat_tsp(mtx, best_lst=None):
    n = np.shape(mtx)[0]

    graph = nx.from_numpy_matrix(mtx)
    mst = nx.minimum_spanning_tree(graph)
    sol = list(nx.dfs_preorder_nodes(mst, source=0))

    # Encontra o peso total na solução produzida
    best = 0.0
    sol.append(0)
    for i, j in zip(sol, sol[1:]):
        try:
            best += graph[i][j]['weight']
        except ValueError:
            print(f'Size: {n}')
            print(f'Node: ({i}, {j})')
            print(ValueError)

    if best_lst is not None:
        best_lst.append(best)

    return best, sol
