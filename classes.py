import math
import random
import pygame as pg

class Event:
    def __init__(self, title, desc, effects):
        self.title = title
        self.desc = desc
        self.effects = effects


class Nation:
    emergency_tax = False
    uk_opinion = 0
    fr_opinion = 0
    rs_opinion = 0
    economic_buff = 1
    emancipation_proclamation = False

    completed_focuses = []

    def __init__(self, name, provinces, score, money, manpower, morale, uk_opinion, fr_opinion, rs_opinion, focuses):
        self.name = name
        self.provinces = provinces
        self.score = score
        self.money = money
        self.manpower = manpower
        self.morale = morale
        self.uk_opinion = uk_opinion
        self.fr_opinion = fr_opinion
        self.rs_opinion = rs_opinion
        self.focuses = focuses

    def has_focus(self, foc):
        if(foc in self.completed_focuses):
            return True
        else:
            return False

    def collect_taxes(self):
        for province in self.provinces:
            if(self.emergency_tax):
                self.money += province.warscore * 50 * self.economic_buff
                self.money += province.factories * 150 * self.economic_buff
            else:
                self.money += province.warscore * 25 * self.economic_buff
                self.money += province.factories * 75 * self.economic_buff

    def initiate_emergency_taxes(self):
        self.emergency_tax = True
        self.morale /= 1.5

    def end_emergency_taxes(self):
        self.emergency_tax= False
        self.morale *= 1.2

    def build_fort(self, prov):
        if(self.money >= 100_000*prov.fort_level):
            prov.upgrade_fort()
            self.money -= 100_000*prov.fort_level

    def build_factory(self, prov):
        if (self.money >= 50_000 * prov.factories):
            prov.build_factory()
            self.money -= 50_000 * prov.factories

    def build_railroads(self, prov):
        if (self.money >= 10_000 * prov.railroads):
            prov.build_railroads()
            self.money -= 10_000 * prov.railroads

    def build_barracks(self, prov):
        if (self.money >= 50_000 * prov.barracks):
            prov.build_barracks()
            self.money -= 50_000 * prov.barracks

    def add_units(self, army, unit):
        if(self.money >= unit.cost and self.manpower >= unit.manpower):
            self.money -= unit.cost
            self.manpower -=  unit.manpower
            army.units.append(unit)
    def update(self, otherNation):
        self.collect_taxes()
        seceded = []
        for prov in self.provinces:
            self.manpower += (prov.barracks * 20) * (self.morale - 50)
            if(prov.support < -20):
                if(len(prov.armies) == 0):
                    otherNation.provinces.append(prov)
                    self.provinces.remove(prov)
                    otherNation.score += prov.warscore
                    self.score -= prov.warscore
                    self.morale -= prov.warscore
                    otherNation.morale += prov.warscore
                    prov.support = min(100,-prov.support + random.randint(20, 50))
                    seceded.append(prov)
            if(self.score < 0):
                prov.support -= random.randint(0,5)
            if(self.score > 30):
                prov.support += random.randint(0, 5)
        if(self.manpower < 0):
            self.manpower=0
        if(self.manpower > 1_000_000):
            self.manpower = 1_000_000
        if(self.morale < 0):
            self.morale = 0
        if(self.morale > 100):
            self.morale = 100
        return seceded
class Province:
    fort_level = 1
    def __init__(self, name, warscore, factories, barracks, armies, railroads, support, fort_level, slaveholding, coords):
        self.name = name
        self.warscore = warscore
        self.factories = factories
        self.barracks = barracks
        self.armies = armies
        self.railroads = railroads
        self.support = support
        self.fort_level = fort_level
        self.slaveholding = slaveholding
        self.coords = coords
        self.clicked = False
        self.border_states = []
        self.land = True
    def build_factory(self):
        self.factories += 1

    def build_barracks(self):
        self.barracks += 1

    def build_railroads(self):
        self.railroads += 1

    def upgrade_fort(self):
        self.fort_level += 1

    def raze(self):
        self.factories = 1
        self.barracks = 1
        self.railroads = 1
        self.fort_level = 1
        self.support -= random.randint(0,30)

