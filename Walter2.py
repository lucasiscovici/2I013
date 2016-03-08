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

#but adv
T1_BUT=GAME_WIDTH
T2_BUT=0
#sens pour aller au but adverse
T1_SENS=1
T2_SENS=-1
COEFF_FORCEUR=5
#V2D designant les buts de la team 1 et 2
GOAL1=V2D(T2_BUT,GAME_HEIGHT/2)
GOAL2=V2D(T1_BUT,GAME_HEIGHT/2)
ZONE_GOAL=0
ANGLE1=0
ANGLE2=math.pi
#Zone d'attack du goal
GOAL_ATTACK=35
#Zone d'alert du goal
GOAL_ALERT=60
INCER=10
BALLE_MIN_VITESSE=0.5578
BALLE_MAX_NORM=1
#rayon ball + joueur
RAYON_BALL_PLAYER=PLAYER_RADIUS + BALL_RADIUS
NORM_DVT=0.5
MODULO_GOAL=2
GOAL_ATTACK2=20
GAMMA=1.5
#Autorisation de print
PRINT=1
PRINTN=1
#num des strategies pour les changements temporaires (voir to_change)
TO_GOAL=2
TO_ATTACK=3
TO_FORCEUR=1
#Zone dans laquelle un attaquant peut frapper au but
TIR_ZONE_ATTACK=30
#Norm max ball un attaquant peut frapper au but
TIR_NORM=3.5
#aucune action
VIDE=SA(V2D(),V2D())
#strategies
tech=[2,3]
#historique (id_strat):id_team_gagnant_round
history_me={}

#Variables d'autorisations (0,1) et d'information (0,1) et historique, tech,listener
dico_clever={"auto1_attack":1,"auto1_goal":1,"auto_goal_inside":1,"auto1_round":0,"onetoone_begin_round":
1,"auto1_all":1,"one_to_one_goal_auto1":1,"two_to_two_goal_attack":0,"one_to_one_goal_attack":
0,"one_to_one_goal_max":0,"master":0,"master_round":0,"master_base":0,"master_debut":-1,"history_me":
history_me,"alert":0,"count":0,"tech":tech,"listener":0}

#Variable à reset
dico_clever_up={"onetoone_begin_round":1,"one_to_one_goal_auto1":1,"two_to_two_goal_attack":0,"one_to_one_goal_attack":
0,"one_to_one_goal_max":0,"alert":0}
###############################################
#INIT STRATEGIES################################
###############################################

#STRATEGIE PRINCIPALE AVEC CHANGEMENT GLOBALE, DISPACHE AU STRATEGIE CORRESPONDANT AU NOMBRE DE JOUEUR
class all(AS):
        def __init__(self,num):
                printnn("all\ __init__ all")
                #memory
            	self.clever=clever()
                printnn("all\ Clever crée")
                #strat en cours
            	self.clever.master=num
                #strat round
            	self.clever.master_round=num
                #strat d'origine
                self.clever.master_debut=num
                #l'objet all
                self.clever.listener=self
                printnn("all\ master",self.clever.master,"master_round",self.clever.master,"master_debut",self.clever.master)
                self.num=num
            	self.name="ALL"
                printn("all\ All initialisé")
        
        def compute_strategy(self,state1,id_team,id_player):
            printn("all-compute_strategy\ Joueur ",id_team,id_player)
            #creation du decorateur et des bibli
            self.state=AllState(state1,id_team,id_player)
            self.bibli=Bibli(self.state,self.clever)
            printnn("all-compute_strategy\ AllState, Bibli initialisé")
            nb_pers=self.bibli.nb_p()
            printn("all-compute_strategy\ master",self.clever.master,"master_round",self.clever.master_round)
            #appel des objets correspondants au nb de joueurs
            if nb_pers==2:
                if self.num==0:
                    return ia().compute_strategy(self.bibli,self.id_team,self.id_player)
                else:
                    return illumination_one_to_one(self.clever.master).compute_strategy(self.bibli)
            elif nb_pers==4:
                return illumination_two_to_two(self.clever.master).compute_strategy(self.bibli)

        #Appele qd il y a un changement temporaire de strat
        def compute_strategy_change(self,state,bibli):
            printn("all-compute_strategy_change\Changement de strategie temporaire (master != master_round)")
            self.state1=state
            self.state=bibli
            nb_pers=self.state.nb_p()
            if nb_pers==2:
                return illumination_one_to_one(self.clever.master).compute_strategy(self.state)
            elif nb_pers==4:
                return illumination_two_to_two(self.clever.master).compute_strategy(self.state)

        #Change la strategie temporaire en @num
        def to_change(self,num):
            self.clever.master=num
            return self.compute_strategy_change(self.state,self.bibli)


        def begin_round(self, team1, team2, state):
            printn("joueur",team1)
            return self.clever.begin_round()

        def end_match(self, team1, team2, state):
            printn("joueur",self.id_team,self.id_player)

            return self.clever.end_match()
        
        def begin_match(self, team1, team2, state):
            printn("joueur",team1)

            return self.clever.begin_match(self.num)
        
        def end_round(self, team1, team2, state):
            printn("joueur",self.id_team,self.id_player)
            return self.clever.end_round(state,self.state)

        def __getattr__(self,name):
            return getattr(self.bibli,name)


