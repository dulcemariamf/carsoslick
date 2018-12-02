import MDPReader as mdpr
class ValueIterationAgent:

    def __init__(self, mdp, iterations):
        self.mdp = mdp
        self.discount = 0.9
        self.iterations = iterations

        self.values = {}
        print("hello")
        mdpReader = mdpr.MDPReader()
        for s in mdpReader.getStates(self.mdp):
            self.values[s] = 0
        for i in range(0, self.iterations):
            newVals = {}
            #calculate the state value for each iteration
            for s in mdpReader.getStates(self.mdp):
                #print(self.mdp[s[1]][s[0]])
                charAtState = self.mdp[s[1]][s[0]]
                bestActV = -999999
                actions = mdpReader.getLegalActions(self.mdp, s)
                if actions is None:
                    newVals[s] = 0
                for a in actions:
                    #print(str(s) + " " + str(a))
                    actSum = self.computeQValueFromValues(s, a)
                    #print(actSum)
                    if bestActV < actSum:
                        bestActV = actSum
                newVals[s] = bestActV
            self.values = newVals
        print("hello again")

    def computeQValueFromValues(self, state, action):
        Qval = 0
        mdpReader = mdpr.MDPReader()
        #getTransitionStatesAndProbs will give us the next state the the agent will land in
        for nextState, probability in mdpReader.getTransitionStatesAndProbs(self.mdp, state, action):
            #get the reward that will result from moving to the next state
            resultingReward = mdpReader.getReward(self.mdp, state, action, nextState)
            nextQValues = self.values[(nextState[1], nextState[0])]
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

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def dothing(self):
        for i in range(self.iterations):
            print("hello")
