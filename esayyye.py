import soccersimulator, soccersimulator.settings,math
from soccersimulator.settings import *
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, AbstractStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS

class usefull:
	def __init__(self):
		self.name="czc"
	def nb_p(self,state):
		return len([x for x in state._configs.keys()])
		
class coco(AS):
		def __init__(self):
			AS.__init__(self,"Mourinho")
			
		def dr(self,state,d1,d2):
				return d1
		def donne_autre(self,state,d):
			a=[x for x in state.players if x[0]==d][0]
			(x,y)=a
			return y		
		
		
		def one_to_one(self,state,id_team,id_player):
			if id_team==1:
				nb=GAME_WIDTH
				nbb=4
				qui=2
			elif id_team==2:
				nb=0
				nbb=-4
				qui=1
			autre=self.donne_autre(state,qui)
			coc=0
			dis=state.player_state(qui,autre).position
			print(dis)
			ball_to_player=state.ball.position.distance(state.player_state(id_team,id_player).position)
			if ball_to_player <= (PLAYER_RADIUS + BALL_RADIUS):
				
				return SA(V2D(0,0),V2D(nb,45)-state.ball.position)

			else:
				if ball_to_player <=40:
					return SA(state.ball.position-state.player_state(id_team,id_player).position,V2D(0,0))
				else:
					return SA(V2D(0,0),V2D(0,0))
		def compute_strategy(self,state,id_team,id_player):
			if usefull().nb_p(state)==2 :
				return self.one_to_one(state,id_team,id_player)

		
class simple(AS):
		def __init__(self):
				AS.__init__(self,"Gardiola")
		def compute_strategy(self,state,id_team,id_player):
			return SA(V2D(0,45)-state.player_state(id_team,id_player).position,V2D(0,0))
				
				
	
			   

class cocof(AS):
		def __init__(self):
				AS.__init__(self,"Gardiola")
				self._bl=False
		def compute_strategy(self,state,id_team,id_player):
				if (state.ball.position.distance(state.player_state(id_team,id_player).position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
						print("oco")
						if id_team==1:
							nb=GAME_WIDTH
							nbb=4
						elif id_team==2:
							nb=0
							nbb=-4
						self._bl=True
						return SA(V2D(0,0),V2D(nb,45)-state.ball.position)
				else:
					print("IIIo")
					self_bl=False
					return SA(state.ball.position-state.player_state(id_team,id_player).position,V2D(0,0))
		


psg= STe("psg",[Player("Ibra",coco())])
marseille= STe("marseille",[Player("L1a1ss",cocof())])
match=SM(psg,marseille)
soccersimulator.show(match)
#tournoi=ST(1)
#tournoi.add_team(psg)
#tournoi.add_team(marseille)
#soccersimulator.show(tournoi)