class SeaProvince(Province):
    def __init__(self, name, armies, coords):
        self.name = name
        self.warscore = 0
        self.factories = 0
        self.barracks = 0
        self.armies = armies
        self.railroads = 0
        self.support = 9999999
        self.fort_level = 1
        self.slaveholding = False
        self.coords = coords
        self.clicked = False
        self.border_states = []
        self.land = False

class SeaZone:
    landNeighbors = []
    seaNeighbors = []
    def __init__(self, name, armies, coords):
        self.name = name
        self.armies = armies
        self.coords = coords
        self.clicked = False


class Unit:
    def __init__(self, name, health, atk, cost, speed, manpower):
        self.name = name
        self.ogHealth= health
        self.health = health
        self.atk = atk
        self.cost = cost
        self.speed = speed
        self.manpower = manpower

    def getAtk(self):
        return self.atk

    def getOgHealth(self):
        return self.ogHealth

    def getHealth(self):
        return self.health
    def getName(self):
        return self.name

    def setHealth(self, int):
        self.health = int
#Units
class Militia(Unit):
    def __init__(self):
        self.name = "Militia"
        self.health = 70
        self.ogHealth = self.health
        self.atk = 5
        self.cost = 5000
        self.speed = 2
        self.manpower = 5_000

class Line_Infantry(Unit):
    def __init__(self):
        self.name = "Line Infantry"
        self.health = 100
        self.ogHealth = self.health
        self.atk = 7
        self.cost = 8000
        self.speed = 2
        self.manpower = 5_000

class Cavalry(Unit):
    def __init__(self):
        self.name = "Cavalry"
        self.health = 180
        self.ogHealth = self.health
        self.atk = 15
        self.cost = 20000
        self.speed = 4
        self.manpower = 2_500

class Dragoons(Unit):
    def __init__(self):
        self.name = "Dragoons"
        self.health = 250
        self.ogHealth = self.health
        self.atk = 20
        self.cost = 25000
        self.speed = 4
        self.manpower = 3_000

class Artillery(Unit):
    def __init__(self):
        self.name = "Artillery"
        self.health = 180
        self.atk = 10
        self.cost = 30000
        self.speed = 1
        self.ogHealth = self.health
        self.manpower = 1_000


class General:
    in_use = False
    def __init__(self, name, skill, charisma, image):
        self.name = name
        self.skill = skill
        self.charisma = charisma
        self.image = image

