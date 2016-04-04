from soccersimulator import *
from strategies import *
# coding: utf-8
#Strat temporaire = strategie modifie au cours d'un round
#Start global = strategie du round
import soccersimulator, soccersimulator.settings,math
import random
from soccersimulator.settings import *
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS, MobileMixin as MM
from soccersimulator.mdpsoccer import Ball
from random import uniform,randint
settings=soccersimulator.settings
DISTANCE_MIN=10

class PADState(SoccerState):
    """ Etat d'un tour du jeu. Contient la balle (MobileMixin), l'ensemble des configurations des joueurs, le score et
    le numero de l'etat.
    """
    def __init__(self, **kwargs):
        SoccerState.__init__(self,**kwargs)
        self.cur_score = 0

    def apply_actions(self, actions=None):
        sum_of_shoots = Vector2D()
        if actions:
            for k, c in self._configs.items():
                if k in actions:
                    act = actions[k].copy()
                    if k[0] == 1 and self.player_state(k[0],k[1]).vitesse.norm>0.01:
                        act.shoot = Vector2D()
                    sum_of_shoots += c.next(self.ball, act)
        self.ball.next(sum_of_shoots)
        self.step += 1
        dball = [(it,ip) for it,ip in self.players
                 if self.player_state(it,ip).position.distance(self.ball.position)<settings.BALL_RADIUS+settings.PLAYER_RADIUS]
        mines = [(it,ip) for it,ip in dball if it ==1 ]
        others = [(it,ip) for it,ip in dball if it==2 ]
        if len(others)==0 or len(mines)>0 or self.ball.vitesse.norm>1:
            self.cur_score += 1
        else:
            self._score[1]=max(self._score[1],self.cur_score)
            self.cur_score=0
            self._score[2]+=1
            self._winning_team = 2
        if self.ball.position.x < 0:
            self.ball.position.x = -self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y < 0:
            self.ball.position.y = -self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y
        if self.ball.position.x > settings.GAME_WIDTH:
            self.ball.position.x = 2 * settings.GAME_WIDTH - self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y > settings.GAME_HEIGHT:
            self.ball.position.y = 2 * settings.GAME_HEIGHT - self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y

    def reset_state(self, nb_players_1=0, nb_players_2=0):
        SoccerState.reset_state(self,nb_players_1,nb_players_2)
        self.ball = Ball.from_position(self.player(1,0).position.x,self.player(1,0).position.y)
        self.cur_score = 0

class team1(AS):
	def __init__(self,state,id_team,id_player):
        	self.state=state
		self.id_team=id_team
		self.id_player=id_player
		if id_team==1:
		    self._autre=2
		elif id_team==2:
		    self._autre=1
		self.moi=self.config=state.player(id_team,id_player)
		self.ma_position=self.moi.position
		self.ma_vitesse=self.moi.vitesse
		self.can_shoot=0 
	



class PasseStrategy(AS):
	def __init__(self,state,id_team,id_player):
	        AS.__init__(self,"PassStrategy")
	        self.state=state
		self.id_team=id_team
		self.id_player=id_player
		if id_team==1:
		    self._autre=2
		elif id_team==2:
		    self._autre=1
		self.moi=self.config=state.player(id_team,id_player)
		self.ma_position=self.moi.position
		self.ma_vitesse=self.moi.vitesse
		self.can_shoot=0

	def compute_strategy(self):
		#joueur peut tirer si v<0.01	
		if (nb_p==3):
			if (self.ma_vitesse<=0.01 and self.have_ball()):
				self.can_shoot=1
				for (k,v) in self.state.players:
					#si le coequipier est bien place on lui fait la passe
					if(k==id_team and v!=id_player and self.state.player(self._autre,0).distance(self.state.player(id_team,v)>=DISTANCE_MIN)):
						return SA(V2D(),self.state.player(k,v).position-self.ma_position)
			#Si joueur a la balle au prochain tour, il ne bouge plus
			if self.trou() and not self.check_shoot():
		    		printnn("trou")
		    		return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
		
			if(not self.have_ball()):
				return SA(self.state.ball.position-self.ma_position,V2D())

			else:
				return SA(V2D(),V2D())

		if (nb_p==5):
			if (self.ma_vitesse<=0.01 and self.have_ball()):
				self.can_shoot=1
				for (k,v) in self.state.players:
					
					#si l un des coequipier est bien place on lui fait la passe
					if(k==id_team and v!=id_player and ((self.state.player(self._autre,0).distance(self.state.player(id_team,v)>=DISTANCE_MIN))and(self.state.player(self._autre,1).distance(self.state.player(id_team,v)>=DISTANCE_MIN)) and (self.state.player(self._autre,2).distance(self.state.player(id_team,v)>=DISTANCE_MIN)))) :
						return SA(V2D(),self.state.player(k,v).position-self.ma_position)
	
			#Si joueur a la balle au prochain tour, il ne bouge plus
			if self.trou() and not self.check_shoot():
		    		printnn("trou")
		    		return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
		
			if(not self.have_ball()):
				return SA(self.state.ball.position-self.ma_position,V2D())

			else:
				return SA(V2D(),V2D())

				
	def __getattr__(self,name):
       		return getattr(self.state,name) 


team2= SoccerTeam("T1",[Player("1", PasseStrategy()),Player("2",PasseStrategy())])
team4= SoccerTeam("T1",[Player("1", PasseStrategy()),Player("2",PasseStrategy()),Player("3",PasseStrategy()),
                             Player("4",PasseStrategy())])
team1 = SoccerTeam("T2",[Player("1", FonceurStrategy())])
team3 = SoccerTeam("T2",[Player("1", FonceurStrategy()),Player("2", FonceurStrategy()),
                         Player("3",FonceurStrategy())])
match = SoccerMatch(team2,team1,init_state=PADState.create_initial_state(2,1))
show(match)
match = SoccerMatch(team4,team3,init_state=PADState.create_initial_state(4,3))
show(match)
