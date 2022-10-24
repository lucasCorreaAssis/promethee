'''Promethee Module, which contains its implementation and auxilary data classes'''

from dataclasses import dataclass
from typing import List
from .exceptions import IncompatibleWeights
from .curves import Curve

@dataclass
class Criteria:
    '''Promethee's criteria'''
    name: str
    weight: float
    goal: str
    curve: Curve

@dataclass
class Phi:
    '''Promethee Phi element'''
    alternative: str
    value: float

    def __str__(self) -> str:
        return f'{self.alternative}: {self.value}'

@dataclass
class PrometheeOutput:
    '''Output from Promethee'''
    negative_phi: List[Phi]
    positive_phi: List[Phi]
    unicriteria_phi: List[Phi]

class Promethee:
    '''Promethee - Multi Criteria Decision Method Implementation'''
    def __init__(self, alternatives: List[str], criterias: List[Criteria]) -> None:
        self.alternatives = alternatives
        self.criterias = criterias

    def update_weights(self, weights: List[float]) -> None:
        '''Update criteria's weight'''
        if len(weights) != len(self.criterias):
            raise IncompatibleWeights()

        for i, criteria in enumerate(self.criterias):
            criteria.weight = weights[i]

    def prioritize(self, values):
        '''Prioritize alternatives based on values'''
        comparison_matrix = self.__compute_comparison_matrix(values)
        aggregate_preference_matrix = self.__compute_aggregate_preference_matrix(comparison_matrix)
        return self.__compute_output(aggregate_preference_matrix)

    def __compute_comparison_matrix(self, values):
        comparison_matrix = []
        for j, criteria in enumerate(self.criterias):
            criteria_comparison_matrix = []
            for i, _ in enumerate(self.alternatives):
                values_comparison = []
                for k, _ in enumerate(self.alternatives):

                    if criteria.goal == 'max':
                        alternative_comparison_value = ((values[j][i]) - (values[j][k]))
                    elif criteria.goal == 'min':
                        alternative_comparison_value = ((values[j][k]) - (values[j][i]))

                    degree = criteria.curve.compute_preference_degree(alternative_comparison_value)

                    alternative_value = float((degree) * criteria.weight)

                    values_comparison.append(alternative_value)
                criteria_comparison_matrix.append(values_comparison)
            comparison_matrix.append(criteria_comparison_matrix)
        return comparison_matrix

    def __compute_aggregate_preference_matrix(self, comparison_criteria_weight_matrix):
        aggregate_preference_matrix = []
        for i, _ in enumerate(self.alternatives):
            final_values = []
            for k, _ in enumerate(self.alternatives):
                value_sum = 0
                for j, _ in enumerate(self.criterias):
                    final_value = comparison_criteria_weight_matrix[j][i][k]
                    value_sum += final_value
                final_value_mean = value_sum 
                final_values.append(final_value_mean)
            aggregate_preference_matrix.append(final_values)
        return aggregate_preference_matrix

    def __compute_output(self, aggregate_preference_matrix) -> PrometheeOutput:
        positive_phi = self.__compute_positive_phi(aggregate_preference_matrix)
        negative_phi = self.__compute_negative_phi(aggregate_preference_matrix)
        unicriteria_phi = self.__compute_unicriteria_phi(positive_phi, negative_phi)

        return PrometheeOutput(negative_phi, positive_phi, unicriteria_phi)

    def __compute_negative_phi(self, aggregate_preference_matrix):
        negative_phi_values = []
        for i, alternative in enumerate(self.alternatives):
            negative_flow_net = 0
            for k, _ in enumerate(self.alternatives):
                negative_flow_net += aggregate_preference_matrix[k][i]
            negative_flow_net *= 1/(len(self.alternatives)-1)
            negative_phi = Phi(alternative, negative_flow_net)
            negative_phi_values.append(negative_phi)
        return negative_phi_values

    def __compute_positive_phi(self, aggregate_preference_matrix):
        positive_phi_values = []
        for i, alternative in enumerate(self.alternatives):
            positive_flow_net = 0
            for k, _ in enumerate(self.alternatives):
                positive_flow_net += aggregate_preference_matrix[i][k]
            positive_flow_net *= 1/(len(self.alternatives)-1)
            positive_phi = Phi(alternative, positive_flow_net)
            positive_phi_values.append(positive_phi)
        return positive_phi_values

    def __compute_unicriteria_phi(self, positive_phi: List[Phi], negative_phi: List[Phi]):
        unicriteria_phi_values = []
        for i, alternative in enumerate(self.alternatives):
            unicriteria_net_flow = (positive_phi[i].value) - (negative_phi[i].value)
            unicriteria_phi = Phi(alternative, unicriteria_net_flow)
            unicriteria_phi_values.append(unicriteria_phi)
        return sorted(unicriteria_phi_values, key=lambda x: x.value, reverse=True)
