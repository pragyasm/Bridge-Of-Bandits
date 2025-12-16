
import pygame 
import sys
import random

pygame.init()

width, height=1100,720
fps=30

min_players=3
max_players=12
start_money=100
light_weight_range=(4, 6)
heavy_weight_range=(9, 12)

#colors ---- (r,g,b)
card = (28, 28, 32)
bg =(18, 18, 20)
white = (235, 235, 235)
green =(70, 160, 90)
dark_green=(20, 80, 45)
dark_red=(110, 20, 30)
yellow = (170, 140, 50)
pink = (220, 135, 165)
blue = (90, 160, 255)
gray = (140, 140, 150)
black = (0, 0, 0)
dark_pink=(150, 50, 85)
red=(170, 45, 45)
lilac=(170, 150, 190)
cream=(245, 240, 220)


#fonts
font = pygame.font.SysFont("times", 24)
font1=pygame.font.SysFont("times", 18)
big = pygame.font.SysFont("times", 28, bold=True)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bridge of Bandits")
clock = pygame.time.Clock()

def txt(s, f, color=cream): #pygame udf for test
    return f.render(str(s), True, color)

class Player:
    '''but to give yall a gist of what classes are:
    if i go on about naming like a thousand variables thats a huge waste of time
    so instead, i create a CLASS where i'm creating my OWN data type 
    (just like a user defined function, this is a user defined data type) - like int bool etc are all built in datatypes'''

    def __init__(self,name):#this function is user defined but __init__ is built in
        #its called a 'constructor' & runs auromatically when class player is made
        '''very important - self is an object 
        and everything u see below are data stored inside the object 
        everything will make sense up ahead just be patient and dont panic'''
        self.name=name
        self.gold=start_money
        self.alive=True
        self._choice=None
        self._sabotage=False

class Button:
    def __init__(self,rect,label,color=card,text_color=black):
        self.rect=pygame.Rect(rect)#makes a rectangle using dimensions
        self.label=label#THE TEXT SHOWN ON BUTTONS!!!
        self.color=color#colour of buttons
        self.text_color=text_color#colour of text on buttons

    def draw(self,surf): #surf stands for surafce, basically pushes everything we did, onto the surface(screen)
        pygame.draw.rect(surf,self.color,self.rect,border_radius=8)
        r=txt(self.label,font,self.text_color)
        surf.blit(r,r.get_rect(center=self.rect.center))#takes the above text and puts it at given position on screen
        # eg : [text surface]  ───blit──▶  [screen surface]

    def clicked(self,pos):
        return self.rect.collidepoint(pos)

class TextBox:
    def __init__(self,rect,text=""):
        self.rect=pygame.Rect(rect)
        self.text=text
        self.active=False

    def handle_event(self,ev):
        if ev.type==pygame.MOUSEBUTTONDOWN:
            self.active=self.rect.collidepoint(ev.pos)

        if ev.type==pygame.KEYDOWN and self.active:
            if ev.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
            elif ev.key==pygame.K_RETURN:
                return "enter"
            else:
                if len(self.text)<12:
                    self.text+=ev.unicode

    def draw(self,surf):
        color=red if self.active else black
        pygame.draw.rect(surf,color,self.rect,2)
        surf.blit(txt(self.text,font),(self.rect.x+6,self.rect.y+6))

def instructions_screen():
    #udf for the instructions to appear on screen
    while True:
        screen.fill(bg)
        pygame.draw.rect(screen,card,(180,120,740,480),border_radius=15)

        y=150
        screen.blit(txt("HOW TO PLAY",big,red),(450,y));y+=50

        lines=[
            "You are bandits escaping with stolen gold...",
            "And suddenly stumble upon a bridge that grants you freedom",
            "But the bridge is cursed... Only a maximum of 2 players can make it out alive.",
            "Every player has to select one of two weights, either: ",
            "Light weight = low risk, low reward OR Heavy weight = high risk, high reward.",
            "If total weight exceeds bridge limit: Heavy weight players fall and die.",
            "And if bridge weight exceeds total weight: Everyone survives.",
            "Light players may sabotage for bonuses, as an added advantage- ",
            "but it comes with a high reward/penalty",
            "Last survivor(s) or richest wins.",
            "",
            "Click anywhere to go back."
        ]

        for line in lines:
            screen.blit(txt(line,font1,yellow),(260,y))
            y+=32

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit();sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN or ev.type==pygame.KEYDOWN:
                return

        clock.tick(fps)

def intro_screen():
    #udf to ask playgame/see instructions
    btn_play=Button((380,360,140,60),"play game",yellow,black)
    btn_rules=Button((560,360,180,60),"see instructions",red,black)

    while True:
        screen.fill(bg)
        pygame.draw.rect(screen,card,(200,180,700,360),border_radius=15)

        screen.blit(txt("BRIDGE OF BANDITS",big,red),(405,260))

        btn_play.draw(screen)
        btn_rules.draw(screen)

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit();sys.exit()

            if ev.type==pygame.MOUSEBUTTONDOWN:
                if btn_play.clicked(ev.pos):
                    return
                if btn_rules.clicked(ev.pos):
                    instructions_screen()

        clock.tick(fps)

