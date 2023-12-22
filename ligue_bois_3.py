import sys
import math
import collections

# classes #################################################################


# classe Board
class Board:
    def __init__(self):
        self.side = 100
        self.grid = []
        self.build()
        

    def build(self):
        index = 0
        for i in range(self.side):
            line = []
            for j in range (self.side):
                cell = Cell(index, i, j)
                line.append(cell)
                index += 1
            self.grid.append(line)


# classe Cell 
class Cell:
    def __init__(self, index, cell_y, cell_x):
        self.index = index
        self.cell_y = cell_y
        self.cell_x = cell_x
    

# classe Drone
class Drone:
    my_drone_count = 0
    foe_drone_count = 0

    def __init__(self, drone_id, drone_x, drone_y, battery, scanList):
        self.drone_id = drone_id
        self.drone_x = drone_x
        self.drone_y = drone_y
        self.battery = battery
        self.scanList = scanList
        self.flashLight = False

    @property
    def drone_id(self):
        return self._drone_id

    @drone_id.setter
    def drone_id(self, value):
        self._drone_id = value

    @property
    def drone_x(self):
        return self._drone_x
    
    @drone_x.setter
    def drone_x(self, value):
        self._drone_x = value

    @property
    def drone_y(self):
        return self._drone_y

    @drone_y.setter
    def drone_y(self, value):
        self._drone_y = value

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = value

    @property
    def scanList(self):
        return self._scanList

    @scanList.setter
    def scanList(self, value):
        self._scanList = value


    def moveToFish(self, FishCoord):
        self.drone_x = FishCoord.x
        self.drone_y = FishCoord.x 

# classe creature 
class Creature:
    # liste statique du nombre de créatures à l'écran 
    creatureList = []
    visible_creature_total = 0

    def __init__(self, creature_id, creature_x, creature_y, creature_vx, creature_vy):
        self.creature_id = creature_id
        self.creature_x = creature_x
        self.creature_y = creature_y
        self.creaturePos = (self.creature_y, self.creature_x)
        self.creature_vx = creature_vx
        self.creature_vy = creature_vy
        self.color = ""
        self.type = ""
        self.isScanned = False

        Creature.creatureList.append(self)


