import numpy as np
import analysis.newCalc as calc


def print_magntude_diff_vector(vector_list):
    for n, vec in enumerate(vector_list):
        print(f"{n}. Vektor")
        # print(vec)
        print(np.linalg.norm(vec))


if __name__ == "__main__":
    temp = calc.getDataPairs()
    groundThruth = temp.getListHomMatrixLaser_LaserRef()
    compari = temp.getListHomMatrixVive_LaserRef()
    val = 5
    # print(groundThruth[val])
    # print(compari[val])
    # print(groundThruth[val]-compari[val])
    diff_matrix_list = list()
    for true_val, compare_val in zip(groundThruth, compari):
        diff_matrix_list.append(true_val-compare_val)
    diff_vector_list = [x[:3, 3] for x in diff_matrix_list]
    print_magntude_diff_vector(diff_matrix_list)
"""
1. Gib die Fehler in den Achsen aus
2. Optimiere auch den Abstand
3. Plotte die Fehler in den Achsen
4. Mache Sequenzplan für Kalibrierung
5. Refaktoriere den Code
"""
