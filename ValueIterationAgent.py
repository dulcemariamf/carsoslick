class ValueIterationAgent:

    def __init__(self, mdp, iterations):
        self.mdp = mdp
        self.discount = 0.9
        self.iterations = iterations

        

    def dothing(self):
        for i in range(self.iterations):
            print("hello")