#STRATEGIE PRINCIPALE SANS CHANGEMENT GLOBALE, DISPACHE AU STRATEGIE CORRESPONDANT AU NOMBRE DE JOUEUR (voir all)
class all2(AS):
    def __init__(self,num):
                printnn("all2\ __init__ all2")
                self.clever=clever()
                self.clever.all=2
                printnn("all2\ Clever crée")
                self.clever.master=num
                self.clever.master_round=num
                self.clever.master_debut=num
                self.clever.listener=self
                printnn("all2\ master",self.clever.master,"master_round",self.clever.master,"master_debut",self.clever.master)
                self.num=num
                self.name="ALL2"
                printn("all2\ All2 initialisé")

    def compute_strategy(self,state1,id_team,id_player):
        printn("all2-compute_strategy\ Joueur ",id_team,id_player)
        self.state=AllState(state1,id_team,id_player)
        self.bibli=Bibli(self.state,self.clever)
        printnn("all2\ All State, Bibli initialisé")
        nb_pers=self.bibli.nb_p()
        printn("all2\ master",self.clever.master,"master_round",self.clever.master_round)
        if nb_pers==2:
            if self.num==0:
                return ia().compute_strategy(self.bibli,self.id_team,self.id_player)
            else:
                return illumination_one_to_one(self.clever.master).compute_strategy(self.bibli)
        elif nb_pers>=4:
            return illumination_two_to_two(self.clever.master).compute_strategy(self.bibli)

    def compute_strategy_change(self,state,bibli):
            printn("all2-compute_strategy_change\ Changement de strategie temporaire (master != master_round)")
            self.state1=state
            self.state=bibli
            nb_pers=self.state.nb_p()
            if nb_pers==2:
                return illumination_one_to_one(self.clever.master).compute_strategy(self.state)
            elif nb_pers==4:
                return illumination_two_to_two(self.clever.master).compute_strategy(self.state)

    def to_change(self,num):
        self.clever.master=num
        if self.clever.all==1:
            return self.compute_strategy_change(self.state,self.bibli)
        else:
            return self.compute_strategy_change(self.state,self.bibli)

    def begin_round(self, team1, team2, state):
        try:
            printn("joueur",self.id_team,self.id_player)
        except:
            pass
        return self.clever.begin_round()
    
    def __getattr__(self,name):
        return getattr(self.state,name)

#SELECTOR STRATEGIE DE 1-1 (ATTACK,GOAL,FORCEUR)
class illumination_one_to_one(AS):
    def __init__(self,id=0):
        AS.__init__(self,"illumination")
        self.id=id
    
    def compute_strategy(self,state):
        printnn("illumination_one_to_one-compute_strategy\\")
        self.state=state
        if self.id==1:
            return forceur(state).compute_strategy()
        elif self.id==2:
            return goal_one_to_one(Bibli_Goal(state)).compute_strategy()
        elif self.id==3:
            return attack_one_to_one(state).compute_strategy()


#SELECTOR STRATEGIE DE 2-2 (ATTACK,GOAL,FORCEUR)
class illumination_two_to_two(AS):
    def __init__(self,id=0):
        AS.__init__(self,"illumijnation")
        self.id=id
        
    def compute_strategy(self,state):
        printnn("illumination_two_to_two-compute_strategy\\")
        self.state=state
        if self.id==1:
            return forceur(state).compute_strategy()
        elif self.id==2:
            return goal_two_to_two(Bibli_Goal(state)).compute_strategy()
        elif self.id==3:
            return attack_two_to_two(state).compute_strategy()



##########################################
#INIT DECORATEUR + BIBLI##################
##########################################
#DECORATEUR PRINCIPALE INIT (GETTER)
class AllState:
    def __init__(self,state,id_team,id_player):
        #initialisation des decorateurs
        self.state=StatePlayer(StateBall(StateTerrain(state,id_team,id_player),id_team,id_player),id_team,id_player)
        self.id_team=id_team
        self.id_player=id_player
    
    def __getattr__(self,name):
        return getattr(self.state,name)

#BIBLIOTHEQUE PRINCIPALE INIT (FCT) (bibliotheque contient aussi les decorateurs)
class Bibli:
    def __init__(self,state,clever=0):
        self.state=state
        self.clever=clever
        #initialisation des bibliotheques
        self.bibli=Bibli_Player(state,Bibli_Ball(state,usefull()))


    def __getattr__(self,name):
        return self.bibli.get_attr3(self.bibli,self.state,self.clever.listener,name)


##########################################################
#STRATEGIE GOAL###########################################
##########################################################
class goal_one_to_one(AS):
    def __init__(self,state):
        AS.__init__(self,"goal_one_to_one")
        self.state=state
    
    def compute_strategy(self):
        printn("goal_one_to_one-compute_strategy\\")
        
        #Si joueur a la balle au prochain tour, il ne bouge plus
        if self.trou() and not self.check_shoot():
            printnn("trou")
            return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
        #check Si le joueur a la balle, Si oui, le joueur devient attaquan
        if self.check_shoot():
            printnn("shoot")
            self.clever.one_to_one_goal_auto1=1
            self.clever.one_to_one_goal_attack=1
            return self.to_change(TO_ATTACK)
        
        #Check si on peux interdire au goal de rentrer dans ses cages
        if self.check_no_goal():
            printnn("no goal")
            self.clever.one_to_one_goal_auto1=0
        
        #Check si le goal est bien oriente
        if self.check_goal_dvt():
            printnn("dvt")
            self.clever.one_to_one_goal_auto1=0
            return self.dvt()
        
        #check si le goal doit revenir dans ces cage, et qu'il y est autorise
        if (not self.check_goal() and self.clever.one_to_one_goal_auto1) or self.bb():
            printnn("goal")
            return self.revien_goal()
        
        #check si le goal "attaquer" , c'est a dire aller vers la balle
        if self.check_attack():
            printnn("attack")
            return self.attack()
        
        #check si le goal ne doit  plus s'orienter vers le balle
        if self.check_stop_alert():
            printnn("stop alert")
            self.clever.alert=0
            return self.stop_alert()
        
        #check si le goal  doit  s'orienter vers le balle
        if self.check_alert():
            printnn("alert")
            self.clever.alert=1
            return self.alert()
        
        printnn("rien")
        return SA()

    def __getattr__(self,name):
        return getattr(self.state,name)

