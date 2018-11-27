#Purpose: This program will be responsible for reading in the MDP and returning information back to our agent for use within our AI algorithms
class MDPReader:
    
    #e is empty , b is bad car, p is player, oil is o 
    
    #tells us where the bad cars are located on the board. Will work for when there is one bad car, or more.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getListOfCarCoordinates(self, MDP):
        carCoordinateArray = []
        for i in range(len(MDP)):
            for j in range(len(MDP[i])):
                if MDP[i][j] == 'b' :
                    carCoordinateArray.append((i,j)) 
        return carCoordinateArray     
            
    #this tells us where the oil spills are within the MDP. Will work for one oil spill, or more.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getListOfOilCoordinates (self, MDP):
        oilCoordinateArray = [] 
        for i in range(len(MDP)):
            for j in range(len(MDP[i])):
                if MDP[i][j] == 'o':
                    oilCoordinateArray.append((i,j)) 
        return oilCoordinateArray 

    #this tells us where our agent currently is within the MDP.
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getAgentCoordinates(self, MDP):
        playerCoordinates = (0,0) 
        for i in range(len(MDP)):
            for j in range(len(MDP[i])):
                if MDP[i][j] == 'p':
                    playerCoordinates = (i,j) 
        return playerCoordinates 
    
    #this tells us all of the moves our agents can make. 
    #The returned list is list of tuples, where each tuple is an (x,y) coordinate. 
    def getLegalActions (self, MDP): 
        currentPlayerPosition = self.getAgentCoordinates(MDP)
        #get length of the row and columns
        MDPRows = len(MDP) 
        MDPColumns = len(MDP[0])
        #break up the coordinates 
        row = currentPlayerPosition[0] 
        column = currentPlayerPosition[1] 
        #create a list to hold all of the agent's moves
        legalActions = [] 
        
        #want to know, can we move up or down, which is i, or left and right, which is denoted by j 
        #first check to see if i+1 and/or i-1 are available moves 
        if (row+1 < MDPRows and MDPRows > 1) :
            legalActions.append((row+1, column)) 
        if (row-1 >= 0 and MDPRows > 1):
            legalActions.append((row-1, column)) 
        
        #then, check to see if j+1 or j-1 are available moves 
        if (column+1 < MDPColumns and MDPColumns > 1) :
            legalActions.append((row, column+1)) 
        if (column-1 >= 0 and MDPColumns > 1) :
            legalActions.append((row, column-1)) 
        
        return legalActions 
        
    #pass in two sets of coordinates, and get the manhattan distance between them 
    def manhattanDistance (self, xy1, xy2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

#some things used for testing. Commented out right now, but if you want to test something, you can uncomment and do it here :)         
#columns = 7
#numLanes = 2 
#MDP = [['c' for x in range(columns)] for y in range (numLanes)] 
#MDP[0][0] = 'p' 
#a = MDPReader()  


#newArray = [] 
#newArray = a.getLegalActions(MDP) 
#print (newArray)