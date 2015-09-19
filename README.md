#### Experimentation framework for the manuscript:

> Miklós Homolya, and David A. Ham. "A parallel edge orientation algorithm for quadrilateral meshes." arXiv preprint arXiv:1505.03357 (2015).

#### Usage

Type `make` to generate the meshes for the experiments. Gmsh is required for this step.

`submit.pbs.in` contains a submission template for PBS. To submit an experiment, type

    ./submit.sh n

where `n` denotes the number of computing nodes. The number of cores will be 24 * `n`.

On ARCHER, the above will generate files `measure_`_nnnn_`.o`_kkkkkk_ and `measure_`_nnnn_`.e`_kkkkkk_, containing the standard output and standard error of the job. Our results are uploaded into the results folder. Running `python evaluate.py` will look for these files, process them, show some diagnostic output, and generate the CSV files which are directly used for plots and tables in the paper.