#voir goal1-to_1
class goal_two_to_two(AS):
    def __init__(self,state):
        AS.__init__(self,"goal_one_to_one")
        self.state=state
    def compute_strategy(self):
        printn("goal_two_to_two-compute_strategy\\")
        if self.trou() and not self.check_shoot():
            printnn("trou")
            return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
        if self.check_shoot() and not self.dvt_adv2or():
            printnn("shoot")
            self.clever.one_to_one_goal_auto1=1
            self.clever.one_to_one_goal_attack=1
            return self.to_change(TO_ATTACK)
        if self.check_no_goal():
            printnn("no goal")
            self.clever.one_to_one_goal_auto1=0
        if self.check_goal_dvt():
            printnn("dvt")
            self.clever.one_to_one_goal_auto1=0
            return self.dvt()
        if (not self.check_goal() and self.clever.one_to_one_goal_auto1) or self.bb():
            printnn("goal")
            return self.revien_goal()
        if self.check_attack():
            printnn("attack")
            return self.attack()
        if self.check_stop_alert():
            printnn("stop alert")
            self.clever.alert=0
            return self.stop_alert()
        if self.check_alert():
            printnn("alert")
            self.clever.alert=1
            return self.alert()
        printnn("ri")
        return SA()

    def __getattr__(self,name):
        return getattr(self.state,name)
###################################################
#BIBLI GOAL#######################################
###################################################
class Bibli_Goal:
    def __init__(self,state):
        self.bibli=self.state=state
    
    def revien_goal(self):
        s=self.state
        return SA(s.goal - s.ma_position,V2D())

    def check_attack(self):
        yh=self.ball_in_zone(GOAL_ATTACK)
        regle1=self.ma_position.distance(self.ball.position) < self.autre_position.distance(self.ball.position)
        regle2=self.ball_position.distance(self.ma_position) < GOAL_ATTACK
        return regle1 or regle2

    def attack(self):
        yi=usefull().simulate(self.moi,self.state)
        yy=self.next_position_ball(yi)
        k=PLAYER_RADIUS + BALL_RADIUS + settings.maxPlayerSpeed +2
        if self.ball_vitesse.norm < settings.maxPlayerSpeed and ((self.ma_position.distance(self.ball_position)<k or self.ma_position.distance(yi.position)<k or self.ma_position.distance(yy.position)<k))  :
           	yi=self.ball
       	return SA((yi.position-self.config.position).norm_max(yy.vitesse.norm),V2D())
    
    
    def shoot(self):
        yy=(GAME_HEIGHT-self.autre_player.position.y )*1.5
        while self.Min(abs(yy-self.autre_player.position.y),5):
            yy=yy*1.5
        y=V2D(75 ,yy)-self.state.ball.position
        return SA(V2D(),y)
    
    def check_stop_alert(self):
        yh=self.ball_in_zone(GOAL_ALERT)
        if self.id_team==1:
            g= self.ball_vitesse.x > 0
        else:
            g= self.ball_vitesse.x < 0
        ty=self.projector_ball_goal()
        return (not self.check_goal_m(20) or (yh and g and not self.check_goal_m(20))) and self.clever.alert==1

    def stop_alert(self):
        self.clever.one_to_one_goal_auto1=1
        self.alert=0
        return VIDE
    
    #A Enlever
    def bb(self):
        regle2=self.ball_position.distance(self.ma_position) < GOAL_ATTACK
        f=not self.check_goal_m(20) and (self.state.ball.position.distance(self.ma_position) > self.state.ball.position.distance(self.autre_position)) and not regle2
        if f:
            self.clever.one_to_one_goal_auto1=1
        return f
    
    #renvoi le V2D de la position dans les cages du goal, la plus proche de la balle
    def d_but(self):
        min=self.ball_position.distance(self.mes_goal +V2D(0,GAME_GOAL_HEIGHT/2))
        d=self.mes_goal +V2D(0,GAME_GOAL_HEIGHT/2)
        for i in range(-GAME_GOAL_HEIGHT/2,GAME_GOAL_HEIGHT/2):
            k=self.ball_position.distance(self.mes_goal +V2D(0,i))
            if k <min:
                min=k
                d=self.mes_goal +V2D(0,i)
        return d +V2D(self.mon_sens*4,0)

    def check_alert(self):
        yh=self.ball_in_zone(GOAL_ALERT)
        return yh and not self.check_ball() and abs(self.state.ball.vitesse.x) >=0
               
    def check_no_goal(self):
        return self.ball.position.distance(self.ma_position) < self.ball.position.distance(self.autre.position)
    
    def check_goal(self):
        return ( self.check_goal_m(0))
    
    #verifie si le joueur est au goal avec une marge @m
    def check_goal_m(self,m=0):
        s=self.state
        b=self.bibli
        return b.player_in_but(s.mes_goal,ZONE_GOAL + m,MODULO_GOAL+m)
                                     
    def check_ball(self):
        return self.has_ball_dvt()
    
    #Renvoi le x de la balle projeter sur l'axe des y du joueur
    def projector_ball_goal(self):
        ball=self.ball
        return self.projector_ball_x(ball,self.ma_position.x)
                                     
    def projector_ball_goal_x(self,ball):
        return self.projector_ball_x(ball,self.ma_position.x)

    def check_goal_dvt(self):
        angle=self.moi.position.angle
        if self.check_goal():
            if self.id_team==1:
                return angle != ANGLE1
            else:
                return angle != ANGLE2
        else:
            return False

    def alert(self):
        yy=self.projector_ball_goal()
        if self.In(yy,40,50):
            yi=usefull().simulate(self.moi,self.state)
            printnn(yi,self.ma_position)
            if True:
                return SA((yi.position-self.config.position).norm_max(self.ball_vitesse.norm),V2D())
            else:
                return SA(V2D(),V2D())
        else:
            f=self.d_but()
            printnn(f,self.ma_position)
            if not self.In(f.y,self.config.position.y-1,self.config.position.y+1):
                return SA((f-self.config.position).norm_max(0.1),V2D())
            else:
                return SA(V2D(),V2D())

    #check si joueur bien oriente
    def dvt(self):
        if self.id_team==1:
            return SA(V2D(angle=ANGLE1,norm=NORM_DVT),V2D(4,4))
        else:
            return SA(V2D(angle=ANGLE2,norm=NORM_DVT),V2D(4,4))

    def __getattr__(self,name):
        return self.bibli.get_attr(self.bibli,self.state,name)


