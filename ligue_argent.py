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
    commonScanList = []
    ennemiScanList = []
    waitingScanList = []
    ennemiWaitingScanList = []
    commonMonsterVisibleListe = []
    lastcreatureFollowedDirection = []

    def __init__(self, drone_id, drone_x, drone_y, emergency, battery):
        self.drone_id = drone_id
        self.drone_x = drone_x
        self.drone_vx = -1
        self.drone_vy = -1
        self.drone_y = drone_y
        self.battery = battery
        self.emergency = emergency
        self.scanList = []
        self.scanNotSaved = []
        self.flashLight = True
        self.totalScan = 0
        self.isLeader = False
        self.radarListeDetails = []
        self.creatureFollowed = -1 # id de la creature suivie
        debug("creature_suivie : ", self.creatureFollowed)
        self.escape = False
        self.evasion_angle_degrees = 180
        self.initial_escape_angle = None
        self.escape_distance = 600
        self.monsterFollowing = [] #liste de te tuples ( monster : entite , distance)
        self.nextPos = {'x' : 0, 'y' : 0}
        self.flashLightInit()


    # Init de la fashlight : si aucun monstre n'est en mode following, alors on pet activer les flashlights
    def flashLightInit(self):
        if(len(self.monsterFollowing) == 0):
            self.flashLight = True
        else:
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

    # fonction que permet de contourner un monstre
    def move_around_monster(self, monster):
        min_distance = 500
        desired_distance = 600

        # Calcul de la distance actuelle entre le drone et le monstre
        current_distance = math.sqrt((self.drone_x - monster.creature_x)**2 + (self.drone_y - monster.creature_y)**2)

        # Si la distance actuelle est inférieure à la distance minimale, ajustez la distance désirée
        if current_distance < min_distance:
            desired_distance = min_distance + 100  # Ajoutez un petit surplus pour éviter d'être trop proche

        # Calcul de l'angle entre le drone et le monstre
        angle_to_monster = math.atan2(monster.creature_y - self.drone_y, monster.creature_x - self.drone_x)

        # Calcul du nouvel angle pour se déplacer latéralement
        lateral_angle = angle_to_monster + math.radians(45)

        # Calcul des nouvelles coordonnées polaires
        new_x = self.drone_x + (desired_distance) * math.cos(lateral_angle)
        new_y = self.drone_y + (desired_distance) * math.sin(lateral_angle)

        return (math.floor(new_x), math.floor(new_y))

    def simpleEscape(self, creature):
        # calcul des vecteurs du drone
        drone_vx = self.drone_x - creature.creature_x
        drone_vy = self.drone_y - creature.creature_y
        # drone_vx = self.nextPos['x'] - self.drone_x
        debug("drone_next_pos_x :", self.nextPos['x'])
        debug("drone_vx :", drone_vx)
        # drone_vy = self.nextPos['y'] - self.drone_y
        debug("drone_next_pos_y :", self.nextPos['y'])
        debug("drone_vy :", drone_vy)

        angle_to_monster = math.atan2(creature.creature_y - self.drone_y, creature.creature_x - self.drone_x)
        debug("angle_to_monster : ", angle_to_monster)
        angle_to_monster += math.radians(250)

        # Ajustement des vecteurs du drone pour s'éloigner du monstre tout en maintenant la distance minimale
        drone_vx += 600 * math.cos(angle_to_monster)
        debug("drone_vx :", drone_vx)
        drone_vy += 600 * math.sin(angle_to_monster)
        debug("drone_vy :", drone_vy)

        drone_new_x = self.drone_x + drone_vx
        debug("drone_new_x :", drone_new_x)
        drone_new_y = self.drone_y + drone_vy
        debug("drone_new_y : ", drone_new_y)

        return (math.floor(drone_new_x), math.floor(drone_new_y))



    def escapeFromCreature(self, creature):

        evasion_angle_degrees=90
        evasion_distance=10
        # Vecteur de déplacement de la créature
        vecteurX_creature = creature.creature_vx
        vecteurY_creature = creature.creature_vy



        # Norme du vecteur de la créature
        norme_creature = math.sqrt(vecteurX_creature**2 + vecteurY_creature**2)

        # Normalisation du vecteur de la créature
        vecteurX_creature /= norme_creature
        vecteurY_creature /= norme_creature

        # Calcul de l'angle initial de déplacement de la créature
        angle_creature_degrees = math.degrees(math.atan2(vecteurY_creature, vecteurX_creature))

        # Calcul de l'angle d'évitement (ajout de l'angle initial)
        evasion_angle_radians = math.radians(angle_creature_degrees + evasion_angle_degrees)

        # Calcul du vecteur de déplacement pour l'évitement
        evasion_vector = (
            evasion_distance * math.cos(evasion_angle_radians),
            evasion_distance * math.sin(evasion_angle_radians)
        )

        # Nouvelle position du drone en tenant compte de l'évitement
        droneNewPosX = self.drone_x + evasion_vector[0]
        droneNewPosY = self.drone_y + evasion_vector[1]

        return (math.floor(droneNewPosX), math.floor(droneNewPosY))

    def escapeFromCreatures(self, monsters):
        # Initialisation du vecteur résultant
        resultant_vector = (0, 0)

        # Calcul de la somme des vecteurs entre le drone et chaque monstre
        for monster in monsters:
            debug("monster_id :", monster.creature_id)
            vector_to_monster = (monster.creature_x - self.drone_x, monster.creature_y - self.drone_y)
            resultant_vector = (resultant_vector[0] + vector_to_monster[0], resultant_vector[1] + vector_to_monster[1])

        # Normalisation du vecteur résultant
        magnitude = math.sqrt(resultant_vector[0]**2 + resultant_vector[1]**2)
        normalized_resultant = (resultant_vector[0] / magnitude, resultant_vector[1] / magnitude)

        # Nouvelle position pour éviter les monstres
        escape_distance = 500
        new_position = (
            math.floor(self.drone_x + escape_distance * - normalized_resultant[0]),
            math.floor(self.drone_y + escape_distance * - normalized_resultant[1])
        )

        return new_position


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
    total_creature = -1
    my_score = -1
    foe_score = -1
    IA_scan_count = -1
    radarRange = 0 
    nearest_creature = None
    global_radar_list = []
    total_creature_list = []
    total_creature_list_without_monsters = []
    monster_id_liste = []
    monster_liste = []

    # méthode de mise à jour des scans de créatures pour le joueur 
    @staticmethod
    def updateScanPlayer():
        # nombre de scans joueur 

        Drone.commonScanList = []
        Game.IA_scan_count = int(input())

        for i in range(Game.IA_scan_count):
            # debug('anciens_scan', Game.IA_scan_count)
            # ID de chaques créatures scannées
            creature_id = int(input())

            #mise à jour des scans des drones dans la liste des joueurs
            # for drone in Drone.my_drones_list:
            #     drone.scanList.append(creature_id)
            Drone.commonScanList.append(creature_id)
    
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
            Drone.ennemiScanList.append(creature_id)

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
            # debug("myDrone_y : ", drone.drone_y)
            # debug("myDrone_x : ", drone.drone_y)


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


    @staticmethod
    def updateCreatureVisibility():
        Creature.visiblesCreature = []
        visible_creature_count = int(input())

        debug("creatures visibes : ", visible_creature_count)

        for i in range(visible_creature_count):
            
            creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
            creature = Creature(creature_id, creature_x, creature_y, creature_vx, creature_vy)
            Creature.visiblesCreature.append(creature)

        debug('Liste des creatures visibles : ', [creature.creature_id for creature in Creature.visiblesCreature])

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

    @staticmethod
    def distanceBetweenDroneCreature2(drone, creature):
        return math.sqrt(pow(creature.creature_x - drone.drone_x ,2) + pow(creature.creature_y - drone.drone_y,2))

    @staticmethod
    def distanceBetweenDroneCreatureWithCoords(drone, creature):
        return math.sqrt(pow(creature['x'] - drone['x'] ,2) + pow(creature['y'] - drone['y'],2))

    
    

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
        dep = 600
        # for creature in Creature.visiblesCreature:
        #     if creature.creature_id in Game.monster_id_liste:
        #         dep = 200
        #         break
           
        drone_y = 0
        drone_x = 0

        if direction == 'BR':
            drone_x = calculDistanceX(45, dep) + playerDronePos.drone_x
            drone_y = calculDistanceY(45, dep) + playerDronePos.drone_y

        elif direction == 'BL':
            drone_x =  playerDronePos.drone_x - calculDistanceX(45, dep)
            drone_y = calculDistanceY(45, dep) + playerDronePos.drone_y

        elif direction == 'TL':
            drone_x =  playerDronePos.drone_x - calculDistanceX(45, dep)
            drone_y =  playerDronePos.drone_y - calculDistanceY(45, dep)

        elif direction == 'TR':
            drone_x =  calculDistanceX(45, dep) + playerDronePos.drone_x
            drone_y =  playerDronePos.drone_y - calculDistanceY(45, dep)

        # Ici on va alimenter la propriété droneNextPos pour connaitre la nouvelle position du drone 
        playerDronePos.nextPos['x'] = drone_x
        playerDronePos.nextPos['y'] = drone_y


        return (math.floor(drone_y), math.floor(drone_x))

    @staticmethod 
    def calculDroneVector(drone):
        drone_vx = drone.nextPos['x'] - drone.drone_x
        drone_vy = drone.nextPos['y'] - drone.drone_y

        return drone_vx, drone_vy



    @staticmethod
    def updateDroneRadarDetails():

        Game.global_radar_list = []
        
        radar_blip_count = int(input())

        for i in range(radar_blip_count):
            radarTuple = ()


            inputs = input().split()
            # debug("Radar_inputs", inputs)
            drone_id = int(inputs[0])
            creature_id = int(inputs[1])
            radar = inputs[2]
            radarTuple = (drone_id, creature_id, radar)

            Game.global_radar_list.append(radarTuple)


            # mise à jour des radars de chaque drone 
            for drone in Drone.my_drones_list:
                if drone.drone_id == drone_id:
                    drone.radarListeDetails.append(radarTuple)

            for ennemiDrone in Drone.ennemi_drones_list:
                if ennemiDrone.drone_id == drone_id:
                    ennemiDrone.radarListeDetails.append(radarTuple)
            
        debug("Global_radar_liste", Game.global_radar_list)
            

    @staticmethod
    def getAllCreatures():

        Game.total_creature_list = []
        Game.total_creature_list_without_monsters = []
        Game.monster_id_liste = []
        Game.monster_liste = []

        creature_count = int(input())
        Game.total_creature = creature_count
        # debug("creature_count ;", creature_count)
        for i in range(creature_count):
            creature_id, color, _type = [int(j) for j in input().split()]
            # debug("creature_id : ", creature_id)

            Game.total_creature_list.append((creature_id, color, _type))

        for creature in Game.total_creature_list:
            if creature[1] != -1:
                Game.total_creature_list_without_monsters.append(creature)
            else:
                Game.monster_liste.append(creature)
                Game.monster_id_liste.append(creature[0])

        # debug("liste des créatures total :", Game.total_creature_list)
        # debug("len : ", len(Game.total_creature_list))
        # debug("liste des creatures sans les monstres : ", Game.total_creature_list_without_monsters)
        # debug("len : ", len(Game.total_creature_list_without_monsters))

    @staticmethod
    def updateNotSavedScans():

        drone_scan_count = int(input())

        for i in range(drone_scan_count):
            drone_id, creature_id = [int(j) for j in input().split()]

            # gestion des scans si le drone_id sont les miens : 
            for drone in Drone.my_drones_list:
                if drone.drone_id == drone_id:
                    drone.scanNotSaved.append(creature_id)
                    Drone.waitingScanList.append(creature_id)

            for ennemiDrone in Drone.ennemi_drones_list:
                if ennemiDrone == drone_id:
                    ennemiDrone.scanNotSaved.append(creature_id)
                    Drone.ennemiWaitingScanList.append(creature_id)

    # mettre en place un méthode qui va chercher l'ID DU DRONE DONT LE MONSTRE EST A PROXIMITE

    @staticmethod
    def findProximityDroneToMonster(monster, currentDrone):
        # calcul de la distance entre le monstre et le drone : 
        d = Game.distanceBetweenDroneCreature2(currentDrone, monster)
        debug("d", d)
        if( d <= 2000 ):
            debug("drone concerné : " + str(currentDrone.drone_id), "monster : " + str(monster.creature_id))
            debug("distance : ", d)
            # Si un monstre poursuit, alors on le met dans la liste avec la distance qui le sécpare
            currentDrone.monsterFollowing.append((monster, d))

    @staticmethod
    def findNewCoorsDroneNextTurn(monster, currentDrone):
        # calcul des nouvelles coordonnées du drone : 
        new_drone_x = currentDrone.nextPos['x']
        new_drone_y = currentDrone.nextPos['y']

        new_monster_x = monster.creature_x + monster.creature_vx
        new_monster_y = monster.creature_y + monster.creature_vy

        new_coords_drone = {  'x' : new_drone_x, 'y' : new_drone_y}
        new_coords_monster = { 'x' : new_monster_x, 'y' : new_monster_y }

        return new_coords_drone, new_coords_monster

    @staticmethod
    def calculDistanceNextTurn( new_coords_drone, new_coords_monster):
        # calcul de la distance entre le monstre et le drone : 
        d = Game.distanceBetweenDroneCreatureWithCoords(new_coords_drone, new_coords_monster)
        debug("d", d)
        return d


        
            
        
        


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


