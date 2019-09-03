import pandas as pd

class Person:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0
        self.draws = []
        
    def display(self):
        print("Name: " + self.name)
        print("Score: " + str(self.score))
        print("Strategy: " + str(self.strategy))
        print()
        
    def isValid(self):
        return sum(self.strategy) == 100
    
def createPopulation():
    pop = []
    df = pd.read_excel (r'C:\Users\Ross\Documents\3rd_Year\Softwire\Wirelords.xlsx')
    for i in df.index:
        player = df.loc[i]
        strategy = [player['Castle1'],player['Castle2'],player['Castle3'],player['Castle4'],
                    player['Castle5'],player['Castle6'],player['Castle7'],player['Castle8'],
                    player['Castle9'],player['Castle10'],]
        pop.append(Person(player['Name'], strategy))
    return pop

def doesAWinWar(A,B):
    a = 0
    b = 0
    for i in range(10):
        if A[i] > B[i]:
            a += (i+1)
        elif B[i] > A[i]:
            b += (i+1)
        elif B[i] != A[i]:
            return "Invalid Comparison"
    if a > b:
        return 1
    elif b > a:
        return 0
    else:
        return 0.5
            
def tournament():
    pop = createPopulation()
    for i in range(len(pop)):
        for j in range(len(pop)):
            if i > j:
                battleOutcome = doesAWinWar(pop[i].strategy, pop[j].strategy)
                pop[i].score += battleOutcome
                pop[j].score += (1 - battleOutcome)
                if battleOutcome == 0.5:
                    pop[i].draws.append(pop[j].name)
                    pop[j].draws.append(pop[i].name)
    
    pop.sort(key=lambda x: x.score)
    
    for i in pop:
        i.display()

tournament()     