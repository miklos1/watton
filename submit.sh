#!/bin/bash

nnodes="$1"
nprocs=$((24 * ${nnodes}))
id=$(printf "%04d" ${nnodes})

sed -e "s/@@id@@/${id}/g" -e "s/@@nnodes@@/${nnodes}/g" -e "s/@@nprocs@@/${nprocs}/g" submit.pbs.in > submit.pbs
qsub submit.pbs
rm -f submit.pbs
