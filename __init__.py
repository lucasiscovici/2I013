from soccersimulator import settings, SoccerAction,Vector2D,DecisionTreeClassifier, KeyboardStrategy, BaseStrategy
from soccersimulator import export_graphviz
from soccersimulator import *
import Walter2 as W2
from WalterIA import *
import os
fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),"tree.pkl")
import cPickle
import sys
def gen_features(state,id_team,id_player):
    bpos = state.ball.position
    mpos = state.player_state(id_team,id_player).position
    myg = Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    return [bpos.distance(mpos),bpos.distance(myg),bpos.distance(hisg)]
#Nom des features (optionel)
gen_features.names = ["ball_dist","mygoal_dist","hisgoal_dist"]


def build_apprentissage(fn,generator):
    ex_raw = KeyboardStrategy.read(fn)
    exemples = []
    labels = []
    for x in ex_raw:
        exemples.append(generator(x[1],x[0][0],x[0][1]))
        labels.append(x[0][2])
    return exemples,labels

def apprendre_arbre(train,labels,depth=5,min_samples_leaf=2,min_samples_split=2):
    tree= DecisionTreeClassifier(max_depth=depth,min_samples_leaf=min_samples_leaf,min_samples_split=min_samples_split)
    tree.fit(train,labels)
    return tree

def affiche_arbre(tree):
    long = 10
    sep1="|"+"-"*(long-1)
    sepl="|"+" "*(long-1)
    sepr=" "*long
    def aux(node,sep):
        if tree.tree_.children_left[node]<0:
            ls ="(%s)" % (", ".join( "%s: %d" %(tree.classes_[i],int(x)) for i,x in enumerate(tree.tree_.value[node].flat)))
            return sep+sep1+"%s\n" % (ls,)
        return (sep+sep1+"X%d<=%0.2f\n"+"%s"+sep+sep1+"X%d>%0.2f\n"+"%s" )% \
                    (tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_left[node],sep+sepl),
                    tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_right[node],sep+sepr))
    return aux(0,"")
class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict([self.gen_feat(state,id_team,id_player)])[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)


tree = cPickle.load(file(fn))
dic = {"GOAL":all2(2),"ATTACK":all2(3),"FORCEUR":all2(1),"GOGOLE":gogole()}
treeStrat = DTreeStrategy(tree,dic,gen_features)
teamIA = SoccerTeam("keyb",[Player("KBs", treeStrat)])
team1= STe("psg",[Player("Thiago Silva",W2.all(2))])
team2= STe("psg",[Player("Thiago Silva",W2.all(2)),Player("Ibra",W2.all(3))])
team4=STe("mars",[Player("Thiago Silva",W2.all(2)),Player("Ibra",W2.all(1)),Player("Cavani",W2.all(3)),Player("Thiago Silva",W2.all(2))])