def player_setup_gui():
    #udf to ask number and name of ppl
    minus_btn=Button((400,260,60,50),"-",red)
    plus_btn=Button((660,260,60,50),"+",green)
    next_btn=Button((470,440,180,60),"next",yellow)

    name_box=TextBox((360,360,380,50))

    player_count=min_players
    players=[]
    current=0
    stage="count"

    while True:
        screen.fill(bg)
        pygame.draw.rect(screen,card,(280,160,540,420),border_radius=12)

        if stage=="count":
            screen.blit(txt("number of players",big,yellow),(435,200))

            minus_btn.draw(screen)
            plus_btn.draw(screen)

            num=txt(str(player_count),big,yellow)
            screen.blit(num,num.get_rect(center=(560,285)))

            next_btn.draw(screen)

        else:
            screen.blit(
                txt(f"enter name of player {current+1}",big,yellow),
                (400,300)
            )
            name_box.draw(screen)

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type==pygame.MOUSEBUTTONDOWN:
                if stage=="count":
                    if minus_btn.clicked(ev.pos):
                        player_count=max(min_players,player_count-1)

                    elif plus_btn.clicked(ev.pos):
                        player_count=min(max_players,player_count+1)

                    elif next_btn.clicked(ev.pos):
                        stage="names"

            if stage=="names":
                result=name_box.handle_event(ev)

                if result=="enter":
                    if name_box.text.strip():
                        players.append(Player(name_box.text.strip()))
                        name_box.text=""
                        current+=1

                        if current==player_count:
                            return players

def play_again_screen(winner_text):
    #udf to ask if user wants to play game again or quit
    btn_again = Button((350, 400, 180, 60), "play again", green)
    btn_quit  = Button((570, 400, 180, 60), "quit", red)

    while True:
        screen.fill(bg)
        pygame.draw.rect(screen, card, (200, 180, 700, 360), border_radius=15)

        screen.blit(txt(winner_text, big,cream), (360, 260))

        btn_again.draw(screen)
        btn_quit.draw(screen)

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_again.clicked(ev.pos):
                    return True
                if btn_quit.clicked(ev.pos):
                    pygame.quit(); sys.exit()

        clock.tick(fps)

def draw_player_sidebar():
    #the stats of the player being shown on the right side of the screen
    x = width - 320
    pygame.draw.rect(screen, card, (x, 0, 320, height))
    screen.blit(txt("players:", big,cream), (x + 12, 8))

    y = 48
    for p in players:
        c = green if p.alive else red
        screen.blit(txt(p.name, font, c), (x + 12, y))
        screen.blit(txt(f"${int(p.gold)}", font,yellow), (x + 150, y))
        state = "alive" if p.alive else "dead"
        screen.blit(txt(state, font,c), (x + 210, y))
        y += 38

def get_choices_gui(p):
    choice=None
    sabotage=False

    btn_light=Button((120,430,220,80),"light (safer)",green)
    btn_heavy=Button((380,430,220,80),"heavy (riskier)",red)
    btn_confirm=Button((240,610,240,60),"lock choice",yellow)

    while True:
        screen.fill(bg)
        pygame.draw.rect(screen,card,(40,40,width-420,height-80),border_radius=10)
        draw_player_sidebar()

        screen.blit(txt(f"{p.name}'s turn — secret",big,cream),(60,60))
        screen.blit(txt(f"your gold: ${p.gold}",font,yellow),(60,110))

        btn_light.draw(screen)
        btn_heavy.draw(screen)

        sab_label=f"sabotage: {'on' if sabotage else 'off'}"
        sab_color=blue if choice=='L' else card
        btn_toggle=Button((120,530,480,60),sab_label,sab_color)
        btn_toggle.draw(screen)

        btn_confirm.draw(screen)

        if choice:
            screen.blit(
                txt(f"selected: {choice} {'(sabotage)' if sabotage else ''}",big,cream),
                (60,320)
            )

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit();sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                pos=ev.pos
                if btn_light.clicked(pos):
                    choice='L';sabotage=False
                elif btn_heavy.clicked(pos):
                    choice='H';sabotage=False
                elif btn_toggle.clicked(pos) and choice=='L':
                    sabotage=not sabotage
                elif btn_confirm.clicked(pos) and choice:
                    p._choice=choice
                    p._sabotage=sabotage
                    return

        clock.tick(fps)

def evaluate_round():
    global deaths_this_round,applied_weight
    deaths_this_round=[]
    applied_weight=sum(
        light_weight if p._choice=='L' else heavy_weight
        for p in players
        if p.alive and p._choice is not None
    )

    if applied_weight<=bridge_limit:
        for p in players:
            if not p.alive:
                continue
            if p._choice=='L' and p._sabotage:
                p.gold=10
            elif p._choice=='L':
                p.gold+=20
            else:
                p.gold+=80
    else:
        for p in players:
            if p.alive and p._choice=='H':
                p.alive=False
                deaths_this_round.append(p)

        for p in players:
            if not p.alive:
                continue
            if p._choice=='L' and p._sabotage:
                p.gold*=2
            elif p._choice=='L':
                p.gold+=20

