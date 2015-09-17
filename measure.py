import math
import numpy as np

from firedrake import *
from pyop2 import MPI
from pyop2.profiling import Timer

parameters["pyop2_options"]["profiling"] = True


def measure(name, thunk):
    if MPI.comm.rank == 0:
        print "name:", name

    mesh = thunk()
    mesh.init()

    timer = Timer("Mesh: cell_closure (quadrilateral)")
    runtime = timer._timings[-1]
    sendbuf = np.array([runtime, runtime * runtime], dtype=float)
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
