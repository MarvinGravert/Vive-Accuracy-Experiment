import numpy as np
from scipy.spatial.transform import Rotation
import analysis.newCalc as calc
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint, Bounds
from geneticalgorithm import geneticalgorithm as ga
"""
So basically i want to find the
  Okay genius idea:
  rausfinden der transformation zwischen Vive tracker und Laser target. Wir suchen T: VT->LT das bedeutet wir kennen den TRansformationsvektor bereits also brauchen wir nur noch R wissen.
  Für R können wir davon ausgehen dass nur nur eine Rotation relevant ist. Wir splitten die große Matrix einfach auf in drei kleine. Hoffentlich so dass die Drehung um die Z-Achse zuletzt kommt.
  Aber selbst wenn, könnten wir mti constraints auf der Rotationsmatrix ein optimal problem lösen.
Die interesseante Frage ist nun was ist unsere objective funktion. Wir haben den Ground truth vom Laser. Sprich Laser KOS[0] zu LaserKos[1] yielded ne Transformation.
Diese 4x4 matrix ist unser2 Ziel, das es zu erreichen gilt. Von der Vive haben wir Tv->vt @ Tvt->lt. Dies einmal zu [0] und einmal zu [1] damit kriegen wir das richtige auch raus. Bzw was richtig sein soll.
Problem die eine MAtrix VT->LT ist falsch. Wir können nun für alle [0]->[n] groundthruth matrizen finden und das jeweilige Gegenstück in Abhängigkeit von der zu findenen Matrix.
Was wir wollen ist dass der average Fehler (mean squared error)der matrixeinträge gering wird->Im Prinzip sollten beiden ja gleich sein (es wird aber auch natürlich noch ein fehler existieren)

=> aufbauen der obejective function, obj(f)->class die zuerst die ganzen Matrizen in den Speicher lädt(ini methode) dann jedesmal für eine neue Matrix gecalled werden kann. Input ist immer eine Matrix R. t haben wir schon gegeben, wir können also die matrizen bestimmen und die elementwise abwichung(funktion dafür bestimmen). Für die INput matrix gilt:

t= bekannt durch geometrie

R=9 Werte
orthogonale matrix => beträge sind 1 und die vektoren müssen untereinander rechtwinklig sein=> nicht =0 sondern Werte nahe null wählen dot.proudct<small value. Selbiges für die Beträge betrag-1<small value

"""


class FindOptimal():

    def __init__(self):

        temp = calc.getDataPairs()
        # get list of the ground truth rotations laserref->laser emasurment n
        self.laser_ref2meas_list_hom_matrix = temp.getListHomMatrixLaser_LaserRef()
        # we need list of all viveref->vivemeasure
        self.vive_ref2meas_list_hom_matrix = temp.getListHomMatrixVive_ViveRef()
        # so essentially we now need just need to the matrix to find

    def objective_function(self, R):
        # R is the target matrix
        # R describes the transformation from vive to laser
        # make hommatrix(R)
        # lets loop through the ground truth and vive matrix
        sum_norms = 0
        for laser, vive in zip(self.laser_ref2meas_list_hom_matrix, self.vive_ref2meas_list_hom_matrix):
            # create teh matrix that compares
            compar = R@vive@calc.invertHomMatrix(R)
            diff_matrix = compar-laser
            sum_norms += np.linalg.norm(diff_matrix, ord="fro")
        return sum_norms / len(self.laser_ref2meas_list_hom_matrix)

    def pre_objective_function(self, quaternion_list):
        # turn list into matrix
        temp = Rotation.from_quat(quaternion_list)
        R = temp.as_matrix()
        t = np.array([62, 62, -10])
        hom = calc.makeHomogenousMatrix(R, t)
        return self.objective_function(hom)

    def pre_objective_function_fullmatrix(self, full_list):
        temp = Rotation.from_quat(full_list[:4])
        R = temp.as_matrix()
        t = np.array([86.6, 85.6, -50])+full_list[4:]
        hom = calc.makeHomogenousMatrix(R, t)
        return self.objective_function(hom)

    def useScipy(self, x0=[0.7071068, 0.7071068, 0, 0], t=np.array([62, 62, -10])):
        # we will run a quaternion optimizer
        # basically through in 4 quanterion =>rotation matrix
        # so x0=x, x1=y, x2=z, x3=w
        # initial condition
        # x,y,z,w[[0, 1, 0], [1, 0, 0], [0, 0, -1]
        # x0 = [0.7071068, 0.7071068, 0, 0]
        # Bounds
        bounds = ([-1, 1], [-1, 1], [-1, 1], [-1, 1])
        res = minimize(fun=self.pre_objective_function, x0=x0,
                       bounds=bounds)
        return res

    def use_genetic_algo(self):
        varbound = np.array([[-1, 1]]*4)
        model = ga(
            function=self.pre_objective_function,
            dimension=4,
            variable_type='real',
            variable_boundaries=varbound)
        model.run()

    def useScipy_fullmatrix(self, x0=[0.7071068, 0.7071068, 0, 0, 5, 5, 5]):
        bounds = ([-1, 1], [-1, 1], [-1, 1],
                  [-1, 1], [-5, 5], [-5, 5], [-5, 5])
        res = minimize(fun=self.pre_objective_function_fullmatrix, x0=x0,
                       bounds=bounds)
        return res

    def use_genetic_algo_fullmatrix(self):
        varbound = np.array([[-1, 1], [-1, 1], [-1, 1],
                             [-1, 1], [-2, 2], [-2, 2], [-20, 0]])
        model = ga(
            function=self.pre_objective_function_fullmatrix,
            dimension=7,
            variable_type='real',
            variable_boundaries=varbound)
        model.run()


def print4Settings(R):
    s = ""
    for row in R:
        for elem in row:
            s += str(elem) + " "
        s += ";"
    print(s[:-1])


if __name__ == "__main__":
    test = FindOptimal()
    # mat = np.array([[1, 0, 0], [0, 0, -1], [0, -1, 0]])
    # res = test.useScipy(Rotation.from_matrix(mat).as_quat())
    # res = test.useScipy_fullmatrix()
    # tempR = Rotation.from_quat(res.x)
    # print(res)
    # print4Settings(np.linalg.inv(tempR.as_matrix()))
    # test.use_genetic_algo()
    # test.useScipy()
    test.use_genetic_algo_fullmatrix()
