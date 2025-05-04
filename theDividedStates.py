import sys
import time
from collections import deque

import pygame as pg
import pygame.display

from classes import *
from focus_trees import *

#focuses added

Union.focuses = [
    The_Anaconda_Plan(),
    Blockade_The_South(),
    The_War_In_The_West(),
    Emancipation_Proclamation(),
    Control_The_Mississippi(),
    Grants_Campaign(),
    Shermans_March(),
    Abolish_Slavery()
]

Confederacy.focuses = [
    King_Cotton_Diplomacy(),
    Preemptive_Emancipation(),
    Lees_Northern_Offensive(),
    Seek_Recognition(),
    Protect_The_Mississippi(),
    Sway_The_Copperheads(),
    Western_Front()
]

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def game_runner():
    def do_flood_fill(surface, x, y, new_color):
        x, y = int(x), int(y)
        width, height = surface.get_size()
        target_color = surface.get_at((x, y))
        if target_color == new_color:
            return
        queue = deque()
        queue.append((x, y))
        counter = 0
        while queue:
            cx, cy = queue.popleft()
            if not (0 <= cx < width and 0 <= cy < height):
                continue
            current_color = surface.get_at((cx, cy))
            if current_color != target_color:
                continue
            surface.set_at((cx, cy), new_color)
            queue.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

    def do_flood_fill_gradient(surface, x, y, new_color):
        x, y = int(x), int(y)
        width, height = surface.get_size()
        target_color = surface.get_at((x, y))
        if target_color == new_color:
            return
        queue = deque()
        queue.append((x, y))
        counter = 0
        while queue:
            cx, cy = queue.popleft()
            if not (0 <= cx < width and 0 <= cy < height):
                continue
            current_color = surface.get_at((cx, cy))
            if current_color != target_color:
                continue
            if(counter % 10 == 0):
                surface.set_at((cx, cy), pg.color(min(255,new_color.r + 1), min(255,new_color.g + 1), min(255,new_color.b + 1)))
            queue.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
            counter += 1




    def UnionVictory():
        return Union.score >= 100

    def ConfederateVictory():
        return Confederacy.score >= 100

    width = 1500
    height = 800


    pg.init()

    pygame.mixer.init()
    song1 = "assets/Star_Spangled_Banner_minor_key_rx2.wav"
    song2 = "assets/Confederate States of America _1861-1865_ Patriotic song _Dixie_ - Duration_ 4_53_.mp3"
    song3 = "assets/battle_hymn_of_the_republic.mp3"


    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)

    pygame.mixer_music.load(random.choice([song1, song2, song3]))
    pygame.mixer_music.play()


    SCREEN = pg.display.set_mode((width, height))
    pg.display.set_caption("Menu")

    BG = pg.image.load("assets/lincolnBackground.jpg")
    BG = pygame.transform.scale(BG,(width, height))


    def get_font(size):
        return pygame.font.Font("assets/Trajan-Regular.ttf", size)

    def main_menu():
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(75).render("The Divided States", True, "Grey")
            MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height*(8/23)))

            MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(width/2, height*(1/2)),
                                 text_input="Multiplayer", font=get_font(25), base_color="Grey", hovering_color="White")
            SINGLEPLAYER_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(width/2, height*(2/3)),
                                    text_input="Singleplayer", font=get_font(25), base_color="Grey",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(width/2, height*(5/6)),
                                 text_input="QUIT", font=get_font(25), base_color="Grey", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            UnionFlag = pygame.transform.scale(pg.image.load("assets/unionFlagOfficial.png"), (191, 122))
            ConfederateFlag = pygame.transform.scale(pg.image.load("assets/confederateFlagOfficial.png"), (191, 122))

            for button in [MULTIPLAYER_BUTTON, SINGLEPLAYER_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        playWithAI()
                    if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        winner = play()
                        if winner == Union:
                            back = pygame.image.load("assets/UnionVictory.jpg")
                            back.set_alpha(50)
                            epi = ["At long last, after " + str(Year - 1861) + " grueling years of war and bloodshed, the war that would come to be known as the Civil War is over.",
                                   "In the end, the Union would prevail, its ideals of liberty and unity having triumphed...at great cost.",
                                   "To keep the vile institution of slavery, the Southern States seceded.",
                                   "Hundreds of thousands of lives have been lost, dozens of towns and cities burned, families torn apart.", "It seems as though the nation will never be the same again.",
                                   "And yet...The United States of America will push on, as it always has, and always will.",  "Reconstruction will be difficult, and the scars of war may never truly fade away.",
                                   "But we must yet march on. For the Union is more than a nation. It is an idea.",
                                   "An idea that there is a place where man is neither bound by the will of tyrants nor by his origin, a place where man's only master is himself.",
                                   "The idea that there is a place...",
                                   "with Freedom and Justice for all."]


                        else:
                            back = pygame.transform.scale(pg.image.load("assets/ConfederateVictory.jpg"), (width + 100, height + 100))
                            back.set_alpha(50)
                            epi = ["At long last, after " + str(
                                Year - 1861) + " grueling years of war and bloodshed, the war that would come to be known as the War of Southern Independence is over.",
                                   "In the end, the Confederacy would prevail, its soviergnty guaranteed in its crushing military defeats of the Union.",
                                   "To uphold its vision of states' rights   and form a more perfect confederacy of free states, the Confederate States seceded."
                                   "Hundreds of thousands of lives have been lost, dozens of towns and cities burned, families torn apart." , "It seems as though this continent will never be the same again.",
                                   "And yet...the Confederate States of America will push on, as it must.", "Reconstruction will be difficult, and the scars of war may never truly fade away.",
                                   "But we must yet march on. For the Confederacy is more than a nation. It is an idea.",
                                   "An idea that there is a place where man is neither bound by the will of tyrants nor by the oppressive hand of a central authority..",
                                   "The idea that there is a place...",
                                   "with Liberty and Opportunity for all."]
                        SCREEN.blit(pg.transform.scale(pg.image.load("assets/white.jpg"), (2000, 2000)), (0,0))
                        SCREEN.blit(back, (0,0))
                        pygame.display.update()
                        font = get_font(12)
                        x = 10
                        y = 10
                        for ep in epi:
                            epList = list(ep)
                            for character in epList:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                text = font.render(character, True, "Black")
                                SCREEN.blit(text, (x, y))
                                x += 10
                                pygame.display.update()
                                pygame.time.wait(50)
                            x = 10
                            y += 60

                        pygame.display.update()
                        pygame.time.wait(10000)


                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def draw_focuses(nat):
        BlueUI = pygame.transform.scale(pygame.image.load("assets/unionSteel.jpg"), (220, 50))
        GreyUI = pygame.transform.scale(pygame.image.load("assets/confederateSteel.jpg"), (220, 50))



        font = get_font(10)
        text_color = "#000000"
        box_width, box_height = 220, 50
        spacing = 30
        start_x = 320
        top_y = 100
        bottom_y = 200

        focuses = nat.focuses
        focus_texture = BlueUI if nat == Union else GreyUI

        titleColor = "Light Blue" if nat == Union else "Light Grey"

        font2= get_font(50)

        if(nat == Confederacy):
            titleCard = font2.render("Confederate Focuses", True, titleColor)
        else:
            titleCard = font2.render("Union Focuses", True, titleColor)

        SCREEN.blit(titleCard, (560, 20))

        if nat == Union:
            top_row = focuses[:4]
            bottom_row = focuses[4:]
            prerequisites = {
                "Control the Mississippi": "The Anaconda Plan",
                "Sherman's March to the Sea": "The War in the West",
                "Abolish Slavery": "Emancipation Proclamation"
            }
        else:
            top_row = focuses[:3]
            bottom_row = focuses[3:]
            prerequisites = {
                "Seek Recognition": "King Cotton Diplomacy"
            }

        focus_positions = {}

        for i, focus in enumerate(top_row):
            x = start_x + i * (box_width + spacing)
            y = top_y
            SCREEN.blit(focus_texture, (x, y))
            if nat.has_focus(focus):
                if (nat == Union):
                    border_color = "Dark Blue"
                else:
                    border_color = "Dark Grey"
            elif focus.requirements():
                border_color = "#00FF00"
            else:
                border_color = "Black"
            pygame.draw.rect(SCREEN, border_color, pygame.Rect(x, y, box_width, box_height), 5)
            text = font.render(focus.name, True, text_color)
            SCREEN.blit(text, (x + 10, y + 10))
            focus_positions[focus.name] = (x, y)

        for i, focus in enumerate(bottom_row):
            x = start_x + i * (box_width + spacing)
            y = bottom_y
            SCREEN.blit(focus_texture, (x, y))
            if nat.has_focus(focus):
                if (nat == Union):
                    border_color = "Dark Blue"
                else:
                    border_color = "Dark Grey"
            elif focus.requirements():
                border_color = "#00FF00"
            else:
                border_color = "Black"
            pygame.draw.rect(SCREEN, border_color, pygame.Rect(x, y, box_width, box_height), 5)
            text = font.render(focus.name, True, text_color)
            SCREEN.blit(text, (x + 10, y + 10))
            focus_positions[focus.name] = (x, y)

        for child, parent in prerequisites.items():
            if parent in focus_positions and child in focus_positions:
                start_x, start_y = focus_positions[parent]
                end_x, end_y = focus_positions[child]
                start_pos = (start_x + box_width // 2, start_y + box_height)
                end_pos = (end_x + box_width // 2, end_y)
                pygame.draw.line(SCREEN, "White", start_pos, end_pos, 3)
        return focus_positions

    def stats(nat):
        StatsBackground = pygame.transform.scale(pygame.image.load("assets/black.jpg"), (width, height))

        FrenchFlag = pygame.transform.scale(pygame.image.load("assets/frenchFlag.png"), (200, 100))
        BritishFlag = pygame.transform.scale(pygame.image.load("assets/britishFlag.png"), (200, 100))
        RussianFlag = pygame.transform.scale(pygame.image.load("assets/russiaFlag.png"), (200, 100))

        brownUI = pygame.transform.scale(pygame.image.load("assets/brownUI.jpg"), (300, 50))

        opinColor = (173, 216, 230) if nat == Union else (211, 211, 211)

        font2 = get_font(40)

        opinCard = font2.render("Diplomatic Relationships", True, opinColor)

        running = True
        font = get_font(18)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if 550 <= mx <= 850 and 460 <= my <= 510 and nat.uk_opinion > 20:
                        nat.money += 50000
                        nat.uk_opinion -= 20
                    elif 550 <= mx <= 850 and 570 <= my <= 620 and nat.fr_opinion > 20:
                        nat.money += 50000
                        nat.fr_opinion -= 20
                    elif 550 <= mx <= 850 and 680 <= my <= 730 and nat.rs_opinion > 20:
                        nat.money += 50000
                        nat.rs_opinion -= 20


            SCREEN.blit(StatsBackground, (0, 0))

            SCREEN.blit(BritishFlag, (50, 445))
            SCREEN.blit(FrenchFlag, (50, 555))
            SCREEN.blit(RussianFlag, (50, 665))

            SCREEN.blit(opinCard, (100, 350))

            uk_text = font.render(f"British Opinion: {nat.uk_opinion}", True, (255, 255, 255))
            fr_text = font.render(f"French Opinion: {nat.fr_opinion}", True, (255, 255, 255))
            rs_text = font.render(f"Russian Opinion: {nat.rs_opinion}", True, (255, 255, 255))

            SCREEN.blit(uk_text, (300, 480))
            SCREEN.blit(fr_text, (300, 590))
            SCREEN.blit(rs_text, (300, 700))

            text_loan = get_font(12).render("Ask for a loan (-20 opinion)", True, (255, 255, 255))

            SCREEN.blit(brownUI, (550, 460))
            SCREEN.blit(brownUI, (550, 570))
            SCREEN.blit(brownUI, (550, 680))

            SCREEN.blit(text_loan, (580, 480))
            SCREEN.blit(text_loan, (580, 590))
            SCREEN.blit(text_loan, (580, 700))

            focus_positions = draw_focuses(nat)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            box_width, box_height = 220, 50

            for focus in nat.focuses:
                if focus.name in focus_positions:
                    x, y = focus_positions[focus.name]
                    rect = pygame.Rect(x, y, box_width, box_height)
                    if rect.collidepoint(mouse):
                        text_desc = get_font(12).render(focus.desc, True, (255, 255, 255))
                        if(not nat.has_focus(focus)):
                            text_req = get_font(12).render("Requirements: " + focus.requirements_desc, True, "Red")
                        else:
                            text_req = get_font(12).render("Focus Completed!", True, "Green")
                        if(pg.mouse.get_pos()[0] <= width/2):
                            SCREEN.blit(text_desc, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] + 30))
                            SCREEN.blit(text_req, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] + 50))
                        else:
                            SCREEN.blit(text_desc, (pg.mouse.get_pos()[0] - width/2, pg.mouse.get_pos()[1] + 30))
                            SCREEN.blit(text_req, (pg.mouse.get_pos()[0] - width/2, pg.mouse.get_pos()[1] + 50))
                        if(click[0]):
                            if not nat.has_focus(focus) and focus.requirements():
                                focus.effect()

            text_esc = get_font(12).render("Press esc to leave", True, (255, 255, 255))
            SCREEN.blit(text_esc, (10, 10))

            pygame.display.update()

    def play():
        Turn = 1
        Year = 1861
        Month = 5


        zoom_factor = 1
        PlayerTurn = "Confederacy"


        clickedProvince = []
        clickedArmy = []



        # load assets
        pg.display.set_caption("The Divided States")
        Map = pg.image.load("assets/civilWarMap.png")
        Mask = pg.image.load("assets/civilWarMask.png")
        Terrain = pg.image.load("assets/theTerrain.jpg")
        Ocean = pg.image.load("assets/ocean.jpg")
        #
        Black = pygame.transform.scale(pg.image.load("assets/black.jpg"), (96, 30))
        White = pg.image.load("assets/white.jpg")

        FlagHolder = pygame.transform.scale(pg.image.load("assets/woodenBox.png"), (240, 155))
        Holder = pygame.transform.scale(pg.image.load("assets/woodenBox.png"), (120, 40))

        MoneyIcon = pygame.transform.scale(pg.image.load("assets/moneyIcon.png"), (30, 30))
        SoldierIcon = pygame.transform.scale(pg.image.load("assets/soldierIcon4.png"), (30, 30))
        MoraleIcon = pygame.transform.scale(pg.image.load("assets/morale.png"), (30, 30))

        UnionFlag = pygame.transform.scale(pg.image.load("assets/unionFlagOfficial.png"), (191, 122))
        ConfederateFlag = pygame.transform.scale(pg.image.load("assets/confederateFlagOfficial.png"), (191, 122))

        UnionFlagSmall = pygame.transform.scale(pg.image.load("assets/unionFlagOfficial.png"), (20, 10))
        ConfederateFlagSmall = pygame.transform.scale(pg.image.load("assets/confederateFlagOfficial.png"), (20, 10))

        BronzeUI = pygame.transform.scale(pg.image.load("assets/bronze.png"), (400, 50))
        SilverUI = pygame.transform.scale(pg.image.load("assets/silver.png"), (400, 50))
        GoldUI = pygame.transform.scale(pg.image.load("assets/gold.png"), (400, 50))
        BlueUI = pygame.transform.scale(pg.image.load("assets/unionSteel.jpg"), (400, 50))
        GreyUI = pygame.transform.scale(pg.image.load("assets/confederateSteel.jpg"), (400, 50))
        BlackUI = pygame.transform.scale(pg.image.load("assets/black.jpg"), (400, 500))

        nextTurn = pygame.transform.scale(pygame.image.load("assets/play.png"), (80, 80))
        PlusSign = pygame.transform.scale(pygame.image.load("assets/plusSign.png"), (15, 15))
        PlusSignLarge = pygame.transform.scale(pygame.image.load("assets/plusSign.png"), (50, 50))
        PlusSignLight = pygame.transform.scale(pygame.image.load("assets/plusSignLight.png"), (15, 15))
        PlusSignLightLarge = pygame.transform.scale(pygame.image.load("assets/plusSignLight.png"), (50, 50))
        FireBall = pygame.transform.scale(pygame.image.load("assets/fireBall3.png"), (50, 50))

        Anchor = pygame.transform.scale(pygame.image.load("assets/anchor.png"), (30, 30))

        ogWidth = Map.get_width()
        ogHeight = Map.get_height()
        Map = pygame.transform.scale(Map, (width, height))

        Ocean = pg.transform.scale(Ocean, (width, height))
        Terrain = pg.transform.scale(Terrain, (width, height))
        Mask = pg.transform.scale(Mask, (width, height))

        Terrain.set_alpha(50)





        for x in range(width):
            for y in range(height):
                mask_color = Mask.get_at((x, y))
                if mask_color == pg.Color(255,255,255) or mask_color == pg.Color(255,232,232) or mask_color == pg.Color(219, 255, 226) or mask_color == pg.Color(164, 167, 190) :
                    Map.set_at((x, y), Ocean.get_at((x,y)))




        while not ConfederateVictory() and not UnionVictory():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MUSIC_END:
                    pygame.mixer.init()
                    song1 = "assets/Star_Spangled_Banner_minor_key_rx2.wav"
                    song2 = "assets/Confederate States of America _1861-1865_ Patriotic song _Dixie_ - Duration_ 4_53_.mp3"
                    song3 = "assets/battle_hymn_of_the_republic.mp3"

                    pygame.mixer_music.load(random.choice([song1, song2, song3]))
                    pygame.mixer_music.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if(UnionFlag.get_rect().collidepoint(pg.mouse.get_pos())):
                        if PlayerTurn == "Union":
                            stats(Union)
                        else:
                            stats(Confederacy)


                    if (clickedArmy and clickedArmy[1] == PlayerTurn):
                        GenName = get_font(10).render(
                            (clickedArmy[0].general.name if clickedArmy[0].general != None else "None"), False,
                            "#DEEFF5")
                        GenName_rect = Gen.get_rect(topleft=(1110, 680))
                        if(GenName_rect.collidepoint(mouse_pos)):
                            if(PlayerTurn == "Union"):
                                for gen in Union_Generals:
                                    if gen != None and not gen.in_use:
                                        if (clickedArmy[0].general != None):
                                            clickedArmy[0].general.in_use = False
                                        clickedArmy[0].general = gen
                                        gen.in_use = True
                                        break
                            else:
                                for gen in Confederate_Generals:
                                    if gen != None and not gen.in_use:
                                        if(clickedArmy[0].general != None):
                                            clickedArmy[0].general.in_use = False
                                        clickedArmy[0].general = gen
                                        gen.in_use = True
                                        break
                        for j in range(5):
                            total_rect = pygame.Rect(1470, 570 + (40 * j), 15, 15)
                            if total_rect.collidepoint(mouse_pos):
                                clickedArmy[0].moved = True
                                if j == 0:
                                    if clickedArmy[1] == "Union":
                                        Union.add_units(clickedArmy[0], Militia())
                                    else:
                                        Confederacy.add_units(clickedArmy[0], Militia())
                                elif j == 1:
                                    if clickedArmy[1] == "Union":
                                        Union.add_units(clickedArmy[0], Line_Infantry())
                                    else:
                                        Confederacy.add_units(clickedArmy[0], Line_Infantry())
                                elif j == 2:
                                    if clickedArmy[1] == "Union":
                                        Union.add_units(clickedArmy[0], Cavalry())
                                    else:
                                        Confederacy.add_units(clickedArmy[0], Cavalry())
                                elif j == 3:
                                    if clickedArmy[1] == "Union":
                                        Union.add_units(clickedArmy[0], Dragoons())
                                    else:
                                        Confederacy.add_units(clickedArmy[0], Dragoons())
                                elif j == 4:
                                    if clickedArmy[1] == "Union":
                                        Union.add_units(clickedArmy[0], Artillery())
                                    else:
                                        Confederacy.add_units(clickedArmy[0], Artillery())
                                break

                    for prov in Union.provinces + Confederacy.provinces:
                        prov_x = int(prov.coords[0] * (width / ogWidth))
                        prov_y = int(prov.coords[1] * (height / ogHeight))
                        if(prov.clicked == True and ((PlayerTurn == "Union" and prov in Union.provinces) or ((PlayerTurn == "Confederacy") and prov in Confederacy.provinces))):
                            factories_plus_rect = PlusSign.get_rect(topleft=(1280, 600))
                            barracks_plus_rect = PlusSign.get_rect(topleft=(1280, 625))
                            railroad_plus_rect = PlusSign.get_rect(topleft=(1280, 650))
                            fortLevel_plus_rect = PlusSign.get_rect(topleft=(1280, 700))

                            mouse_pos = pygame.mouse.get_pos()

                            if factories_plus_rect.collidepoint(mouse_pos):
                                if(PlayerTurn == "Union"):
                                    Union.build_factory(prov)
                                else:
                                    Confederacy.build_factory(prov)
                            if barracks_plus_rect.collidepoint(mouse_pos):
                                if(PlayerTurn == "Union"):
                                    Union.build_barracks(prov)
                                else:
                                    Confederacy.build_barracks(prov)
                            if railroad_plus_rect.collidepoint(mouse_pos):
                                if(PlayerTurn == "Union"):
                                    Union.build_railroads(prov)
                                else:
                                    Confederacy.build_railroads(prov)
                            if fortLevel_plus_rect.collidepoint(mouse_pos):
                                if(PlayerTurn == "Union"):
                                    Union.build_fort(prov)
                                else:
                                    Confederacy.build_fort(prov)
                            if PlusSignLarge.get_rect(topleft=(1360,600)).collidepoint(mouse_pos):
                                prov.armies.append(Army("Army of " + prov.name, [], None, 0.3))
                            if(FireBall.get_rect(topleft=(1360, 700)).collidepoint(mouse_pos)):
                                if(PlayerTurn == "Union"):
                                    Confederacy.morale -= 10
                                    Union.fr_opinion -= 20
                                    Union.uk_opinion -= 20
                                    Union.rs_opinion -= 20
                                else:
                                    Union.morale -= 10
                                    Confederacy.fr_opinion -= 20
                                    Confederacy.uk_opinion -= 20
                                    Confederacy.rs_opinion -= 20

                                prov.raze()

                        if Mask.get_at(mouse_pos) == Mask.get_at((prov_x, prov_y)):
                            prov.clicked = True
                            clickedProvince.clear()
                            clickedProvince.append(prov)

                            if clickedArmy:
                                if clickedArmy[1] == PlayerTurn:
                                    if prov in Union.provinces and PlayerTurn == "Confederacy" and prov in clickedArmy[2].border_states and clickedArmy[0].moved == False:
                                        if(not len(prov.armies)== 0):
                                            clickedArmy[0].attack(prov.armies[0], clickedArmy[2], prov, Confederacy, Union)
                                            clickedArmy[0].moved = True
                                        else:
                                            clickedArmy[0].take(clickedArmy[2], prov, Confederacy,Union)
                                            clickedArmy[0].moved = True
                                    elif prov in Confederacy.provinces and PlayerTurn == "Union" and prov in clickedArmy[2].border_states and clickedArmy[0].moved == False:
                                        if (not len(prov.armies) == 0):
                                            clickedArmy[0].attack(prov.armies[0], clickedArmy[2], prov, Union, Confederacy)
                                            clickedArmy[0].moved = True
                                        else:
                                            clickedArmy[0].take(clickedArmy[2], prov, Union, Confederacy)
                                            clickedArmy[0].moved = True
                                    elif clickedArmy[0].moved == False and prov in clickedArmy[2].border_states:
                                        clickedArmy[0].move(clickedArmy[2], prov)
                                        if(prov.railroads < len(clickedArmy[0].units)):
                                            clickedArmy[0].moved = True
                        else:
                            prov.clicked = False
                            if prov in clickedProvince:
                                clickedProvince.remove(prov)

                        for i, army in enumerate(prov.armies):
                            army_rect = UnionFlagSmall.get_rect(topleft=(
                                prov.coords[0] * (width / ogWidth),
                                prov.coords[1] * (height / ogHeight) + i * 20
                            ))

                            if army_rect.collidepoint(mouse_pos):
                                army.select()
                                clickedArmy.clear()
                                if(prov in Union.provinces):
                                    clickedArmy.append(army)
                                    clickedArmy.append("Union")
                                    clickedArmy.append(prov)
                                elif(prov in Confederacy.provinces):
                                    clickedArmy.append(army)
                                    clickedArmy.append("Confederacy")
                                    clickedArmy.append(prov)
                            else:
                                army.deselect()

                    nextTurnRect = nextTurn.get_rect(topleft=(1410, 10))

                    if nextTurnRect.collidepoint(pg.mouse.get_pos()):


                        if PlayerTurn == "Confederacy":
                            PlayerTurn = "Union"

                            secedeUnion = Union.update(Confederacy)
                            for province in secedeUnion:
                                tex = get_font(15).render(province.name + " has seceded from the Union!", False, "Red")
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            waiting = False

                                    SCREEN.blit(pygame.transform.scale(BlackUI, (700, 100)), (width/2 - 350, height/2 - 50))
                                    SCREEN.blit(tex, (width/2 - 280, height/2 - 10))
                                    pygame.display.update()

                            for prov in Union.provinces:
                                for army in prov.armies:
                                    army.moved = False

                        elif PlayerTurn == "Union":
                            Turn += 1
                            if Month < 12:
                                Month += 1
                            else:
                                Year += 1
                                Month = 1


                            PlayerTurn = "Confederacy"

                            secedeConfed = Confederacy.update(Union)


                            for province in secedeConfed:
                                tex = get_font(15).render(province.name + " has seceded from the Confederacy!", False, "Red")
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            waiting = False

                                    SCREEN.blit(pygame.transform.scale(BlackUI, (700, 100)), (width/2 - 350, height/2 - 50))
                                    SCREEN.blit(tex, (width/2 - 280, height/2 - 10))
                                    pygame.display.update()

                            for prov in Confederacy.provinces:
                                for army in prov.armies:
                                    army.moved = False


            SCREEN.blit(Map, (0, 0))
            SCREEN.blit(Terrain, (0,0))

            # harbors
            SCREEN.blit(Anchor, (1238, 283))  # new york city
            SCREEN.blit(Anchor, (1360, 230))  # massachussetts
            SCREEN.blit(Anchor, (1131, 365))  # delmarva
            SCREEN.blit(Anchor, (955, 512))  # charleston
            SCREEN.blit(Anchor, (585, 635))  # new orleans

            for prov in Union.provinces:
                if((Mask.get_at(pg.mouse.get_pos()) == Mask.get_at((int(prov.coords[0]*(width/ogWidth)), int(prov.coords[1]*(height/ogHeight)))) or prov.clicked) and not (UnionFlag.get_rect().collidepoint(pg.mouse.get_pos()))):
                    do_flood_fill(Map, prov.coords[0] * (width / ogWidth), prov.coords[1] * (height / ogHeight),pg.Color("Light Blue"))
                else:
                    do_flood_fill(Map, prov.coords[0]*(width/ogWidth), prov.coords[1]*(height/ogHeight), pg.Color(0,0,255))
                if(prov.clicked):
                    color = ""
                    if(prov.warscore < 4):
                        SCREEN.blit(BronzeUI, (1100, 500))
                        lett= get_font(20).render(prov.name, False, "Brown")
                        color = "Brown"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    elif(prov.warscore < 8):
                        SCREEN.blit(SilverUI, (1100, 500))
                        lett = get_font(20).render(prov.name, False, "#141414")
                        color = "Grey"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    else:
                        SCREEN.blit(GoldUI, (1100, 500))
                        lett = get_font(20).render(prov.name, False, "#79704D")
                        color = "#79704D"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    #name, warscore, factories, barracks, armies, railroads, support, fort_level, slaveholding, coords
                    SCREEN.blit(BlackUI, (1100, 550))
                    if(prov.land):
                        scoreText = get_font(10).render("Warscore: " + str(prov.warscore), False, color)
                        score_rect = lett.get_rect(topleft=(1120, 575))
                        factoriesText = get_font(10).render("Number of Factories: " + str(prov.factories), False, color)
                        factories_rect = lett.get_rect(topleft=(1120, 600))
                        barracksText = get_font(10).render("Barracks Level: " + str(prov.barracks), False, color)
                        barracks_rect = lett.get_rect(topleft=(1120, 625))
                        railroadText = get_font(10).render("Railroads: " + str(prov.railroads), False, color)
                        railroad_rect = lett.get_rect(topleft=(1120, 650))
                        supportText = get_font(10).render("Support for the war: " + str(prov.support), False, color)
                        support_rect = lett.get_rect(topleft=(1120, 675))
                        fortLevelText = get_font(10).render("Fort Level: " + str(prov.fort_level), False, color)
                        fortLevel_rect = lett.get_rect(topleft=(1120, 700))
                        slaveholdingText = get_font(10).render("Slavery Legal: " + str(prov.slaveholding), False, color)
                        slaveholding_rect = lett.get_rect(topleft=(1120, 725))
                        SCREEN.blit(scoreText, score_rect)
                        SCREEN.blit(factoriesText, factories_rect)
                        SCREEN.blit(barracksText, barracks_rect)
                        SCREEN.blit(railroadText, railroad_rect)
                        SCREEN.blit(supportText, support_rect)
                        SCREEN.blit(fortLevelText, fortLevel_rect)
                        SCREEN.blit(slaveholdingText, slaveholding_rect)

                        armyText = get_font(15).render("Build an Army", False, color)
                        army_rect = lett.get_rect(topleft=(1320, 575))
                        SCREEN.blit(armyText, army_rect)

                        razeText = get_font(15).render("Raze Province", False, "Red")
                        raze_rect = lett.get_rect(topleft=(1320, 675))
                        SCREEN.blit(razeText, raze_rect)

                        factories_plus_rect = PlusSign.get_rect(topleft=(1280, factories_rect.top))
                        barracks_plus_rect = PlusSign.get_rect(topleft=(1280, barracks_rect.top))
                        railroad_plus_rect = PlusSign.get_rect(topleft=(1280, railroad_rect.top))
                        fortLevel_plus_rect = PlusSign.get_rect(topleft=(1280, fortLevel_rect.top))
                        army_plus_rect = PlusSignLarge.get_rect(topleft=(1360, 600))
                        fire_rect = FireBall.get_rect(topleft=(1360, 700))

                        mouse_pos = pygame.mouse.get_pos()

                        for plus_rect in [factories_plus_rect, barracks_plus_rect, railroad_plus_rect, fortLevel_plus_rect]:
                            if plus_rect.collidepoint(mouse_pos):
                                SCREEN.blit(PlusSignLight, plus_rect)
                            else:
                                SCREEN.blit(PlusSign, plus_rect)

                        if army_plus_rect.collidepoint(mouse_pos):
                            SCREEN.blit(PlusSignLightLarge, army_plus_rect)
                        else:
                            SCREEN.blit(PlusSignLarge, army_plus_rect)

                        SCREEN.blit(FireBall, fire_rect)

                for i in range(len(prov.armies)):
                    SCREEN.blit(UnionFlagSmall, (prov.coords[0]*(width/ogWidth), prov.coords[1]*(height/ogHeight) + i * 20))
                    army_rect = UnionFlagSmall.get_rect(topleft=(prov.coords[0]*(width/ogWidth), prov.coords[1]*(height/ogHeight) + i * 20))
                    if(army_rect.collidepoint(pg.mouse.get_pos()) or prov.armies[i].clicked == True):
                        num = get_font(10).render(str(len(prov.armies[i].units)), False, "Black")
                    else:
                        num = get_font(10).render(str(len(prov.armies[i].units)), False, "White")
                    if(prov.armies[i].clicked == True):
                        SCREEN.blit(BlueUI, (1100, 500))
                        SCREEN.blit(BlackUI, (1100, 550))
                        lett = get_font(20).render(prov.armies[i].name, False, "#DEEFF5")
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)

                        if (prov.armies[i].general != None):
                            SCREEN.blit(pg.transform.scale(prov.armies[i].general.image, (100, 100)), (1100, 550))
                        Gen = get_font(15).render("General: ", False, "#DEEFF5")
                        Genrect = Gen.get_rect(topleft=(1110, 660))
                        GenName = get_font(10).render(
                            (prov.armies[i].general.name if prov.armies[i].general != None else "None"), False,
                            "#DEEFF5")
                        GenName_rect = Gen.get_rect(topleft=(1110, 680))
                        SCREEN.blit(Gen, Genrect)
                        SCREEN.blit(GenName, GenName_rect)

                        mil = 0
                        linInf = 0
                        cav = 0
                        dra = 0
                        art = 0

                        for unit in prov.armies[i].units:
                            if (unit.name == "Militia"):
                                mil += 1
                            elif (unit.name == "Line Infantry"):
                                linInf += 1
                            elif (unit.name == "Cavalry"):
                                cav += 1
                            elif (unit.name == "Dragoons"):
                                dra += 1
                            elif (unit.name == "Artillery"):
                                art += 1

                        milText = get_font(10).render("Militia units: " + str(mil), False, "#DEEFF5")
                        linText = get_font(10).render("Line Infantry units: " + str(linInf), False, "#DEEFF5")
                        cavText = get_font(10).render("Cavalry units: " + str(cav), False, "#DEEFF5")
                        draText = get_font(10).render("Dragoons units: " + str(dra), False, "#DEEFF5")
                        artText = get_font(10).render("Artillery units: " + str(art), False, "#DEEFF5")

                        SCREEN.blit(milText, (1300, 570))
                        SCREEN.blit(linText, (1300, 610))
                        SCREEN.blit(cavText, (1300, 650))
                        SCREEN.blit(draText, (1300, 690))
                        SCREEN.blit(artText, (1300, 730))

                        for j in range(5):
                            total_rect = pygame.Rect(1470, 570 + (40 * j), 15, 15)

                            if total_rect.collidepoint(mouse_pos):
                                plus_surface = PlusSignLight
                            else:
                                plus_surface = PlusSign

                            SCREEN.blit(plus_surface, (1470, 570 + (40 * j)))

                    SCREEN.blit(num, (prov.coords[0]*(width/ogWidth) + 10, prov.coords[1]*(height/ogHeight) + 10  + i * 20))
                # fort_button = Button(
                #    image=pygame.transform.scale(pg.image.load("assets/StarFort01.jpg"), (15, 15)),
                #    pos=(prov.coords[0] * (width / ogWidth), prov.coords[1] * (height / ogHeight)),
                #    text_input="",
                #    font=get_font(25),
                #    base_color="Grey",
                #    hovering_color="White"
                # )
                # fort_button.update(SCREEN)
            for prov in Confederacy.provinces:
                if((Mask.get_at(pg.mouse.get_pos()) == Mask.get_at((int(prov.coords[0]*(width/ogWidth)), int(prov.coords[1]*(height/ogHeight)))) or prov.clicked) and not (ConfederateFlag.get_rect().collidepoint(pg.mouse.get_pos()))):
                    do_flood_fill(Map, prov.coords[0] * (width / ogWidth), prov.coords[1] * (height / ogHeight),pg.Color("Grey"))
                else:
                    do_flood_fill(Map, prov.coords[0]*(width/ogWidth), prov.coords[1]*(height/ogHeight), pg.Color("#5A5A5A"))
                if (prov.clicked):
                    color = ""
                    if (prov.warscore < 4):
                        SCREEN.blit(BronzeUI, (1100, 500))
                        lett = get_font(20).render(prov.name, False, "Brown")
                        color = "Brown"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    elif (prov.warscore < 8):
                        SCREEN.blit(SilverUI, (1100, 500))
                        lett = get_font(20).render(prov.name, False, "#141414")
                        color = "Grey"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    else:
                        SCREEN.blit(GoldUI, (1100, 500))
                        lett = get_font(20).render(prov.name, False, "#79704D")
                        color = "#79704D"
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)
                    # name, warscore, factories, barracks, armies, railroads, support, fort_level, slaveholding, coords
                    SCREEN.blit(BlackUI, (1100, 550))
                    if (prov.land):
                        scoreText = get_font(10).render("Warscore: " + str(prov.warscore), False, color)
                        score_rect = lett.get_rect(topleft=(1120, 575))
                        factoriesText = get_font(10).render("Number of Factories: " + str(prov.factories), False, color)
                        factories_rect = lett.get_rect(topleft=(1120, 600))
                        barracksText = get_font(10).render("Barracks Level: " + str(prov.barracks), False, color)
                        barracks_rect = lett.get_rect(topleft=(1120, 625))
                        railroadText = get_font(10).render("Railroads: " + str(prov.railroads), False, color)
                        railroad_rect = lett.get_rect(topleft=(1120, 650))
                        supportText = get_font(10).render("Support for the war: " + str(prov.support), False, color)
                        support_rect = lett.get_rect(topleft=(1120, 675))
                        fortLevelText = get_font(10).render("Fort Level: " + str(prov.fort_level), False, color)
                        fortLevel_rect = lett.get_rect(topleft=(1120, 700))
                        slaveholdingText = get_font(10).render("Slavery Legal: " + str(prov.slaveholding), False, color)
                        slaveholding_rect = lett.get_rect(topleft=(1120, 725))
                        SCREEN.blit(scoreText, score_rect)
                        SCREEN.blit(factoriesText, factories_rect)
                        SCREEN.blit(barracksText, barracks_rect)
                        SCREEN.blit(railroadText, railroad_rect)
                        SCREEN.blit(supportText, support_rect)
                        SCREEN.blit(fortLevelText, fortLevel_rect)
                        SCREEN.blit(slaveholdingText, slaveholding_rect)

                        armyText = get_font(15).render("Build an Army", False, color)
                        army_rect = lett.get_rect(topleft=(1320, 575))
                        SCREEN.blit(armyText, army_rect)

                        razeText = get_font(15).render("Raze Province", False, "Red")
                        raze_rect = lett.get_rect(topleft=(1320, 675))
                        SCREEN.blit(razeText, raze_rect)

                        factories_plus_rect = PlusSign.get_rect(topleft=(1280, factories_rect.top))
                        barracks_plus_rect = PlusSign.get_rect(topleft=(1280, barracks_rect.top))
                        railroad_plus_rect = PlusSign.get_rect(topleft=(1280, railroad_rect.top))
                        fortLevel_plus_rect = PlusSign.get_rect(topleft=(1280, fortLevel_rect.top))
                        army_plus_rect = PlusSignLarge.get_rect(topleft=(1360, 600))
                        fire_rect = FireBall.get_rect(topleft=(1360, 700))

                        mouse_pos = pygame.mouse.get_pos()

                        for plus_rect in [factories_plus_rect, barracks_plus_rect, railroad_plus_rect,
                                          fortLevel_plus_rect]:
                            if plus_rect.collidepoint(mouse_pos):
                                SCREEN.blit(PlusSignLight, plus_rect)
                            else:
                                SCREEN.blit(PlusSign, plus_rect)

                        if army_plus_rect.collidepoint(mouse_pos):
                            SCREEN.blit(PlusSignLightLarge, army_plus_rect)
                        else:
                            SCREEN.blit(PlusSignLarge, army_plus_rect)

                        SCREEN.blit(FireBall, fire_rect)

                for i in range(len(prov.armies)):
                    SCREEN.blit(ConfederateFlagSmall,
                                (prov.coords[0] * (width / ogWidth), prov.coords[1] * (height / ogHeight) + i * 20))
                    army_rect = ConfederateFlagSmall.get_rect(
                        topleft=(prov.coords[0] * (width / ogWidth), prov.coords[1] * (height / ogHeight) + i * 20))
                    if (army_rect.collidepoint(pg.mouse.get_pos()) or prov.armies[i].clicked == True):
                        num = get_font(10).render(str(len(prov.armies[i].units)), False, "Black")  # display units
                    else:
                        num = get_font(10).render(str(len(prov.armies[i].units)), False, "White")  # display units
                    if (prov.armies[i].clicked == True):
                        SCREEN.blit(GreyUI, (1100, 500))
                        SCREEN.blit(BlackUI, (1100, 550))
                        lett = get_font(20).render(prov.armies[i].name, False, 	"#636363")
                        text_rect = lett.get_rect(center=(1300, 525))
                        SCREEN.blit(lett, text_rect)

                        if(prov.armies[i].general != None):
                            SCREEN.blit(pg.transform.scale(prov.armies[i].general.image, (100, 100)), (1100, 550))
                        Gen = get_font(15).render("General: ", False, "#636363")
                        Genrect = Gen.get_rect(topleft=(1110, 660))
                        GenName = get_font(10).render((prov.armies[i].general.name if prov.armies[i].general != None else "None"),False, "#636363")
                        GenName_rect = Gen.get_rect(topleft=(1110, 680))
                        SCREEN.blit(Gen, Genrect)
                        SCREEN.blit(GenName, GenName_rect)

                        mil = 0
                        linInf = 0
                        cav = 0
                        dra = 0
                        art = 0

                        for unit in prov.armies[i].units:
                            if(unit.name == "Militia"):
                                mil+=1
                            elif(unit.name == "Line Infantry"):
                                linInf+=1
                            elif(unit.name == "Cavalry"):
                                cav+=1
                            elif(unit.name == "Dragoons"):
                                dra+=1
                            elif(unit.name == "Artillery"):
                                art+=1

                        milText = get_font(10).render("Militia units: " + str(mil), False, "#636363")
                        linText = get_font(10).render("Line Infantry units: " + str(linInf), False, "#636363")
                        cavText = get_font(10).render("Cavalry units: " + str(cav), False, "#636363")
                        draText = get_font(10).render("Dragoons units: " + str(dra), False, "#636363")
                        artText = get_font(10).render("Artillery units: " + str(art), False, "#636363")

                        SCREEN.blit(milText, (1300, 570))
                        SCREEN.blit(linText, (1300, 610))
                        SCREEN.blit(cavText, (1300, 650))
                        SCREEN.blit(draText, (1300, 690))
                        SCREEN.blit(artText, (1300, 730))

                        for j in range(5):
                            total_rect = pygame.Rect(1470, 570 + (40 * j), 15, 15)

                            if total_rect.collidepoint(mouse_pos):
                                plus_surface = PlusSignLight
                            else:
                                plus_surface = PlusSign

                            SCREEN.blit(plus_surface, (1470, 570 + (40 * j)))


                    SCREEN.blit(num,(prov.coords[0] * (width / ogWidth) + 10, prov.coords[1] * (height / ogHeight) + 10  + i * 20))


            do_flood_fill(Map, 872 * (width / ogWidth), 99 * (height / ogHeight), pg.Color("#FF69B4")) # canada paint
            do_flood_fill(Map, 1045 * (width / ogWidth), 122 * (height / ogHeight), pg.Color("#FF69B4"))  # canada paint
            do_flood_fill(Map, 112 * (width / ogWidth), 745 * (height / ogHeight), pg.Color(75, 83, 32)) # mexico paint
            SCREEN.blit(FlagHolder, (0, 0)) # flag holder
            SCREEN.blit(Holder, (240, 0))  # total national money holder
            SCREEN.blit(Black, (252, 5))
            SCREEN.blit(MoneyIcon, (312, 5))
            SCREEN.blit(Holder, (350, 0))  # total national manpower holder
            SCREEN.blit(Black, (362, 5))
            SCREEN.blit(SoldierIcon, (422, 5))
            SCREEN.blit(Holder, (460, 0))  # total national morale holder
            SCREEN.blit(Black, (472, 5))
            SCREEN.blit(MoraleIcon, (532, 5))
            SCREEN.blit(pg.transform.scale(Holder, (480, 40)), (590, 0))  # total warscore
            SCREEN.blit(pg.transform.scale(Black, (456, 30)), (602, 5))
            if(PlayerTurn == "Union"):
                if(Union.score > 66):
                    White.fill("Dark Green")
                elif(Union.score > 33):
                    White.fill("Green")
                elif (Union.score >= 0):
                    White.fill("Yellow")
                elif (Union.score > -33):
                    White.fill("Gold")
                elif (Union.score > -66):
                    White.fill("Red")
                elif (Union.score >= -100):
                    White.fill("Dark Red")
                SCREEN.blit(pg.transform.scale(White, (max(0,(228 + (Union.score* 2.28))), 33)), (602,4))
                SCREEN.blit(pg.transform.scale(pg.image.load("assets/steelTriangle.png"), (40, 40)), (808, 30))
            else:
                if (Confederacy.score > 66):
                    White.fill("Dark Green")
                elif (Confederacy.score > 33):
                    White.fill("Green")
                elif (Confederacy.score >= 0):
                    White.fill("Yellow")
                elif (Confederacy.score > -33):
                    White.fill("Gold")
                elif (Confederacy.score > -66):
                    White.fill("Red")
                elif (Confederacy.score >= -100):
                    White.fill("Dark Red")
                SCREEN.blit(pg.transform.scale(White, (max(0,(228 + (Confederacy.score* 2.28))), 33)), (602, 4))
                SCREEN.blit(pg.transform.scale(pg.image.load("assets/steelTriangle.png"), (40, 40)), (808, 30))
            Black = pygame.transform.scale(pg.image.load("assets/black.jpg"), (96, 30))


            if(PlayerTurn == "Union"):
                SCREEN.blit(UnionFlag, (25,17))
                if(UnionFlag.get_rect().collidepoint(pg.mouse.get_pos())):
                    overlayWhite = pg.image.load("assets/white.jpg")
                    overlayWhite.set_alpha(100)
                    SCREEN.blit(pg.transform.scale(overlayWhite, (191, 122)), (25, 17))
                displayMoney = get_font(12).render(str(Union.money), False, "White") # display money
                SCREEN.blit(displayMoney, (257, 15))
                displayManpower = get_font(12).render(str(Union.manpower), False, "White")  # display manpower
                SCREEN.blit(displayManpower, (367, 15))
                displayMorale = get_font(12).render(str(Union.morale), False, "White")  # display morale
                SCREEN.blit(displayMorale, (477, 15))
            elif(PlayerTurn == "Confederacy"):
                SCREEN.blit(ConfederateFlag, (25, 17))
                if (ConfederateFlag.get_rect().collidepoint(pg.mouse.get_pos())):
                    overlayWhite = pg.image.load("assets/white.jpg")
                    overlayWhite.set_alpha(100)
                    SCREEN.blit(pg.transform.scale(overlayWhite, (191, 122)), (25, 17))
                displayMoney = get_font(12).render(str(Confederacy.money), False, "White")  # display money
                SCREEN.blit(displayMoney, (257, 15))
                displayManpower = get_font(12).render(str(Confederacy.manpower), False, "White")  # display manpower
                SCREEN.blit(displayManpower, (367, 15))
                displayMorale = get_font(12).render(str(Confederacy.morale), False, "White")  # display morale
                SCREEN.blit(displayMorale, (477, 15))
            SCREEN.blit(Holder, (1300, 0))  # turn
            SCREEN.blit(Black, (1312, 5))
            displayTurn = get_font(12).render("Turn:   " + str(Turn), False, "White")
            SCREEN.blit(displayTurn, (1322, 15))
            SCREEN.blit(Holder, (1190, 0))  # year
            SCREEN.blit(Black, (1202, 5))
            displayYear= get_font(12).render("Year:   " + str(Year), False, "White")
            SCREEN.blit(displayYear, (1212, 15))
            SCREEN.blit(Holder, (1080, 0))  # month
            SCREEN.blit(Black, (1092, 5))
            displayMonth = get_font(12).render("Month:   " + str(Month), False, "White")
            SCREEN.blit(displayMonth, (1102, 15))

            nextTurnRect = nextTurn.get_rect(topleft=(1410, 10))
            SCREEN.blit(pygame.transform.scale(Holder, (100,100)), (1400, 0))
            SCREEN.blit(pygame.transform.scale(Black, (80,83)), (1410, 10))
            overlay = pg.transform.scale(pg.image.load("assets/white.jpg"), (80, 83))
            overlay.set_alpha(125)
            SCREEN.blit(nextTurn, (1410, 10))
            if nextTurnRect.collidepoint(pg.mouse.get_pos()):
                SCREEN.blit(overlay, (1410, 10))
            pygame.display.update()

        return Union if Union.score >= 100 else Confederacy

    def playWithAI():
        unesc = True
        while unesc:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        unesc = False
            SCREEN.blit(pg.transform.scale(pg.image.load("assets/white.jpg"), (2000, 2000)), (0, 0))
            comingSoon = get_font(50).render(" Coming Soon! Press esc to leave. ", False, "Black")
            SCREEN.blit(comingSoon, (200, 300))
            pg.display.update()




    main_menu()

game_runner()