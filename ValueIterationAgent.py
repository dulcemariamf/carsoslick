import MDPReader as mdpr
class ValueIterationAgent:

    def __init__(self, mdp, iterations):
        self.mdp = mdp
        self.discount = 0.9
        self.iterations = iterations

        self.values = {}

        for i in range(0, self.iterations):
            newVals = {}
            mdpReader = mdpr.MDPReader()
            for s in mdpReader.getStates(self.mdp):
                bestActV = -999999
                actions = mdpReader.getLegalActions(self.mdp, s)
                if actions is None:
                    newVals[s] = 0
                for a in actions:
                    actSum = self#--CONTINUE HERE

    def computeQValueFromValues(self, state, action):
        Qval = 0
        return Qval

    def dothing(self):
        for i in range(self.iterations):
            print("hello")