# # nombre de créatures 
# creature_count = int(input())
# # debug("creature_count ;", creature_count)
# for i in range(creature_count):
#     creature_id, color, _type = [int(j) for j in input().split()]
#     # debug("creature_id : ", creature_id)

Game.getAllCreatures()

touchDeep = False
gameCount = 0

# game loop #################################################################
while True:
    # myScans = 0
    gameCount += 1

    # scansEnAttente = []
    Creature.creatureFollowed = []

    Drone.commonMonsterVisibleListe = []

    Drone.lastcreatureFollowedDirection = []


    # mise à jour du scan global des ennemis
    Drone.ennemiScanList = []

    # mise à jour du scan global des joueurs
    Drone.commonScanList = []

    # mise à jour de la liste des scans globaux en attente de sauvegarde des joueurs
    Drone.waitingScanList = []

    # mise à jour de la liste des scans globax en attente de ennemis
    Drone.ennemiWaitingScanList = []

    # init de la creature la plus proche
    Game.nearest_creature = None

    # init radarDetails du Drone
    Drone.radar_details = []

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

    # Gestion des scans en attente ####################################################
    Game.updateNotSavedScans()

    # update de la liste des créatures
    Game.updateCreatureVisibility()
    
    # inutile pour l'instant ####################################################

    Game.updateDroneRadarDetails()
    