############################################
#STRATEGIE ATTACK############################A RE-TRAVAILLER
#############################################
class attack_two_to_two(AS):
    def __init__(self,state):
        self.state=state
    
    def next_position_adv_ball(self):
	if self.dvt_adv2or():
		ai=self.dvt_adv2qui()
		pi=self.player(self._autre,ai)
	else:
		pi=self.autre
	action_ball = self.ball_position - pi.position
        s = self.next_position_player(action_ball, pi)
	return s 

    def joueur_pres_de_moi(self):
	if self.dvt_adv2or():
		ai=self.dvt_adv2qui()
		pi=self.player(self._autre,ai)
	else:
		pi=self.autre
	r1=self.ma_position.y - pi.position.y <=10
	r2=self.ma_position.y - pi.position.y >=0
	e1=r1 and r2
	r3=pi.position.y - self.ma_position.y <=10
	r4=pi.position.y - self.ma_position.y >=0
	e2=r3 and r4
	r5=self.In(abs(self.ma_position.x-pi.position.x),0,3)
	ef1=e1 and r5
	ef2=e2 and r5
	

	if self.ma_position.y>=self.mes_goal.y:
		return ef1
	else:
		return ef2

    def check_tir(self):
	return self.autre_goal.distance(self.ma_position)<=TIR_ZONE_ATTACK

    def attack_o(self):
        printnn("STRAT attack",self.id_team,self.id_player)
        if self.have_ball() :
            printnn("j\'ai la balle")
            auto_dvt_adv=self.dvt_adv2()
            next_position_adv_ball=self.next_position_adv_ball()
            if auto_dvt_adv:
                printnn("Je suis dvt adv")
                if self.check_tir():
                    printnn("Je peux tirer")
                    y=self.action_ball_moi()
                    return SA(V2D(0,0),(y).norm_max(TIR_NORM))
                else:
                    printnn("Je ne peux pas tirer (ma position, adv pos)",self.ma_position,self.autre_position)

                    if self.joueur_pres_de_moi():
                        printnn("Joueur pres de moi")
                    	if self.autre_position.y > self.ma_position.y:
                        	py=-1
                    	else:
                        	py=1

                    	y=V2D(self.ball_position.x+1.5*self.mon_sens,self.ball_position.y) -self.ball_position
                    	printnn(y)
			if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball):
                    		printnn("adv a la balle")
                    		return SA(V2D(),V2D((600)*self.mon_sens,-200))
                	if self.autre_ball():
				yy=self.ma_position.y
				d=abs(self.autre_position.x-self.ma_position.x)
				if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
					yy=self.ball_position.y
				else:
					if self.autre_position.y > self.ma_position.y:
				    		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
							yy=yy-0.25
							if yy == 0:
					    			break
					else:
				   		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER :
							yy=yy+0.25
							if yy == GAME_HEIGHT:
					    			break

				pm=V2D(self.ball_position.x ,yy)-self.ball.position
				y=(pm).norm_max(1.1)
				printnn("ic",y)
				return SA(V2D(),y)
			else:
                    		return SA(V2D(0,0),(y).norm_max(TIR_NORM))
		    else:
			printnn("Joueur pas pres de moi")
                    	nom=3.5
                    	y=self.goal2-self.state.ball.position
                    	return SA(V2D(0,0),(y).norm_max(nom))
            else:
                printnn("Je suis derriere adv")
		if self.dvt_adv2or():
			printnn("je suis dvt un joueur")
			ai=self.dvt_adv2qui()
			pi=self.player(self._autre,ai)
			auto_adv_ball_next=self.has_ball_merge(self.state,next_position_adv_ball,8)
		        if self.check_tir():
		            printnn("Je peux tirer")
			    ball=self.action_ball_moi()
		            y=self.autre_goal-self.ball_position
		            return SA(V2D(0,0),(y).norm_max(TIR_NORM))

		        if self.joueur_pres_de_moi():
		                printnn("Joueur pres de moi")
		            	if pi.position.y > self.ma_position.y:
		                	py=-1
		            	else:
		                	py=1
				if self.autre_ball() or auto_adv_ball_next :
				
					yy=self.ma_position.y
					d=abs(pi.position.x-self.ma_position.x)
					if abs(yy-pi.position.y) > d/1.5 +RAYON_BALL_PLAYER:
						yy=self.ball_position.y
					else:
						if pi.position.y > self.ma_position.y:
					    		while abs(yy-pi.position.y) <=d/1.5 +RAYON_BALL_PLAYER-0.5:
								yy=yy-0.25
								if yy == 0:
						    			break
						else:
					   		while abs(yy-pi.position.y) <=d/1.5 +RAYON_BALL_PLAYER -0.5:
								yy=yy+0.25
								if yy == GAME_HEIGHT:
						    			break

					pm=V2D(self.ball_position.x+1*self.sens ,yy)-self.ball.position
					y=(pm).norm_max(1.1)
					printnn("ic",y)
					return SA(V2D(),y)
		            	y=V2D(self.ball_position.x+1*self.sens,self.ball_position.y) -self.ball_position
		            	return SA(V2D(0,0),(y).norm_max(TIR_NORM))
		        if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball) or auto_adv_ball_next:
		            printnn("adv a la balle")
		            return SA(V2D(),V2D((600)*self.mon_sens,-200))
			if auto_adv_ball_next:
		                printnn("Adv aura la balle")
				yy=self.ma_position.y
				d=abs(pi.position.x-self.ma_position.x)
				if abs(yy-pi.position.y) > d/1.5 +RAYON_BALL_PLAYER:
					yy=self.ball_position.y
				else:
					if pi.position.y > self.ma_position.y:
					    while abs(yy-pi.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
						yy=yy-0.25
						if yy == 0:
						    break
					else:
					    while abs(yy-pi.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
						yy=yy+0.25
						if yy == GAME_HEIGHT:
						    break

					pm=V2D(self.ball_position.x +1*self.sens ,yy)-self.ball.position
					y=(pm).norm_max(1.1)
					printnn("ic",y)
					return SA(V2D(),y)
			else:
				printnn("Adv n\'aura pas la balle",self.clever.one_to_one_goal_attack)
				if self.autre_position.y > self.ma_position.y:
				    py=-1
				else:
				    py=1
				if self.In(abs(self.ma_position.y-self.autre_position.y),0,3):
				    nom=0.8
				else:
				    nom=1.5
				y=self.goal2 - self.state.ball.position
				return SA(V2D(0,0),(y).norm_max(nom))
		else:
			print("je suis derriere tout le monde")
		
		        if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball):
		            printnn("adv a la balle")
		            return SA(V2D(),V2D((600)*self.mon_sens,-200))

		        auto_adv_ball_next=self.has_ball_merge(self.state,next_position_adv_ball,8)

		        if self.check_tir():
		            printnn("Je peux tirer")
			    ball=self.action_ball_moi()
		            y=self.autre_goal-self.ball_position
		            return SA(V2D(0,0),y)

		        if self.joueur_pres_de_moi():
		                printnn("Joueur pres de moi")
		            	if self.autre_position.y > self.ma_position.y:
		                	py=-1
		            	else:
		                	py=1
				if self.autre_ball() or auto_adv_ball_next :
				
					yy=self.ma_position.y
					d=abs(self.autre_position.x-self.ma_position.x)
					if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
						yy=self.ball_position.y
					else:
						if self.autre_position.y > self.ma_position.y:
					    		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER-0.5:
								yy=yy-0.25
								if yy == 0:
						    			break
						else:
					   		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER -0.5:
								yy=yy+0.25
								if yy == GAME_HEIGHT:
						    			break

					pm=V2D(self.ball_position.x+1*self.sens ,yy)-self.ball.position
					y=(pm).norm_max(1.1)
					printnn("ic",y)
					return SA(V2D(),y)
		            	y=V2D(self.ball_position.x+1*self.sens,self.ball_position.y) -self.ball_position
		            	return SA(V2D(0,0),(y).norm_max(TIR_NORM))
		        if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball) or auto_adv_ball_next:
		            printnn("adv a la balle")
		            return SA(V2D(),V2D((600)*self.mon_sens,-200))
			if auto_adv_ball_next:
		                printnn("Adv aura la balle")
				yy=self.ma_position.y
				d=abs(self.autre_position.x-self.ma_position.x)
				if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
					yy=self.ball_position.y
				else:
					if self.autre_position.y > self.ma_position.y:
					    while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
						yy=yy-0.25
						if yy == 0:
						    break
					else:
					    while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
						yy=yy+0.25
						if yy == GAME_HEIGHT:
						    break

					pm=V2D(self.ball_position.x +1*self.sens ,yy)-self.ball.position
					y=(pm).norm_max(1.1)
					printnn("ic",y)
					return SA(V2D(),y)
               		else:
				printnn("Adv n\'aura pas la balle",self.clever.one_to_one_goal_attack)
				if self.autre_position.y > self.ma_position.y:
				    py=-1
				else:
				    py=1
				if self.In(abs(self.ma_position.y-self.autre_position.y),0,3):
				    nom=0.8
				else:
				    nom=1.5
				y=self.autre_goal-self.ball_position
				printn("y aut",y)
				return SA(V2D(0,0),(y).norm_max(nom))
                                
        
        else:
		printnn("j\'ai pas la balle")
		yi=usefull().simulate(self.moi,self.state)
		return SA(yi.position-self.config.position,V2D(0,0))


    def compute_strategy(self):
        printn("attack_two_to_two-compute_strategy\\")
        if self.trou() and not self.check_shoot():
            printnn("trou")
            return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
        if self.clever.two_to_two_goal_attack==1 and self.autre_ball() and not self.check_shoot() or (self.has_ball(self.state,self.player(self.id_team,1-self.id_player).position) and self.clever.two_to_two_goal_attack==1):
            self.clever.two_to_two_goal_attack=0
            return self.to_change(TO_GOAL)
        if self.clever.one_to_one_goal_attack==1 and self.autre_ball() and not self.check_shoot():
            self.clever.one_to_one_goal_attack=0
            self.clever.alert=1
            return self.to_change(TO_GOAL)
        
        return self.attack_o()
                                     
    def __getattr__(self,name):
       return getattr(self.state,name)

                                                                      
