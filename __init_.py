import soccersimulator, soccersimulator.settings,math,AllStrategies as AllS, As
from soccersimulator.settings import *
from soccersimulator import  SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS
settings=soccersimulator.settings



team1= STe("marseille",[Player("L1a1ss",AllS.all(2))])
team2= STe("marseille",[Player("L1a1ss",AllS.all(2)),Player("Ibra",As.all(0))])
team4=STe("marseille",[Player("L1a1ss",AllS.all(2)),Player("Ibra",As.all(0))],Player("Ibra",As.all(0))],[Player("L1a1ss",AllS.all(2)))
