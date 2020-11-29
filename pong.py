import pygame 
import random 

pygame.init()
pygame.mixer.init()

D=(800,500)
win=pygame.display.set_mode(D)
pygame.display.set_caption("MERENEMAZZ PONG")

#CHANGE THIS VARIABLE TO YOUR PATH
PATH=r"C:\Users\HP\Music"

#Comment out below 2 lines if you dont give a shit about the BGM"
pygame.mixer.music.load(PATH+r"\Alors.mp3") 
pygame.mixer.music.set_volume(1) 
 


class Player():
	def __init__(self,X,P):
		#PLAYER ATTRIBUTES
		self.x=X
		self.y=D[1]//2
		self.width=10
		self.height=65
		self.color=(255,255,255)
		self.vel=10
		self.lost=0
		if P=='A':
			self.key=(pygame.K_w,pygame.K_s)
			self.ply='A'
		elif P=='B':
			self.key=(pygame.K_UP,pygame.K_DOWN)
			self.ply='B'
	def draw(self):
		pygame.draw.rect(win,self.color,pygame.Rect(self.x,self.y,self.width,self.height))


	def move(self,keys):

		if keys[self.key[0]]==1:
			self.y-=self.vel
			if not(self.y<=D[1]-self.height and self.y>=0):
				self.y+=self.vel
		elif keys[self.key[1]]==1:
			self.y+=self.vel
			if not(self.y<=D[1]-self.height and self.y>=0):
				self.y-=self.vel


class Ball():
	def __init__(self,x,y):
		#BALL ATTRIBUTES
		self.x=x
		self.y=y
		self.color=(255,255,255)
		self.side=10
		self.vel=5
		self.xparams=1
		self.yparams=1
		self.dirx=1
		self.diry=0
	def move(self):
		self.x+=abs(self.xparams)*self.vel*self.dirx
		self.y+=abs(self.yparams)*self.vel*self.diry
	def check_collision(self,other):
		
		if self.x==other.x or self.x+self.side==other.x:
			if self.y+self.side//2>=other.y and self.y+self.side//2<=other.y+other.height:
				
				angle_factor=self.y+self.side//2-(other.y+other.height//2)
				self.yparams=angle_factor//5
				try:
					self.diry=self.yparams//abs(self.yparams)
				except ZeroDivisionError:
					self.diry=0
				return True
			else:
				self.x=D[0]//2
				self.y=D[1]//2
				self.diry=random.choice([-1,1])
				other.lost+=1
				
		elif not(self.y>=0 and self.y+self.side<=D[1]-self.side):			
			if (self.y<0):
				self.yparams=1
				self.diry=1
			elif self.y+self.side>D[1]-self.side:
				self.yparams=1
				self.diry=-1

		else:
			return False


	def draw(self):
		pygame.draw.rect(win,self.color,pygame.Rect(self.x,self.y,self.side,self.side))





	