class Army:
    retreat_margin = 0.3
    morale = 1.0
    clicked = False
    moved = False
    current_zone = None
    def __init__(self, name, units, general, retreat_margin):
        self.name = name
        self.units = units
        self.general = general
        self.retreat_margin = retreat_margin

    def select(self):
        self.clicked = True

    def deselect(self):
        self.clicked = False
    def retreat(self, prov, nation):
        hasNeighbor = False
        if(len(self.units) > 0):
            for neighbor in prov.border_states:
                if(neighbor in nation.provinces):
                    hasNeighbor = True
                    prov.armies.remove(self)
                    neighbor.armies.append(self)
                    break
            if(not hasNeighbor):
                prov.armies.remove(self)
        else:
            prov.armies.remove(self)


    def take(self, attackingProv, defendingProv, attackingNation, defendingNation):
        if(len(self.units) > 0):
            attackingNation.provinces.append(defendingProv)
            defendingNation.provinces.remove(defendingProv)
            attackingProv.armies.remove(self)
            defendingProv.armies.append(self)
            attackingNation.score += defendingProv.warscore
            defendingNation.score -= defendingProv.warscore
            attackingNation.morale += defendingProv.warscore
            defendingNation.morale -= defendingProv.warscore

    def move(self, prov1, prov2):
        try:
            prov1.armies.remove(self)
            prov2.armies.append(self)
            current_zone = prov2
        except:
            pass

    def move_to_sea(self, sea_zone):
        try:
            current_prov = self.get_current_province()
            current_prov.armies.remove(self)
            sea_zone.armies.append(self)
            self.current_zone = sea_zone
        except Exception as e:
            pass

    def move_to_land(self, land_prov, sea_zone):
        try:
            sea_zone.armies.remove(self)
            land_prov.armies.append(self)
            self.current_zone = land_prov
        except Exception as e:
            pass
    def get_current_province(self):
        return self.current_zone

    def attack(self, other, attackingProv, defendingProv, attackingNation, defendingNation):
        isSurrounded = True
        for neighbor in defendingProv.border_states:
            if(neighbor in defendingNation.provinces):
                isSurrounded= False

        initSize = len(self.units)
        otherInitSize = len(other.units)
        if(otherInitSize!= 0 and initSize != 0):
            while len(self.units) / initSize >= self.retreat_margin and len(other.units) / otherInitSize >= other.retreat_margin:
                for attacker in self.units[:]:
                    if attacker.getName() == "Artillery":
                        for target in other.units:
                            skill_buff = (self.general.skill / 50) if self.general else 1
                            charisma_buff = (self.general.charisma / 50) if self.general else 1



                            damage = attacker.getAtk() * (attacker.getHealth() / attacker.getOgHealth()) * self.morale \
                                     * random.uniform(0.5, 1.5 * skill_buff) \
                                     * random.uniform(0.8, 1 * charisma_buff)


                            if random.uniform(0, 1) > 0.95:
                                if defendingProv.fort_level > 1:
                                    defendingProv.fort_level -= 1

                            target.setHealth((target.getHealth() - (damage * (3 if isSurrounded else 1) / defendingProv.fort_level)))
                        other.units = [unit for unit in other.units if unit.getHealth() > 0]

                    else:
                        if other.units:
                            index = random.randint(0, len(other.units) - 1)
                            target = other.units[index]

                            skill_buff = (self.general.skill / 50) if self.general else 1
                            charisma_buff = (self.general.charisma / 50) if self.general else 1

                            damage = attacker.getAtk() * (attacker.getHealth() / attacker.getOgHealth()) * self.morale \
                                     * random.uniform(0.5, 1.5 * skill_buff) \
                                     * random.uniform(0.8, 1 * charisma_buff)

                            target.setHealth((target.getHealth() - (damage * (3 if isSurrounded else 1) / defendingProv.fort_level)))


                        other.units = [unit for unit in other.units if unit.getHealth() > 0]

                for defender in other.units[:]:
                    if defender.getName() == "Artillery":
                        for target in self.units:
                            skill_buff = (other.general.skill / 50) if other.general else 1
                            charisma_buff = (other.general.charisma / 50) if other.general else 1

                            damage = defender.getAtk() * (defender.getHealth() / defender.getOgHealth()) * other.morale \
                                     * random.uniform(0.5, 1.5 * skill_buff) \
                                     * random.uniform(0.8, 1 * charisma_buff)

                            target.setHealth((target.getHealth() - damage))
                            self.units = [unit for unit in self.units if unit.getHealth() > 0]
                    else:
                        if self.units:
                            index = random.randint(0, len(self.units) - 1)
                            target = self.units[index]

                            skill_buff = (other.general.skill / 50) if other.general else 1
                            charisma_buff = (other.general.charisma / 50) if other.general else 1

                            damage = defender.getAtk() * (defender.getHealth() / defender.getOgHealth()) * other.morale \
                                     * random.uniform(0.5, 1.5 * skill_buff) \
                                     * random.uniform(0.8, 1 * charisma_buff)

                            target.setHealth((target.getHealth() - damage))

                            self.units = [unit for unit in self.units if unit.getHealth() > 0]
            other.units = [unit for unit in other.units if unit.getHealth() > 0]
            if (len(self.units) / initSize <= self.retreat_margin):
                    if (self.morale - 0.2 >= 0):
                        self.morale -= 0.2
                    other.morale += 0.2
            if(len(other.units)/initSize <= other.retreat_margin):
                    other.retreat(defendingProv, defendingNation)
                    attackingNation.provinces.append(defendingProv)
                    defendingNation.provinces.remove(defendingProv)
                    attackingNation.morale -= defendingProv.warscore
                    defendingNation.morale += defendingProv.warscore
                    defendingProv.armies.append(self)
                    attackingProv.armies.remove(self)
                    if(other.morale - 0.2 >= 0):
                        other.morale -= 0.2
                    self.morale += 0.2
                    attackingNation.score += defendingProv.warscore
                    defendingNation.score -= defendingProv.warscore
                    attackingNation.morale += defendingProv.warscore
                    defendingNation.morale -= defendingProv.warscore
                    defendingProv.support -= random.randint(0, 50)


