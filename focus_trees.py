import random
import pygame as pg
from classes import *


class Focus:
    def __init__(self, name, country):
        self.name = name
        self.country = country

#Union focuses
class The_Anaconda_Plan(Focus):
    def __init__(self):
        self.name = "The Anaconda Plan"
        self.desc = "To defeat the Confederacy, we must strangle them from all fronts, land and sea."
        self.requirements_desc = "Control either Boston or New York, and have at least 10 units in the seas."
        self.country = Union

    def requirements(self):
        has_new_york_or_boston = False
        for province in self.country.provinces:
            if province.name == "New York" or province.name == "Boston":
                has_new_york_or_boston = True
        ship_units = 10
        for prov in self.country.provinces:
            if(prov.name == "North Atlantic" or prov.name == "South Atlantic" or prov.name == "Gulf of Mexico"):
                for army in prov.armies:
                    for unit in army.units:
                        if(unit != None):
                            ship_units+=1
        return (ship_units >= 10 and has_new_york_or_boston)


    def effect(self):
        self.country.economic_buff *= 1.5
        Confederacy.economic_buff *= 0.75
        self.country.score += 5
        Confederacy.score -= 5
        self.country.completed_focuses.append(self)

class Blockade_The_South(Focus):
    def __init__(self):
        self.name = "Blockade The South"
        self.desc = "By cutting the highly dependent South off from trade with Europe, we will effectively drain their ability to fight."
        self.requirements_desc = "Control the entire Eastern Seaboard."
        self.country = Union

    def requirements(self):
        controls_North = False
        controls_South = False
        for prov in self.country.provinces:
            if(prov.name == "North Atlantic"):
                controls_North = True
            elif(prov.name == "South"):
                controls_South = True
        return controls_South and controls_North

    def effect(self):
        self.country.economic_buff *= 1.2
        Confederacy.economic_buff *= 0.5
        self.country.fr_opinion -= 20
        self.country.uk_opinion -= 20
        self.country.score += 10
        self.country.morale += 10
        Confederacy.score -= 15
        Confederacy.morale -= 20

        self.country.completed_focuses.append(self)



class Control_The_Mississippi(Focus):
    def __init__(self):
        self.name = "Control the Mississippi"
        self.desc = "Control of the Mississippi will split the Confederacy in two and grant us control over vital transport routes."
        self.requirements_desc = "Must have completed 'The Anaconda Plan'. Control both Vicksburg and New Orleans."
        self.country = Union

    def requirements(self):
        has_anaconda_plan = self.country.has_focus("The Anaconda Plan")
        has_Vick = False
        has_NewOr = False
        for province in self.country.provinces:
            if province.name == "Vicksburg":
                has_Vick = True
            elif province.name == "New Orleans":
                has_NewOr = True
        return has_anaconda_plan and has_Vick and has_NewOr

    def effect(self):
        self.country.supply_efficiency += 0.25
        Confederacy.supply_efficiency -= 0.25
        self.country.economic_buff += 0.1
        self.country.score += 15
        self.country.morale += 15
        Confederacy.score -= 15
        Confederacy.morale -= 10

        self.country.completed_focuses.append(self)


class The_War_In_The_West(Focus):
    def __init__(self):
        self.name = "The War in the West"
        self.desc = "Push through Tennessee and the Mississippi Valley to undermine Confederate supply lines."
        self.requirements_desc = "Control Memphis and Nashville."
        self.country = Union

    def requirements(self):
        has_memphis = False
        has_nashville = False
        for province in self.country.provinces:
            if province.name == "Memphis":
                has_memphis = True
            elif province.name == "Nashville":
                has_nashville = True

        return has_memphis and has_nashville

    def effect(self):
        self.country.score += 10
        Confederacy.score -= 10
        self.country.morale += 10
        Confederacy.morale -= 10
        self.country.completed_focuses.append(self)



