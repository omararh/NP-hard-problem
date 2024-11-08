from src.LocalSearch import LocalSearch
from src.ValidatorService import Validator
import math
import random


class SimulatedAnnealing(LocalSearch):

    def __init__(self, G, T0, Tf, alpha, nbMaxIt, nbNeighbors):
        super().__init__(G, nbMaxIt, nbNeighbors)
        self.T = T0
        self.Tf = Tf
        self.alpha = alpha
        self.currentTemperature = T0

    @staticmethod
    def acceptanceProbability(delta_f, T):
        """
        Compute the acceptance probability based on the Metropolis criterion.
        :param delta_f: Change in objective function value
        :param T: Current temperature
        :return: Probability of accepting worse solution
        """
        if delta_f < 0:
            return 1
        return math.exp(-delta_f / T)

    def coolDown(self):
        """
        Update the current temperature using the cooling factor.
        """
        self.currentTemperature *= self.alpha

    def search(self):
        """
        Simulated annealing implementation
        :return:
        """
        self.setInitialSolution()
        cp = 0
        while self.currentTemperature > self.Tf and cp < self.nbMaxIt:
            self.generateNeighborhood()
            chosenNeighbor = random.choice(self.neighbors)

            objectiveSolution = Validator.objectiveFunction(self.currentSolution)
            objectiveNeighborSolution = Validator.objectiveFunction(chosenNeighbor)
            delta_f = objectiveNeighborSolution - objectiveSolution

            if (delta_f < 0 or
                    random.random() < SimulatedAnnealing.acceptanceProbability(delta_f, self.currentTemperature)):
                self.currentSolution = chosenNeighbor

            self.cleanNeighborhood()
            self.coolDown()
            cp += 1
