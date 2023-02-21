import pygame
import random

pygame.mixer.init(frequency= 44100,size=-16,channels=2,buffer=512)
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((290,512))
pygame.display.set_caption("Flappy Bird")
icon=pygame.image.load('assests/images/redbird.png')
pygame.display.set_icon(icon)

game_font=pygame.font.Font('assests/fonts/04B_19.ttf',20)

bk_image=pygame.image.load('assests/images/fappy_bk.png').convert()
ground_image=pygame.image.load('assests/images/fappy_ground.png').convert()

bird_down=pygame.image.load('assests/images/redbird-downflap.png').convert_alpha()
bird_mid=pygame.image.load('assests/images/redbird-midflap.png').convert_alpha()
bird_up=pygame.image.load('assests/images/redbird-upflap.png').convert_alpha()

bird_frames=[bird_down,bird_mid,bird_up]
bird_index=0
bird_image=bird_frames[bird_index]
bird_reac=bird_image.get_rect(center=(75,256))

BIRDFLAP=pygame.USEREVENT+1
pygame.time. set_timer(BIRDFLAP,200)

pipe_image=pygame.image.load('assests/images/pipe.png').convert()
pipe_list=[]
pipe=pygame.USEREVENT
pygame.time.set_timer(pipe,1200)

bird_y=0
gravity=0.2
floor_xpos=0
backg_xpos=0
pipe_height=[190,195,200,205,200,210,220,240,230,250,260,270,280,290,295,300,305,310,315,320,330,340,350,360,365,370,380,380,385,390,395,400,410]
game_running =True

game_over_image=pygame.image.load('assests/images/gameover.png').convert_alpha()
game_over_rect=game_over_image.get_rect(center=(144,256))

score=0
high_score=0
score_play=0

def draw_bk():
      screen.blit(bk_image,(backg_xpos,0))
      screen.blit(bk_image,(backg_xpos+288,0))
   
def floor():
      screen.blit(ground_image,(floor_xpos,450))
      screen.blit(ground_image,(floor_xpos+288,450))

def create_pipe():
      rand_height=random.choice(pipe_height)
      bottom_pipe=pipe_image.get_rect(midtop=(400,rand_height))
      top_pipe=pipe_image.get_rect(midbottom=(400,rand_height-150))
      return bottom_pipe,top_pipe

def move_pipe(pipes):
   for pipe in pipes:
      pipe.centerx-=2
   return pipes
      
def draw_pipe(pipes):
   for pipe in pipes:
      if pipe.bottom>=512:
         screen.blit(pipe_image,pipe)
      else:
          flip_pipe=pygame.transform.flip(pipe_image,False,True)
          screen.blit(flip_pipe,pipe)   

def collision(pipes):
   for pipe in pipes:
         if bird_reac.colliderect(pipe):
            hit.play()
            return False
   if bird_reac.top<=-100 or bird_reac.bottom>=450:
         hit.play()
         return False
   return True
         
def rotate_bird(bird):
      new_bird=pygame.transform.rotozoom(bird,-bird_y*3,1)
      return new_bird   

def bird_animation():
      new_bird_=bird_frames[bird_index]
      new_bird_rect=new_bird_.get_rect(center=(75,bird_reac.centery))
      return new_bird_,new_bird_rect       

def score_display(game_state):
   if game_state=="main_game":
      score_source=game_font.render(str(int(score)),True,(255,255,255))
      score_rect=score_source.get_rect(center=(144,50))
      screen.blit(score_source,score_rect)

   if game_state=="game-over":
         score_source=game_font.render(f"Score : {str(int(score))}",True,(255,255,255))
         score_rect=score_source.get_rect(center=(144,50))
         screen.blit(score_source,score_rect)

         high_score_source=game_font.render(f"highscore : {str(int(score))}",True,(255,255,255))
         score_rect=high_score_source.get_rect(center=(144,420))
         screen.blit(high_score_source,score_rect)
      

def score_update(score,high_score):
   if score>high_score:
      high_score=score
   return high_score   

flap=pygame.mixer.Sound('assests/audios/sfx_wing.wav')
hit=pygame.mixer.Sound('assests/audios/sfx_hit.wav')
points=pygame.mixer.Sound('assests/audios/sfx_point.wav')

pygame.mixer.music.load('assests/audios/pubg.mp3')
pygame.mixer.music.play(-1)

while True:
   for event in pygame.event.get():
         if event.type ==pygame.QUIT:
            exit()
            False
         if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_running:
               bird_y=0
               bird_y-=5
               flap.play()

            if event.key==pygame.K_SPACE and game_running== False:
               game_running=True
               pipe_list.clear()
               bird_reac.center=(78,256)
               bird_y=0
               score=0
               score_play=0

         if event.type==pipe:
                pipe_list.extend(create_pipe())      
                print(pipe_list)  
         
         if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1   
            else :
                bird_index=0

            bird_image,bird_reac=bird_animation()

   screen.fill((2,50,100))   
   screen.blit(bk_image,(0,0))
   floor_xpos-=1
   backg_xpos-=1
   
   draw_bk()
   
   
   if game_running:

      pipe_list=move_pipe(pipe_list) 
      draw_pipe(pipe_list) 

   
      bird_y+=gravity
      rotated_bird=rotate_bird(bird_image)

      bird_reac.centery+=bird_y
      screen.blit(rotated_bird,bird_reac)
 
   
      game_running=collision(pipe_list)
      

      score+=0.01
      score_play+=0.01

      if score_play>1.0:
         points.play()
         score_play=0

      score_display('main_game')
      floor() 
   else :
      screen.blit(game_over_image,game_over_rect)
      high_score=score_update(score,high_score)
      floor() 
      
      By_source=game_font.render("@SureshKrishna",True,(10,10,10))
      By_sourcerect=By_source.get_rect(center=(290/2,500))
      screen.blit(By_source,By_sourcerect)

      score_display('game-over')   

     
   if floor_xpos<=-288 and backg_xpos<=-288:
        floor_xpos=0
        backg_xpos=0 
   pygame.display.update()
   
   clock.tick(120)



   #Developed BY S.SURESH KRISHNA
