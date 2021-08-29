import time
from memory_profiler import memory_usage

from src.bnb_tsp import bnb_tsp
from src.tat_tsp import tat_tsp
from src.chr_tsp import chr_tsp
from src.get_instance import get_instance


# Executa uma função e retorna o tempo e mémoria utilizados por ela
# assim como seu resultado
def time_space(algorithm, mtx, INITIAL_MEM):
    best_lst = []
    start = time.time()
    mem = memory_usage((algorithm, (mtx, best_lst)))
    end = time.time()

    return end - start, max(mem) - INITIAL_MEM, best_lst.pop()


# Imprime as métricas e resultado dos algorítmos em um arquivo
def print_metrics(file, lst):
    tab = '\t\t'
    exp = "{:<20}".format('size')
    sec = "{:<20}".format('time(sec)')
    mb = "{:<20}".format('space(MiB)')
    sol = "{:<20}".format('solution')

    for idx, val in enumerate(lst):
        if idx == 0:
            file.write('twice-around-the-tree' + '\n\n')
        elif idx == 1:
            file.write('christofides' + '\n\n')
        else:
            file.write('branch-and-bound' + '\n\n')

        tmp = '\n'.join([tab.join([f'{j:<20}' for j in i]) for i in val])
        file.write(exp + tab + sec + tab + mb + tab + sol + '\n')
        file.write(tmp)
        file.write('\n' + '-' * 120 + '\n\n')


def metrics():
    INITIAL_MEM = max(memory_usage(-1, interval=.2, timeout=1))

    bnb_limit = False

    tat_m = []
    chr_m = []
    bnb_m = []

    tat_e = []
    chr_e = []
    bnb_e = []

    for i in list(range(8, 33)) + [2 ** x for x in range(6, 11)]:
        if bnb_limit and i < 32:
            continue

        _, m, e = get_instance(5, i)

        # Métricas para twice-around-the-tree com distância manhattan
        tat_m.append((i, *time_space(tat_tsp, m, INITIAL_MEM)))

        # Métricas para twice-around-the-tree com distância euclidiana
        tat_e.append((i, *time_space(tat_tsp, e, INITIAL_MEM)))

        # Métricas para christofedes com distância manhattan
        chr_m.append((i, *time_space(chr_tsp, m, INITIAL_MEM)))

        # Métricas para christofedes com distância euclidiana
        chr_e.append((i, *time_space(chr_tsp, e, INITIAL_MEM)))

        while not bnb_limit:
            # Métricas para branch-and-bound com distância manhattan
            max_time, max_space, sol = time_space(bnb_tsp, m, INITIAL_MEM)
            if sol != float('inf'):
                bnb_m.append((i, max_time, max_space, sol))
            else:
                bnb_limit = True

            # Métricas para branch-and-bound com distância euclidiana
            max_time, max_space, sol = time_space(bnb_tsp, e, INITIAL_MEM)
            if sol != float('inf'):
                bnb_e.append((i, max_time, max_space, sol))
            else:
                bnb_limit = True

            break

        f = open("metrics.txt", "w")
        print_metrics(f, [tat_m, chr_m, bnb_m])
        print_metrics(f, [tat_e, chr_e, bnb_e])
        f.close()


if __name__ == '__main__':
    metrics()