#############
#generals
George = General("George B. McClellan", skill=60, charisma=85, image = pg.image.load("assets/George B. McClellan.jpg"))
George.in_use = True
Union_Generals = [
    General("Ulysses S. Grant", skill=95, charisma=80, image = pg.image.load("assets/Ulysses S. Grant.webp")),
    General("William Tecumseh Sherman", skill=90, charisma=75, image = pg.image.load("assets/William Tecumseh Sherman.jpg")),
    George
]


Beauregard = General("P.G.T. Beauregard", skill=75, charisma=65, image = pg.image.load("assets/P.G.T. Beauregard.jpg"))
Beauregard.in_use = True
Confederate_Generals = [
    General("Robert E. Lee", skill=95, charisma=90, image = pg.image.load("assets/Robert E. Lee.webp")),
    General("Thomas 'Stonewall' Jackson", skill=90, charisma=80, image = pg.image.load("assets/Thomas 'Stonewall' Jackson.jpg")),
    Beauregard
]



Army_Of_The_Potomac = Army(
    name = "Army Of The Potomac",
    units=[
        Line_Infantry(), Line_Infantry(), Line_Infantry(),
        Militia(), Artillery(), Cavalry(), Dragoons()
    ],
    general=Union_Generals[2],
    retreat_margin=0.25
)

Army_Of_Northern_Virginia = Army(
    name="Army Of Northern Virginia",
    units=[
        Line_Infantry(), Line_Infantry(), Militia(),
        Militia(), Cavalry(), Artillery()
    ],
    general=Confederate_Generals[2],
    retreat_margin=0.2
)


Union_Armies = [Army_Of_The_Potomac]
Confederate_Armies = [Army_Of_Northern_Virginia]



#union territories

Maine = Province("Maine", 2, 1, 0, [], 0, 80, 1, False, [1102, 119])
New_Hampshire = Province("New Hampshire", 3, 1, 0, [], 0, 85, 1, False, [1020, 191])
Vermont = Province("Vermont", 1, 0, 0, [], 0, 90, 1, False, [1003, 156])
Massachusetts = Province("Massachusetts", 3, 5, 3, [], 1, 95, 1, False, [989, 221])
Rhode_Island = Province("Rhode Island", 1, 1, 1, [], 0, 90, 1, False, [1006, 244])
Connecticut = Province("Connecticut", 1, 2, 2, [], 1, 88, 1, False, [973, 244])
Albany = Province("Albany", 4, 3, 2, [], 1, 75, 1, False, [949, 180])
New_Jersey = Province("New Jersey", 3, 4, 3, [], 1, 80, 1, False, [917, 276])
Philadelphia = Province("Philadelphia", 7, 8, 5, [], 2, 100, 2, False, [880, 267])
District_Of_Columbia = Province("District of Columbia", 9, 4, 3, [Army_Of_The_Potomac], 3, 100, 3, True, [844, 312])
Delmarva = Province("Delmarva", 4, 4, 3, [], 2, 40, 2, True, [873, 332])
Pittsburgh = Province("Pittsburgh", 3, 4, 3, [], 1, 70, 1, False, [802, 267])
Rochester = Province("Rochester", 1, 2, 1, [], 1, 60, 1, False, [873, 210])
Cleveland = Province("Cleveland", 3, 4, 3, [], 1, 75, 1, False, [739, 271])
Cincinnati = Province("Cincinnati", 3, 4, 3, [], 1, 50, 1, False, [680, 300])
Louisville = Province("Louisville", 2, 3, 2, [], 1, 30, 1, True, [580, 380])
Lexington = Province("Lexington", 2, 3, 2, [], 1, 20, 1, True, [658, 358])
Indianapolis = Province("Indianapolis", 2, 4, 3, [], 1, 70, 1, False, [603, 321])
Ft_Wayne = Province("Ft Wayne", 2, 3, 2, [], 1, 65, 1, False, [631, 265])
Saint_Louis = Province("Saint Louis", 4, 5, 3, [], 1, 45, 1, True, [479, 367])
Kansas = Province("Kansas", 3, 4, 2, [], 1, 40, 1, True, [279, 343])
Wisconsin = Province("Wisconsin", 4, 5, 3, [], 1, 75, 1, False, [579, 138])
Iowa = Province("Iowa", 2, 3, 2, [], 1, 65, 1, False, [452, 228])
Michigan = Province("Michigan", 5, 6, 4, [], 2, 85, 1, False, [700, 189])
Colorado_Territory = Province("Colorado Territory", 1, 3, 2, [], 1, 60, 1, False, [111, 328])
Nebraska_Territory = Province("Nebraska Territory", 2, 3, 2, [], 1, 55, 1, False, [297, 247])
Dakota_Territory = Province("Dakota Territory", 1, 2, 1, [], 1, 50, 1, False, [249, 106])
New_York_City = Province("New York City", 15, 10, 6, [], 3, 90, 2, False, [936, 240])
Minnesota = Province("Minnesota", 2, 3, 2, [], 1, 80, 1, False, [485, 107])
Illinois = Province("Illinois", 4, 3, 2, [], 1, 80, 1, False, [539, 298])
Springfield = Province("Springfield", 2, 3, 2, [], 1, 80, 1, True, [415, 358])


