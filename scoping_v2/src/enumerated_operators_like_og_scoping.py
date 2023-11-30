from __future__ import annotations
from typing import List, TypeVar
from dataclasses import dataclass


from scoping_v2.src.abstract_groundings import OperatorWithGroundingsSet, PVarGroundedSet
from scoping_v2.src.atomic_classes import PVarWithGroundings, OperatorLifted, GroundingsSet, PartialState


class Grounding:
    """TODO"""
    pass

@dataclass
class OperatorGrounded:
    lifted_operator: OperatorLifted
    grounding: Grounding


class PVarGrounded:
    pass

@dataclass
class ListOfPvarGrounded:
    pvars: List[PVarGrounded]


@dataclass
class ListOfOperatorGroundeds:
    operators_grounded: List[OperatorGrounded]

    def get_affected_pvars(self) -> ListOfPvarGrounded:
        # TODO: Clean this up. Use union.
        raise NotImplementedError()
    def get_non_guaranteed_pvars(
        self, initial_state_guaranteed: PartialState
    ) -> PVarGroundedSet:
        raise NotImplementedError()

    def get_merged_operators(
        self, initial_state: PartialState, relevant_pvars: PVarGroundedSet
    ) -> ListOfOperatorGroundeds:
        raise NotImplementedError()