class attack_one_to_one(AS):
    def __init__(self,state):
        self.state=state
    
    def trouve(self):
        a=self.autre_position.y
    
    def next_position_adv_ball(self):
	action_ball = self.action_ball_adv()
        s = self.next_position_player(action_ball, self.autre_player)
	return s 

    def joueur_pres_de_moi(self):
	r1=self.ma_position.y - self.autre_position.y <=10
	r2=self.ma_position.y - self.autre_position.y >=0
	e1=r1 and r2
	r3=self.autre_position.y - self.ma_position.y <=10
	r4=self.autre_position.y - self.ma_position.y >=0
	e2=r3 and r4
	r5=self.In(abs(self.ma_position.x-self.autre_position.x),0,3)
	ef1=e1 and r5
	ef2=e2 and r5
	

	if self.ma_position.y>=self.mes_goal.y:
		return ef1
	else:
		return ef2

    def check_tir(self):
	return self.autre_goal.distance(self.ma_position)<=TIR_ZONE_ATTACK


    def attack_o(self):
        printnn("STRAT attack",self.id_team,self.id_player)
        if self.have_ball() :
            printnn("j\'ai la balle")
            auto_dvt_adv=self.dvt_adv()
            next_position_adv_ball=self.next_position_adv_ball()
            if auto_dvt_adv:
                printnn("Je suis dvt adv")
                if self.check_tir():
                    printnn("Je peux tirer")
                    y=self.action_ball_moi()
                    return SA(V2D(0,0),(y).norm_max(TIR_NORM))
                else:
                    printnn("Je ne peux pas tirer (ma position, adv pos)",self.ma_position,self.autre_position)

                    if self.joueur_pres_de_moi():
                        printnn("Joueur pres de moi")
                    	if self.autre_position.y > self.ma_position.y:
                        	py=-1
                    	else:
                        	py=1

                    	y=V2D(self.ball_position.x+1.5*self.mon_sens,self.ball_position.y) -self.ball_position
                    	printnn(y)
			if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball):
                    		printnn("adv a la balle")
                    		return SA(V2D(),V2D((600)*self.mon_sens,-200))
                	if self.autre_ball():
				yy=self.ma_position.y
				d=abs(self.autre_position.x-self.ma_position.x)
				if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
					yy=self.ball_position.y
				else:
					if self.autre_position.y > self.ma_position.y:
				    		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
							yy=yy-0.25
							if yy == 0:
					    			break
					else:
				   		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER :
							yy=yy+0.25
							if yy == GAME_HEIGHT:
					    			break

				pm=V2D(self.ball_position.x ,yy)-self.ball.position
				y=(pm).norm_max(1.1)
				printnn("ic",y)
				return SA(V2D(),y)
			else:
                    		return SA(V2D(0,0),(y).norm_max(TIR_NORM))
		    else:
			printnn("Joueur pas pres de moi")
                    	nom=3.5
                    	y=self.goal2-self.state.ball.position
                    	return SA(V2D(0,0),(y).norm_max(nom))
            else:
                printnn("Je suis derriere adv")

                if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball):
                    printnn("adv a la balle")
                    return SA(V2D(),V2D((600)*self.mon_sens,-200))

                auto_adv_ball_next=self.has_ball_merge(self.state,next_position_adv_ball,8)

                if self.check_tir():
                    printnn("Je peux tirer")
		    ball=self.action_ball_moi()
                    y=self.autre_goal-self.ball_position
                    return SA(V2D(0,0),y)

                if self.joueur_pres_de_moi():
                        printnn("Joueur pres de moi")
                    	if self.autre_position.y > self.ma_position.y:
                        	py=-1
                    	else:
                        	py=1
			if self.autre_ball() or auto_adv_ball_next :
				
				yy=self.ma_position.y
				d=abs(self.autre_position.x-self.ma_position.x)
				if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
					yy=self.ball_position.y
				else:
					if self.autre_position.y > self.ma_position.y:
				    		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER-0.5:
							yy=yy-0.25
							if yy == 0:
					    			break
					else:
				   		while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER -0.5:
							yy=yy+0.25
							if yy == GAME_HEIGHT:
					    			break

				pm=V2D(self.ball_position.x+1*self.sens ,yy)-self.ball.position
				y=(pm).norm_max(1.1)
				printnn("ic",y)
				return SA(V2D(),y)
                    	y=V2D(self.ball_position.x+1*self.sens,self.ball_position.y) -self.ball_position
                    	return SA(V2D(0,0),(y).norm_max(TIR_NORM))
                if self.autre_ball() or self.has_ball(self.ball,next_position_adv_ball) or auto_adv_ball_next:
                    printnn("adv a la balle")
                    return SA(V2D(),V2D((600)*self.mon_sens,-200))
		if auto_adv_ball_next:
                        printnn("Adv aura la balle")
			yy=self.ma_position.y
			d=abs(self.autre_position.x-self.ma_position.x)
			if abs(yy-self.autre.position.y) > d/1.5 +RAYON_BALL_PLAYER:
				yy=self.ball_position.y
			else:
				if self.autre_position.y > self.ma_position.y:
				    while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
					yy=yy-0.25
					if yy == 0:
					    break
				else:
				    while abs(yy-self.autre.position.y) <=d/1.5 +RAYON_BALL_PLAYER:
					yy=yy+0.25
					if yy == GAME_HEIGHT:
					    break

				pm=V2D(self.ball_position.x +1*self.sens ,yy)-self.ball.position
				y=(pm).norm_max(1.1)
				printnn("ic",y)
				return SA(V2D(),y)
                else:
                        printnn("Adv n\'aura pas la balle",self.clever.one_to_one_goal_attack)
		        if self.autre_position.y > self.ma_position.y:
		            py=-1
		        else:
		            py=1
		        if self.In(abs(self.ma_position.y-self.autre_position.y),0,3):
		            nom=0.8
		        else:
		            nom=1.5
		        y=V2D(self.goal2.x,self.ball_position.y + 2.4*py*(abs(self.ma_position.x-self.autre_position.x))) -self.state.ball.position
		        return SA(V2D(0,0),(y).norm_max(nom))
                                
        
        else:
            printnn("j\'ai pas la balle")
            yi=usefull().simulate(self.moi,self.state)
            return SA(yi.position-self.config.position,V2D(0,0))


    def compute_strategy(self):
        printn("attack_one_to_one-compute_s trategy\\")
        if self.trou() and not self.check_shoot():
            printnn("trou")
            return SA(V2D(self.ma_vitesse.x*-1,self.ma_vitesse.y*-1),V2D())
        if self.clever.two_to_two_goal_attack==1 and self.autre_ball() and not self.check_shoot():
            self.clever.two_to_two_goal_attack=0
            return self.to_change(TO_GOAL)
        if self.clever.one_to_one_goal_attack==1 and self.autre_ball() and not self.check_shoot():
            self.clever.one_to_one_goal_attack=0
            self.clever.alert=1
            return self.to_change(TO_GOAL)
        
        return self.attack_o()
                                     
    def __getattr__(self,name):
       return getattr(self.state,name)

                                     
