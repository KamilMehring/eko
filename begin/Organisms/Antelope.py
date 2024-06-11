from .Animal import Animal
from .Lynx import Lynx
from Action import Action
from ActionEnum import ActionEnum
from Position import Position 

class Antelope(Animal):

    def __init__(self, antelope=None, position=None, world=None):
        super(Antelope, self).__init__(antelope, position, world)

    def clone(self):
        return Antelope(self, None, None)

    def initParams(self):
        self.power = 4 
        self.initiative = 3 
        self.liveLength = 11 
        self.powerToReproduce = 5  
        self.sign = 'A' 

    def move(self):
        result = []  # Lista wyników działań
        # Pobiera pozycje sąsiadujące, na których znajduje się ryś
        lynx_positions = [pos for pos in self.getNeighboringPosition() if isinstance(self.world.getOrganismFromPosition(pos), Lynx)]

        if lynx_positions:  # Oblicza róznicę pozycji względem ryia
            for lynx_pos in lynx_positions:
                dx = self.position.x - lynx_pos.x
                dy = self.position.y - lynx_pos.y
                # Oblicza nową pozycję, oddaloną od rysia
                new_position = Position(xPosition=self.position.x + 2 * dx, yPosition=self.position.y + 2 * dy)
                # Sprawdza, czy nowa pozycja jest na planszy i czy jest pusta
                if self.world.positionOnBoard(new_position) and self.world.getOrganismFromPosition(new_position) is None:
                    # Dodaje akcję ruchu do wyników
                    result.append(Action(ActionEnum.A_MOVE, new_position, 0, self))
                    self.lastPosition = self.position  # Ustawia ostatnią pozycję
                    self.position = new_position  # Ustawia nową pozycję
                    return result

            # Jeżeli ucieczka nie jest możliwa, atakuje rysia
            lynx = self.world.getOrganismFromPosition(lynx_positions[0])
            if lynx:
                if self.power > lynx.power:  # Jeśli antylopa jest silniejsza od rysia
                    # Dodaje akcję usunięcia rysia do wyników
                    result.append(Action(ActionEnum.A_REMOVE, Position(xPosition=-1, yPosition=-1), 0, lynx))
                else:  # Jeśli ryś jest silniejszy od antylopy
                    # Dodaje akcję usunięcia antylopy do wyników
                    result.append(Action(ActionEnum.A_REMOVE, Position(xPosition=-1, yPosition=-1), 0, self))
        else:
            # Jeśli nie ma rysi, wykonuje standardowy ruch
            result = super(Antelope, self).move()

        return result