def deadlock_gui(p1,p2):
    btn_share=Button((120,420,220,80),"share",green)
    btn_steal=Button((380,420,220,80),"steal",red)

    def prompt(p):
        while True:
            screen.fill(bg)
            pygame.draw.rect(screen,card,(40,40,width-420,height-80),border_radius=10)
            draw_player_sidebar()

            screen.blit(txt(f"{p.name} — deadlock",big,yellow),(60,60))
            screen.blit(txt(f"gold: ${int(p.gold)}",font),(60,110))

            btn_share.draw(screen)
            btn_steal.draw(screen)

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit();sys.exit()
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    if btn_share.clicked(ev.pos):return "share"
                    if btn_steal.clicked(ev.pos):return "steal"

            clock.tick(fps)

    d1=prompt(p1)
    d2=prompt(p2)
    POT = 1000

    if d1=="share" and d2=="share":
        p1.gold+=POT//2
        p2.gold+=POT//2
    elif d1=="share" and d2=="steal":
        p2.gold+=POT
        p1.gold=0
    elif d1=="steal" and d2=="share":
        p1.gold+=POT
        p2.gold=0
    else:
        p1.gold//=2
        p2.gold//=2

def reveal_round():
    total_weight=applied_weight
    sabotagers=[p for p in players if p.alive and p._choice=='L' and p._sabotage]
    ded=', '.join(p.name for p in deaths_this_round) or 'none'

    while True:
        screen.fill(bg)
        pygame.draw.rect(screen,card,(40,40,width-420,height-80),border_radius=10)
        draw_player_sidebar()

        screen.blit(txt(f"round {round_num} — results",big,yellow),(60,60))
        y=110
        if total_weight>bridge_limit:
            screen.blit(txt("BRIDGE COLLAPSED!!!",font,red),(60,y));y+=26
        else:
            screen.blit(txt("BRIDGE INTACT!",font,green),(60,y));y+=26
        screen.blit(txt(f"bridge limit: {bridge_limit}",font),(60,y));y+=26
        screen.blit(txt(f"total weight on bridge: {total_weight}",font),(60,y));y+=26
        screen.blit(txt(f"light weight: {light_weight}",font),(60,y));y+=26
        screen.blit(txt(f"heavy weight: {heavy_weight}",font),(60,y));y+=26
        screen.blit(txt(f"sabotagers: {', '.join(p.name for p in sabotagers) or 'none'}",font,yellow),(60,y));y+=26
        screen.blit(txt(f"died this round: {ded}",font,red),(60,y));y+=36

        x1,x2,x3,x4=60,260,380,520
        screen.blit(txt("player",font,cream),(x1,y))
        screen.blit(txt("gold",font,cream),(x2,y))
        screen.blit(txt("choice",font,cream),(x3,y))
        screen.blit(txt("sabotage",font,cream),(x4,y))
        y+=26

        for p in players:
            c=green if p.alive else red
            screen.blit(txt(p.name,font,c),(x1,y))
            screen.blit(txt(f"${int(p.gold)}",font,yellow),(x2,y))
            screen.blit(txt(p._choice or "-",font,cream),(x3,y))
            screen.blit(txt("yes" if p._sabotage else "-",font,
                            yellow if p._sabotage else cream),(x4,y))
            y+=24

        screen.blit(txt("click or press any key to continue",font,cream),
                    (60,height-70))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit();sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN or ev.type==pygame.KEYDOWN:
                return

        clock.tick(fps)

def run_game():
    global players,light_weight,heavy_weight,bridge_limit,round_num
    intro_screen()
    players=player_setup_gui()
    round_num=0

    while True:
        alive=[p for p in players if p.alive]

        if len(alive)==0:
            return

        if len(alive)==1:
            w=alive[0]
            again=play_again_screen(f"{w.name} wins with ${int(w.gold)}!")
            return again

        if len(alive)==2:
            deadlock_gui(alive[0],alive[1])
            alive=[p for p in players if p.alive]
            alive.sort(key=lambda x:x.gold,reverse=True)
            if alive[0].gold == alive[1].gold:
                names = " and ".join(p.name for p in alive)
                again = play_again_screen(
                    f"It's a tie! {names} both win with ${int(alive[0].gold)}!"
                )
            else:
                w = alive[0]
                again = play_again_screen(
                    f"{w.name} wins with ${int(w.gold)}!"
                )

            return again
        
        round_num+=1
        light_weight=random.randint(*light_weight_range)
        heavy_weight=random.randint(*heavy_weight_range)
        bridge_limit=random.randint(4*len(alive)-3,12*len(alive)+3)

        for p in alive:
            get_choices_gui(p)

        evaluate_round()
        reveal_round()

#main game running loop
while True:
    again = run_game()
    if not again:
        pygame.quit()
        sys.exit()