# output ############################################################################################

    # Si la liste des créatures visibles est vide, alors il faut faire appel au radar

    # Game.moveToRadarPosition(myDrone, Drone.radar_details[0][2])

    Game.radarRange = 0


    # for i in range(Drone.my_drones_count):
    for drone in Drone.my_drones_list:

        monster = None
        output = ""
        
        debug("Strategie pour le drone : ", drone.drone_id)

        # si la scanList est complete est que l'ordinateur n'a pas fini
        if(len(set(Drone.commonScanList)) == Game.total_creature_list_without_monsters):
            if drone.isLeader:
                output += "Move 10000 10000 "
            else:
                output += "Move 0 10000 "

        # si tous les drones sont scannés 
        elif(len(drone.scanNotSaved) + len(Drone.commonScanList) == Game.total_creature_list_without_monsters or len(drone.scanNotSaved)  >= 11 or Game.total_creature_list_without_monsters == len(set(Drone.waitingScanList))):
            output += f'Move {drone.drone_x} 450 '

        
        
        # elif(gameCount <= 3):

        #     if drone.isLeader:
        #         output = f'Move 5500 2300 '
        #     else:
        #         output = f'Move 4500 2300 '

        
        # SI LA SCAN LISTE N ET PAS COMPLETE 
        else:
            # if drone.battery > 0:
            #     drone.flashLight = True
            # ici il faudra gérer la logique pour poursuivre une entité visible
            if len(Creature.visiblesCreature) > 0:
                debug("Attention Creature à proximité", "")
                # parcours de la liste des creature visible et recherche si il s'agit d'un monstre: 
                debug("liste des monstres :", Game.monster_liste)

                for creature in Creature.visiblesCreature:
                    if creature.creature_id in Game.monster_id_liste:
                        debug("Attention Cette créature est un monstre", "")
                        # si la créature est un monstre, on va chercher l'id du drone dont il est à proximité est alimenter le tableau
                        Game.findProximityDroneToMonster(creature, drone)

                        Drone.commonMonsterVisibleListe.append(creature)
                        debug("liste des monstres visibles :", Drone.commonMonsterVisibleListe)

            
            # On peut allumer les lumières
            # surtout éteindre la lumière !
            
            # Si le drone ne suit aucune créature
            if drone.creatureFollowed == -1 :
                # On cherche l'id de la créature non découverte non scannée
                unseen_creatures = [creature for creature in drone.radarListeDetails if creature[1] not in Drone.waitingScanList and creature[1] not in Drone.commonScanList  and creature[1] not in Creature.creatureFollowed and creature[1] not in Game.monster_id_liste]

                if unseen_creatures:
                    # Il y a des créatures non découvertes non scannées
                    unseen_creatures_index = unseen_creatures[0][1]
                    unseen_creatures_direction = unseen_creatures[0][2]

                else:
                    output += f'MOVE {drone.drone_x} 0 '

            else:
                unseen_creatures = [creature for creature in drone.radarListeDetails if creature[1] == drone.creatureFollowed]

            if len(unseen_creatures) > 0:
                debug('unseens',unseen_creatures)
                unseen_creatures_index = unseen_creatures[0][1]
                unseen_creatures_direction = unseen_creatures[0][2]

                # Vérifier si la créature n'est pas déjà suivie par un autre drone
                if unseen_creatures_index not in Creature.creatureFollowed:
                    
                    # Ajout de l'index de la créature suivie dans le tableau des créatures suivies
                    Creature.creatureFollowed.append(unseen_creatures_index)

                    # On attribue aussi l'index de la créature suivie à l'intance du drone
                    drone.creatureFollowed = unseen_creatures_index

                    # On attribue l'index de la cette créature à la variable statique de classe 
                    Drone.lastcreatureFollowedDirection = unseen_creatures_direction

                    # debug("creatutes followed :", Creature.creatureFollowed)
                    # debug("creatute index :", drone.creatureFollowed)

                    current_creature_direction = unseen_creatures_direction
                    debug('current_creature_direction: ', current_creature_direction)

                    # On dirige le drone vers la créature jusqu'à ce qu'elle soit visible
                    destination = Game.moveToRadarPosition(drone, current_creature_direction)

                    output = f'MOVE {destination[1]} {destination[0]} '
                        # debug("output: ", output)


                # Si des monstres nous suivent : 
                if(len(drone.monsterFollowing) != 0):
                

                # ICI on a des monstres qui nous suivent
            
                    newPos = ()
                    # surtout éteindre la lumière !
                    drone.flashlight = False

                    # Si le monstre est immobile, alors on va le contourner 
                    debug("evitement", drone.drone_id)

                    debug("drone_x : ", drone.drone_x)
                    debug("drone_y : ", drone.drone_y)

                    debug("monstre_x :", drone.monsterFollowing[0][0].creature_x)
                    debug("monstre_y :", drone.monsterFollowing[0][0].creature_y)

                    


                    # Si plusieurs monstres suivent, alors on remonte
                    debug("drone_monster_liste_following," , drone.monsterFollowing[0][1])

                    # debug("monster: ", drone.monsterFollowing[0][0].creature_y)


                    # Si un seul monstre en train de nous suivre
                    # if(len(drone.monsterFollowing) == 1):
                    debug("statégie d'évitement un seul monster", "")
                    # Si la vitesse du monstre est nulle, et que d > 600 on va le contourner en continuant notre route vers la creature
                    if(drone.monsterFollowing[0][0].creature_vy == 0 and drone.monsterFollowing[0][0].creature_vx == 0 and drone.monsterFollowing[0][1] > 600 ):
                        debug("evitement: ", "vitesse nulle")
                        newPos = drone.move_around_monster(drone.monsterFollowing[0][0])
                        
                    # Si la vitesse est nulle mais qie la distance est inférieur à 600, alros on s'échappe
                    elif(drone.monsterFollowing[0][1] <= 600 or (drone.monsterFollowing[0][0].creature_vy != 0 and drone.monsterFollowing[0][0].creature_vx != 0) ):
                        debug("v_x du monstre du monstre :",drone.monsterFollowing[0][0].creature_vx)
                        debug("v_y du monstre du monstre :",drone.monsterFollowing[0][0].creature_vy)
                        debug("evitement : ", "vitesse ou d < 600")

                        # calcul des coordonnées / distance du drone et du monstre au tour t+1 
                        drone_new_coords, monster_new_coords = Game.findNewCoorsDroneNextTurn(drone.monsterFollowing[0][0], drone)
                        debug("drone_new_coords", drone_new_coords)
                        debug("monster_new_coords", monster_new_coords)

                        # calcul de la nouvelle distance
                        new_distance = Game.calculDistanceNextTurn(drone_new_coords, monster_new_coords)

                        debug("distance t+1 :", new_distance)

                        if new_distance > 600:
                            debug("distance Ok :", new_distance)
                            output = f'MOVE {destination[1]} {destination[0]} '
                        
                        else:
                            debug("distance insuffisante :", new_distance)
                            newPos = drone.simpleEscape(drone.monsterFollowing[0][0])
                            output = f'Move {newPos[0]} {newPos[1]} '
                        # si distance > distance maxi de détection, alors on ne fait rien 

                        # Sinon on change le vectuer de manière à ce que cette distance reste supérieure. 

                        
                            debug("newPos :", newPos)

                    # else:
                    #     debug("statégie d'évitement pour plusieurs monstres", "")
                    #     debug("liste des montres: ",drone.monsterFollowing)
                    #     newPos = drone.escapeFromCreatures(drone.monsterFollowing)

                   

        # Game.flashLight((myDrone.drone_y, myDrone.drone_x))

        if drone.flashLight == True:
            output += '1'
        else:
            output += '0'

        print(output)
            


   


        