#confederate territories

Charleston = Province("Charleston", 4, 3, 3, [], 1, 90, 2, True, [724, 496])
West_Virginia = Province("West Virginia", 2, 3, 2, [Army_Of_Northern_Virginia], 1, -15, 1, True, [727, 347])
Richmond = Province("Richmond", 15, 5, 6, [], 3, 90, 3, True, [812, 390])
Roanoke = Province("Roanoke", 3, 4, 3, [], 1, 85, 1, True, [754, 386])
Harrisonburg = Province("Harrisonburg", 2, 3, 2, [], 1, 50, 1, True, [803, 348])
Charlotte = Province("Charlotte", 6, 5, 3, [], 1, 88, 1, True, [716, 430])
Raleigh = Province("Raleigh", 3, 4, 3, [], 1, 85, 1, True, [787, 429])
Columbia = Province("Columbia", 3, 2, 3, [], 1, 85, 1, True, [682, 473])
Atlanta = Province("Atlanta", 3, 4, 4, [], 2, 92, 2, True, [608, 484])
Savannah = Province("Savannah", 3, 3, 3, [], 1, 88, 1, True, [640, 547])
Jacksonville = Province("Jacksonville", 4, 5, 3, [], 1, 70, 1, True, [634, 616])
Tampa = Province("Tampa", 3, 2, 3, [], 1, 75, 1, True, [645, 696])
Nashville = Province("Nashville", 5, 2, 4, [], 2, 40, 1, True, [532, 427])
Knoxville = Province("Knoxville", 3, 4, 3, [], 1, 35, 1, True, [616, 419])
Birmingham = Province("Birmingham", 3, 4, 3, [], 1, 60, 1, True, [546, 482])
Montgomery = Province("Montgomery", 3, 4, 3, [], 1, 55, 1, True, [517, 544])
Jackson = Province("Jackson", 3, 2, 3, [], 1, 45, 1, True, [461, 549])
Vicksburg = Province("Vicksburg", 2, 3, 2, [], 1, 40, 1, True, [473, 479])
Little_Rock = Province("Little Rock", 4, 2, 3, [], 1, 75, 1, True, [422, 462])
Fort_Smith = Province("Fort Smith", 3, 4, 3, [], 1, 65, 2, True, [379, 438])
Shreveport = Province("Shreveport", 3, 4, 3, [], 1, 70, 1, True, [369, 538])
New_Orleans = Province("New Orleans", 14, 9, 6, [], 3, 95, 2, True, [397, 594])
Indian_Territory = Province("Indian Territory", 2, 1, 2, [], 1, -10, 1, True, [278, 428])
New_Mexico_Territory = Province("New Mexico Territory", 2, 1, 2, [], 1, -5, 1, False, [63, 456])
Dallas = Province("Dallas", 5, 6, 4, [], 2, 80, 1, True, [292, 517])
Austin = Province("Austin", 4, 5, 3, [], 1, 85, 1, True, [211, 566])
Houston = Province("Houston", 6, 2, 4, [], 2, 90, 1, True, [211, 637])
El_Paso = Province("El Paso", 2, 1, 2, [], 1, 50, 1, True, [148, 514])



Army_Of_The_Potomac.current_zone = District_Of_Columbia
Army_Of_Northern_Virginia = West_Virginia

