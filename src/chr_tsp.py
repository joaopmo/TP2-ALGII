import numpy as np
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit


# Esta função aparece na documentação do Networkx mas não funcionou na minha versão.
# Por isso simplesmente copiei a implementação da fonte:
# https://networkx.org/documentation/stable/_modules/networkx/algorithms/matching.html#min_weight_matching
def min_weight_matching(G, maxcardinality=False, weight="weight"):
    if len(G.edges) == 0:
        return max_weight_matching(G, maxcardinality, weight)
    G_edges = G.edges(data=weight, default=1)
    min_weight = min([w for _, _, w in G_edges])
    InvG = nx.Graph()
    edges = ((u, v, 1 / (1 + w - min_weight)) for u, v, w in G_edges)
    InvG.add_weighted_edges_from(edges, weight=weight)
    return max_weight_matching(InvG, maxcardinality, weight)


# TSP com algoritmo de Christofides
def chr_tsp(mtx, best_lst=None):
    n = np.shape(mtx)[0]

    # Cria o grafo e a minimum spanning tree associada
    graph = nx.from_numpy_matrix(mtx)
    mst = nx.minimum_spanning_tree(graph)

    # Encontra os vértices com grau ímpar na mst
    odd = []
    for i in range(n):
        if mst.degree[i] % 2 != 0:
            odd.append(i)

    # Encontra o matching mínimo no subgrafo formado pelos vértices de grau ímpar
    match = min_weight_matching(graph.subgraph(odd))

    # Cria um multigrafo com os vértices da mst + arestas do matching mínimo
    multg = nx.MultiGraph()
    multg.add_weighted_edges_from([(i, j, graph[i][j]['weight']) for i, j in match])
    multg.add_weighted_edges_from(mst.edges.data('weight'))

    # Encontra o ciclo euleriano no multigrafo e remove os vértices duplicados
    # para obter um ciclo hamiltoniano
    sol = []
    eul = [u for u, v in eulerian_circuit(multg, source=0)]
    [sol.append(x) for x in eul if x not in sol]

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
