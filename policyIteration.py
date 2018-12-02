import MDPReader as mdpr
class policyIterationAgent:


def __init__(self, mdp):
    self.mdp = mdp
    self.discount = 0.9
    #dictionary that contains all actions for each state
    self.stateAction = {}

    #creating our arbitary policy based on the states, always going right
    #saving in dictionary
    for s in mdpr.getStates(self.mdp):
        self.stateAction[s] = (0, "right")



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
     def computeActionFromValues(self, state):
            bestActV = -999999
            bestAct = None
            mdpReader = mdpr.MDPReader()
            actions = mdpReader.getLegalActions(self.mdp, state)
            if actions is None:
                return None
            for a in actions:
                sPrimeSum = self.getQValue(state, a)
                if bestActV < sPrimeSum:
                    bestAct = a
                    bestActV = sPrimeSum
            return bestAct
