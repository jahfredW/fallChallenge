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
    my_drones_count = 0
    foe_drone_count = 0 # 
    radar_details = [] # details du radar
    my_drones_list = [] # liste des drones du joueur
    ennemi_drones_list = []
    isLeader = False
    communScanList = []

    def __init__(self, drone_id, drone_x, drone_y, emergency, battery):
        self.drone_id = drone_id
        self.drone_x = drone_x
        self.drone_y = drone_y
        self.battery = battery
        self.emergency = emergency
        self.scanList = []
        self.scanNotSaved = []
        self.flashLight = False
        self.totalScan = 0
        self.isLeader = False
        self.radarListeDetails = []
        self.creatureFollowed = 0


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
    creatureFollowed = []
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

        Drone.communScanList = []
        Game.IA_scan_count = int(input())

        for i in range(Game.IA_scan_count):
            # debug('anciens_scan', Game.IA_scan_count)
            # ID de chaques créatures scannées
            creature_id = int(input())

            #mise à jour des scans des drones dans la liste des joueurs
            # for drone in Drone.my_drones_list:
            #     drone.scanList.append(creature_id)
            Drone.communScanList.append(creature_id)
    
        # debug("myScanList : ", myDrone.scanList)

    # méthode de mise à jour des scans de créatures pour l'ennemi 
    @staticmethod
    def updateScanEnnemi():
        # nombre de scans ennemis
        foe_scan_count = int(input())

        for i in range(foe_scan_count):

            # ID des créatures scannées par adversaire
            creature_id = int(input())

            #mise à jour des scans des drones dans la liste des ennemis
            for ennemiDrone in Drone.ennemi_drones_list:
                ennemiDrone.scanList.append(creature_id)

        # debug("ennemiScanList", ennemiDrone.scanList)

    # méthode d'update de la logique du drone player pour un tour de jeu 
    @staticmethod
    def updatePlayerDrone():
        # on vide la liste des drones du joueur
        Drone.my_drones_list = []

        # pour chaque drone présent dans le jeu

        Drone.my_drones_count = int(input())
        for i in range(Drone.my_drones_count):
            
            drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
            # infos du drone : id, x, y, emergency, battery 
            drone = Drone(drone_id, drone_x, drone_y, emergency, battery)

            # alimentation de la liste des drones du joueur
            Drone.my_drones_list.append(drone)

            if Drone.isLeader == False:
                Drone.isLeader = True
                drone.isLeader = False
            else:
                Drone.isLeader = False
                drone.isLeader = True
            # myDrone.drone_id = drone_id
            # myDrone.drone_x = drone_x
            # myDrone.drone_y = drone_y
            # myDrone.battery = battery
            debug("myDrone_y : ", drone.drone_y)
            debug("myDrone_x : ", drone.drone_y)


    @staticmethod
    def updateEnnemiDrone():

        # On vide la liste des drones ennemis
        Drone.ennemi_drones_list = []

        Drone.foe_drone_count = int(input())

        for i in range(Drone.foe_drone_count):
        # infos du Drone ennemi 
            drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]

            drone = Drone(drone_id, drone_x, drone_y, emergency, battery)

            Drone.ennemi_drones_list.append(drone)
            # ennemiDrone.drone_id = drone_id
            # ennemiDrone.drone_x = drone_x
            # ennemiDrone.drone_y = drone_y
            # ennemiDrone.battery = battery

         

    @staticmethod
    def updateCreature():
        Creature.visiblesCreature = []
        visible_creature_count = int(input())

        debug("creatures visibes : ", visible_creature_count)

        for i in range(visible_creature_count):
            
            creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
            creature = Creature(creature_id, creature_x, creature_y, creature_vx, creature_vy)
            Creature.visiblesCreature.append(creature)

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
                for drone in Drone.my_drones_list:
                    drone.flashLight = True

    
    @staticmethod
    def distanceBetweenDroneCreature(playerDronePos, creature):
        return math.sqrt(pow(creature.creaturePos[0] - playerDronePos[0],2) + pow(creature.creaturePos[1] - playerDronePos[1],2))

    # @staticmethod
    # def moveToNearestCreature(playerDronePos):
    #     if Creature.visiblesCreature:
    #         debug("visibles_creatures :", Creature.visiblesCreature)
    #         debug('myDroneScanList :' , myDrone.scanList)


    #         nearest_unscanned_creature = min(
    #             creature_id for creature_id in Creature.visiblesCreature if creature_id not in myDrone.scanList
    #             # key=lambda creature: Game.distanceBetweenDroneCreature(playerDronePos, creature)
    #         )
    #         if nearest_unscanned_creature:
    #             Game.nearest_creature = nearest_unscanned_creature

    
    @staticmethod
    def moveToRadarPosition(playerDronePos, direction):

        drone_y = 0
        drone_x = 0

        if direction == 'BR':
            debug( "direction BR", 'ici')
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
    def updateDroneRadarDetails():
        
        radar_blip_count = int(input())

        for i in range(radar_blip_count):
            radarTuple = ()


            inputs = input().split()
            # debug("Radar_inputs", inputs)
            drone_id = int(inputs[0])
            creature_id = int(inputs[1])
            radar = inputs[2]
            radarTuple = (drone_id, creature_id, radar)


            # mise à jour des radars de chaque drone 
            for drone in Drone.my_drones_list:
                if drone.drone_id == drone_id:
                    drone.radarListeDetails.append(radarTuple)

            for ennemiDrone in Drone.ennemi_drones_list:
                if ennemiDrone.drone_id == drone_id:
                    ennemiDrone.radarListeDetails.append(radarTuple)
            
            # Drone.radar_details.append(radarTuple)



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
# myDrone = Drone(1,0,0, None, [])

