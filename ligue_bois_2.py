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
    radar_details = []

    def __init__(self, drone_id, drone_x, drone_y, battery, scanList):
        self.drone_id = drone_id
        self.drone_x = drone_x
        self.drone_y = drone_y
        self.battery = battery
        self.scanList = scanList
        self.flashLight = False
        self.totalScan = 0

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
    creatureScanned = []
    visiblesCreature = []
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
        # nombre de scans joueur 
        Game.IA_scan_count = int(input())

        for i in range(Game.IA_scan_count):
            # debug('anciens_scan', Game.IA_scan_count)
            # ID de chaques créatures scannées
            creature_id = int(input())
            myDrone.scanList.append(creature_id)
    
        # debug("myScanList : ", myDrone.scanList)

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

        # debug("ennemiScanList", ennemiDrone.scanList)

    # méthode d'update de la logique du drone player pour un tour de jeu 
    @staticmethod
    def updatePlayerDrone():
        Drone.my_drone_count = int(input())
        for i in range(Drone.my_drone_count):
        
            drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
            # infos du drone : id, x, y, emergency, battery 

            debug("myDrone_y : ", drone_y)
            myDrone.drone_id = drone_id
            myDrone.drone_x = drone_x
            myDrone.drone_y = drone_y
            myDrone.battery = battery

            debug("myDrone_x : ", myDrone.drone_y)


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

         

    @staticmethod
    def updateCreature():
        Creature.visiblesCreature = []
        visible_creature_count = int(input())

        for i in range(visible_creature_count):
            creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
            creature = Creature(creature_id, creature_x, creature_y, creature_vx, creature_vy)
            Creature.visiblesCreature.append(creature_id)

    # convertir les coordonnées de playerDronePos sour forme de tuple 
    @staticmethod
    def findCreatureBfs(playerDronePos, posList):
        visited, queue = set(), collections.deque([playerDronePos])
        visited.add(playerDronePos)

        while queue:
            vertex = queue.popleft()
            # debug("cellule : ", vertex)

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
        if Creature.visiblesCreature:
            debug("visibles_creatures :", Creature.visiblesCreature)
            debug('myDroneScanList :' , myDrone.scanList)


            nearest_unscanned_creature = min(
                creature_id for creature_id in Creature.visiblesCreature if creature_id not in myDrone.scanList
                # key=lambda creature: Game.distanceBetweenDroneCreature(playerDronePos, creature)
            )
            if nearest_unscanned_creature:
                Game.nearest_creature = nearest_unscanned_creature

    
    @staticmethod
    def moveToRadarPosition(playerDronePos, direction):

        drone_y = 0
        drone_x = 0

        if direction == 'BR':
            drone_x = calculDistanceX(45, 600) + playerDronePos.drone_x
            drone_y = calculDistanceY(45, 600) + playerDronePos.drone_y

        elif direction == 'BL':
            drone_x =  playerDronePos.drone_x - calculDistanceX(45, 600)
            drone_y = calculDistanceY(45, 600) + playerDronePos.drone_y

        elif direction == 'TL':
            drone_x =  playerDronePos.drone_x - calculDistanceX(45, 600)
            drone_y =  playerDronePos.drone_y - calculDistanceY(45, 600)

        elif direction == 'TR':
            drone_x =  calculDistanceX(45, 600) + playerDronePos.drone_x
            drone_y =  playerDronePos.drone_y - calculDistanceY(45, 600)

        return (math.floor(drone_y), math.floor(drone_x))





    @staticmethod
    def updateDroneRadarDetais():

        radar_blip_count = int(input())

        for i in range(radar_blip_count):
            radarTuple = ()
            inputs = input().split()
            # debug("Radar_inputs", inputs)
            drone_id = int(inputs[0])
            creature_id = int(inputs[1])
            radar = inputs[2]
            radarTuple = (drone_id, creature_id, radar)
            Drone.radar_details.append(radarTuple)



