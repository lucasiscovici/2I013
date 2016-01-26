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
ZONE_GOAL=1
GOAL_ATTACK=50

class clever(object):
    def __init__(self):
        self.auto1_attack = 1
        self.auto1_goal=1
    
    def ajoute(self,nom,val):
        self.nom=val


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
			
	def has_ball_dvt(self,state,dis,me,team): 
	 return self.has_ball(state,dis) and not self.dvt(me,dis,team) 
	 
class all(object):
	def __init__(self,num=0): 
            self.clever=clever()
            self.num=num
    
    
		
	def compute_strategy(self,state,id_team,id_player):
		nb_pers=usefull().nb_p(state)
		if nb_pers==2:
			if self.num==0:
				return ia().compute_strategy(state,id_team,id_player)
			else:
				return illumination_one_to_one(self.num).compute_strategy(state,id_team,id_player,self.clever)
			
			
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
    def reviens_au_goal(self):
        return SA(self.goal_zone - self.config.position,V2D())
		
    def check_goal(self):
        if self.id_team==1:
            return self.config.position.x<=self.goal_zone.x
        elif self.id_team==2:
            print("pos: ",self.config.position.x," goal: ",self.goal_zone.x)
            return (self.goal_zone - self.config.position).norm<=1
    def attack(self):
        return SA(self.ball-self.config.position,V2D())
        
    def check_attack(self):
        return self.autre_player.position.distance(self.goal) <= GOAL_ATTACK
        
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
        print(self.autre_player.position.angle,self.autre_player.position.angle+math.pi)
        
        return SA(V2D(),V2D(angle=self.autre_player.position.angle+math.pi,norm=self.autre_player.position.norm))
        
    def compute_strategy(self):
        print("debut")
        if self.config.acceleration==V2D(0,0) and not self.check_goal():
            u=self.reviens_au_goal()
            return u
        if not self.check_goal() and self.clever.auto1_goal:
            print("Check - goal")
            u=self.reviens_au_goal()
            return u
        
        if self.check_goal() and self.check_attack():
            print("Check - goal- Attack 1")
            self.clever.auto1_attack=1

        if self.check_shoot():
            print("CHeck Shoot")
            g= self.shoot()
            print("CHeck Shoot goal 1 , attak 0")
            self.clever.auto1_goal=1
            self.clever.auto1_attack=0
            return g
        if self.check_attack() and self.clever.auto1_attack :
            print("Attack")
            a= self.attack()
            print("Attack goal 0")
            self.clever.auto1_goal=0
            return a
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

