# Target Search Path
VPATH := .

# Phony target (targets in this list can always be re-run, regardless of state)
.PHONY: all python build-python package-python cpp compile-cpp build-cpp clean


# Default target

all:
	@echo Select a target:
	@echo \ \ \ \ make python \(build-python, package-python\)
	@echo \ \ \ \ make cpp \ \ \ \(compile-cpp, build-cpp\)
	@echo \ \ \ \ make clean \ \(removes compiled C++/Python\)


# Python targets

python: clean build-python package-python

build-python:
	python setup.py build

package-python:
	python setup.py sdist


# C++ targets

cpp: compile-cpp build-cpp

compile-cpp:
	./3to2
	cd deepest; shedskin deepest.py

build-cpp:
	cd deepest; make


# Cleanup

clean:
	rm -rf build
	rm -rf dist
	rm -f deepest/Makefile
	rm -f deepest/deepest{,.exe}
	find . -iname "*.pyc" -print -exec rm -f \{\} \;
	find . -iname "*pp" -print -exec rm -f \{\} \;