# fonctions utilitaires ####################################################

def debug(reference, value):
    print(reference + str(value), file=sys.stderr, flush=True)

def toRadian(angle):
    return (angle * math.pi) / 180

def calculDistanceX(angle, hyp):
    return math.cos(toRadian(angle)) * hyp

def calculDistanceY(angle, hyp):
    return math.sin(toRadian(angle)) * hyp



def calculY(angle, hyp):
    return math.sqrt(math.pow(hyp,2) - math.pow((hyp * math.cos(toRadian(angle))), 2))
# init #####################################################################


# instanciation d'un nouveau drone
myDrone = Drone(1,0,0, None, [])

# instanciation d'un nouveau drone ennemi 
ennemiDrone = Drone(1,0,0, None, [])

# nombre de créatures 
creature_count = int(input())
# debug("creature_count ;", creature_count)
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    # debug("creature_id : ", creature_id)


#instanciation de la board

# board = Board()
# debug(board)


# game loop #################################################################
while True:
    myScans = 0

    scansEnAttente = []

    # init de la creature la plus proche
    Game.nearest_creature = None

    # init radarDetails du Drone
    Drone.radar_details = []

    myDrone.scanList = []

    # init de la flashLight
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

   
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        if drone_id == myDrone.drone_id:
            myScans += 1
            scansEnAttente.append(creature_id)
        # myDrone.scanList.append(creature_id)
    ############################################################################


    

    # update de la liste des créatures
    Game.updateCreature()
    
    # inutile pour l'instant ####################################################

    Game.updateDroneRadarDetais()
    


# output ############################################################################################

    # Si la liste des créatures visibles est vide, alors il faut faire appel au radar

    # Game.moveToRadarPosition(myDrone, Drone.radar_details[0][2])

    Game.radarRange = 0


    for i in range(Drone.my_drone_count):
        # debug("drone_count", Drone.my_drone_count)
        output = ""
        
        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>


        # parcours tab radar est si index n'est pas dans la liste des visibles, alors on suit le radar
        # vers cette créature. 
        # si liste visible, on bouge et on la scanne, 
        # si creature est visible est scannée, on va faire une autre créature visible, sinon on suit le scan

        # SI la liste des creatures visibles est egale à la liste des creatures scannées, alors toutes 
        # les creatures visibles ont été scannées 
        # du coup il faut passer en mode radar

        debug("len de droneListeScan:", len(myDrone.scanList))
        debug("myScans:", myScans)
        debug("creatureCount: ", creature_count)


        # if((len(set(myDrone.scanList)) + myScans >= creature_count) or ( myScans  >= 3)):
        if( myScans  >= 5 or creature_count - myScans == len(myDrone.scanList)):
            output = f'Move 5000 480 '
            debug('ici', 'ici')
            # if(myDrone.drone_y == 50):
            #     goUp += 1

        # elif(len(set(myDrone.scanList)) == creature_count and myScans == 0):
        #     output = f'WAIT '

        
        else:

            if (len(Creature.visiblesCreature) > 0):

                myDrone.flashLight = True

             # On cherche l'id de la créature non découverte non scannée
            unseen_creatures = [creature for creature in Drone.radar_details if creature[1] not in myDrone.scanList and creature[1] not in scansEnAttente]

            if unseen_creatures:
                current_creature_direction = unseen_creatures[0]
                debug('current_creature_direction: ', current_creature_direction[2])

                # On dirige le drone vers la créature jusqu'à ce qu'elle soit visible
                destination = Game.moveToRadarPosition(myDrone, current_creature_direction[2])
                output = f'MOVE {destination[1]} {destination[0]} '
                debug("output: ", output)

        # Game.flashLight((myDrone.drone_y, myDrone.drone_x))

        if myDrone.flashLight:
            output += '1'
        else:
            output += '0'

        print(output)
            


   


        

