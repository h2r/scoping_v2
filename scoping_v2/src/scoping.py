"""Core scoping algorithm. Defined using abstract groundings classes, so that we can plug in 
whichever concrete grounding implementation we want."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TypeVar, Type
from abc import ABC, abstractmethod, abstractclassmethod
from scoping_v2.src.atomic_classes import *
from scoping_v2.src.abstract_groundings import *


def scope(
    operators_lifted: OperatorWithGroundingsSet,
    initial_state: PartialState,
    goal: ConcreteVariableValueAssignment,
) -> OperatorWithGroundingsSet:
    """Get a compressed operator set sufficient for optimal planning.
    
    Args:
        operators_lifted: Characterizes the set of lifted operators and all possible groundings.
            The groundings will ideally be specified in a compact way.
        initial_state: Partial initial state.
        goal: Assumed to be a single variable-value assignment, WLOG.
    """
    # Initialize relevant vars. TODO: What is the format?
    # I don't think it's just (lifted pvars, groundingsset) - we may need a union of these

    relevant_pvars_old = PVarGroundedSet.new_empty()
    relevant_pvars = PVarGroundedSet.from_concrete_variable_value_assignment(goal)

    while relevant_pvars_old != relevant_pvars:
        # Get merged operators
        merged_operators = merge_operators(
            operators_lifted, initial_state, relevant_pvars
        )

        # Get affected variables
        affected_pvars_per_operator = merged_operators.get_affected_pvars()

        # Get partial initial state over non-affected pvars
        initial_state_guaranteed = affected_pvars_per_operator.mask_from_partial_state(
            initial_state
        )

        # Update relevant pvars based on non-guaranteed preconditions
        relevant_pvars_old = relevant_pvars
        relevant_pvars = relevant_pvars.union(
            [merged_operators.get_non_guaranteed_pvars(initial_state_guaranteed)]
        )

    return merged_operators  # type: ignore This is never unbound.


def merge_operators(
    operators_lifted: OperatorWithGroundingsSet,
    initial_state: PartialState,
    relevant_pvars: PVarGroundedSet,
) -> OperatorWithGroundingsSet:
    """Merge operators after partitioning them by their effects on relevant_pvars.

    Expected hard parts:

    1. Merging lifted preconditions. We probably can't use z3, since it doesn't have native quantifier (forall, exists) support afaik.
        In the past, we just grounded 'forall' using And, and 'exists' using Or, over all groundings.

    2. Dealing with differently named parameters/symmetries in parameters.
        I _think_ handling this poorly would reduce scoping aggressiveness, but not make it unsound.
    """
    raise NotImplementedError()
