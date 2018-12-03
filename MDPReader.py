#Purpose: This program will be responsible for reading in the MDP and returning information back to our agent for use within our AI algorithms
class MDPReader:
    
    #e is empty , b is bad car, p is player, oil is o 
    
    #tells us where the bad cars are located on the board. Will work for when there is one bad car, or more.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getListOfCarCoordinates(self, MDP):
        carCoordinateArray = []
        for x in range(len(MDP)):
            for y in range(len(MDP[x])):
                if MDP[x][y] == 'b' :
                    carCoordinateArray.append((y,x)) 
        return carCoordinateArray     
            
    #this tells us where the oil spills are within the MDP. Will work for one oil spill, or more.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getListOfOilCoordinates (self, MDP):
        oilCoordinateArray = [] 
        for x in range(len(MDP)):
            for y in range(len(MDP[x])):
                if MDP[x][y] == 'o':
                    oilCoordinateArray.append((y,x)) 
        return oilCoordinateArray 

    #this tells us where our agent currently is within the MDP.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getAgentCoordinates(self, MDP):
        playerCoordinates = (0,0) 
        for x in range(len(MDP)):
            for y in range(len(MDP[x])):
                if MDP[x][y] == 'p':
                    playerCoordinates = (y,x) 
        return playerCoordinates 
    
    #this tells us all of the moves our agents can make from a given state  
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getLegalActions (self, MDP, state ): 
        
        #get length of the row and columns
        MDPColumns= len(MDP[0])
        #print ("Here is the amount of columns per row")
        #print (MDPColumns)
        MDPRows = len(MDP) 
        #break up the coordinates 
        column = state[0] 
        row = state[1] 
        #create a list to hold all of the agent's moves
        legalActions = []
        
        
        #check if we are on the win state because if we are we can only have one actions, called "Win"  
        if( MDP[state[1]][state[0]] == 'w') :
            legalActions.append("Win")
            return legalActions 
        
        #check if we are on the lose state because we can only have one action from here, called "Lose" 
        if (MDP[state[1]][state[0]] == 'b') :
            legalActions.append("Lose")
            return legalActions 
        
        #want to know, can we move up or down, which is y, or left and right, which is denoted by x
        #first check to see if y+1 and/or y-1 are available moves 
        if (row+1 < MDPRows and MDPRows > 1) :
            #legalActions.append((column, row+1))
            legalActions.append("down") 
        if (row-1 >= 0 and MDPRows > 1):
            #legalActions.append((column, row-1)) 
            legalActions.append("up") 
        #then, check to see if j+1 or j-1 are available moves 
        if (column+1 < MDPColumns and MDPColumns > 1) :
            #legalActions.append((column+1, row))
            legalActions.append("right") 
        if (column-1 >= 0 and MDPColumns > 1) :
            #legalActions.append((column-1, row)) 
            legalActions.append("left") 
        return legalActions 
     
    #Print out the coordinates of every state in the MDP 
    def getStates(self,MDP):
        states = [] 
        for x in range(len(MDP)):
            for y in range(len(MDP[x])):
               states.append((y,x)) 
        return states 

    #gets the transition state from the current action and the probability for that action being successful and returns them together 
    #in a list of tuples composed of (coordinates,probability) pairs.
    #when oil comes into play,or we want to give our agent a probability of failing an action, we want to expand this. 
    def getTransitionStatesAndProbs(self,mdp,state,action): 
        transitionStatesAndProbs = []
        transitionProbability = 1.0 
        #currentPlayerPosition = self.getAgentCoordinates(MDP) 
        currentPlayerPosition = state
        newPlayerPosition = None
        #now take the given action 
        if action == "left" :
            newPlayerPosition = (currentPlayerPosition[0]-1,currentPlayerPosition[1]) 
        if action == "right":
            newPlayerPosition = (currentPlayerPosition[0]+1,currentPlayerPosition[1]) 
        if action == "up":
            newPlayerPosition = (currentPlayerPosition[0],currentPlayerPosition[1]-1) 
        if action == "down":
            newPlayerPosition = (state[0],state[1]+1)
        if action == "Win" or action == "Lose":
            newPlayerPosition = state
        
        resultState = (newPlayerPosition[1],newPlayerPosition[0]) 
        #print ("Here is where we are: " )
        #print (state)
        #print ("Given action: " )
        #print (action) 
        #print ("Here is where we moved: " )
        #print (resultState)
        
        resultStateProbPair = (resultState, transitionProbability) 
        transitionStatesAndProbs.append(resultStateProbPair) 
        
        #print (transitionStatesAndProbs)
        return transitionStatesAndProbs
     
    def getPolicyTransitionStatesAndProb(self, mdp, state, policyAction):
        
        transitionStatesAndProbs = []
        transitionProbability = 1.0 
        
        currentPlayerPosition = state
        newPlayerPosition = None
        legalActions = self.getLegalActions(mdp, state)

        legalAction = False 
        
        #now take the given action 
        if policyAction == "left" and "left" in legalActions : 
            newPlayerPosition = (currentPlayerPosition[0]-1,currentPlayerPosition[1])
            legalAction = True
        if policyAction == "right" and "right" in legalActions:      
            newPlayerPosition = (currentPlayerPosition[0]+1,currentPlayerPosition[1])
            legalAction = True
        if policyAction == "up" and (row-1 >= 0 and MDPRows > 1):
            newPlayerPosition = (currentPlayerPosition[0],currentPlayerPosition[1]-1)
            legalAction = True
        if policyAction == "down" and (row+1 < MDPRows and MDPRows > 1):
            newPlayerPosition = (state[0],state[1]+1)
            legalAction = True 
        
        #no legal action or we are on a winning/losing state 
        if policyAction == "Win" or policyAction == "Lose" or legalAction == False:
            newPlayerPosition = state
            
        
        resultState = (newPlayerPosition[1],newPlayerPosition[0]) 
        
        resultStateProbPair = (resultState, transitionProbability) 
        transitionStatesAndProbs.append(resultStateProbPair) 
        
        #print (transitionStatesAndProbs)
        return transitionStatesAndProbs
        
    
    #in the pacman model, there is an additional state from an exit that confers a reward for moving. 
    #rather than make that, what we can do is detect if we are 
    def getReward(self,MDP,state,action,nextState):
        if action == "Win":
            return 10 
        
        if action == "Lose":
            return -10 
            
        return 0
    
    
    #assummes a valid aciton is passed in 
    #returns a state 
    def takeAction(self, MDP, state, action):
        
        currentPlayerPosition = state
        newPlayerPosition = None
        legalActions = self.getLegalActions(MDP, state)
        legalAction = False 
        
        #now take the given action 
        if action == "left" and "left" in legalActions : 
            newPlayerPosition = (currentPlayerPosition[0]-1,currentPlayerPosition[1])
            legalAction = True
        if action == "right" and "right" in legalActions:      
            newPlayerPosition = (currentPlayerPosition[0]+1,currentPlayerPosition[1])
            legalAction = True
        if action == "up" and (row-1 >= 0 and MDPRows > 1):
            newPlayerPosition = (currentPlayerPosition[0],currentPlayerPosition[1]-1)
            legalAction = True
        if action == "down" and (row+1 < MDPRows and MDPRows > 1):
            newPlayerPosition = (state[0],state[1]+1)
            legalAction = True 
        
        #no legal action or we are on a winning/losing state 
        if action == "Win" or action == "Lose" or legalAction == False:
            newPlayerPosition = state
            
        
        resultState = (newPlayerPosition[1],newPlayerPosition[0]) 
        
        return resultState 
      
    #pass in two sets of coordinates, and get the manhattan distance between them.
    def manhattanDistance (self, xy1, xy2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )
        
    
    

#some things used for testing. Commented out right now, but if you want to test something, you can uncomment and do it here :)         
columns = 3
numLanes = 3
MDP = [['c' for x in range(columns)] for y in range (numLanes)] 
MDP[0][2] = 'p' 
a = MDPReader()  


newArray = []


newArray = a.getLegalActions(MDP,(0,2)) 
print ("Here is the current state" ) 
print ((2,0)) #think of it as the opposite of whatever we have in mdp[][] 
newArray = a.getLegalActions(MDP, (0,2)) 
print ("Legal Actions from current state") 
print(newArray) 
newArray = a.getTransitionStatesAndProbs(MDP,(0,2),"right") 
print (newArray )
newArray = a.getPolicyTransitionStatesAndProb(MDP,(0,2),"right") 
print (newArray )
action = a.takeAction(MDP, (0,2),"left") 
print (action)