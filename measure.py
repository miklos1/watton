import math
import numpy as np

from firedrake import *
from pyop2 import MPI
from pyop2.profiling import Timer

parameters["pyop2_options"]["profiling"] = True

timer = Timer("Mesh: cell_closure (quadrilateral)")


def measure(name, thunk):
    timer.reset()

    mesh = thunk()
    mesh.init()

    if timer.ncalls != 1:
        print "Unexpected number of cell_closure calls: %d" % timer.ncalls

    sendbuf = np.array([timer.total, timer.total * timer.total], dtype=float)
    recvbuf = MPI.comm.reduce(sendbuf)
    if MPI.comm.rank == 0:
        M1, M2 = recvbuf
        m = M1 / MPI.comm.size
        s = math.sqrt((M2 - M1*M1 / MPI.comm.size) / (MPI.comm.size - 1))
        print "cell_closure seconds %s: %g +- %g" % (name, m, s)


if __name__ == "__main__":
    measure("s_square", lambda: UnitSquareMesh(512, 512, quadrilateral=True))
    measure("s_sphere", lambda: UnitCubedSphereMesh(9))
    measure("u_square", lambda: Mesh("square.msh"))
    measure("u_sphere", lambda: Mesh("sphere.msh"))
    measure("t10", lambda: Mesh("t10.msh"))
    measure("t11", lambda: Mesh("t11.msh"))