class Shermans_March(Focus):
    def __init__(self):
        self.name = "Sherman's March to the Sea"
        self.desc = "Wreak havoc across Georgia to break Southern morale and destroy their ability to fight in this war."
        self.requirements_desc = "Must have completed 'The War in the West'. Control Atlanta."
        self.country = Union

    def requirements(self):
        has_west = self.country.has_focus("The War in the West")
        has_atlanta = False
        for province in self.country.provinces:
            if province.name == "Atlanta":
                has_atlanta = True
        return has_west and has_atlanta

    def effect(self):
        self.country.score += 10
        Confederacy.score -= 10
        self.country.morale += 20
        Confederacy.morale -= 20
        Confederacy.manpower /= 2
        Confederacy.money /= 2
        self.country.completed_focuses.append(self)



class Grants_Campaign(Focus):
    def __init__(self):
        self.name = "Grant's Virginia Campaign"
        self.desc = "General Grant pushes deep into Confederate territory, aiming to seize Richmond and end the war."
        self.requirements_desc = "Control Washington D.C. and Richmond."
        self.country = Union

    def requirements(self):
        owns_dc = False
        owns_rc = False
        for province in self.country.provinces:
            if province.name == "District of Columbia":
                owns_dc = True
            elif province.name == "Richmond":
                owns_rc = True
        return owns_dc and owns_rc

    def effect(self):
        self.country.morale += 30
        Confederacy.morale -= 50
        self.country.score += 25
        Confederacy.score -= 25
        self.country.completed_focuses.append(self)


class Emancipation_Proclamation(Focus):
        def __init__(self):
            self.name = "Emancipation Proclamation"
            self.country = Union
            self.desc = "The time has come to take our stance on the true root cause of this war: Slavery. Will you be bold, and risk the fragility of the Union for Emancipation?"
            self.requirements_desc = "The year must be at least 1863."

        def requirements(self):
            if Year >= 1863:
                return True
            else:
                return False

        def effect(self):
                self.country.fr_opinion += 20
                self.country.uk_opinion += 20
                self.country.morale += 20
                for prov in self.country.provinces:
                    if (prov.slaveholding == True):
                        prov.support -= 15
                    else:
                        prov.support += 10
                self.country.completed_focuses.append(self)


class Abolish_Slavery(Focus):
    def __init__(self):
        self.name = "Abolish Slavery"
        self.desc = "Its time to strike this war at its moral heart: the institution of slavery. This country must enshrine the abolition of slavery into the Constitution itself, ending this vile practice and ensuring true freedom for all."
        self.requirements_desc = "Emancipation Proclamation must be issued."
        self.country = Union

    def requirements(self):
        if self.country.emancipation_proclamation == True:
            return True
        else:
            return False


    def effect(self):
        self.country.fr_opinion += 20
        self.country.uk_opinion += 20
        self.country.morale += 10
        for prov in self.country.provinces:
            if(prov.slaveholding == True):
                prov.support -= 20
                prov.slaveholding = False
            else:
                prov.support += 10
        self.country.completed_focuses.append(self)


#confederate  focuses


class King_Cotton_Diplomacy(Focus):
    def __init__(self):
        self.name = "King Cotton Diplomacy"
        self.desc = "The Europeans are highly dependent on our cotton for their economy. Perhaps we could use this to exploit their opinion to our advantage..."
        self.requirements_desc = "Spend 300_000 in exporting cotton to sway France and Britain to your favor."
        self.country = Confederacy

    def requirements(self):
        return self.country.money >= 300_000

    def effect(self):
        self.country.fr_opinion += 20
        self.country.uk_opinion += 20
        Union.fr_opinion -= 20
        Union.uk_opinion -= 20
        self.country.morale += 10
        self.country.money -= 300_000
        self.country.economic_buff *= 1.2
        self.country.score += 5
        Union.score -= 5
        self.country.completed_focuses.append(self)




