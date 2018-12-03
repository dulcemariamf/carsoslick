import MDPReader as mdpr
class policyIterationAgent:


def __init__(self, mdp):
    self.mdp = mdp
    self.discount = 0.9
    #dictionary that contains all actions for each state
    self.stateAction = {}
    self.policyIterations = 30
    self.values = {}
    self.stateAction = {}
    mdpReader = mdpr.MDPReader()
    
    #creating our arbitary policy based on the states, always going right and giving value 0
    #saving in both dictionaries
    for s in mdpReader.getStates(self.mdp):
        self.values[s] = 0
        self.stateAction[s] = "right"

     
    #begin step one of policy iteration
    #the times that we have to iterate through the policy. Technically should be until there is no change in the MDP Values in our dictionary 
    for i in range(policyIterations):
        #pass in the value and action dictionary
        newValues = {}
        #oldPolicy
        
        for s in mdpReader.getStates(self.mdp):
            
            #computes the q values for each state passed into the action dictionary
            actSum = self.policyEvaluation( s, self.stateAction[s])
            newValues[s] = actSum
        
        #set the dictionary values to the values they receive after one iteration through all of the states given the policy 
        self.values = newValues 
    
    #begin step two of policy iteration, which is policy improvement 
    #Update the current policy by selecting actions for each state that lead to better values than the ones we get through the current policy
    #again, we want to do this until the dictionary policy is unchanged for every state 
    #big thing: Values do not change. Only the actions at each state 
    for s in mdpReader.getStates(self.mdp):
        
        #grab the value we have from the current state 
        currentAction = stateAction[s]
        nextState = mdpReader.getAction(self.mdp, s, currentAction)
        nextStateValue = self.values[nextState] 
        
        #create list of actions to iterate through but take out the action we have already computed 
        legalActions = mdpReader.getLegalActions(self.mdp,s)
        legalActions.remove(currentAction)
        bestAction = self.stateAction[s] 
        
        #update the policy for the given state by finding the best of all actions from that state here 
        for a in actions:
            actSum = self.policyEvaluation(s, a) 
                if nextStateValue < actSum:
                    bestAction = a 
        
        #update the dictionaries 
        self.stateAction[s] = bestAction
    
    #return the policy 
    return self.stateAction 
    
    def policyEvaluation(self, state, action):
        Qval = 0
        #getTransitionStatesAndProbs will give us the next state the the agent will land in
        for nextState, probability in mdpReader.getPolicyTransitionStatesAndProb(self, mdp, state, action):
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
