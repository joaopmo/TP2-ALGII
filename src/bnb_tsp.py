import time
import heapq
import numpy as np


# Classe para representar os nodes da árvore binária do branch and bound.
class Node:
    def __init__(self, bound, level, cost, path):
        self.bound = bound
        self.level = level
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.bound < other.bound


# Encontra os dois vizinhos mais próximos de um dado node.
def two_nearest(mtx, node):
    first = float('inf')
    second = float('inf')

    for i in range(np.shape(mtx)[0]):
        if i != node:
            if first > mtx[node][i]:
                second = first
                first = mtx[node][i]
            elif second > mtx[node][i]:
                second = mtx[node][i]

    return first, second


# Encontra um limite inferior para o comprimento do caminho a partir de um dado node.
def bound(mtx, path):
    lb = 0

    # Se o existem arestas que devem fazer parte do caminho:
    if path:
        # Adicione o peso da aresta entre o primeiro e segundo nodes do caminho
        # mais o peso da aresta entre o primeiro node e seu vizinho mais próximo
        # que seja diferente do segundo node.
        i, j = path[0], path[1]
        d1, d2 = two_nearest(mtx, i)
        d2 = d2 if d1 == mtx[i][j] else mtx[i][j]
        lb += (d1 + d2)

        # Adicione o peso da aresta entre o último e penúltimo nodes do caminho
        # mais o peso da aresta entre o último node e seu vizinho mais próximo
        # que seja diferente do penúltimo node.
        i, j = path[-1], path[-2]
        d1, d2 = two_nearest(mtx, i)
        d2 = d2 if d1 == mtx[i][j] else mtx[i][j]
        lb += (d1 + d2)

    # Para todos os nodes da lista diferentes do primeiro e último adicione o
    # peso das arestas entre o node e seu antecessor e sucessor.
    for i, j, k in zip(path, path[1:], path[2:]):
        d1 = mtx[i][j]
        d2 = mtx[j][k]
        lb += (d1 + d2)

    # Para todos os nodes sem nenhuma aresta obrigatoria incidente a eles adicione
    # o peso das arestas entre node e seus dois vizinhos mais próximos.
    nonpath = set(range(np.shape(mtx)[0])) - set(path)
    for i in list(nonpath):
        d1, d2 = two_nearest(mtx, i)
        lb += (d1 + d2)

    lb = np.ceil(lb / 2)

    return lb


# Retorna False se o node 2 aparece antes do node 1 em um dado caminho.
def one_first(path):
    idx1 = path.index(1) if (1 in path) else None
    idx2 = path.index(2) if (2 in path) else None
    if idx2 is None:
        return True
    elif idx1 is None:
        return False
    elif idx2 < idx1:
        return False
    else:
        return True


# TSP com branch and bound.
# Implementação basicamente igual à vista em aula, mas com adição de uma
# verificação de precedência do node 1 sobre o node 2 como descrito na
# Seção 12.2 (Levitin).
def bnb_tsp(mtx, best_lst=None, max=600):
    root = Node(bound(mtx, []), 0, 0, [0])
    queue = []
    heapq.heappush(queue, root)
    n = np.shape(mtx)[0] - 1
    best = float('inf')
    sol = None

    start = time.time()

    while queue:
        # Se o tempo exceder max retorne
        if start + max < time.time():
            best_lst.append(float('inf'))
            return float('inf'), None

        node = heapq.heappop(queue)

        if node.level > n:
            if best > node.cost:
                best = node.cost
                sol = node.path
        elif node.bound < best and one_first(node.path):
            if node.level < n:
                for k in range(n + 1):
                    if (k not in node.path
                            and mtx[node.path[-1]][k] != float('inf')
                            and bound(mtx, node.path + [k]) < best):
                        heapq.heappush(queue, Node(bound(mtx, node.path + [k]),
                                                   node.level + 1,
                                                   node.cost + mtx[node.path[-1]][k],
                                                   node.path + [k]))
            elif (mtx[node.path[-1]][0] != float('inf')
                  and bound(mtx, node.path + [0]) < best
                  and len(node.path) == n + 1):
                heapq.heappush(queue, Node(bound(mtx, node.path + [0]),
                                           node.level + 1,
                                           node.cost + mtx[node.path[-1]][0],
                                           node.path + [0]))

    if best_lst is not None:
        best_lst.append(best)

    return best, sol
