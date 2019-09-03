import pandas as pd

filePathOfStrategies = r'C:\Users\Ross\Documents\3rd_Year\Softwire\Wirelords.xlsx'

troopsPerArmy = 100
numberOfCastles = 10

class Person:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy

        self.score = 0

        self.victories = []
        self.losses = []
        self.draws = []

    def isValid(self):
        return self.correctTotal and self.validTroopAmounts and self.correctLength

    def correctTotal(self):
        return sum(self.strategy) == troopsPerArmy

    def validTroopAmounts(self):
        return all(map(Person.isLegalNumberOfTroops, self.strategy))

    def correctLength(self):
        return len(self.strategy) == numberOfCastles

    def resetScore(self):
        self.score = 0

    @staticmethod
    def isLegalNumberOfTroops(troops):
        return 0 <= troops == int(troops)

    def display(self):
        print("Name: " + self.name)
        print("Score: " + str(self.score))
        print("Strategy: " + str(self.strategy))
        print()

    def verboseDisplay(self):
        self.display()
        print("Victorious over: " + str(self.victories))
        print("Defeated by: " + str(self.losses))
        print("Drew with: " + str(self.draws))
        print()

def createPopulationFromLocation(locationString):
    population = []
    excelData = pd.read_excel(locationString)
    for i in excelData.index:
        player = excelData.loc[i]
        strategy = [player['Castle1'], player['Castle2'], player['Castle3'], player['Castle4'],
                    player['Castle5'], player['Castle6'], player['Castle7'], player['Castle8'],
                    player['Castle9'], player['Castle10'], ]
        population.append(Person(player['Name'], strategy))
    return population

def war(A, B):
    pointsForA = sum(i * doesAWinBattle(A.strategy[i], B.strategy[i]) for i in range(numberOfCastles))

    if pointsForA > findTotalPoints()/2:
        A.score += 1
        A.victories.append(B.name)
        B.losses.append(A.name)
    elif pointsForA < findTotalPoints()/2:
        B.score += 1
        B.victories.append(A.name)
        A.losses.append(B.name)
    else:
        A.score += 0.5
        B.score += 0.5
        A.draws.append(B.name)
        B.draws.append(A.name)

def findTotalPoints():
    return sum(i for i in range(numberOfCastles))

def doesAWinBattle(a, b):
    if a > b:
        return 1
    elif b > a:
        return 0
    else:
        return 0.5

def displayPopulation(population, verbose):
    for person in population:
        if verbose:
            person.verboseDisplay()
        else:
            person.display()

def executeTournament(population):
    for i in range(len(population)):
        for j in range(len(population)):
            if i > j:
                war(population[i], population[j])


def roundRobin(verboseDisplay=False):
    population = createPopulationFromLocation(filePathOfStrategies)
    filter(Person.isValid, population)
    executeTournament(population)
    population.sort(key=lambda x: x.score)
    displayPopulation(population, verboseDisplay)

def removeWorstIteratedTournament():
    population = createPopulationFromLocation(filePathOfStrategies)
    while len(population) > 0:
        executeTournament(population)
        population.sort(key=lambda x: x.score)
        eliminatedPlayer = population.pop(0)
        eliminatedPlayer.display()
        map(Person.resetScore, population)


roundRobin()
removeWorstIteratedTournament()