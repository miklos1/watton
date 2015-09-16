GEOMETRIES := $(wildcard *.geo)

.PHONY: all clean

all: $(GEOMETRIES:.geo=.msh)

clean:
	$(RM) *.msh

%.msh: %.geo
	gmsh -2 $<
