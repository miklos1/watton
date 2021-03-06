[![DOI](https://zenodo.org/badge/18466/miklos1/watton.svg)](https://zenodo.org/badge/latestdoi/18466/miklos1/watton)

#### Experimentation framework for the manuscript:

> Miklós Homolya, and David A. Ham. "A parallel edge orientation algorithm for quadrilateral meshes." arXiv preprint arXiv:1505.03357 (2015).

#### Usage

    make

will generate the meshes for the experiments. Gmsh is required for this step.

`submit.pbs.in` contains a submission template for PBS. To submit an experiment, type

    ./submit.sh n

where `n` denotes the number of computing nodes. The number of cores will be 24 * `n`. The submission will run `measure.py` which facilitates the measurement. It also relies on Firedrake having patched with `firedrake.patch`, which adds some instrumentation code.

On ARCHER, the above will generate files `measure_`_nnnn_`.o`_kkkkkk_ and `measure_`_nnnn_`.e`_kkkkkk_, containing the standard output and standard error of the job. Our results are uploaded into the results folder. Running

    python evaluate.py

will look for these files, process them, show some diagnostic output, and generate the CSV files which are directly used for plots and tables in the paper.

#### Licence

`sphere.geo`, `t10.geo`, and `t11.geo` are based on their equivalents in the Gmsh source distribution. You find a copy of the licence of Gmsh in `LICENSE.Gmsh`. Anything else is covered by the MIT licence, see `LICENSE` for details.