#DISPLAYING THE SCORE
def showscore():
	global RUN,MENU
	font=pygame.font.Font("freesansbold.ttf",20)
	text1=font.render(f"PLAYER A:{ply_B.lost}",True,(0,255,0))
	text2=font.render(f"PLAYER B: {ply_A.lost}",True,(0,255,0))
	win.blit(text1,(D[0]//2-(D[0]//4)-(text1.get_width()//2),0))
	win.blit(text2,(D[0]//2+(D[0]//4)-(text2.get_width()//2),0))
	if ply_B.lost==11:
		font=pygame.font.Font("freesansbold.ttf",40)
		text=font.render("PLAYER A WINS THE PONG",True,(255,255,0))
		win.blit(text,(D[0]//2-text.get_width()//2,D[1]//2))
		pygame.display.update()
		pygame.time.delay(2000)
		ply_A.lost,ply_B.lost=0,0
		RUN=False
		MENU=True
	if ply_A.lost==11:
		font=pygame.font.Font("freesansbold.ttf",40)
		text=font.render("PLAYER B WINS THE PONG",True,(255,255,0))
		win.blit(text,(D[0]//2-text.get_width()//2,D[1]//2))
		ply_A.lost,ply_B.lost=0,0
		pygame.display.update()
		pygame.time.delay(2000)		
		RUN=False
		MENU=True

#SUB MENU
def musicMenu():
	while True:
		win.fill((0,0,0))
		font=pygame.font.Font("freesansbold.ttf",40)
		ON_text=font.render("ON",True,(0,0,0))
		ON_button=pygame.Rect(D[0]//2-ON_text.get_width()//2,D[1]//2-D[1]//4,ON_text.get_width(),ON_text.get_height())
		pygame.draw.rect(win,(255,255,255),ON_button)
		win.blit(ON_text,(D[0]//2-ON_text.get_width()//2,D[1]//2-D[1]//4))

		font=pygame.font.Font("freesansbold.ttf",40)
		OFF_text=font.render("OFF",True,(0,0,0))
		OFF_button=pygame.Rect(D[0]//2-OFF_text.get_width()//2,D[1]//2+D[1]//4,OFF_text.get_width(),OFF_text.get_height())
		pygame.draw.rect(win,(255,255,255),OFF_button)
		win.blit(OFF_text,(D[0]//2-OFF_text.get_width()//2,D[1]//2+D[1]//4))

		fontx=pygame.font.Font("freesansbold.ttf",20)
		msg=fontx.render("PRESS ESC TO GO BACK",True,(255,255,255))
		win.blit(msg,(0,0))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONUP:
				None
			elif event.type==pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					x,y=pygame.mouse.get_pos()
					if ON_button.collidepoint((x,y)):
						pygame.mixer.music.set_volume(0.8)
						pygame.mixer.music.play()
					elif OFF_button.collidepoint((x,y)):
						pygame.mixer.music.set_volume(0)
		keym=pygame.key.get_pressed()
		if keym[pygame.K_ESCAPE]:
			break



#MAIN MENU
def menu():
                
	win.fill((0,0,0))
	global MENU,RUN,MAIN
	font=pygame.font.Font("freesansbold.ttf",40)
	header=font.render("MERENEMAZZ PONG",True,(255,255,255))
	win.blit(header,(D[0]//2-header.get_width()//2,5))

	start_text=font.render("START",True,(0,0,0))
	start_button=pygame.Rect(D[0]//2-start_text.get_width()//2,D[1]//2-D[1]//4,start_text.get_width(),start_text.get_height())
	pygame.draw.rect(win,(255,255,255),start_button)
	win.blit(start_text,(D[0]//2-start_text.get_width()//2,D[1]//2-D[1]//4))

	music_text=font.render("MUSIC",True,(0,0,0))
	music_button=pygame.Rect(D[0]//2-music_text.get_width()//2,D[1]//2,music_text.get_width(),music_text.get_height())
	pygame.draw.rect(win,(255,255,255),music_button)
	win.blit(music_text,(D[0]//2-music_text.get_width()//2,D[1]//2))

	quit_text=font.render("QUIT",True,(0,0,0))
	quit_button=pygame.Rect(D[0]//2-quit_text.get_width()//2,D[1]//2+D[1]//4,quit_text.get_width(),quit_text.get_height())
	pygame.draw.rect(win,(255,255,255),quit_button)
	win.blit(quit_text,(D[0]//2-quit_text.get_width()//2,D[1]//2+D[1]//4))

	for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONUP:
				None
			if event.type==pygame.QUIT:
				MENU=False
				MAIN=False
				pygame.quit()
	if pygame.mouse.get_pressed()[0]:
		
		x,y=pygame.mouse.get_pos()		
		if start_button.collidepoint((x,y)):
			MENU=False
			RUN=True
		elif music_button.collidepoint((x,y)):
			#CALLING THE MUSIC MENU
			musicMenu()
		elif quit_button.collidepoint((x,y)):
			pygame.quit()

	pygame.display.update()

#DRAWING JUST THE GAME ON SCREEN
def draw():
	win.fill((0,0,0))
	pygame.draw.rect(win,(255,55,255),pygame.Rect(D[0]//2,0,2,D[1]))
	ball.draw()
	ply_A.draw()
	ply_B.draw()
	showscore()
	pygame.display.update()

#MOVING THE ELEMENTS
def move(key):
	ply_A.move(key)
	ply_B.move(key)
	if ball.dirx==1:
		 if (ball.check_collision(ply_B)):
		 	ball.dirx=-1
	elif ball.dirx==-1:
		if (ball.check_collision(ply_A)):
			ball.dirx=1
	ball.move()


#GAME OBJECTS
ply_A=Player(0,"A")
ply_B=Player(D[0]-10,"B")
ball=Ball(D[0]//2,D[1]//2)
clock=pygame.time.Clock()

#GLOBAL CONSTANTS AND BOOLEANS
RUN=False
FPS=60
MAIN=True
MENU=True


#MAINLOOP
while MAIN:
	#MENU LOOP
	while MENU:
		menu()
	#GAME LOOP
	while RUN:		
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				RUN=False
				MAIN=False
				MENU=False
				pygame.quit()
		
		key=pygame.key.get_pressed()
		if key[pygame.K_ESCAPE]:
			RUN=False
			MENU=True
		clock.tick(FPS)
		move(key)
		draw()