###############################################
#FORCEUR######################################
#############################################
class forceur(AS):
    def __init__(self,state):
        AS.__init__(self,"forceur_one_to_one")
        self.state=state
        
    def compute_strategy(self):
        printn("fonceur-compute_strategy\\")

        id_team=self.id_team
        id_player=self.id_player
        state=self.state
        vod=0
        if id_team==1:
            vod=T1_SENS*COEFF_FORCEUR
            vo=T1_BUT
        elif id_team==2:
            vod=T2_SENS*COEFF_FORCEUR
            vo=T2_BUT
        position=self.ma_position
        ball_to_player=self.state.ball.position.distance(self.state.player(self.id_team,self.id_player).position)
        goal_to_player=self.state.player(self.id_team,self.id_player).position.distance(V2D(vo,GAME_HEIGHT/2))
        goal_to_ball= self.goal2-self.ma_position
        ball= PLAYER_RADIUS + BALL_RADIUS
        if self.have_ball():
            return SA(V2D(0,0),goal_to_ball+V2D(0,randint(-75,75)))
        else:
            return SA(self.ball.position - self.ma_position)

    def __getattr__(self,name):
        return getattr(self.state,name)

#CONTROLE DU PRINT
def printn(*args, **kwargs):
    if PRINT:
        print(args)
    return

