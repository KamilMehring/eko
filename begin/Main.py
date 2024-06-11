from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
import os

if __name__ == '__main__':
    pyWorld = World(10, 10)

    newOrg = Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld)
    pyWorld.addOrganism(newOrg)

    newOrg = Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld)
    pyWorld.addOrganism(newOrg)

    newOrg = Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld)
    pyWorld.addOrganism(newOrg)

    newOrg = Lynx(position=Position(xPosition=3, yPosition=3), world=pyWorld)
    pyWorld.addOrganism(newOrg)

    newOrg = Antelope(position=Position(xPosition=4, yPosition=4), world=pyWorld)
    pyWorld.addOrganism(newOrg)

    print(pyWorld)

    for _ in range(0, 40):
        user_input = input('Naciśnij Enter, aby przejść do następnej tury, wpisz "plaga", aby aktywować plagę, wpisz "dodaj", aby dodać nowy organizm: ')
        if user_input == 'plaga':
            pyWorld.activatePlague()
        elif user_input == 'dodaj':
            organism_type = input('Podaj typ organizmu (Sheep, Lynx, Antelope, Grass): ')
            x = int(input('Podaj pozycję x: '))
            y = int(input('Podaj pozycję y: '))
            pyWorld.addOrganismFromUser(organism_type, x, y)
        else:
            os.system('cls')
            pyWorld.makeTurn()
            print(pyWorld)
