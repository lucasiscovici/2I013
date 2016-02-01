import soccersimulator, soccersimulator.settings,math
from soccersimulator.settings import *
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS


settings=soccersimulator.settings

T1_BUT=GAME_WIDTH
T2_BUT=0
T1_SENS=1
T2_SENS=-1
COEFF_FORCEUR=5
GOAL1=V2D(T2_BUT,GAME_HEIGHT/2)
GOAL2=V2D(T1_BUT,GAME_HEIGHT/2)
ZONE_GOAL=0
ANGLE1=0
ANGLE2=math.pi
GOAL_ATTACK=20
GOAL_ALERT=50
INCER=10

class clever(object):
	def __init__(self):
	        self.auto1_attack = 1
	        self.auto1_goal=1
		self.auto_goal_inside=1
		self.auto1_round=0
		self.onetoone_begin_round=1
		self.auto1_all=1
		self.one_to_one_goal_auto1=1
		self.one_to_one_goal_attack=0
		self.one_to_one_goal_max=0
        def ajoute(self,nom,val):
        	self.nom=val
	def begin_round(self):
		self.onetoone_begin_round=1 
		self.one_to_one_goal_auto1=1
		self.one_to_one_goal_max=0
		self.one_to_one_goal_attack=0   

class usefull(object): 
	def __init__(self): 
		self.name="czc" 
		
	def nb_p(self,state): 
		return len([x for x in state._configs.keys()])
		 
	def next_position_player(self,dis,config): 
		config_state_vitesse = config._state.vitesse * (1 - settings.playerBrackConstant) #frottemnt 
		config_state_vitesse = (config_state_vitesse+dis.norm_max(settings.maxPlayerAcceleration)).norm_max(settings.maxPlayerSpeed)
		config_state_position = config._state.position+ config_state_vitesse.norm_max(settings.maxPlayerSpeed) 
		#if self._state.position.x < 0 or self.position.x > settings.GAME_WIDTH or self.position.y < 0 or self.position.y > settings.GAME_HEIGHT: 
			#self._state.position.x = max(0, min(settings.GAME_WIDTH, self.position.x)) 
			#self._state.position.y = max(0, min(settings.GAME_HEIGHT, self.position.y)) 
			#self._state.vitesse.norm = 0 
		return config_state_position
	def next_position_ball(self,state):
		angle_factor = 1. - abs(math.cos((self.vitesse.angle - self.shoot.angle) / 2.))
		dist_factor = 1. - self._state.position.distance(ball.position) / (
		    settings.PLAYER_RADIUS + settings.BALL_RADIUS)
		shoot = self.shoot * (1 - angle_factor * 0.25 - dist_factor * 0.25)
		shoot.angle = shoot.angle + (2 * random.random() - 1.) * (
		    angle_factor + dist_factor) / 2. * settings.shootRandomAngle * math.pi / 2.
		self._action = SoccerAction()
		return shoot
	def has_ball(self,state,position): 
		return state.ball.position.distance(position) <=PLAYER_RADIUS + BALL_RADIUS
		
	def has_ball_next(self,state,id_team,id_player): 
		dis=state.ball.position - state.player_state(id_team, id_player).position 
		config=state.player(id_team,id_player) 
		f=self.next_position_player(dis,config) 
		return self.has_ball(state,f)
		
	def dvt (self,me,him,team): 
		if team==1:
			return me.x-him.x >0 
		else: 
			return me.x -him.x<0 
			
	def has_ball_dvt(self,state,dis,him,team): 
	 return self.has_ball(state,dis) and not self.dvt(dis,him,team) 
	 
class all(AS):
	def __init__(self,num=0): 
            self.clever=clever()
            self.num=num
	    self.name="ALL"
    
    
		
	def compute_strategy(self,state,id_team,id_player):
		nb_pers=usefull().nb_p(state)
		if nb_pers==2:
			if self.num==0:
				return ia().compute_strategy(state,id_team,id_player)
			else:
				return illumination_one_to_one(self.num).compute_strategy(state,id_team,id_player,self.clever)
	def begin_round(self, team1, team2, state):
		self.clever.begin_round()
		pass
			
class illumination_one_to_one(AS):
	def __init__(self,id=0):
		AS.__init__(self,"illumination") 
		self.id=id
		
	def compute_strategy(self,state,id_team,id_player,clever):
		if self.id==1:
			return forceur_one_to_one().compute_strategy(state,id_team,id_player,clever)
		elif self.id==2:
			return goal_one_to_one(id_team,id_player,state,clever).compute_strategy()
	