Maine.border_states = [New_Hampshire]
New_Hampshire.border_states = [Maine, Vermont, Massachusetts]
Vermont.border_states = [New_Hampshire, Massachusetts, Albany]
Albany.border_states = [Vermont, Massachusetts, New_York_City, Rochester]
Massachusetts.border_states = [New_Hampshire, Vermont, Albany, New_York_City, Connecticut, Rhode_Island]
Rhode_Island.border_states = [Massachusetts, Connecticut]
Connecticut.border_states = [Rhode_Island, New_York_City, Massachusetts]
New_York_City.border_states = [Albany, Rochester, Philadelphia, New_Jersey, Connecticut, Massachusetts]
Rochester.border_states = [Pittsburgh, Philadelphia, New_York_City, Albany]
New_Jersey.border_states = [New_York_City, Philadelphia, Delmarva]
Philadelphia.border_states = [Pittsburgh, Rochester, New_York_City, New_Jersey, Delmarva, District_Of_Columbia]
Pittsburgh.border_states = [Rochester, Philadelphia, District_Of_Columbia, West_Virginia, Cleveland]
District_Of_Columbia.border_states = [Delmarva, Philadelphia, Pittsburgh, West_Virginia, Harrisonburg]
Michigan.border_states = [Wisconsin, Ft_Wayne, Cincinnati]
Wisconsin.border_states = [Michigan, Illinois, Iowa, Minnesota]
Minnesota.border_states = [Wisconsin, Iowa, Nebraska_Territory, Dakota_Territory]
Dakota_Territory.border_states = [Minnesota, Iowa, Nebraska_Territory, Colorado_Territory]
Colorado_Territory.border_states = [New_Mexico_Territory, Indian_Territory, Dakota_Territory, Nebraska_Territory, Kansas]
Nebraska_Territory.border_states = [Colorado_Territory, Dakota_Territory, Kansas, Iowa, Springfield]
Kansas.border_states = [Colorado_Territory, Indian_Territory, Nebraska_Territory, Springfield]
Iowa.border_states = [Minnesota, Dakota_Territory, Nebraska_Territory, Springfield, Saint_Louis, Illinois,Wisconsin]
Springfield.border_states = [Fort_Smith, Little_Rock, Indian_Territory, Saint_Louis, Iowa, Nebraska_Territory, Kansas]
Saint_Louis.border_states = [Little_Rock, Springfield, Iowa, Illinois, Louisville, Nashville]
Illinois.border_states = [Wisconsin, Iowa, Saint_Louis, Louisville, Indianapolis, Ft_Wayne]
Louisville.border_states = [Saint_Louis, Nashville, Knoxville, Roanoke, Lexington, Indianapolis, Illinois]
Lexington.border_states = [Roanoke, West_Virginia, Cincinnati, Indianapolis, Louisville]
Indianapolis.border_states = [Illinois, Louisville, Lexington, Cincinnati, Ft_Wayne]
Ft_Wayne.border_states = [Indianapolis, Cincinnati, Illinois, Michigan]
Cincinnati.border_states = [Michigan, Indianapolis, Ft_Wayne, Lexington, West_Virginia, Cleveland]
Cleveland.border_states = [Cincinnati, West_Virginia, Pittsburgh]

