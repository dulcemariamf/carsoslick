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
            #calculate the state value for each iteration
            for s in mdpReader.getStates(self.mdp):
                #print(self.mdp[s[1]][s[0]])
                charAtState = self.mdp[s[1]][s[0]]
                bestActV = -999999
                actions = mdpReader.getLegalActions(self.mdp, s)
                if actions is None:
                    newVals[s] = 0
                for a in actions:
                    actSum = self.computeQValueFromValues(s, a)
                    if bestActV < actSum:
                        bestActV = actSum
                newVals[s] = bestActV
            self.values = newVals

    def computeQValueFromValues(self, state, action):
        Qval = 0
        #getTransitionStatesAndProbs will give us the next state the the agent will land in
        for nextState, probability in mdpReader.getTransitionStatesAndProbs(self, mdp, state, action):
            #get the reward that will result from moving to the next state
            resultingReward = mdpReader.getReward(state, action, nextState)
            nextQValues = self.values[nextState]
            #the qvalue function
            Qval += probability * (resultingReward + (self.discount * nextQValues))
        return Qval

    def dothing(self):
        for i in range(self.iterations):
            print("hello")
