import MDPReader as mdpr
class policyIterationAgent:


def __init__(self, mdp):
    self.mdp = mdp
    self.discount = 0.9
    #dictionary that contains all actions for each state
    self.stateAction = {}
    self.stateValue = {}
    self.values = {}

    mdpReader = mdpr.MDPReader()
    #creating our arbitary policy based on the states, always going right and giving value 0
    #saving in both dictionaries
    for s in mdpReader.getStates(self.mdp):
        self.stateValue[s] = 0
        self.stateAction[s] = "right"

    #begin step one of policy iteration
    for s in mdpReader.getStates(self.mdp):
        #computes the q values for each state passed into the action dictionary
        actSum = self.computeQValueFromValues( s, self.stateAction[s])
        self.statevalue[s] = actSum


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

     def computeActionFromValue(self, state):
        """
            The policy is the best action according to the values in the given state.

        """
        value = 0
        bestAction = None
        #check if there are no legal actions
        if not mdpreader.getLegalAction(state):
            return None
        #iterate through all the actions
        for action in mdpreader.getLegalAction(state):
            currentValue = self.computeQValueFromValues(state, action)
            if value == 0 or currentValue > value:
                bestAction = actionvalue = currentValue

        return bestAction
