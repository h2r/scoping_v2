# Scoping V2

This is an attempt at lifted scoping. For now it's just the skeleton code and types. Bits we expect to be hard are marked.

## Overview
`abstract_groundings.py` defines some abstract base classes for specifying collections of grounded pvars and operators, potentially compactly. These classes have abstract methods/classmethods for carrying out a portion of scoping. These abstract methods need to be overridden by implementation in concrete child classes.

`scoping.py` has the scoping algorithm, written in terms of the abstract classes.

The idea is that we will find smarter ways to implement the abstract classes, but `scoping.py` will remain unchanged.

`enumerated_operators_like_og_scoping.py` implements the groundings in a way similar to current scoping. (WIP)

`enumerated_operator_level_groundings.py` implements the groundings similar to current scoping, factors it as (lifted operator, set of groundings), where the set of groundings can use a compact format that lets us avoid enumerating all combinations of object groundings.