class Seek_Recognition(Focus):
    def __init__(self):
        self.name = "Seek Recognition"
        self.desc = "To retain our legitimacy as an independent nation, we must be recognized internationally. Britian and France are our best chance for now, due to their dependence on our Cotton industry."
        self.requirements_desc = "French or British opinion must be above 70. Must have completed 'King Cotton Diplomacy'."
        self.country = Confederacy

    def requirements(self):
        return (self.country.fr_opinion > 70 or self.country.uk_opinion > 70) and self.country.has_focus(King_Cotton_Diplomacy)


    def effect(self):
        self.country.fr_opinion += 10
        self.country.uk_opinion += 10
        self.country.morale += 20
        self.country.money *= 1.5
        self.country.economic_buff *= 1.5
        self.country.score += 10
        Union.score -= 10

        self.country.completed_focuses.append(self)



class Lees_Northern_Offensive(Focus):
    def __init__(self):
        self.name = "Lee's Northern Offensive"
        self.desc = "The North has the ability to sustain a far longer war than us. To end this war quickly in a favorable position for us, we must deal a crushing blow to them, and fast."
        self.requirements_desc = "Capture either Washington D.C or Philadelphia."
        self.country = Confederacy

    def requirements(self):
        owns_dc = False
        owns_ph = False
        for province in self.country.provinces:
            if province.name == "District of Columbia":
                owns_dc = True
            elif province.name == "Philadelphia":
                owns_ph = True
        return owns_dc and owns_ph


    def effect(self):
        self.country.fr_opinion += 10
        self.country.uk_opinion += 10
        self.country.morale += 30
        Union.economic_buff *= 0.75
        self.country.score += 20
        Union.score -= 20

        self.country.completed_focuses.append(self)


class Protect_The_Mississippi(Focus):
    def __init__(self):
        self.name = "Protect the Mississippi"
        self.desc = "We must defend the Mississipi, to protect our trade interests and prevent the enemy from cutting us in half."
        self.requirements_desc = "Keep New Orleans and Vicksburg in your control by the beginning of 1863."
        self.country = Confederacy

    def requirements(self):

        owns_no = False
        owns_vc = False
        for province in self.country.provinces:
            if province.name == "New Orleans":
                owns_no = True
            elif province.name == "Vicksburg":
                owns_vc = True
        return owns_no and owns_vc and (Year == 1863)


    def effect(self):
        self.country.fr_opinion += 10
        self.country.uk_opinion += 10
        self.country.morale += 20
        self.country.economic_buff *= 1.5
        self.country.score += 10
        Union.score -= 10

        self.country.completed_focuses.append(self)



class Sway_The_Copperheads(Focus):
    def __init__(self):
        self.name = "Sway the Copperheads"
        self.desc = "If we sway the more peace-insistent party of the Northern Democrats (Copperheads) to oppose the war, we may be able to weaken the unity of our foes."
        self.requirements_desc = "Union morale must be below 50, Confederate war score must be at least 60."
        self.country = Confederacy

    def requirements(self):
        return self.country.score >= 60 and Union.morale < 50

    def effect(self):
        self.country.morale += 20
        Union.morale -= 30
        self.country.score += 5
        Union.score -= 5

        self.country.completed_focuses.append(self)


class Western_Front(Focus):
    def __init__(self):
        self.name = "Western Front"
        self.desc = "To truly secure our territories, we must make an offensive on the Western front and secure the border states that support slavery."
        self.requirements_desc = "Capture Louisville and Lexington."
        self.country = Confederacy

    def requirements(self):
        return (Louisville in self.country.provinces and Lexington in self.country.provinces)

    def effect(self):
        self.country.morale += 10
        Union.morale -= 10
        self.country.score += 10
        Union.score -= 10

        self.country.completed_focuses.append(self)


