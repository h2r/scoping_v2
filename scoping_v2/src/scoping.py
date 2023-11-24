from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PreconditionLifted:
    """Precondition, with free parameters that need to be filled. Filling the free parameters gives a grounded effect."""

    pass


@dataclass
class EffectLifted:
    """Effect, with free parameters that need to be filled. Filling the free parameters gives a grounded effect."""

    pass


@dataclass
class GroundingsSet:
    """A set of groundings. Each grounding is a mapping from free parameter to concrete object."""

    pass


@dataclass
class ObjectType:
    """Type of an object. Eg ball, brick. Will be used in EffectLifted, etc."""

    name: str


@dataclass
class OperatorLifted:
    """Can represent merged or atomic operator"""

    precondition: PreconditionLifted
    effect: EffectLifted
    atomic_operators: Optional[List[OperatorLifted]]
    """None iff this operator is atomic. List of atomic operators otherwise. Or maybe list of component operators."""


@dataclass
class OperatorWithGroundings:
    """A single lifted operator, and a set of groundings."""

    operator_lifted: OperatorLifted
    groundings_set: GroundingsSet

    def get_affected_pvars(self) -> PVarWithGroundings:
        raise NotImplementedError()


@dataclass
class OperatorWithGroundingsSet:
    """Collection of operators with groundings.


    The simplest implementation is just a List[OperatorWithGroundings]
    We have a class for this, rather than just using a list, because we may be able to compress/amortize
    some data/compute this way.
    """

    pass

    def get_affected_pvars(self) -> PVarGroundedSet:
        raise NotImplementedError()

    def get_non_guaranteed_pvars(
        self, initial_state_guaranteed: PartialState
    ) -> PVarGroundedSet:
        """Maybe hard."""
        # TODO: Possibly the input should be something else with more structure, that lets us be more efficient.
        raise NotImplementedError()


@dataclass
class PartialState:
    """Value assignments to some, but not all, variables.

    We may end up needing a 'lifted' version, that lets us express this more compactly for large domains.
    """

    assignments: List[ConcreteVariableValueAssignment]

    def delete_pvars(self, pvars_to_delete: PVarGroundedSet) -> PartialState:
        raise NotImplementedError()


@dataclass
class ConcreteVariableValueAssignment:
    """Used for goal."""

    pass


@dataclass
class PVarWithGroundings:
    """We maybe never need this instead of PVarGroundedSet."""

    pass

    @classmethod
    def from_concrete_variable_value_assignment(
        cls, cvva: ConcreteVariableValueAssignment
    ) -> PVarWithGroundings:
        raise NotImplementedError()


@dataclass
class PVarGroundedSet:
    """Set of grounded PVars. Probably using some smarted encoding than enumeration."""

    pass

    @classmethod
    def new_empty(cls) -> PVarGroundedSet:
        raise NotImplementedError()

    @classmethod
    def from_concrete_variable_value_assignment(
        cls, cvva: ConcreteVariableValueAssignment
    ) -> PVarGroundedSet:
        raise NotImplementedError()

    @classmethod
    def union(cls, grounded_sets: List[PVarGroundedSet]) -> PVarGroundedSet:
        raise NotImplementedError()


def scope(
    operators_lifted: OperatorWithGroundingsSet,
    initial_state: PartialState,
    goal: ConcreteVariableValueAssignment,
) -> OperatorWithGroundingsSet:
    """Get a compressed operator set sufficient for optimal planning."""
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
        initial_state_guaranteed = initial_state.delete_pvars(
            affected_pvars_per_operator
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