def printnn(*args, **kwargs):
    if PRINTN:
        print(args)
    return

#######################################################
#DECORATEUR############################################
#######################################################
class StatePlayer:
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

    @property
    def ma_position_m(self):
        return usefull().mirror(self.ma_position,self.id_team)
    
    def __getattr__(self,name):
        return getattr(self.state,name)

class StateTerrain:
    def __init__(self,state,id_team,id_player):
        self.state=state
        self._state=state
        self.id_team=id_team
        self.id_player=id_player
        if id_team==1:
            self.mes_goal=self.goal=GOAL1
            self.autre_goal=self.goal2=GOAL2
            self.mon_sens=self.sens=T1_SENS
        elif id_team==2:
            self.mes_goal=self.goal=GOAL2
            self.autre_goal=self.goal2=GOAL1
            self.mon_sens=self.sens=T2_SENS
    
    def __getattr__(self,name):
        return getattr(self.state,name)

class StateBall:
    def __init__(self,state,id_team,id_player):
        self.state=state
        self.id_team=id_team
        self.id_player=id_player
        self.ball=self.state.ball
        self.ball_position=self.ball.position
        self.ball_vitesse=self.ball.vitesse

    def __getattr__(self,name):
        return getattr(self.state,name)

################################################
#Proxy##########################################
################################################
# Historique + autorisation de changement de strategie du round (global), et changement pendant une strategie (temporaire) + fct changeant les strategies + variable informant d'un changement
class clever(object):
        def __init__(self):
                for k, c in dico_clever.items():
                   setattr(self, k, c)

	# reset variable +historique
        def begin_match(self,m):
                printn("begin match master_round",self.master_round,"master",self.master)
                for k, c in dico_clever_up.items():
                    setattr(self, k, c)

        # reset variable et change la strategie actuel en  strategie de round 
        def begin_round(self):
                printn("begin round  master_round",self.master_round,"master",self.master)
                self.master=self.master_round
                for k, c in dico_clever_up.items():
                    setattr(self, k, c)

	#rempli historique avec id-strate , id-team gagnant, si id-team gagnant est celle de adv on appelle check
        def end_round(self,state,bibli):

            printn("end round  master_round",self.master_round,"master",self.master)
            self.history_me[self.master_round]=state._winning_team
            if state._winning_team != bibli.id_team:
                self.check(bibli)
            return

        # reset variable +historique
        def end_match(self):
                self.master=self.master_round=self.master_debut
                printn("end match master_debut",self.master_debut,"master_round",self.master_round,"master",self.master)
                self.history_me.clear()
                for k, c in dico_clever_up.items():
                    setattr(self, k, c)
	
 	# cherche quel strategie choisir (quels strategies qui n'a jms perdu)
        def check(self,bibli):
            y = self.tech[:]
            for key, value in self.history_me.items():
                if value != bibli.id_team:
                    if key in y:
                        y.remove(key)
            if len(y) > 0:
                self.auto_master(y[0],bibli)
            else:
                self.count+=1
                if self.count==1:
                    self.count=0
                    self.history_me.clear()
                    self.check(bibli)
        
            return

	#change la strategie du round (master_round) en num
        def auto_master(self,num,bibli):
            printn("strategie round changé en ",num)
            self.master_round=num
	    return
        


############################################################
#BIBLIOTHEQUE###############################################
############################################################
#fct utile bas niveau
class usefull:
    def __init__(self):
        self.name="d"
    
    #cherche dans a et b c(nom)
    def get_attr(self,a,b,c):
        try:
            return getattr(a, c)
        except:
            return getattr(b,c)
    
    #cherche dans a et b et c d(nom)
    def get_attr3(self,a,b,c,d):
        try:
            return getattr(a, d)
        except:
            try:
                return getattr(b, d)
            except:
                return getattr(c,d)

    #renvoi la position de la balle simule au max pour quelle soit dvt le joueur demande
    def simulate(self,config,state):
        i=0
        a=state.copy()
        a=a.ball

        while self.balle_dvt(config,state.id_team,a) and i<=10:
            aa=self.next_position_ball(a)
            bb=self.balle_dvt(config,state.id_team,aa)
            if bb:
                a=aa
            else:
                return a
            i+=1
        i=0
        return a
    
    def next_position_player(self,dis,config):
        config_state_vitesse = config._state.vitesse * (1 - settings.playerBrackConstant) #frottemnt
        config_state_vitesse = (config_state_vitesse+dis.norm_max(settings.maxPlayerAcceleration)).norm_max(settings.maxPlayerSpeed)
        config_state_position = config._state.position+ config_state_vitesse.norm_max(settings.maxPlayerSpeed)
        return config_state_position
    
    #check si balle dvt joueur (par rapport au sens du jeu(par rapport a leurs directions pour marquer dans le but de l'adv))
    def balle_dvt(self,config,id_team,ball):
        if id_team==1:
            return ball.position.x > config.position.x
        else:
            return ball.position.x<config.position.x

    #check si a la @position indique la balle est frappable avec un marge @m
    def has_ball(self,ball,position,m=0):
        try:
            return ball.position.distance(position) <= RAYON_BALL_PLAYER + m
        except:
            return ball.ball.position.distance(position) <= RAYON_BALL_PLAYER + m

    def has_ball_merge(self,ball,position,m):
        return self.has_ball(ball,position,m)

    def _near_of_me(self,config1,id_team,state):
        po=0
        g=ma_position.distance(state.player(id_team,po).position)
        pp=1
        i=config1.position.distance(state.player(id_team,pp).position)
        if g<i:
            j=state.player(id_team,po)
        else:
            j=state.player(id_team,pp)
        return j

    def next_position_ball(self,ball):
        try:
            ballo=Ball(V2D(ball.position.x,ball.position.y),V2D(ball.vitesse.x,ball.vitesse.y))
            ballo.next(V2D())
        except:
            ballo=Ball(V2D(ball.ball.position.x,ball.ball.position.y),V2D(ball.ball.vitesse.x,ball.ball.vitesse.y))
            ballo.next(V2D())
        return ballo

    def projector_ball_x(self,ball,position_x):
        if ball.vitesse.x != 0:
            lamda=(position_x-ball.position.x)/ball.vitesse.x
            return ball.vitesse.y*lamda + ball.position.y
        else:
            return ball.position.y

    def mirror(self,position,id_team):
        if id_team==2:
            return V2D(GAME_WIDTH-position.x,GAME_HEIGHT-position.y)
        return position

    def Min(self,n,min):
        return n<=min

    def Max(self,n,max):
        return n>=max

    def In(self,b,min,max):
        return self.Min(b,max) and self.Max(b,min)

    def In_m(self,position,but,marge):
        return self.In(position, but-marge,but+marge)

