#!/bin/bash

nnodes=$(printf "%04d" "$1")
nprocs=$((24 * ${nnodes}))

sed -e "s/@@nnodes@@/${nnodes}/g" -e "s/@@nprocs@@/${nprocs}/g" submit.pbs.in > submit.pbs
qsub submit.pbs
rm -f submit.pbs
