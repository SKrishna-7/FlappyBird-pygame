import pygame
import sys
import random
pygame.init()


#------------Assets------------------------
BackgroundSurface=pygame.image.load('fappy_bk.png')
FloorSurface=pygame.image.load('fappy_ground.png')
# Bird=pygame.image.load('redbird.png')

BirdDownFlap=pygame.image.load('redbird-downflap.png')
BirdMidFlap=pygame.image.load('redbird-midflap.png')
BirdUpFlap=pygame.image.load('redbird-upflap.png')

BirdFrames=[BirdDownFlap,BirdMidFlap,BirdUpFlap]
BirdIndex=0
Bird=BirdFrames[BirdIndex]
BirdRect=Bird.get_rect(center=(75,256))

BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)
PipeSurface=pygame.image.load('pipe.png') 


GameFont=pygame.font.Font('04B_19.ttf',20)
#------------------------------------------
#----------Game Variables------------------
SCREEN_WIDTH,SCREEN_HEIGHT=288,512
FLOORPOSX,FLOORPOSY=0,450
BGPOSX,BGPOSY=0,0
GRAVITY=0.2
BIRDMOMENT=0
Pipe_List=[]
SPWANPIPE=pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE,1200)
PIPEHIEGHTS=[190,195,200,205,200,210,220,240,230,250,260,270,280,290,295,300,305,310,315,320,330,340,350,360,365,370,380,380,385,390,395,400,410]
GameActive=True
#------------------------------------------


#---------GameFunctions--------------------------
def BlitBg():
    screen.blit(BackgroundSurface,(BGPOSX,BGPOSY))
    screen.blit(BackgroundSurface,(BGPOSX+288,BGPOSY))
def BlitFloor():
    screen.blit(FloorSurface,(FLOORPOSX,FLOORPOSY))
    screen.blit(FloorSurface,(FLOORPOSX+288,FLOORPOSY))

def CreatePipe():
    PipeHeight=random.choice(PIPEHIEGHTS)
    BottomPipe=PipeSurface.get_rect(midtop=(400,PipeHeight))
    TopPipe=PipeSurface.get_rect(midbottom=(400,PipeHeight-150))
    return BottomPipe,TopPipe

def MovePipes(pipes):
    for  pipe in pipes:
        pipe.centerx-=2
    return pipes

def BlitPipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=512:
            screen.blit(PipeSurface,pipe)
        else:
            flipPipe=pygame.transform.flip(PipeSurface,False,True)
            screen.blit(flipPipe,pipe)
def CheckCollision(pipes):
    for pipe in pipes:
        if BirdRect.colliderect(pipe):
            return False
    if BirdRect.top<=-100 or BirdRect.bottom>=450:
        return False
    return True

def RotateBird(Bird):
    NewBird=pygame.transform.rotozoom(Bird,-BIRDMOMENT*3,1)
    return NewBird 
def BirdAnimation():
    NewBird=BirdFrames[BirdIndex]
    NewBirdRect=NewBird.get_rect(center=(78,BirdRect.centery))
    return NewBird,NewBirdRect
# def DisplayScore():
#     ScoreSurface=GameFont.render(Score,True,(255,255,255))
#     ScoreRect=ScoreSurface.get_rect(center=(144,50))
#     screen.blit(ScoreSurface,ScoreRect)

#------------------------------------------------

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
Clock =pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()  
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and GameActive:
                BIRDMOMENT=0
                BIRDMOMENT-=5
            if event.key==pygame.K_SPACE and GameActive==False:
                GameActive=True
                Pipe_List.clear()
                BirdRect.center=(78,256)
                BIRDMOMENT=0
        if event.type==SPWANPIPE:
            Pipe_List.extend(CreatePipe())
            # print(Pipe_List)
        if event.type==BIRDFLAP:
            if BirdIndex<2:
                BirdIndex+=1
            else:
                BirdIndex=0
            Bird,BirdRect=BirdAnimation()
    BGPOSX-=1
    FLOORPOSX-=1
    BlitBg()
    if FLOORPOSX<=-288 and BGPOSX<=288:
            BGPOSX=0
            FLOORPOSX=0

    if GameActive==True:
        Pipe_List=MovePipes(Pipe_List)
        BlitPipe(Pipe_List)

        BIRDMOMENT+=GRAVITY
        RotatedBird=RotateBird(Bird)
        BirdRect.centery+=BIRDMOMENT
        screen.blit(RotatedBird,BirdRect)
        GameActive=CheckCollision(Pipe_List)
        BlitFloor()
        
    pygame.display.update()
    Clock.tick(120)

#sureshkrishna