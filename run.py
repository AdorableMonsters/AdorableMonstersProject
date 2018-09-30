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
import pygame,sys,random,datetime
from pygame.locals import *

from py import colors
from py import words

#_______________________________________________________________________________
# global variables

FPS=50
MODE=0
LANG=0 # 0 - English | 1 - Portuguese

#_______________________________________________________________________________
class AllMunition(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________________________________________________________________
class AllAlien(pygame.sprite.RenderUpdates):
     def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)
#_______________________ ________________________________________________________
class AllBonus(pygame.sprite.RenderUpdates):
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

        pygame.mixer.set_num_channels(30)  #Create a Channel object for controlling playback

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
            self.pngs=[pygame.Surface] #pygame object for representing images. Call pygame.Surface() to create a new image object
            for j in range(1):
                self.pngs[j]=pygame.image.load(self.png[i][j]).convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
            self.png2.append(self.pngs)
            i+=1

        # Array of images for the explosion of the aliens
        self.alien_explosion=[pygame.Surface] * 5 #pygame object for representing images. Call pygame.Surface() to create a new image object
        i=1
        while i<6:
            path="./img/expl" + str(i) + ".png"
            #  Load images of aliens's explosions
            self.alien_explosion[i-1]=pygame.image.load(path).convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
            i+=1

        # Load the Munitions of the ship
        self.munition01=pygame.image.load("./img/munition01.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.munition02=pygame.image.load("./img/munition02.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.munition03=pygame.image.load("./img/bomb_ship.png").convert_alpha()   #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency     

        # Load the Munition of the aliens
        self.alien_munition=pygame.image.load("./img/munition10.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency

        # Load Boss's image
        self.boss=[pygame.Surface] * 3 #pygame object for representing images. Call pygame.Surface() to create a new image object
        self.boss[0]=pygame.image.load("./img/boss01.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.boss[1]=pygame.image.load("./img/boss02.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.boss[2]=pygame.image.load("./img/boss03.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency

        # ship
        # Load the images for the ship.
        self.ship=pygame.image.load("./img/ship.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        
        # Load the images of the explosion of the ship
        self.ship_explosion=[pygame.Surface] * 4  #pygame object for representing images. Call pygame.Surface() to create a new image object
        i=1
        while i<5:
            path="./img/expl" + str(i) + ".png"
            self.ship_explosion[i-1]=pygame.image.load(path).convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
            i+=1

        # Background start
        self.bg2=pygame.image.load("./img/start"+str(LANG)+".png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.bgRect2=self.bg2.get_rect()

        # Background for scrolling - bacground the game
        self.bgscroll=pygame.image.load("./img/scroll.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency

        # Background Intermediate
        self.bg=pygame.image.load("./img/inter"+str(LANG)+".png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.bgRect=self.bg.get_rect()

        # Background About
        self.bg3=pygame.image.load("./img/about"+str(LANG)+".png").convert_alpha() #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.bgRect=self.bg3.get_rect()        

        # Various - bonus and trap
        self.bomb=pygame.image.load("./img/bomb.png").convert_alpha() #bonus #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.life_extra=pygame.image.load("./img/life.png").convert_alpha() #bonus #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.power=pygame.image.load("./img/power.png").convert_alpha() #bonus #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.trap=pygame.image.load("./img/trap.png").convert_alpha() #trap #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency


        # Bomb boss
        self.bomb_boss01=pygame.image.load("./img/bomb_boss01.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency
        self.bomb_boss02=pygame.image.load("./img/bomb_boss02.png").convert_alpha()  #load new image from a file. convert_alpha() method after loading so that the image has per pixel transparency

        # group's alien UFO
        self.allalien=AllAlien()

        # group's bombs for alien UFO
        self.allbombalien=AllBombAlien()

        # group's bombs for space ship
        self.allmunition=AllMunition()

        # group's bonus
        self.allbonus=AllBonus()

        #variables
        self.life=30 # Life
        self.level=1 # Level
        self.game_level = 2 #max number level

        self.bomb_ship=10
        self.nb_bomb_ship=0  #flag
        self.score=0

        # Clock for the Alien's shoots
        self.clock=pygame.time.Clock()  #create an object to help track time. Creates a new Clock object that can be used to track an amount of time. The clock also provides several functions to help control a game’s framerate

        #disable mouse
        pygame.mouse.set_visible(False)        

        
    def screen(self,color=colors.BLACK):

        # Definition of the main surface
        self.color=color
        self.surface= pygame.display.set_mode(self.size,MODE) #Initialize a window or screen for display 
        pygame.display.set_caption(words.words[11][LANG])  #Set the current window caption


    def play_sound(self,sound,loop=0):
        sound.play(loop) #Begin playback of the Sound
        
    def toogle(self):
        global MODE

        # switch display between windowed and fullscreen
        if MODE==0:
            MODE=FULLSCREEN
        else:
            MODE=0
            
        self.surface=pygame.display.set_mode(self.size,MODE) #Initialize a window or screen for display
        self.surface.blit(self.surface,self.surface.get_rect()) #draw one image onto another
        pygame.display.flip()  #Update the full display Surface to the screen


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
        pygame.display.update(self.zone)  #Update portions of the screen for software displays


    def empty(self):

        # Erase all fire of the ship
        self.allmunition.empty()
        
        # Erase all the bomb of the aliens
        self.allbombalien.empty()
        
        # Erase all the aliens
        self.allalien.empty()
        
        # Stop the sounds
        pygame.mixer.stop()
        
        # Erase bomb ship
        self.nb_bomb_ship=0


    def pause(self):
        pause=0
        pygame.event.clear(KEYDOWN)  #remove all events from the queue
        e=pygame.event.Event(KEYDOWN,key=K_n) #create a new event object
        while pause!=1:
            for e in pygame.event.get(): #get events from the queue
                if e.type == pygame.KEYDOWN:  #event type
                    if e.key==112: #p
                        pause=1
                    elif e.key==97 or e.key==113 or e.key==27: #a,enter,esc
                        self.break_high=True
                        pause=1
            pygame.time.wait(100)  #pause the program for an amount of time



    def end(self):
        '''
        Used to display the end mensagem 
        '''

        self.surface.fill(colors.BLACK)  #fill Surface with a solid color
        pygame.display.flip()  #Update the full display Surface to the screen
       
        font = pygame.font.Font(None, 24)  #create a new Font object from a file
        
        if game.life == 0:
            self.text1 = font.render(words.words[9][LANG], 1, colors.WHITE,colors.BLACK)  #draw text on a new Surface. sintax: render(text, antialias, color, background=None)
        else:
            self.text1 = font.render(words.words[10][LANG], 1, colors.WHITE,colors.BLACK)

        self.text1pos=self.text1.get_rect()  #get the rectangular area of the Surface
        x=(self.width/2)-(self.text1pos.width/2) #center
        y=(self.height/2)-(self.text1pos.height/2) #center
        self.text1pos=self.text1pos.move(x,y)
        self.surface.blit(self.text1,self.text1pos)  #draw one image onto another
        self.update(self.text1pos) 
        pygame.time.wait(3000)  #pause the program for an amount of time

###__________________________________________________________________________________________________
class Info(pygame.sprite.Sprite):

    def __init__(self):

        ## ------- pygame.sprite.Sprite is simple base class for visible game objects
        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor
        self.font = pygame.font.Font(None, 24)  #create a new Font object from a file
        
        self.image=pygame.Surface((800,20))  #pygame object for representing images. The Surface has a fixed resolution and pixel format
        self.rect=self.image.get_rect()  #get the rectangular area 


    def update(self):

        # The informations of the gamer
        #top
        self.text1 = self.font.render(words.words[3][LANG] + str(game.level) + "  " , 1, colors.WHITE,colors.BLACK)
        self.textpos1 = self.text1.get_rect()  #get the rectangular area 
        self.image.blit(self.text1, self.textpos1)  #draw one image onto another

        self.text2 = self.font.render(words.words[4][LANG]+ str(game.life) + "  " , 1, colors.WHITE,colors.BLACK)
        self.textpos2 = self.text2.get_rect() #get the rectangular area 
        self.textpos2 =self.textpos2.move(90,0) #position
        self.image.blit(self.text2, self.textpos2)  #draw one image onto another

        self.text3 = self.font.render(words.words[5][LANG] + str(game.bomb_ship) + "  ",1,colors.WHITE,colors.BLACK)
        self.textpos3 = self.text3.get_rect() #get the rectangular area 
        self.textpos3 = self.textpos3.move(180,0) #position
        self.image.blit(self.text3, self.textpos3)  #draw one image onto another

        try:
            self.text4 = self.font.render(words.words[6][LANG] + str(ship.power) + "  ",1,colors.WHITE,colors.BLACK)
        except:
             self.text4 = self.font.render(words.words[6][LANG] ,1,colors.GREEN,colors.BLACK)
        self.textpos4 = self.text4.get_rect() #get the rectangular area
        self.textpos4 = self.textpos4.move(300,0) #position
        self.image.blit(self.text4, self.textpos4)  #draw one image onto another

        self.text5 = self.font.render(words.words[7][LANG]+ str(game.score)+"  ",1, colors.WHITE,colors.BLACK)
        self.textpos5 = self.text5.get_rect() #get the rectangular area
        self.textpos5 = self.textpos5.move(400,0) #position
        self.image.blit(self.text5, self.textpos5)  #draw one image onto another


#__________________________________________________________________________________________________

class Bg (pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor
        self.image=game.bgscroll
        self.rect=self.image.get_rect()  #get the rectangular area

    def update(self):

       # scroll background 
       self.rect.bottom += 1
       if self.rect.bottom >= self.rect.height:
           self.rect.top=-(self.rect.height-600)

#_____________________________________________________
class Alien(pygame.sprite.Sprite):

    def __init__(self,lig,col,extra=False):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        game.allalien.add(self)
        self.indexplosion=0
        self.exploded=False
        self.grow=1 # used for grow or shrink the alien 
        
        # Time for the shoots
        self.time_for_shoot=random.randint(0,2000)

        #Alien's image
        self.fond=game.png2[game.level-1]

        # the first image is use to define rect and image property, necessary in class sprite
        self.image=self.fond[0]
        self.rect=self.fond[0].get_rect() #get the rectangular area
        
        # Flag used to determine which image is blitted
        self.indice_image=-1
        self.r=32

        # coordinates of birth
        self.x=lig
        self.y=col

        # Positioning on the screen 
        self.rect.top=self.y
        self.rect.left=self.x

        # Some aliens can have a surprise - bonus
        self.bonus=False
        self.bonus_type=0

        # lottery for ADN
        bonus=random.randint(0,200)
        
        #--------------------------------------------------------------------------------------
        # bonus
        #--------------------------------------------------------------------------------------
        if game.level<=3: # under level 3
       
            # The bonus
            if bonus==10: 
                # life
                self.bonus=True
                self.bonus_type=0
                
            elif bonus>=20 and bonus<30:
                # bomb for space ship
                self.bonus=True
                self.bonus_type=1

            elif bonus>=100 and bonus<105:
                 # Power
                self.bonus=True
                self.bonus_type=2
                
            elif bonus>=50 and bonus<=60:
                 # Trap - Bomb Alien
                self.bonus=True
                self.bonus_type=3
                
            else:
                self.bonus=False
                self.bonus_type=99
            
        self.coup=0

        self.sensx=random.sample([-1,1],1)[0] # horizontal movement
        self.sensy=0 # at this step no vertical movement


    def update(self,pas=4):

        self.time_for_shoot+=game.clock.get_time()  #time used in the previous tick
        
                
        ##################################################################################      
        # Alien shoot a munition after a duration
        ##################################################################################
                 
        if self.time_for_shoot>=3000 and game.level<=game.game_level:
            self.time_for_shoot=0
            munition=BombAlien(self.rect)
            game.allbombalien.add(munition)
            
            
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

        self.rect=self.rect.move(pas*self.sensx,self.sensy) #position

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
                game.allalien.remove(self)  	#remove the sprite from groups
                self.explosion()
                if len(game.allalien)==0:
                    game.nb_bomb_ship=0
            
    def explosion(self):
        if self.bonus==True:
            bonus=Bonus(self.bonus_type,self.rect.top,self.rect.right)
            game.allbonus.add(bonus)

#_______________________________________________________________________________
class Bonus(pygame.sprite.Sprite):

    def __init__(self,type_bonus,top,right):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        self.type_bonus=type_bonus
        
        if self.type_bonus==0:
            #life
            self.image=game.life_extra
        elif self.type_bonus==1:
            #bomb
            self.image=game.bomb
        elif self.type_bonus==2:
            #power
            self.image=game.power
        elif self.type_bonus==3:
            #trap
            self.image=game.trap
       

        self.rect=self.image.get_rect() #get the rectangular area
        self.rect.top=top
        self.rect.right=right

    def update(self):

        # set the limit of the fall for the surprises
        limite=590

        # fall of the object
        if self.rect.top<limite:
            self.rect=self.rect.move(0,4) #position
        else:
            self.kill()

            # if the suprise is a trap (tnt), explosion at the end of the downfall
            if self.type_bonus==3:
               trap=Trap(self.rect.top,self.rect.right)

        # collide surprises and ship
        if self.rect.colliderect(ship.rect):
            # life
            if self.type_bonus==0:
                game.life+=1
                game.score+=100
                
            # bomb
            elif self.type_bonus==1:
                game.bomb_ship+=1
                game.score+=50
                
            # Power
            elif self.type_bonus==2:
                game.score+=25
                if(ship.power < 5):  #max 5
                    ship.power+=1
                game.score+=25

             # TNT    
            elif self.type_bonus==3:
                game.life-=1
                ship.explosion()
               
            self.kill()
###_______________________________________________________________________________
class Trap(pygame.sprite.Sprite):

    def __init__(self,top,right):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        self.rect=game.trap.get_rect()  #get the rectangular area

        self.rect.top=top
        self.rect.right=right+96
        self.update()
        
        game.update(self.rect) 

        # Test collision between ship and trap (tnt)
        if self.rect.colliderect(ship.rect):

            if game.life >= 0:   #life ship
                self.kill()
                ship.explosion()
                
        pygame.time.wait(30)

#_______________________________________________________________________________
class BombAlien (pygame.sprite.Sprite):

    def __init__(self,rect):

        # Rect is the rect of the alien
        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        # Load the image of the bomb
        self.image=game.alien_munition
        self.rect=self.image.get_rect()  #get the rectangular area
        
        # display the munition under the alien
        x=(rect.width-self.rect.width)/2
        self.rect=self.rect.move(rect.left+x,rect.top+32)  #position

    def update(self):
        stepx=0
        stepy=3

        self.rect=self.rect.move(stepx,stepy)
        if self.rect.top>600:
            self.kill()

        if self.rect.colliderect(ship.rect):
            self.kill()
            ship.explosion()
                     

#_______________________________________________________________________________        
class Ship(pygame.sprite.Sprite):

    def __init__ (self):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        self.power=1
        self.ship_explosion=[pygame.Surface] * 4 #pygame object for representing images. Call pygame.Surface() to create a new image object
        self.image=game.ship
        self.rect=self.image.get_rect()  #get the rectangular area
        
      
    def pos(self,x,y):
        self.rect=self.rect.move(x,y)  #position

    def start(self):
        self.rect.top=0
        self.rect.right=0
        self.pos(304,530)
        game.surface.blit(self.image,self.rect)

    def update(self):
        self.image=game.ship
        keypressed=pygame.key.get_pressed()
        
        if keypressed[pygame.K_SPACE]: 
            self.shoot_ship()

        if keypressed[pygame.K_LEFT]:
            if self.rect.left>0:
                self.rect.left-=8
            if keypressed[pygame.K_SPACE]:
                self.shoot_ship()

        if keypressed[pygame.K_RIGHT]:
            if self.rect.right<800:
                self.rect.left+=8
            if keypressed[pygame.K_SPACE]:
                self.shoot_ship()

        if keypressed[pygame.K_UP]:
            if self.rect.top>40:
                self.rect.top-=8
            if keypressed[pygame.K_SPACE]:
                self.shoot_ship()

        if keypressed[pygame.K_DOWN]:
            if self.rect.top<530:
                self.rect.top+=8
            if keypressed[pygame.K_SPACE]:
                self.shoot_ship()

    def shoot_ship(self):

        # the fire of the ship
        if self.power==1:
            self.power1(5)
            self.image=game.ship
            
        elif self.power==2:
             self.power2(15)
             self.image=game.ship

        elif self.power>=3:
            self.power3(25)
            self.image=game.ship

        
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
        if self.power>1:
            self.power-=1
        else:
            self.power=1
        game.life-=1
        for image in game.ship_explosion:
            game.surface.blit(image,self.rect)  #draw one image onto another
            game.update(self.rect) 
            game.play_sound(game.sound_ship_expl)
            pygame.time.wait(50)  #pause the program for an amount of time

#_______________________________________________________________________________
class Munition(pygame.sprite.Sprite):

    def __init__(self,type,pos):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor
        
        self.type=type
        self.pos=pos
        #self.sens=self.sens2=1
        
        if self.type==1:    #munition
            self.image=game.munition01
        elif self.type==2:  #munition
            self.image=game.munition02
        elif self.type==3:  #bomb
            self.image=game.munition03            
           
            
        self.rect=self.image.get_rect()  #get the rectangular area

        # Blit the munition onto the ship
        self.rect.left=ship.rect.left
        self.rect=self.rect.move(self.pos,ship.rect.top-2)
        game.surface.blit(self.image,self.rect)  #draw one image onto another

    def update(self):
        
        if self.type>=1 and self.type<=3:  #munition or bomb
            self.rect=self.rect.move(0,-16)
            game.play_sound(game.sound_ship_laser)

        if self.rect.top<32 or self.rect.left<1 or self.rect.left>game.width:
            self.kill()

        # Collision test with Alien with fire!!!
        collision=pygame.sprite.spritecollide(self,game.allalien,0, collided = None)  #Find sprites in a group that intersect another sprite
        if (collision!=[]):
            for alien in collision:
                    game.score+=1*game.level
                    if self.type<3:  #munition or bomb
                        alien.coup+=1
                    else:
                        alien.coup=game.level

        # Section to test collision with the Boss
        try:

            if self.rect.colliderect(boss.rect):
                if self.type==1 or self.type==2: #munition
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
        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

        self.image=game.boss[game.level-1]
        self.rect=self.image.get_rect()  #get the rectangular area
        self.rect= self.rect.move(320,100)  #position
        self.force=game.level*100  #force
        self.time_for_shoot=0
        self.sensx=4
        self.sensy=4

    def moves(self):

        font = pygame.font.Font(None, 16)  #create a new Font object from a file
        spaces=32*" "
        self.info = font.render(spaces+words.words[8][LANG]+ str(self.force) + spaces, 1, colors.WHITE,colors.RED)
        self.infoRect=self.info.get_rect() #get the rectangular area
        self.infoRect.top=23
        self.infoRect.left=((game.width-self.infoRect.width)/2)
        
        # Blit force info
        if self.force>=0:
            game.surface.blit(self.info, self.infoRect)  #draw one image onto another

        # Refresh clock for shoot
        self.time_for_shoot+=game.clock.get_time()  #time used in the previous tick

        if self.rect.right>=game.width:
            self.sensx=-4
        elif self.rect.left<=0:
            self.sensx=4
        if self.rect.top<50:
            self.sensy=4
        elif self.rect.top>=250:
            self.sensy=-4
        self.rect=self.rect.move(self.sensx,self.sensy)  #position

        # Blit boss
        game.surface.blit(self.image, self.rect)  #draw one image onto another

        # Test if it's the moment to shoot
        tps=700-(game.level*25)
        if self.time_for_shoot>tps:
            self.time_for_shoot=0
            bomb=BombBoss(random.randint(1,2))
            game.allbombalien.add(bomb)

    def explosion(self):
        game.surface.blit(game.bg,self.rect,self.rect) #draw one image onto another
        game.score+=50*game.level
        self.kill()
#_______________________________________________________________________________
class BombBoss(pygame.sprite.Sprite):

    def __init__(self,id):

        pygame.sprite.Sprite.__init__(self)  #Call the parent class (Sprite) constructor

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

        self.rect=self.image.get_rect()  #draw one image onto another

        # display under the boss
        self.rect=self.rect.move(boss.rect.left+32,boss.rect.top+64)
        game.surface.blit(self.image,self.rect) #draw one image onto another


    def update(self):

        limit=590  #limit width screen        

        if self.rect.right>=game.width:
            self.sensx=-1*self.sensx
        elif self.rect.left<=0:
            self.sensx=-1*self.sensx

        self.rect=self.rect.move(self.sensx,4)
        game.surface.blit(self.image,self.rect)  #draw one image onto another

        if self.rect.top>limit and self.id==1:
            game.allbombalien.remove(self)  #remove the sprite from groups
        elif self.rect.top>limit and self.id==2:
            game.allbombalien.remove(self)  #remove the sprite from groups
            trap=Trap(self.rect.top,self.rect.right)

        if self.rect.colliderect(ship.rect):
            self.kill()
            ship.explosion()



#-------------------------------------------------------------------------------
#                              end classes
#_______________________________________________________________________________

def keyboard():

  # Keyboard
  pygame.event.get(pygame.KEYDOWN)   #get events from the queue

  if pygame.key.get_pressed()[K_SPACE]:
      ship.update()
  elif pygame.key.get_pressed()[112]: #p
      game.pause()
  elif pygame.key.get_pressed()[98]: # b
      ship.bomb_ship()
  elif pygame.key.get_pressed()[K_ESCAPE]:
      pygame.quit()
      sys.exit()
  elif pygame.key.get_pressed()[K_f]: #f - mode FULLSCREEN or 800x600
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
while True:

    # Menu loop
    pygame.font.init()
    choice=-1

    #start menu
    while choice!=0:
        
        pygame.time.Clock().tick(FPS)
        game.surface.blit(game.bg2,game.bgRect2) #draw one image onto another
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
          game.surface.blit(game.bg3,game.bgRect) #draw one image onto another
          game.update(game.bgRect)
          pygame.time.wait(5000)          

     
    #---------------------------------------------------------------------------
    # The Game
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    # Intermediate Screen.
    #---------------------------------------------------------------------------
    game.surface.blit(game.bg,game.bgRect)  #draw one image onto another
    game.update(game.bgRect)
    pygame.time.wait(3000)
    game.sound_intro_game.stop()


    #---------------------------------------------------------------------------
    # Game Start
    #---------------------------------------------------------------------------
    pygame.key.set_repeat(1,1)

    # the ship
    ship=Ship()
    ship.start()

    # Add the first alien , the max number of the aliens is set to 10. It's due
    # at my method to set the intersection between them.
    game.add_alien(0,10)
    '''
    game.nb_alien=1
    game.nb_alien_max=0
    '''
    bg=Bg()
    bg = pygame.sprite.RenderPlain((bg))  #A container class to hold and manage multiple Sprite objects

    info=Info()
    allinfo=pygame.sprite.RenderPlain(info)  #A container class to hold and manage multiple Sprite objects

    # Game loop
    while(game.life>0 and game.level <= game.game_level):

        game.clock.tick(FPS)
        keyboard()

        if len(game.allalien)!=0:

            # Background
            bg.update()  #Calls the update() method on all Sprites in the Group
            bg.draw(game.surface)  #Draws the contained Sprites to the Surface argument

            # ship
            game.surface.blit(ship.image,ship.rect)  #draw one image onto another

            # alien
            game.allalien.update()  #Calls the update() method on all Sprites in the Group
            game.allalien.draw(game.surface)  #Draws the contained Sprites to the Surface argument

            # bomb of the Aliens
            game.allbombalien.update()  #Calls the update() method on all Sprites in the Group
            game.allbombalien.draw(game.surface)  #Draws the contained Sprites to the Surface argument

            # fire of the ship
            game.allmunition.update()  #Calls the update() method on all Sprites in the Group
            game.allmunition.draw(game.surface)  #Draws the contained Sprites to the Surface argument

            # bonus
            game.allbonus.update()  #Calls the update() method on all Sprites in the Group
            game.allbonus.draw(game.surface) #Draws the contained Sprites to the Surface argument

            allinfo.update()  #Calls the update() method on all Sprites in the Group
            allinfo.draw(game.surface)  #Draws the contained Sprites to the Surface argument

            pygame.display.flip()  #Update the full display Surface to the screen

        elif len(game.allalien)==0 and game.nb_alien<game.nb_alien_max:

            game.add_alien(game.nb_alien,game.nb_alien_max)

            # game level
        elif game.level<=game.game_level :

            game.nb_alien=0

            ####################################################################
            # BOSS LEVEL
            ####################################################################

            game.empty()
            ship.start()
            boss=Boss()
    
            while boss.force>0 and game.life>0:
                game.clock.tick(FPS)  #update the clock

                # Background
                bg.update()  #Calls the update() method on all Sprites in the Group
                bg.draw(game.surface)  #Draws the contained Sprites to the Surface argument

                # ship
                game.surface.blit(ship.image,ship.rect)  #draw one image onto another

                # fire of the ship
                game.allmunition.update()  #Calls the update() method on all Sprites in the Group
                game.allmunition.draw(game.surface)  #Draws the contained Sprites to the Surface argument

                # Movement of bomb of the boss
                game.allbombalien.update()  #Calls the update() method on all Sprites in the Group
                game.allbombalien.draw(game.surface)  #Draws the contained Sprites to the Surface argument

                #game.info()
                allinfo.update()  #Calls the update() method on all Sprites in the Group
                allinfo.draw(game.surface)  #Draws the contained Sprites to the Surface argument

                # Boss move
                boss.moves()

                keyboard()

                pygame.display.flip()  #Update the full display Surface to the screen

            boss = None

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
