import numpy as np

from src.bnb_tsp import bnb_tsp
from src.tat_tsp import tat_tsp
from src.chr_tsp import chr_tsp
from src.get_instance import get_instance_exp


def main():
    exp = int(input("tamanho(2^i) i = "))
    p, m, e = get_instance_exp(5, exp)

    best, sol = tat_tsp(m)
    print(f'twice-around-the-tree: {best}')
    if len(sol) <= 10:
        print(sol, '\n')

    best, sol = chr_tsp(m)
    print(f'christofides: {best}')
    if len(sol) <= 10:
        print(sol, '\n')


    best, sol = bnb_tsp(m)
    print(f'branch-and-bound: {best}')
    if len(sol) <= 10:
        print(sol, '\n')

    print()

    best, sol = tat_tsp(e)
    print(f'twice-around-the-tree: {best}')
    if len(sol) <= 10:
        print(sol, '\n')

    best, sol = chr_tsp(e)
    print(f'christofides: {best}')
    if len(sol) <= 10:
        print(sol, '\n')

    best, sol = bnb_tsp(e)
    print(f'branch-and-bound: {best}')
    if len(sol) <= 10:
        print(sol)

main()
