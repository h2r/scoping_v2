# Scoping V2

This is an attempt at lifted scoping. For now it's just the skeleton code and types. Bits we expect to be hard are marked.

## Overview
`abstract_groundings.py` defines some abstract base classes for specifying collections of grounded pvars and operators, potentially compactly. These classes have abstract methods/classmethods for carrying out a portion of scoping. These abstract methods need to be overridden by implementation in concrete child classes.

`scoping.py` has the scoping algorithm, written in terms of the abstract classes.

`enumerated_groundings.py` implements the groundings in a way similar to current scoping. (WIP)

The idea is that we will find smarter ways to implement the abstract classes, but `scoping.py` will remain unchanged.