New_Mexico_Territory.border_states = [Colorado_Territory, El_Paso, Indian_Territory]
El_Paso.border_states = [Colorado_Territory, Indian_Territory, Dallas, Austin, Houston]
Houston.border_states = [Austin, Dallas, El_Paso, New_Orleans, Shreveport]
Austin.border_states = [El_Paso, Houston, Dallas]
Dallas.border_states = [Austin, Houston, El_Paso, Shreveport, Fort_Smith, Indian_Territory]
Indian_Territory.border_states = [Kansas, Colorado_Territory, New_Mexico_Territory, Dallas, El_Paso, Shreveport, Springfield]
New_Orleans.border_states= [Houston, Shreveport, Jackson]
Shreveport.border_states = [Dallas, Houston, New_Orleans, Jackson, Vicksburg, Fort_Smith, Little_Rock]
Fort_Smith.border_states = [Indian_Territory, Dallas, Shreveport, Little_Rock, Springfield, Kansas]
Little_Rock.border_states = [Saint_Louis, Springfield, Fort_Smith, Shreveport, Vicksburg, Nashville]
Jackson.border_states = [New_Orleans, Shreveport, Vicksburg, Montgomery]
Vicksburg.border_states = [Nashville, Little_Rock, Shreveport, Jackson, Montgomery, Birmingham]
Nashville.border_states = [Louisville, Saint_Louis, Little_Rock, Vicksburg, Birmingham, Knoxville]
Montgomery.border_states = [Birmingham, Vicksburg, Jackson, Savannah, Jacksonville]
Jacksonville.border_states = [Tampa, Savannah, Montgomery]
Tampa.border_states = [Jacksonville]
Savannah.border_states = [Jacksonville, Montgomery, Birmingham, Atlanta, Columbia, Charleston]
Birmingham.border_states = [Nashville, Vicksburg, Montgomery, Savannah, Atlanta, Knoxville]
Knoxville.border_states = [Nashville, Louisville, Lexington, Roanoke, Charlotte, Atlanta, Birmingham]
Atlanta.border_states = [Knoxville, Birmingham, Savannah, Columbia, Charlotte]
Charleston.border_states = [Columbia, Savannah, Raleigh]
Columbia.border_states = [Charlotte, Atlanta, Savannah, Charleston, Raleigh]
Charlotte.border_states =[Roanoke, Knoxville, Atlanta, Columbia, Raleigh]
Raleigh.border_states = [Richmond, Roanoke, Charlotte, Columbia, Charleston]
Richmond.border_states = [Harrisonburg, Roanoke, Raleigh]
Roanoke.border_states = [Richmond, Harrisonburg, West_Virginia, Lexington, Knoxville, Charlotte, Raleigh]
Harrisonburg.border_states = [District_Of_Columbia, West_Virginia, Roanoke, Richmond]
West_Virginia.border_states = [Cleveland, Cincinnati, Lexington, Roanoke, Harrisonburg, District_Of_Columbia, Pittsburgh]





North_Atlantic = SeaProvince("North Atlantic", [], (1057, 358))
South_Atlantic = SeaProvince("South Atlantic", [], (772, 668))
Gulf_Of_Mexico = SeaProvince("Gulf Of Mexico", [], (426, 691))


Gulf_Of_Mexico.landNeighbors = [New_Orleans]

North_Atlantic.border_states = [South_Atlantic, New_York_City, Massachusetts, Delmarva]
South_Atlantic.border_states = [Gulf_Of_Mexico, North_Atlantic, Charleston]
Gulf_Of_Mexico.border_states = [South_Atlantic, New_Orleans]

New_York_City.border_states.append(North_Atlantic)
Massachusetts.border_states.append(North_Atlantic)
Delmarva.border_states.append(North_Atlantic)
Charleston.border_states.append(South_Atlantic)
New_Orleans.border_states.append(Gulf_Of_Mexico)

Union_Provinces = [
    Maine, New_Hampshire, Vermont, Massachusetts, Rhode_Island,
    Connecticut, Albany, New_Jersey, Philadelphia, District_Of_Columbia,
    Delmarva, Pittsburgh, Rochester, Cleveland, Cincinnati,
    Louisville, Lexington, Indianapolis, Ft_Wayne, Saint_Louis,
    Kansas, Wisconsin, Iowa, Michigan, Colorado_Territory,
    Nebraska_Territory, Dakota_Territory, New_York_City, Minnesota, Illinois, Springfield, North_Atlantic
]

Confederate_Provinces = [
    Charleston, West_Virginia, Richmond, Roanoke, Harrisonburg,
    Charlotte, Raleigh, Columbia, Atlanta,
    Savannah, Jacksonville, Tampa, Nashville, Knoxville,
    Birmingham, Montgomery, Jackson, Vicksburg, Little_Rock,
    Fort_Smith, Shreveport, New_Orleans, Indian_Territory,
    New_Mexico_Territory, Dallas, Austin, Houston, El_Paso, Gulf_Of_Mexico, South_Atlantic
]

Union = Nation(
    name="United States of America",
    provinces=Union_Provinces,
    score=0,
    money=0,
    manpower=75_000,
    morale=60,
    uk_opinion=-10,
    fr_opinion=10,
    rs_opinion=60,
    focuses=[

    ]
)

Confederacy = Nation(
    name="Confederate States of America",
    provinces=Confederate_Provinces,
    score=0,
    money=0,
    manpower=80_000,
    morale=80,
    uk_opinion=40,
    fr_opinion=25,
    rs_opinion=-40,
    focuses=[
    ]
)


Turn = 1
Year = 1861
Month = 5