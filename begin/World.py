from Position import Position
from Organisms.Plant import Plant
from Action import Action
from ActionEnum import ActionEnum
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
from Organisms.Grass import Grass

class World(object):

    def __init__(self, worldX, worldY):
        self.__worldX = worldX
        self.__worldY = worldY
        self.__turn = 0
        self.__organisms = []
        self.__newOrganisms = []
        self.__separator = '.'
        self.__plagueActive = False  # określam, czy plaga jest aktywna
        self.__plagueTurnsRemaining = 0  # Liczba tur pozostałych do końca plagi

    @property
    def worldX(self):
        return self.__worldX

    @property
    def worldY(self):
        return self.__worldY

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, value):
        self.__turn = value

    @property
    def organisms(self):
        return self.__organisms

    @organisms.setter
    def organisms(self, value):
        self.__organisms = value

    @property
    def newOrganisms(self):
        return self.__newOrganisms

    @newOrganisms.setter
    def newOrganisms(self, value):
        self.__newOrganisms = value

    @property
    def separator(self):
        return self.__separator

    def makeTurn(self):
        if self.__plagueActive:#zastosowanie efektu plagi podczas tury
            self.applyPlague()

        actions = []

        for org in self.organisms:
            if self.positionOnBoard(org.position):
                actions = org.move()
                for a in actions:
                    self.makeMove(a)
                actions = []
                if self.positionOnBoard(org.position):
                    actions = org.action()
                    for a in actions:
                        self.makeMove(a)
                    actions = []

        self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]
        for o in self.organisms:
            o.liveLength -= 1
            o.power += 1
            if o.liveLength < 1:
                print(str(o.__class__.__name__) + ': umarł ze starości na pozycji: ' + str(o.position))
        self.organisms = [o for o in self.organisms if o.liveLength > 0]

        self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
        self.organisms.extend(self.newOrganisms)
        self.organisms.sort(key=lambda o: o.initiative, reverse=True)
        self.newOrganisms = []

        self.enforceNatureProtectionRules()#zastosowanie zasady ochrony przyrody

        self.turn += 1

    def makeMove(self, action):
        print(action)
        if action.action == ActionEnum.A_ADD:
            self.newOrganisms.append(action.organism)
        elif action.action == ActionEnum.A_INCREASEPOWER:
            action.organism.power += action.value
        elif action.action == ActionEnum.A_MOVE:
            action.organism.position = action.position
        elif action.action == ActionEnum.A_REMOVE:
            action.organism.position = Position(xPosition=-1, yPosition=-1)

    def addOrganism(self, newOrganism):
        newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

        if self.positionOnBoard(newOrgPosition) and self.getOrganismFromPosition(newOrgPosition) is None:
            self.organisms.append(newOrganism)
            self.organisms.sort(key=lambda org: org.initiative, reverse=True)
            return True
        return False

    def positionOnBoard(self, position):
        return position.x >= 0 and position.y >= 0 and position.x < self.worldX and position.y < self.worldY

    def getOrganismFromPosition(self, position):
        for org in self.organisms:
            if org.position == position:
                return org
        for org in self.newOrganisms:
            if org.position == position:
                return org
        return None

    def getNeighboringPositions(self, position):
        result = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                newPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
                if self.positionOnBoard(newPosition) and not (x == 0 and y == 0):
                    result.append(newPosition)
        return result

    def filterFreePositions(self, fields):
        return [field for field in fields if self.getOrganismFromPosition(field) is None]

    def filterPositionsWithoutAnimals(self, fields):
        return [field for field in fields if isinstance(self.getOrganismFromPosition(field), Plant) or self.getOrganismFromPosition(field) is None]

    def __str__(self):
        result = '\ntura: ' + str(self.__turn) + '\n'
        result += '   ' + ' '.join([f'{x:2}' for x in range(self.worldX)]) + '\n'
        for wY in range(0, self.worldY):
            row = f'{wY:2} '
            for wX in range(0, self.worldX):
                org = self.getOrganismFromPosition(Position(xPosition=wX, yPosition=wY))
                if org:
                    row += str(org.sign) + '  '
                else:
                    row += self.separator + '  '
            result += row + '\n'
        return result

    def activatePlague(self):
        self.__plagueActive = True
        self.__plagueTurnsRemaining = 2
        print("Plaga aktywowana! Wszystkie organizmy będą miały skrócone życie o połowę przez następne dwie tury.")

    def applyPlague(self):
        if self.__plagueActive:
            for org in self.organisms:
                org.liveLength = max(1, org.liveLength // 2)
            self.__plagueTurnsRemaining -= 1
            if self.__plagueTurnsRemaining <= 0:
                self.__plagueActive = False
                print("Plaga zakończona!")

    def enforceNatureProtectionRules(self):
        from collections import Counter    #Importuje Counter z modułu collections do liczenia wystąpień gatunków	
        species_count = Counter(type(org).__name__ for org in self.organisms)#liczy liczbę wystąpień kazdego gatunku organizmów na swiecie 
        total_organisms = len(self.organisms)
        
        min_population = 2
        max_dominance_ratio = 0.5 #maksymalny udział(wielkość wystąpień) jednego gatunku względem innych dla całej populacji
        
		# Przechodzi przez wszystkie gatunki i ich liczebność
        for species, count in species_count.items():
            if count < min_population:# Jeśli liczba organizmów danego gatunku jest mniejsza niż minimalna populacja, dodaje brakujące organizmy
                self.repopulateSpecies(species, min_population - count)
            elif count / total_organisms > max_dominance_ratio:# Jeśli liczba organizmów danego gatunku przekracza maksymalny udział, zmniejsza ich populację
                self.reduceSpecies(species, count - int(total_organisms * max_dominance_ratio))
                
    def repopulateSpecies(self, species, count):
        print(f"Uzupełnianie gatunku {species} o {count} nowych organizmów.")
        for _ in range(count):
            position = self.getRandomFreePosition()
            if position:
                if species == 'Sheep':
                    newOrg = Sheep(position=position, world=self)
                elif species == 'Lynx':
                    newOrg = Lynx(position=position, world=self)
                elif species == 'Antelope':
                    newOrg = Antelope(position=position, world=self)
                elif species == 'Grass':
                    newOrg = Grass(position=position, world=self)
                self.addOrganism(newOrg)
    # Przechodzi przez wszystkie organizmy i zmniejsza ich długość życia do 0 co powoduje ich usunięcie
    def reduceSpecies(self, species, count):
        print(f"Zmniejszanie populacji gatunku {species} o {count}.")
        reduced_count = 0
        for org in list(self.organisms):  # Używamy kopii listy do iteracji
            if type(org).__name__ == species and reduced_count < count:
                org.liveLength = 0
                reduced_count += 1
        # Usunięcie martwych organizmów po ich zredukowaniu
        self.organisms = [org for org in self.organisms if org.liveLength > 0]

                
    def getRandomFreePosition(self):
        from random import randint# Importuje funkcję randint do losowania liczb
        for _ in range(100):  # szukanie  wolnej pozycji
            x = randint(0, self.worldX - 1)
            y = randint(0, self.worldY - 1)
            position = Position(xPosition=x, yPosition=y)
            if self.getOrganismFromPosition(position) is None:
                return position
        return None

    def addOrganismFromUser(self, organismType, x, y):#funkcja gdzie uzytkownik moze sam dodac nowe zwierze
        position = Position(xPosition=x, yPosition=y)
        if not self.positionOnBoard(position) or self.getOrganismFromPosition(position) is not None:
            print(f"Nie można dodać organizmu na ({x}, {y}). Pozycja jest zajęta lub poza planszą.")
            return

        if organismType == 'Sheep':
            newOrg = Sheep(position=position, world=self)
        elif organismType == 'Lynx':
            newOrg = Lynx(position=position, world=self)
        elif organismType == 'Antelope':
            newOrg = Antelope(position=position, world=self)
        elif organismType == 'Grass':
            newOrg = Grass(position=position, world=self)
        else:
            print(f"Nieznany typ organizmu: {organismType}")
            return

        self.addOrganism(newOrg)
        print(f"{organismType} dodany na ({x}, {y})")