class goal_one_to_one(AS):
    def __init__(self,id_team,id_player,state,clever):
        AS.__init__(self,"goal_one_to_one")
        self.va_au_goal=1
        self.id_team=id_team
        self.id_player=id_player
        self.player=0
        if id_team==1:
            self.goal=GOAL1
            self.sens=T2_SENS
            self.autre=2
        elif id_team==2:
            self.goal=GOAL2
            self.sens=T2_SENS
            self.autre=1
        self.clever=clever
        self.config=state.player(id_team,id_player)
        self.state=state
        self.ball=state.ball.position
        self.goal_zone=self.goal + V2D(ZONE_GOAL*self.sens,0)
        self.autre_player=state.player(self.autre,self.player)
    def revien_goal(self):
        return SA(self.goal - self.config.position,V2D())
    def check_goal(self,marge=0):
	if self.id_team==1:
		return self.config.position.y >=44 and  self.config.position.y<=46 and self.config.position.x<= ZONE_GOAL + marge
	else:
		return self.config.position.y >=44 and  self.config.position.y<=46 and self.config.position.x>= GAME_WIDTH-ZONE_GOAL - marge
    def check_goal_dvt(self):
	angle=self.config.position.angle
	if self.check_goal(0):
		if self.id_team==1:
			return angle != ANGLE1
		else:
			return angle != ANGLE2 
    def dvt(self):
	if self.id_team==1:
		return SA(V2D(angle=ANGLE1,norm=0.5),V2D(4,4))
	else:
		return SA(V2D(angle=ANGLE2,norm=0.5),V2D(4,4))
    def attack(self):
        return SA((self.ball-self.config.position).norm_max(0.1),V2D())
        
    def check_attack(self):
	print("vitesse",self.state.ball.vitesse,"ball x",self.ball.x)
	return (self.ball.x >= GAME_WIDTH-GOAL_ATTACK) or (abs(self.state.ball.vitesse.x) <= 0.5 and abs(self.state.ball.vitesse.y) <= 0.5 and self.ball.x >= GAME_WIDTH-GOAL_ATTACK -20) and  self.state.ball.vitesse.norm <=1
    def projector(self,ball):	
	print("ball x",ball.position.x," posirion x",self.config.position.x)
	while (ball.position.x <= self.config.position.x) and ball.vitesse != V2D(0,0):
		if ball.vitesse == V2D(0,0):
			break
		ball.vitesse.norm = ball.vitesse.norm - settings.ballBrakeSquare * ball.vitesse.norm ** 2 - settings.ballBrakeConstant * ball.vitesse.norm
		## decomposition selon le vecteur unitaire de ball.speed
		ball.vitesse = ball.vitesse.norm_max(settings.maxBallAcceleration)
		ball.position += ball.vitesse
		print("bp ", ball.vitesse )
	return ball.position.y
    def projector2(self,ball):
	lamda=(self.config.position.x-ball.position.x)/ball.vitesse.x
	return ball.vitesse.y*lamda + ball.position.y
    def check_ball(self):
	return usefull().has_ball_dvt(self.state,self.config.position,self.autre_player.position,self.id_team)
    def alert(self):
	#fd=self.state.ball
	yy=self.projector2(self.state.ball)

	return SA(V2D(0,yy-self.config.position.y),V2D(0,0))
	
    def check_shoot(self):
        #print("lko")
        return usefull().has_ball(self.state,self.config.position)
    def shooti(self):
        if self.check_shoot():
            #print("dfez")
            return self.shoot()
    def goali(self):
        if not self.check_goal():
            return self.reviens_au_goal()
    def shoot(self):
        #print("prince")
        print(self.autre_player.position.angle,self.autre_player.position.angle-math.pi/2)
        
        return SA(V2D(),V2D(self.autre_player.position.x,GAME_HEIGHT-10-self.autre_player.position.y)-self.config.position)
    def check_alert(self):
	return self.ball.x >= GAME_WIDTH-GOAL_ALERT and  not self.check_ball()
    def check_angle(self):
	return self.config.position.y -self.autre_player.position.y >= 10

    def compute_strategy(self):
	if usefull().has_ball(self.state,self.autre_player.position) and self.clever.one_to_one_goal_max:
		self.clever.one_to_one_goal_max=0
	#if self.clever.one_to_one_goal_attack and self.check_angle() and self.check_ball() or self.clever.one_to_one_goal_max :
	#	print("ANGLE")
	#	self.clever.one_to_one_goal_max=1
	#	return forceur_one_to_one().compute_strategy(self.state,self.id_team,self.id_player,self.clever)
	if self.check_goal_dvt():
		print("dvt")
		self.clever.one_to_one_goal_auto1=0
		return self.dvt()
	if not self.check_goal() and self.clever.one_to_one_goal_auto1:
		print("goal")
		return self.revien_goal()
	if self.check_shoot():
		print("shoot")
		self.clever.one_to_one_goal_auto1=1
		self.clever.one_to_one_goal_attack=1
		return self.shoot()	
	if self.check_attack():
		print("attack")
		return self.attack()
	if self.check_alert() and usefull().has_ball(self.state,self.autre_player.position):
		print("alert")
		return self.alert()
	return SA()

class attack_one_to_one(AS):
    def __init__(self):
        AS.__init__(self,"attack_one_to_one") 
        
    def compute_strategy(self,state,id_team,id_player):
        return 
class ia(AS):
    def __init__(self):
        AS.__init__(self,"ia") 
        
    def compute_strategy(self,state,id_team,id_player):
        return

class forceur_one_to_one(AS):
    def __init__(self):
        AS.__init__(self,"forceur_one_to_one") 
        
    def compute_strategy(self,state,id_team,id_player,clever):
        vod=0
        if id_team==1:
            vod=T1_SENS*COEFF_FORCEUR
            vo=T1_BUT
        elif id_team==2:
            vod=T2_SENS*COEFF_FORCEUR
            vo=T2_BUT
        position=state.player(id_team,id_player).position
        ball_to_player=state.ball.position.distance(state.player(id_team,id_player).position)
        goal_to_player=state.player(id_team,id_player).position.distance(V2D(vo,GAME_HEIGHT/2))
        goal_to_ball= V2D(vo,GAME_HEIGHT/2) -state.ball.position
        ball= PLAYER_RADIUS + BALL_RADIUS
        if usefull().has_ball(state,position):
            return SA(V2D(0,0),goal_to_ball)
        else:
            return SA(state.ball.position - state.player(id_team,id_player).position,V2D(0,0))