#Fct haut niveau ayant besoin de d'info sur joueur, ball, terrain
class Bibli_Player:
        def __init__(self,state,bibli):
            self.state=state
            self.bibli=bibli
            self.autre_player=self.autre
        
        def nb_p(self):
            return len([x for x in self._configs.keys()])
        
        #le vecteur acceleration pour que le joueurs se dirige vers le balle
        def action_ball_moi(self):
            return self.ball_position - self.ma_position
        
        #le vecteur acceleration pour que le joueurs adv se dirige vers le balle
        def action_ball_adv(self):
            return self.ball_position - self.autre_position
               
        @property
        def autre(self):
            return self.near_of_me()
               
        @property
        def autre_position(self):
            return self.autre.position
               
        @property
        def autre_vitesse(self):
            return self.autre.vitesse
        
        #check si joueur a la balle
        def have_ball(self):
            return self.has_ball(self.ball,self.ma_position)
        
        #check si joueur dvt adv
        def dvt_lui(self,him):
            me=self.ma_position
            if self.id_team==1:
                return me.x >him.x
            else:
                return me.x <him.x
               
        def attack(self):
            yi=usefull().simulate(self.moi,self.state)
            yy=self.next_position_ball(yi)
            k=PLAYER_RADIUS + PLAYER_RADIUS + settings.maxPlayerSpeed
            if self.ball_vitesse.norm < settings.maxPlayerSpeed and (self.ma_position.distance(self.ball_position)<k or self.ma_position.distance(yi.position)<k or self.ma_position.distance(yy.position)<k):
                yi=self.ball
            return SA((yi.position-self.config.position).norm_max(yy.vitesse.norm),V2D())
        
        #check si le joueur va avoir la balle au prochain step
        def has_ball_next(self):
            f=self.next_position_ball_state()
            return self.has_ball(f,self.ma_position)
        
        #check si au prochain step le joueurs aurai la balle sans bouger
        def trou(self):
            yp=self.next_position_ball_state()
            yo=self.next_position_ball(yp)
            yy=self.next_position_ball(yo)
            return self.has_ball(yo,self.ma_position) or self.has_ball(yp,self.ma_position) or self.has_ball(yy,self.ma_position)
        
        #check si joueur oriente du bon cote
        def has_ball_dvt(self):
            him=self.near_of_me()
            return self.have_ball() and not self.dvt_lui(him.position)

        def check_shoot(self):
            return self.have_ball()
        
        #check si dvt adv le plus proche de lui
        def dvt_adv(self):
            him=self.near_of_me()
            return self.dvt_lui(him.position)
        
        #check si dvt les 2 joueurs adv
        def dvt_adv2(self):
            him=self.player(self._autre,0)
            him2=self.player(self._autre,1)
            return self.dvt_lui(him.position) and self.dvt_lui(him2.position)
        
        #check si dvt l'un des 2 joueurs adv
        def dvt_adv2or(self):
            him=self.player(self._autre,0)
            him2=self.player(self._autre,1)
            return self.dvt_lui(him.position) or self.dvt_lui(him2.position)

        #renvoi l'id_player de l'adv qui est dvt le joueur (fct utiliser que si dvt_adv2or est vrai)
        def dvt_adv2qui(self):
            him=self.player(self._autre,0)
            him2=self.player(self._autre,1)
            if self.dvt_lui(him.position):
                return 1
            else:
                return 0

        #check un adv a la balle
        def autre_ball(self):
            nb=self.nb_p()/2
            for i in range (0,nb):
                if self.has_ball(self.ball,self.state.player(self._autre,i).position):
                    return 1
            return 0
    
        #donne le joueur le plus proche
        def near_of_me(self):
            config1,id_team,state = self.moi,self._autre,self.bibli
            if self.nb_p()==2:
                return state.player(id_team,0)
            po=0
            g=self.ma_position.distance(state.player(id_team,po).position)
            pp=1
            i=self.ma_position.distance(state.player(id_team,pp).position)
            if g<i:
                j=state.player(id_team,po)
            else:
                j=state.player(id_team,pp)
            return j

        #check si joueur dans la zone @but avec une marge en x et y
        def player_in_but(self,but,marge_x,marge_y):
            but=GOAL1
            return self.In_m(self.ma_position_m.x,but.x,marge_x) and self.In_m(self.ma_position.y,but.y,marge_y)

        def __getattr__(self,name):
            return self.bibli.get_attr(self.bibli,self.state,name)

#Fct haut niveau necessitant la balle et usefull
class Bibli_Ball:
    def __init__(self,state,d):
        self.state=state
        self.d=d
    
    
    def next_position_ball_state(self):
        return self.next_position_ball(self.state)
    
    #check si ball dans la @zone
    def ball_in_zone(self,zone):
        return abs(self.ball_position.x - self.mes_goal.x) <= zone

    def __getattr__(self,name):
        return  self.d.get_attr(self.state,self.d,name)

#nulm
class ia(AS):
    def __init__(self):
        AS.__init__(self,"ia") 
        
    def compute_strategy(self,state,id_team,id_player):
        return