# classe qui gère la logique de jeu 
class Game:
    my_score = -1
    foe_score = -1
    IA_scan_count = -1
    radarRange = 0 
    nearest_creature = None

    # méthode de mise à jour des scans de créatures pour le joueur 
    @staticmethod
    def updateScanPlayer():
        myDrone.scanList = []
        # nombre de scans joueur 
        Game.IA_scan_count = int(input())

        for i in range(Game.IA_scan_count):
            # ID de chaques créatures scannées
            creature_id = int(input())
            myDrone.scanList.append(creature_id)
    
        debug(myDrone.scanList)

    # méthode de mise à jour des scans de créatures pour l'ennemi 
    @staticmethod
    def updateScanEnnemi():
        ennemiDrone.scanList = []

        # nombre de scans ennemis
        foe_scan_count = int(input())

        for i in range(foe_scan_count):

            # ID des créatures scannées par adversaire
            creature_id = int(input())
            ennemiDrone.scanList.append(creature_id)

        debug(ennemiDrone.scanList)

    # méthode d'update de la logique du drone player pour un tour de jeu 
    @staticmethod
    def updatePlayerDrone():
        Drone.my_drone_count = int(input())
        for i in range(Drone.my_drone_count):
        
            drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
            # infos du drone : id, x, y, emergency, battery 

            debug(drone_y)
            myDrone.drone_id = drone_id
            myDrone.drone_x = drone_x
            myDrone.drone_y = drone_y
            myDrone.battery = battery

            debug(myDrone.drone_y)


    @staticmethod
    def updateEnnemiDrone():
        Drone.foe_drone_count = int(input())

        for i in range(Drone.foe_drone_count):
        # infos du Drone ennemi 
            drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
            ennemiDrone.drone_id = drone_id
            ennemiDrone.drone_x = drone_x
            ennemiDrone.drone_y = drone_y
            ennemiDrone.battery = battery

            debug(ennemiDrone.drone_y)

    @staticmethod
    def updateCreature():
        visible_creature_count = int(input())

        for i in range(visible_creature_count):
            creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
            creature = Creature(creature_id, creature_x, creature_y, creature_vx, creature_vy)

    # convertir les coordonnées de playerDronePos sour forme de tuple 
    @staticmethod
    def findCreatureBfs(playerDronePos, posList):
        visited, queue = set(), collections.deque([playerDronePos])
        visited.add(playerDronePos)

        while queue:
            vertex = queue.popleft()
            debug(vertex)

            for neighboor in posList:
                if neighboor not in visited:
                    
                    # on teste si il y a une créature dans un rayon de 100 
                    for creature in Creature.creatureList:
                        if creature.creaturePos[0] == neighboor[0] and creature.creaturePos[1] == neighboor[1]:
                            print("flash!")
                    
                    
                    visited.add(neighboor)
                    queue.append(neighboor)

    
    # méthode de recherche des créatures avec le sonar, limité à 100 u autour 
    @staticmethod
    def findNeighboorsWithBfs(playerDronePos):
        
        if Game.radarRange <= 1000 and playerDronePos[0] >= 0 and playerDronePos[0] <= 10000 and playerDronePos[1] >= 0 and playerDronePos[1] <= 10000:

            Game.radarRange += 1
            up = (playerDronePos[0] - 1, playerDronePos[1])
            down = (playerDronePos[0] + 1, playerDronePos[1])
            left = (playerDronePos[0], playerDronePos[1] - 1)
            right = (playerDronePos[0], playerDronePos[1] + 1)

            posList = [up, down, left, right]

            Game.findCreatureBfs(playerDronePos, posList)

            for pos in posList:
                Game.findNeighboors(pos)

           
            return posList 

        
        return []

    
    @staticmethod 
    def flashLight(playerDronePos):
        # methode de calcul de coordonnées dans un repère orthogonal
        for creature in Creature.creatureList:
            d = Game.distanceBetweenDroneCreature(playerDronePos, creature)
            if 800 < d <= 1000:
                myDrone.flashLight = True

    
    @staticmethod
    def distanceBetweenDroneCreature(playerDronePos, creature):
        return math.sqrt(pow(creature.creaturePos[0] - playerDronePos[0],2) + pow(creature.creaturePos[1] - playerDronePos[1],2))

    @staticmethod
    def moveToNearestCreature(playerDronePos):
        if Creature.creatureList:
            nearest_unscanned_creature = min(
                (creature for creature in Creature.creatureList if creature.creature_id not in myDrone.scanList),
                key=lambda creature: Game.distanceBetweenDroneCreature(playerDronePos, creature)
            )
            if nearest_unscanned_creature:
                Game.nearest_creature = nearest_unscanned_creature


# fonctions utilitaires ####################################################

def debug(value):
    print(value, file=sys.stderr, flush=True)

# init #####################################################################


# instanciation d'un nouveau drone
myDrone = Drone(1,0,0, None, [])

# instanciation d'un nouveau drone ennemi 
ennemiDrone = Drone(1,0,0, None, [])

# nombre de créatures 
creature_count = int(input())
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    print(creature_id, file=sys.stderr, flush=True)



# game loop #################################################################
while True:

    # remise à zéro de la position de la créature la plus proche
    Game.nearest_creature = None
    # réinitialisation de la flashlight
    myDrone.flashLight = False
    # init de la liste des creatures
    Creature.creatureList = []
    # score actuel
    Game.my_score = int(input())
    # score de l'adversaire
    Game.foe_score = int(input())
    # update de la liste de scan du joueur 
    Game.updateScanPlayer()
    # update de la liste de scan de l'ennemi 
    Game.updateScanEnnemi()
    # update de la logique métier du player drone
    Game.updatePlayerDrone()
    # update de la logique métier du ennemi drone 
    Game.updateEnnemiDrone()



    # inutile pour l'instant ####################################################
    drone_scan_count = int(input())

    debug(drone_scan_count)
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
    ############################################################################

    # update de la liste des créatures
    Game.updateCreature()

    
    # inutile pour l'instant ####################################################
    radar_blip_count = int(input())
    for i in range(radar_blip_count):
        inputs = input().split()
        debug(inputs)
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]

# output ############################################################################################


    # On se déplace vers la créature la plus proche
    Game.moveToNearestCreature((myDrone.drone_y, myDrone.drone_x))

    # activation de la flashLight si une créature se trouve à portée 
    Game.flashLight((myDrone.drone_y, myDrone.drone_x))

    # réinit du radar Range
    Game.radarRange = 0


    for i in range(Drone.my_drone_count):
        
        output = ""
        
        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>

        if Game.nearest_creature:
            output = f'MOVE {Game.nearest_creature.creaturePos[1]} {Game.nearest_creature.creaturePos[0]} '

        if myDrone.flashLight:
            output += '1'
        else:
            output += '0'

        print(output)

