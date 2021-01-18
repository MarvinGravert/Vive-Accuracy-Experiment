'''
Calculate the errors between the ground truth (laser) and the vive 
The error being considered is the vector error, that means we look at the error
between of the vector between registration point and measurement point n 
calculated once in ground truth system once in vive system
Additionally the distance is printed as well as an average over all points
'''
import numpy as np
import analysis.newCalc as calc


def print_average(diff_vector_list, dist_list):
    diff_avg = np.mean(diff_vector_list, 0)
    dist_avg = np.mean(dist_list)
    print("Averages:")
    print(
        f"""
    Durchschnittsdifferenzvektor:
    {diff_avg[0]}
    {diff_avg[1]}
    {diff_avg[2]}
    Durchschnittsbetrag:
    {np.linalg.norm(diff_avg)}

    Durschnittslängenunterschied:
    {dist_avg}
    """)


def print_error(diff_vector_list, dist_list):
    for n, (diff, dist) in enumerate(zip(diff_vector_list, dist_list)):
        print(f"{n}. Vektor")
        print(f"""
        Differenzvektor:
        {diff[0]}
        {diff[1]}
        {diff[2]}
        Betrag Differenzvektor:
        {np.linalg.norm(diff)}

        Unterschied der Beträge der Ursprungsvektoren:
        {dist}
        ----------------------------------------------
        """)


if __name__ == "__main__":
    temp = calc.getDataPairs()
    # The data is calculated into the laser system
    groundThruth = temp.getListHomMatrixLaser_LaserRef()
    compari = temp.getListHomMatrixVive_LaserRef()

    diff_matrix_list = list()
    for true_val, compare_val in zip(groundThruth, compari):
        diff_matrix_list.append(true_val-compare_val)
    diff_vector_list = [x[:3, 3] for x in diff_matrix_list]
    dist_list = [abs(np.linalg.norm(truth)-np.linalg.norm(vive))
                 for truth, vive in zip(groundThruth, compari)]

    print_error(diff_vector_list, dist_list)
    print_average(diff_vector_list, dist_list)
