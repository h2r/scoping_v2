"""Base classes for scoping objects. We subclass these with concrete implementations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TypeVar, Type
from abc import ABC, abstractmethod, abstractclassmethod
from scoping_v2.src.atomic_classes import *


PVGS = TypeVar("PVGS")


class PVarGroundedSet(ABC):
    """Set of grounded PVars. Probably using some smarted encoding than enumeration."""

    pass

    @classmethod
    def new_empty(cls: Type[PVGS]) -> PVGS:
        raise NotImplementedError()

    @classmethod
    def from_concrete_variable_value_assignment(
        cls: Type[PVGS], cvva: ConcreteVariableValueAssignment
    ) -> PVGS:
        raise NotImplementedError()

    @classmethod
    def union(cls: Type[PVGS], grounded_sets: List[PVGS]) -> PVGS:
        raise NotImplementedError()

    @abstractmethod
    def mask_from_partial_state(self, partial_state: PartialState) -> PartialState:
        """Return a new partial state with these grounded PVars ignores"""
        raise NotImplementedError()


OWGS = TypeVar("OWGS")


class OperatorWithGroundingsSet(ABC):
    """Collection of operators with groundings.


    The simplest implementation is just a List[OperatorWithGroundings]
    We have a class for this, rather than just using a list, because we may be able to compress/amortize
    some data/compute this way.
    """

    @abstractmethod
    def get_affected_pvars(self) -> PVarGroundedSet:
        raise NotImplementedError()

    @abstractmethod
    def get_non_guaranteed_pvars(
        self, initial_state_guaranteed: PartialState
    ) -> PVarGroundedSet:
        """Maybe hard."""
        # TODO: Possibly the input should be something else with more structure, that lets us be more efficient.
        raise NotImplementedError()

    @abstractmethod
    def get_merged_operators(
        self: OWGS, initial_state: PartialState, relevant_pvars: PVarGroundedSet
    ) -> OWGS:
        """This is probably the hardest thing to implement.
        Make sure to keep track of groundings for operator params, and groundings
        for quantifiers separately.

        Also: how do we cope with the initial_state when without grounding everything?
        """
        raise NotImplementedError("Child class should implement this")