# # instanciation d'un nouveau drone ennemi 
# ennemiDrone = Drone(1,0,0, None, [])

# nombre de créatures 
creature_count = int(input())
# debug("creature_count ;", creature_count)
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    # debug("creature_id : ", creature_id)


#instanciation de la board

# board = Board()
# debug(board)
touchDeep = False
gameCount = 0

# game loop #################################################################
while True:
    # myScans = 0
    gameCount += 1

    # scansEnAttente = []
    Creature.creatureFollowed = []

    Drone.communScanList = []
    # init de la creature la plus proche
    Game.nearest_creature = None

    # init radarDetails du Drone
    Drone.radar_details = []

    # myDrone.scanList = []

    # init de la flashLight
    # myDrone.flashLight = False
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

        # gestion des scans si le drone_id sont les miens : 
        for drone in Drone.my_drones_list:
            if drone.drone_id == drone_id:
                drone.scanNotSaved.append(creature_id)
                Drone.communScanList.append(creature_id)

        for ennemiDrone in Drone.ennemi_drones_list:
            if ennemiDrone == drone_id:
                ennemiDrone.scanNotSaved.append(creature_id)
            # scansEnAttente.append(creature_id)
        # myDrone.scanList.append(creature_id)
    ############################################################################

    # update de la liste des créatures
    Game.updateCreature()
    
    # inutile pour l'instant ####################################################

    Game.updateDroneRadarDetails()
    


# output ############################################################################################

    # Si la liste des créatures visibles est vide, alors il faut faire appel au radar

    # Game.moveToRadarPosition(myDrone, Drone.radar_details[0][2])

    Game.radarRange = 0


    # for i in range(Drone.my_drones_count):
    for drone in Drone.my_drones_list:
        debug("total drones: ", creature_count )
        debug("drones :", drone.drone_id)
        # debug("drone_count", Drone.my_drone_count)
        output = ""

        debug("commun ListeScan:", Drone.communScanList)
        debug("myScans:", drone.scanNotSaved)
        debug("creatureCount: ", creature_count)
        # debug("creatures_visibles : ", Creature.visiblesCreature)

        if( len(drone.scanNotSaved)  >= 11 or creature_count == len(set(Drone.communScanList))):
            debug('ici', 'ici')
            output = f'Move 5000 450 '
        
        elif(gameCount <= 8):

            if drone.isLeader:
                output = f'Move 5500 2300 '
            else:
                output = f'Move 4500 2300 '

        
        

        # elif(len(set(myDrone.scanList)) == creature_count and myScans == 0):
        #     output = f'WAIT '

        
        else:
            if len(Drone.communScanList) < 8:
                drone.flashLight = True

                # ici il faudra gérer la logique pour poursuivre une entité visible


            # Si le drone ne suit aucune créature
            if drone.creatureFollowed == 0:
                # On cherche l'id de la créature non découverte non scannée
                unseen_creatures = [creature for creature in drone.radarListeDetails if creature[1] not in Drone.communScanList  and creature[1] not in Creature.creatureFollowed]

                if unseen_creatures:
                    # Il y a des créatures non découvertes non scannées
                    unseen_creatures_index = unseen_creatures[0][1]
                    unseen_creatures_direction = unseen_creatures[0][2]

                else:
                    output += f'MOVE 5000 0 '

            else:
                unseen_creatures = [creature for creature in drone.radarListeDetails if creature[1] == drone.creatureFollowed]

            if len(unseen_creatures) > 0:
                debug('unseens',unseen_creatures)
                unseen_creatures_index = unseen_creatures[0][1]
                unseen_creatures_direction = unseen_creatures[0][2]

                # Vérifier si la créature n'est pas déjà suivie par un autre drone
                if unseen_creatures_index not in Creature.creatureFollowed:
                    debug("ici", 'la')
                    # Ajout de l'index de la créature suivie dans le tableau des créatures suivies
                    Creature.creatureFollowed.append(unseen_creatures_index)



                    # On attribue aussi l'index de la créature suivie à l'intance du drone
                    drone.creatureFollowed = unseen_creatures_index



                    debug("creatutes followed :", Creature.creatureFollowed)
                    debug("creatute index :", drone.creatureFollowed)

                    current_creature_direction = unseen_creatures_direction
                    debug('current_creature_direction: ', current_creature_direction)

                    # On dirige le drone vers la créature jusqu'à ce qu'elle soit visible
                    destination = Game.moveToRadarPosition(drone, current_creature_direction)
                    output = f'MOVE {destination[1]} {destination[0]} '
                    debug("output: ", output)


        # Game.flashLight((myDrone.drone_y, myDrone.drone_x))

        if drone.flashLight == True:
            output += '1'
        else:
            output += '0'

        print(output)
            


   


        

