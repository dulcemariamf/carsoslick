#Purpose: This program will be responsible for reading in the MDP and returning information back to our agent for use within our AI algorithms
class MDPReader:
    
    
    def getListOfCarCoordinates(self, MDP):
        carCoordinateArray = []
        for i in range(len(MDP)):
            for j in range(len(MDP[i])):
                if MDP[i][j] == 'c' :
                    carCoordinateArray.append((i,j)) 
        return carCoordinateArray     
            
    
    def getListOfOilCoordinates (self, MDP):
        oilCoordinateArray = [] 
        for i in range(len(MDP)):
            for j in range(len(MDP[i])):
                if MDP[i][j] == 'o':
                    oilCoordinateArray.append((i,j)) 
        return oilCoordinateArray 

            
         
 
columns = 7
numLanes = 2 
MDP = [['c' for x in range(columns)] for y in range (numLanes)] 
MDP[0][1] = 'o' 
a = MDPReader()  


newArray = [] 
newArray = a.getListOfOilCoordinates(MDP) 
print (newArray)