class Preemptive_Emancipation(Focus):
    def __init__(self):
        self.name = "Preemptive Emancipation"
        self.desc = "Facing mounting pressure, we could preempt Lincoln’s proclamation by offering limited emancipation, securing foreign support, more manpower, and undermining Northern moral claims."
        self.requirements_desc = "No requirements."
        self.country = Confederacy

    def requirements(self):
        return True

    def effect(self):
        self.country.morale -= 20
        for prov in self.country.provinces:
            prov.support -= 20
        self.country.fr_opinion += 30
        self.country.uk_opinion += 30
        self.country.manpower += 50_000
        self.country.completed_focuses.append(self)


#events

class Event:
    def __init__(self, name, country):
        self.name = name
        self.country = country

#Union events

class Gettysburg_Address(Event):
    def __init__(self):
        self.name = "The Gettysburg Address"
        self.country = Union
        self.desc = "In the aftermath of a major battle, President Lincoln delivers a rousing speech to honor the fallen and redefine the very moral intentions of the war itself. "

    def requirements(self):
        if Year == 1863 and Month == 11 and self.country.morale > 50:
            return True
        else:
            return False


    def effect(self):
        self.country.morale += 20
        for prov in self.country.provinces:
            prov.support += 10
        return " 'We here highly resolve that these dead shall not have died in vain...that government of the people, by the people, for the people, shall not perish from the earth.' Lincoln's speech invigorates the spirit of the Union and its desire to finish this war once and for all, not just for the Union, but also for the principles of freedom and equality that this nation was founded upon, which so many died for."



class Election_Of_1864(Event):
    def __init__(self):
        self.name = "The Election of 1864"
        self.country = Union
        self.desc = "The Election of 1864 will be a landmark point in determining the future of this war. Will Lincoln and the Republican Party remain in office and finish this war, or will the peace advocates led by George B. McLellan of the Northern Democrats prevail?"

    def requirements(self):
        if Year == 1864:
            return True
        else:
            return False


    def effect(self):
        if(self.country.morale <= 30) or random.randint(0,100) < 30:
            self.country.morale -= 30
            for prov in self.country.provinces:
                prov.support -= 20
            return "The Northern Democrats win! The support of both the government and people to continue this war has drastically declined."
        else:
            self.country.morale += 30
            for prov in self.country.provinces:
                prov.support += 20
            return "Lincoln prevails! This war for the moral good and existence of the Union as a whole will continue a while longer, with the support of the people."



#Generic events
class Draft_Riots(Event):
    def __init__(self, country):
        self.name = "Draft Riots of " + str(Year)
        self.country = country
        self.desc = "The populace is disappointed and resentful of the prolonged war, and the discontent has boiled over, leading to riots in major cities over the draft."

    def requirements(self):
        if self.country.morale < 60 and random.randint(0, 10) > 8:
            return True
        else:
            return False

    def effect(self):
        self.country.morale -= 10
        for prov in self.country.provinces:
            prov.support -= 5
        self.country.manpower *= 0.8
        return "Draft riots erupt in the North, causing a plummet in morale and enlistment."

class War_Weariness(Event):
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.desc = "The constant toll of war is wearing down the civilian population. Families grow tired of loss, rationing, and uncertainty."

    def requirements(self):
        return self.country.morale < 50 and Year >= 1863 and random.randint(0, 10) > 8

    def effect(self):
        self.country.morale = max(0, self.country.morale - 10)
        for prov in self.country.provinces:
            prov.support = max(0, prov.support - 5)
        return "War weariness grips the nation, shaking confidence in victory."


#Confederate events


class Nation_Collapses(Event):
    def __init__(self):
        self.name = "Nation Begins to Collapse"
        self.country = Confederacy
        self.desc = "As the Confederacy suffers defeat after defeat on military, diplomatic, and economic fronts, it finally begins to crumble even from within."

    def requirements(self):
        if self.country.morale < 30 and len(self.country.provinces) < 15 and self.country.score < 30:
            return True
        else:
            return False


    def effect(self):
            self.country.morale -= 20
            for prov in self.country.provinces:
                prov.support -= 10
            self.country.manpower /= 2
            return "As our nation faces defeat on all fronts, it even begins to crumble from within..."





