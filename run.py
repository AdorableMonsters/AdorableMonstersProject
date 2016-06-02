# -*- coding: utf-8 -*-
################################################################################
# 
# DEVELOPMENT PYTHON 3.5
#
# KEY USED:
# LEFT, RIGHT, UP AND DOWN FOR MOVING THE SHIP, SPACE FOR SHOOT, B FOR BOMB, P FOR PAUSE
# ESC FOR QUIT , F FOR FULLSCREEN
#
# DEVELOPED FOR A MASTER'S DEGREE IN APPLIED COMPUTER GRADUATION PROGRAM (PIPCA)
# AT UNISINOS UNIVERSITY, TO ATTEND THE TECHNIQUES OF PROGRAMMING CLASS.
#
# STUDENTS: Dienifer Karlini, Gilberto Luis Gonsioroski Junior, Karen Braga
# EMAILS: {dieniferkarlini, gilbertojun, karencbraga}@gmail.com
################################################################################
# import
import pygame,sys,random,os,datetime,math
from pygame.locals import *
from platform import system

from py import colors
from py import words

from sys import exit

OS = system().upper()
random.seed()

#_______________________________________________________________________________
# global variables

FPS=50
MODE=0
LANG=1 # 0 - English | 1 - Portuguese

#_______________________________________________________________________________
class AllMunition(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________________________________________________________________
class AllGun(pygame.sprite.RenderUpdates):

     def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________________________________________________________________
class AllAlien(pygame.sprite.RenderUpdates):

     def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________ ________________________________________________________
class AllGift(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________________________________________________________________
class AllBombAlien(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________________________________________________________________
class AllBombShip(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)        
#_______________________________________________________________________________
        
class Game():

    def __init__(self,width=800,height=600):

        pygame.init()

        # the dimensions of the Surface of the game
        self.width=width
        self.height=height
        self.size = width, height
        self.mode=0 # use to toggle fullscreen
        self.screen()

        pygame.mixer.set_num_channels(30)

        ########################################################################
        # Sounds
        ########################################################################
        self.sound_ship_expl=pygame.mixer.Sound("./sound/ship_explosion.wav")
        self.sound_ship_laser=pygame.mixer.Sound("./sound/ship_shot.wav")
        self.sound_intro_game=pygame.mixer.Sound("./sound/intro.ogg")  

        ########################################################################
        # Images
        ########################################################################
        # Array of the paths of the images for the aliens sprite 
        self.png=3*[""]

        self.png[0]=["./img/space1.png"]
        self.png[1]=["./img/space2.png"]
        self.png[2]=["./img/space3.png"]

        # Array of images (surface) for the aliens sprite 
        self.png2=[]

        # Load the images of the aliens
        i=0
        while i<len(self.png):
            self.pngs=[pygame.Surface]
            for j in range(1):
                self.pngs[j]=pygame.image.load(self.png[i][j]).convert_alpha()
            self.png2.append(self.pngs)
            i+=1

        # Array of images for the explosion of the aliens
        self.alien_explosion=[pygame.Surface] * 5
        i=1
        while i<6:
            path="./img/expl" + str(i) + ".png"
            #  Load images of aliens's explosions
            self.alien_explosion[i-1]=pygame.image.load(path).convert_alpha()
            i+=1

        # Load the Munitions of the ship
        self.munition01=pygame.image.load("./img/munition01.png").convert_alpha()
        self.munition02=pygame.image.load("./img/munition03.png").convert_alpha()
        self.munition03=pygame.image.load("./img/bomb_ship.png").convert_alpha()        

        # Load the bombs of the aliens
        self.alien_bomb10=pygame.image.load("./img/munition10.png").convert_alpha()

        # Load Boss's image
        self.boss=[pygame.Surface] * 3
        self.boss[0]=pygame.image.load("./img/boss01.png").convert_alpha()
        self.boss[1]=pygame.image.load("./img/boss02.png").convert_alpha()
        self.boss[2]=pygame.image.load("./img/boss03.png").convert_alpha()

        # ship
        # Load the images for the ship.
        self.ship01=pygame.image.load("./img/ship01.png").convert_alpha()
        
        # Load the images of the explosion of the ship
        self.ship_explosion=[pygame.Surface] * 4
        i=1
        while i<5:
            path="./img/expl" + str(i) + ".png"
            self.ship_explosion[i-1]=pygame.image.load(path).convert_alpha()
            i+=1

        # Background start
        self.bg2=pygame.image.load("./img/start"+str(LANG)+".png").convert_alpha()
        self.bgRect2=self.bg2.get_rect()

        # Background for scrolling
        self.bgscroll=pygame.image.load("./img/scroll.png").convert_alpha()

        # Background Intermediate
        self.bg=pygame.image.load("./img/inter"+str(LANG)+".png").convert_alpha()
        self.bgRect=self.bg.get_rect()

        # Background About
        self.bg3=pygame.image.load("./img/about"+str(LANG)+".png").convert_alpha()
        self.bgRect=self.bg3.get_rect()        

        # Various
        self.bomb=pygame.image.load("./img/bomb.png").convert_alpha() #bonus
        self.life_extra=pygame.image.load("./img/life.png").convert_alpha() #bonus
        self.power=pygame.image.load("./img/power.png").convert_alpha() #bonus
        self.trap=pygame.image.load("./img/trap.png").convert_alpha() #trap


        # Bomb boss
        self.bomb_boss01=pygame.image.load("./img/bomb_boss01.png").convert_alpha()
        self.bomb_boss02=pygame.image.load("./img/bomb_boss02.png").convert_alpha()

         # group's alien UFO
        self.allalien=AllAlien()

        # group's bombs for alien UFO
        self.allbombalien=AllBombAlien()

        # group's bombs for space ship
        self.allmunition=AllMunition()

        # group's surprises
        self.allgift=AllGift()
        
        # Group of guns
        self.allgun=AllGun()

        self.life=30 # Life
        self.level=1 # Level
        self.game_level = 3 #max number level

        self.bomb_ship=10
        self.nb_bomb_ship=0
        self.score=0

        # Clock for the Alien's shoots
        self.clock=pygame.time.Clock()

        # Clock for the Alien's shields
        #self.clock_shield=pygame.time.Clock()

        pygame.mouse.set_visible(False)        
        
    def screen(self,color=(0,0,0,)):

        # Definition of the main surface
        self.color=color
        self.surface= pygame.display.set_mode(self.size,MODE)
        pygame.display.set_caption(words.words[11][LANG])

    def play_sound(self,sound,loop=0):
        
        try:
            canal=pygame.mixer.find_channel(force=True)
            canal.stop()
            canal.play(sound,loop)
        except:
            sound.play(loop)
            pass
        
    def toogle(self):
        global MODE

        # switch display between windowed and full screen
        if MODE==0:
            MODE=FULLSCREEN
        else:
            MODE=0
        s=self.surface.copy()
        self.surface= pygame.display.set_mode(self.size,MODE)
        self.surface.blit(s,s.get_rect())
        pygame.display.update()

    ########################################################################
    # Add ufo sprite
    ########################################################################

    def add_alien(self,nb_alien=0,nb_alien_max=10):
        self.nb_alien=nb_alien
        self.nb_alien_max=nb_alien_max
        if self.nb_alien<self.nb_alien_max:
            self.nb_alien+=1
        else:
            self.nb_alien=1
            
        # list of coordinates for abscissa
        valy=[44,64,96,128,160]
        valx=[]
        i=0
        
        # Fills the ordinates by step of 32 pixels
        while i<=600:
            valx.append(int(i))
            i+=32
        i=0
        while i<self.nb_alien:

            # Choose coordenates
            y=random.sample(valy,1)
            x=random.sample(valx,1)

            # Create an alien
            objet_alien=Alien(x[0],y[0])

            valx.remove(x[0])
            i+=1

    def update(self,zone):
        # update a zone of main surface
        self.zone=zone
        pygame.display.update(self.zone)

    def raz(self):
        self.surface.fill(colors.BLACK)

    def empty(self):

        # Erase all fire of the ship
        self.allmunition.empty()
        
        # Erase all the bomb of the aliens
        self.allbombalien.empty()
        
        # Erase all the aliens
        self.allalien.empty()
        
        # Stop the sounds
        pygame.mixer.stop()
        
        #self.nb_extra_bomb=0
        self.nb_bomb_ship=0

    def pause(self):
        pause=0
        pygame.event.clear(KEYDOWN)
        e=pygame.event.Event(KEYDOWN,key=K_n)
        while pause!=1:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key==112: #p
                        pause=1
                    elif e.key==97 or e.key==113 or e.key==27: #a,enter,esc
                        self.break_high=True
                        pause=1
            pygame.time.wait(100)


    def end(self):
        '''
        Used to display the end mensagem 
        '''

        self.surface.fill(colors.BLACK)
        pygame.display.flip()
       
        font = pygame.font.Font(None, 24)
        
        if game.life == 0:
            self.text1 = font.render(words.words[9][LANG], 1, colors.WHITE,colors.BLACK)
        else:
            self.text1 = font.render(words.words[10][LANG], 1, colors.WHITE,colors.BLACK)

        self.text1pos=self.text1.get_rect()
        x=(self.width/2)-(self.text1pos.width/2) #center
        y=(self.height/2)-(self.text1pos.height/2) #center
        self.text1pos=self.text1pos.move(x,y)
        self.surface.blit(self.text1,self.text1pos)
        self.update(self.text1pos)
        pygame.time.delay(3000)

###__________________________________________________________________________________________________
class Info(pygame.sprite.Sprite):

    global OS

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 24)
        
        self.image=pygame.Surface((800,20))
        self.rect=self.image.get_rect()

        # Array of character use for display Extra Life
        self.timer=-1
        pygame.time.set_timer(USEREVENT+1, 300)

    def update(self):

        # The informations of the gamer
        #top
        self.text1 = self.font.render(words.words[3][LANG] + str(game.level) + "  " , 1, colors.WHITE,colors.BLACK)
        self.textpos1 = self.text1.get_rect()
        self.image.blit(self.text1, self.textpos1)

        self.text2 = self.font.render(words.words[4][LANG]+ str(game.life) + "  " , 1, colors.WHITE,colors.BLACK)
        self.textpos2 = self.text2.get_rect()
        self.textpos2 =self.textpos2.move(90,0)
        self.image.blit(self.text2, self.textpos2)

        self.text3 = self.font.render(words.words[5][LANG] + str(game.bomb_ship) + "  ",1,colors.WHITE,colors.BLACK)
        self.textpos3 = self.text3.get_rect()
        self.textpos3 = self.textpos3.move(180,0)
        self.image.blit(self.text3, self.textpos3)

        try:
            self.text4 = self.font.render(words.words[6][LANG] + str(ship.power) + "  ",1,colors.WHITE,colors.BLACK)
        except:
             self.text4 = self.font.render(words.words[6][LANG] ,1,colors.GREEN,colors.BLACK)
        self.textpos4 = self.text4.get_rect()
        self.textpos4 = self.textpos4.move(300,0)
        self.image.blit(self.text4, self.textpos4)

        self.text5 = self.font.render(words.words[7][LANG]+ str(game.score)+"  ",1, colors.WHITE,colors.BLACK)
        self.textpos5 = self.text5.get_rect()
        self.textpos5 = self.textpos5.move(400,0)
        self.image.blit(self.text5, self.textpos5)


#__________________________________________________________________________________________________

class Bg (pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=game.bgscroll
        self.rect=self.image.get_rect()

    def update(self):

       # For remenber : Height of info 
       self.rect.bottom += 1
       if self.rect.bottom >= self.rect.height:
           self.rect.top=-(self.rect.height-600)


#__________________________________________________________________________________________________

class BgInter (pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=game.bg
        self.rect=self.image.get_rect()


#__________________________________________________________________________________________________

class BgAbout (pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=game.bg
        self.rect=self.image.get_rect()
        
#_____________________________________________________
class Alien(pygame.sprite.Sprite):

    def __init__(self,lig,col,extra=False):

        pygame.sprite.Sprite.__init__(self)

        game.allalien.add(self)
        self.indexplosion=0
        self.exploded=False
        self.grow=1 # used for grow or shrink the alien 
        
        # Time for the shoots
        self.time_for_shoot=random.randint(0,2000)

        # Time for the shield
        self.time_for_shield=random.randint(0,2000)

        if(game.level-1 <= 3):
            self.fond=game.png2[game.level-1]
        else:    
            self.fond=game.png2[0]
        
        # the first image is use to define rect and image property, necessary in class sprite
        self.image=self.fond[0]
        self.rect=self.fond[0].get_rect()
        
        # Flag used to determine which image is blitted
        self.indice_image=-1
        self.r=32

        # coordinates of birth
        self.x=lig
        self.y=col

        # Positioning on the screen 
        self.rect.top=self.y
        self.rect.left=self.x

        # Some aliens can have a surprise
        self.gift=False
        self.gift_type=0

        # lottery for ADN
        gift=random.randint(0,200)
        
        #--------------------------------------------------------------------------------------
        # gift bonus
        #--------------------------------------------------------------------------------------
        if game.level<=3: # under level 3
       
            # The bonus
            if gift==10: 
                # life
                self.gift=True
                self.gift_type=0
                
            elif gift>=20 and gift<30:
                # bomb for space ship
                self.gift=True
                self.gift_type=1

            elif gift==100:
                 # Power
                self.gift=True
                self.gift_type=2
                
            elif gift>=50 and gift<=60:
                 # Trap - Bomb Alien
                self.gift=True
                self.gift_type=3
                
            else:
                self.gift=False
                self.gift_type=99
            
        self.coup=0

        self.sensx=random.sample([-1,1],1)[0] # horizontal movement
        self.sensy=0 # at this step no vertical movement


    def update(self,pas=4):

        self.time_for_shoot+=game.clock.get_time()
        #self.time_for_shield+=game.clock_shield.get_time()
        #print(self.time_for_shield)
        
                
        ##################################################################################      
        # Alien shoot a bomb after a duration
        ##################################################################################
                 
        if self.time_for_shoot>=3000 and game.level<=3:
            self.time_for_shoot=0
            bomb=BombAlien(self.rect)
            game.allbombalien.add(bomb)
            
            
        self.pas=pas
        
        # loop for the images to display
        if self.indice_image<len(self.fond)-1:
            self.indice_image+=1
            self.image=self.fond[self.indice_image]
        else:
            self.indice_image=-1

        # determine the movement of the alien 
        ########################################################################
        # Here is the section to handle the movements
        ########################################################################

        if self.rect.right>=game.width:
            self.sensx=-1
        elif self.rect.left<=0:
            self.sensx=1

        self.rect=self.rect.move(pas*self.sensx,self.sensy)

        # test if an collision between ship and alien appears
        if self.rect.colliderect(ship.rect):
            self.coup=99
            if self.exploded==False: # Mean it collide the ship
                ship.explosion()
                self.exploded=True

        if self.coup>=game.level:       
            if self.indexplosion<5:
                self.image=game.alien_explosion[self.indexplosion]
                self.indexplosion+=1
            else:
                self.indexplosion=-1
                game.score+=1*game.level
                game.allalien.remove(self)
                self.explosion()
                if len(game.allalien)==0:
                    game.nb_bomb_ship=0
            
    def explosion(self):
        if self.gift==True:
            bonus=Gift(self.gift_type,self.rect.top,self.rect.right)
            game.allgift.add(bonus)

#_______________________________________________________________________________
class Gift(pygame.sprite.Sprite):

    def __init__(self,type_gift,top,right):

        pygame.sprite.Sprite.__init__(self)

        self.type_gift=type_gift
        
        if self.type_gift==0:
            self.image=game.life_extra
        elif self.type_gift==1:
            self.image=game.bomb
        elif self.type_gift==2:
            self.image=game.power
        elif self.type_gift==3:
            self.image=game.trap
       

        self.rect=self.image.get_rect()
        self.rect.top=top
        self.rect.right=right

    def update(self):

        # set the limit of the fall for the surprises
        limite=590

        # fall of the object
        if self.rect.top<limite:
            self.rect=self.rect.move(0,4)
        else:
            self.kill()

            # if the suprise is a trap (tnt), explosion at the end of the downfall
            if self.type_gift==3:
               trap=Trap(self.rect.top,self.rect.right)

        # collide surprises and ship
        if self.rect.colliderect(ship.rect):
            # life
            if self.type_gift==0:
                game.life+=1
                game.score+=100
                
            # bomb
            elif self.type_gift==1:
                game.bomb_ship+=1
                game.score+=50
                
            # Power
            elif self.type_gift==2:
                game.score+=25
                ship.power+=1
                game.score+=25

             # TNT    
            elif self.type_gift==3:
                game.life-=1
                ship.explosion()
               
            self.kill()
###_______________________________________________________________________________
class Trap(pygame.sprite.Sprite):

    def __init__(self,top,right):

        pygame.sprite.Sprite.__init__(self)

        self.rect=game.trap.get_rect()

        self.rect.top=top
        self.rect.right=right+96
        self.update()
        touch=False
        
        game.update(self.rect) 

        # Test collision between ship and trap (tnt)
        if self.rect.colliderect(ship.rect):
                touch=True
                
        if touch==True:
            ship.protected-=6

            if ship.protected<=0:
                self.kill()
                ship.explosion()
            info.shield.fill(colors.BLACK)

        pygame.time.delay(30)

#_______________________________________________________________________________
class BombAlien (pygame.sprite.Sprite):

    def __init__(self,rect):

        # Rect is the rect of the alien
        pygame.sprite.Sprite.__init__(self)

        # Load the image of the bomb
        self.image=game.alien_bomb10
        self.rect=self.image.get_rect()
        
        # display the bomb under the alien
        x=(rect.width-self.rect.width)/2
        self.rect=self.rect.move(rect.left+x,rect.top+32)

    def update(self):

        if game.level<=3:
            stepx=0
            stepy=3

        self.rect=self.rect.move(stepx,stepy)
        if self.rect.top>600:
            self.kill()

        if self.rect.colliderect(ship.rect):
            ship.protected-=1

            self.kill()
            # Test if the ship is exploded
            if ship.protected<0:
               ship.explosion()
                     

#_______________________________________________________________________________        
class Ship(pygame.sprite.Sprite):

    def __init__ (self):

        pygame.sprite.Sprite.__init__(self)

        self.power=1
        self.protected=0 # the shield 
        self.ship_explosion=[pygame.Surface] * 4
        self.image=game.ship01
        self.rect=self.image.get_rect()
        
      
    def pos(self,x,y):
        self.rect=self.rect.move(x,y)

    def raz(self):
        self.rect.top=0
        self.rect.right=0
        self.pos(304,530)
        game.surface.blit(self.image,self.rect)

    def update(self):
                
        self.image=game.ship01
        if self.power>6:
            self.power = 5
        
        test=pygame.key.get_pressed()
        
        if test[pygame.K_SPACE]: 
            self.shoot_ship()

        if test[pygame.K_LEFT]:
            if self.rect.left>0:
                self.rect.left-=8
            if test[pygame.K_SPACE]:
                self.shoot_ship()

        if test[pygame.K_RIGHT]:
            if self.rect.right<800:
                self.rect.left+=8
            if test[pygame.K_SPACE]:
                self.shoot_ship()

        if test[pygame.K_UP]:
            if self.rect.top>40:
                self.rect.top-=8
            if test[pygame.K_SPACE]:
                self.shoot_ship()

        if test[pygame.K_DOWN]:
            if self.rect.top<530:
                self.rect.top+=8
            if test[pygame.K_SPACE]:
                self.shoot_ship()

    def shoot_ship(self):

        # the fire of the ship
        if self.power==1:
            self.power1(5)
            self.image=game.ship01
            
        elif self.power==2:
             self.power2(15)
             self.image=game.ship01

        elif self.power>=3:
            self.power3(25)
            self.image=game.ship01

        
    def power1(self,nb_munition):
        if len(game.allmunition)<nb_munition:
            munition=Munition(1,14)
            game.allmunition.add(munition)

    def power2(self,nb_munition):

        if len(game.allmunition)<nb_munition:
            self.power1(nb_munition)
            munition=Munition(2,4)
            game.allmunition.add(munition)
            munition=Munition(2,24)
            game.allmunition.add(munition)

    def power3(self,nb_munition):

        if len(game.allmunition)<nb_munition:
            self.power1(nb_munition)
            self.power2(nb_munition)
            munition=Munition(2,0)
            game.allmunition.add(munition)
            munition=Munition(2,31)
            game.allmunition.add(munition)

    #shoot bomb   
    def bomb_ship(self):
        if game.bomb_ship > 0 and game.nb_bomb_ship==0:
            game.nb_bomb_ship=1
            game.bomb_ship-=1
            munition=Munition(3,0)
            game.allmunition.add(munition)

         
    # ship's explosion
    def explosion(self):
        
        if self.protected<=0:
            self.protected=random.randint(2,9)
        if self.power>1:
            self.power-=1
        else:
            self.power=1
        game.life-=1
        for image in game.ship_explosion:
            game.surface.blit(image,self.rect)
            game.update(self.rect) 
            game.play_sound(game.sound_ship_expl)
            pygame.time.delay(50)

#_______________________________________________________________________________
class Munition(pygame.sprite.Sprite):

    def __init__(self,type,pos):

        pygame.sprite.Sprite.__init__(self)
        
        self.type=type
        self.pos=pos
        self.sens=self.sens2=1
        
        if self.type==1:
            self.image=game.munition01
        elif self.type==2:
            self.image=game.munition02
        elif self.type==3:
            self.image=game.munition03            
           
            
        self.rect=self.image.get_rect()

        # Blit the munition onto the ship
        self.rect.left=ship.rect.left
        self.rect=self.rect.move(self.pos,ship.rect.top-2)
        game.surface.blit(self.image,self.rect)

    def update(self):
        
        if self.type>=1 and self.type<=3:
            self.rect=self.rect.move(0,-16)
            game.play_sound(game.sound_ship_laser)

        if self.rect.top<32 or self.rect.left<1 or self.rect.left>game.width:
            self.kill()

        # Collision test with Alien with fire!!!
        test=pygame.sprite.spritecollide(self,game.allalien,0, collided = None)
        if (test!=[]):
            for alien in test:
                    game.score+=1*game.level
                    if self.type<=3:
                        alien.coup+=1
                    else:
                        alien.coup=game.level

        # Section to test collision with the Boss
        try:

            if self.rect.colliderect(boss.rect):
                if self.type==1 or self.type==2:
                    boss.force-=10
                elif self.type==3: #bomb
                    boss.force-=30
                
                game.score+=10
                self.kill()
                if boss.force<=0:
                    boss.explosion()

        except:
            pass

#_______________________________________________________________________________
class Boss(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=game.boss[game.level-1]
        self.rect=self.image.get_rect()
        self.rect= self.rect.move(320,100)
        self.force=game.level*100
        self.time_for_shoot=0
        self.coup=0
        self.sensx=4
        self.sensy=4
        self.grow=1 # used for grow or shrink the 


    def moves(self):

        font = pygame.font.Font(None, 16)
        spaces=32*" "
        self.info = font.render(spaces+words.words[12][LANG]+ str(self.force) + spaces, 1, colors.WHITE,colors.RED)
        self.infoRect=self.info.get_rect()
        self.infoRect.top=23
        self.infoRect.left=((game.width-self.infoRect.width)/2)
        
        # Blit force info
        if self.force>=0:
            game.surface.blit(self.info, self.infoRect)

        # Refresh clock for shoot
        self.time_for_shoot+=game.clock.get_time()

        if self.rect.right>=game.width:
            self.sensx=-4
        elif self.rect.left<=0:
            self.sensx=4
        if self.rect.top<50:
            self.sensy=4
        elif self.rect.top>=250:
            self.sensy=-4
        self.rect=self.rect.move(self.sensx,self.sensy)

        if self.rect.width<=24:
            self.grow=-1
        elif self.rect.width>=64:
            self.grow=1

        self.rect.width-=self.grow
        self.rect.height-=self.grow

        # Blit boss
        game.surface.blit(self.image, self.rect)

        # Test if it's the moment to shoot
        tps=700-(game.level*25)
        if self.time_for_shoot>tps:
            self.time_for_shoot=0
            bomb=BombBoss(random.randint(1,2))
            game.allbombalien.add(bomb)

    def explosion(self):
        game.surface.blit(game.bg,self.rect,self.rect)
        #game.update(self.rect)
        game.score+=50*game.level
        self.kill()
#_______________________________________________________________________________
class BombBoss(pygame.sprite.Sprite):

    def __init__(self,id):

        pygame.sprite.Sprite.__init__(self)

        # Set the speed of the fall of the bombs
        if game.level<=2:
            multi=1
        else:
            multi=2

        self.id=id

        if self.id==1:
            self.image=game.bomb_boss01
            self.sensx=random.randint(-4*multi,4*multi)
        elif self.id==2:
            self.image=game.bomb_boss02
            self.sensx=0

        self.rect=self.image.get_rect()

        # display under the boss
        self.rect=self.rect.move(boss.rect.left+32,boss.rect.top+64)
        game.surface.blit(self.image,self.rect)


    def update(self):

        if self.rect.right>=game.width:
            self.sensx=-1*self.sensx
        elif self.rect.left<=0:
            self.sensx=-1*self.sensx

        self.rect=self.rect.move(self.sensx,4)
        game.surface.blit(self.image,self.rect)

        if self.rect.top>590 and self.id==1:
            game.allbombalien.remove(self)
        elif self.rect.top>590 and self.id==2:
            game.allbombalien.remove(self)
            trap=Trap(self.rect.top,self.rect.right)

        if self.rect.colliderect(ship.rect):
            self.kill()
            ship.explosion()



#-------------------------------------------------------------------------------
#                              end classes
#_______________________________________________________________________________

def keyboard():

  # Keyboard
  pygame.event.get(pygame.KEYDOWN)

  if pygame.key.get_pressed()[K_SPACE]:
      ship.update()
  elif pygame.key.get_pressed()[112]: #p
      game.pause()
  elif pygame.key.get_pressed()[98]: # b
      ship.bomb_ship()
  elif pygame.key.get_pressed()[K_ESCAPE]:
      pygame.quit()
      sys.exit()
  elif pygame.key.get_pressed()[K_f]:
      game.toogle()
  else:
       ship.update()
       game.nb_bomb_ship=0


#-------------------------------------------------------------------------------
#                              End functions
#_______________________________________________________________________________

game=Game()
game.play_sound(game.sound_intro_game)

# Main loop
fin=False
while fin==False:

    # Menu loop
    pygame.font.init()
    choice=-1

    #start menu
    while choice!=0:
        
        pygame.time.Clock().tick(FPS)
        game.surface.blit(game.bg2,game.bgRect2)
        game.update(game.bgRect2)

        pygame.event.get(pygame.KEYDOWN)

        if pygame.key.get_pressed()[K_ESCAPE]:
          choice=0
          pygame.quit()
          sys.exit()
        elif pygame.key.get_pressed()[13]: #enter          
          choice=0
        elif pygame.key.get_pressed()[97]: #a
          choice=1          

          #---------------------------------------------------------------------------
          # About Screen.
          #---------------------------------------------------------------------------
          bg=BgAbout()
          bg = pygame.sprite.RenderPlain((bg))
          game.surface.blit(game.bg3,game.bgRect)
          game.update(game.bgRect)
          pygame.time.wait(5000)          

     
    #---------------------------------------------------------------------------
    # The Game
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # Intermediate Screen.
    #---------------------------------------------------------------------------
    bg=BgInter()
    bg = pygame.sprite.RenderPlain((bg))

    game.surface.blit(game.bg,game.bgRect)
    game.update(game.bgRect)
    pygame.time.wait(3000)
    game.sound_intro_game.stop()


    #---------------------------------------------------------------------------
    # Game Start
    #---------------------------------------------------------------------------
    pygame.key.set_repeat(1,1)

    # the ship
    ship=Ship()
    ship.raz()
    sens=1

    # Add the first alien , the max number of the aliens is set to 15. It's due
    # at my method to set the intersection between them :
      #
    game.add_alien(0,10)
    '''
    game.nb_alien=1
    game.nb_alien_max=0
    '''
    bg=Bg()
    bg = pygame.sprite.RenderPlain((bg))

    info=Info()
    allinfo=pygame.sprite.RenderPlain(info)

    # Game loop
    while(game.life>0 and game.level <= game.game_level):

        game.clock.tick(FPS)
        keyboard()

        if len(game.allalien)!=0:

            # Background
            bg.update()
            bg.draw(game.surface)

            # ship
            game.surface.blit(ship.image,ship.rect)
            game.allgun.update()
            game.allgun.draw(game.surface)

            # alien
            game.allalien.update()
            game.allalien.draw(game.surface)

            # bomb of the Aliens
            game.allbombalien.update()
            game.allbombalien.draw(game.surface)

            # fire of the ship
            game.allmunition.update()
            game.allmunition.draw(game.surface)

            # surprise
            game.allgift.update()
            game.allgift.draw(game.surface)

            allinfo.update()
            allinfo.draw(game.surface)

            pygame.display.update()

        elif len(game.allalien)==0 and game.nb_alien<game.nb_alien_max:

            game.add_alien(game.nb_alien,game.nb_alien_max)

            # game level
        elif game.level<=game.game_level :

            game.nb_alien=0

            ####################################################################
            # BOSS LEVEL
            ####################################################################

            game.empty()
            ship.raz()
            fin=False
            boss=Boss()
    
            while boss.force>0 and game.life>0:
                game.clock.tick(FPS)

                # Background
                bg.update()
                bg.draw(game.surface)

                # ship
                game.surface.blit(ship.image,ship.rect)
                game.allgun.update()
                game.allgun.draw(game.surface)

                # fire of the ship
                game.allmunition.update()
                game.allmunition.draw(game.surface)

                # Movement of bomb of the boss
                game.allbombalien.update()
                game.allbombalien.draw(game.surface)

                #game.info()
                allinfo.update()
                allinfo.draw(game.surface)

                # Boss move
                boss.moves()

                keyboard()

                pygame.display.update()

            boss = None

            game.raz()
            if game.life!=0:
                game.level+=1

            # Last level is reached, so go to level 1 and loop
            # Adorable Monsters is stronger than you !
        else:
            game.nb_alien=0
            game.level=1
            

    #END
    game.empty()
    game.end()
    game.__init__()
