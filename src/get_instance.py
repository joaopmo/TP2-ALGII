import numpy as np
from scipy.spatial.distance import cdist

# Recebe um coeficiente "coeff" para controlar a distância máxima da origem para os
# pontos gerados na instância e argumento "size" para o tamanho da instância.
# Retona um vetor com pontos do plano e matrizes de adjascencia com a
# distância euclidiana e distância manhattan dos pontos.
def get_instance(coeff, size):
    positions = np.random.randint(coeff * size, size=(size, 2))
    manhattan = cdist(positions, positions, 'cityblock')
    euclidean = cdist(positions, positions, 'euclidean')

    np.fill_diagonal(manhattan, float('inf'))
    np.fill_diagonal(euclidean, float('inf'))

    return positions, manhattan, euclidean


def get_instance_exp(coeff, exp):
    return get_instance(coeff, 2 ** exp)
