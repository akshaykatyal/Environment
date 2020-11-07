import numpy as np
#This class act as the specifictation class for the hider and seeker the is the definition class
class Hideseekspec(object):
    def __init__(self,nos,noa,alpha_rate):
        self._nos = nos
        self._noa = noa
        self._alpha_rate = alpha_rate

    @property
    #this function returns the number of states
    def nos(self) -> int:
        return  self._nos

    @property
    #this function gives the number of actions possible
    def noa(self) -> int:
        return self._noa

    @property
    # this the discont rate denoted by alpha
    def alpha_rate(self) -> float:
        return self._alpha_rate
#This class act like the hide and seek game environment class
class Hideseekenv(object):
    def __init__ (self, hideseek_spec):
        self._hideseek_spec= hideseek_spec
    #getting specifications from the above class
    @property
    def features(self) -> Hideseekspec:
        return self._hideseek_spec
    #this function reset the environment
    def envreset(selfself) -> int:
        raise NotImplementedError()

    #this function gives the next state taken by the player
    def step(self, player_action:int) -> (int,int,bool):
        raise NotImplementedError()
#This is the base class for the model environment class
class Hideseekenvmodel(Hideseekenv):
    @property
    #this function gives the reward for player action
    def reward(self) -> np.array:
        #this function returns a array
        return NotImplementedError()
    @property
    # This function gives the transition when player performs an action
    def Playactiontransition(self) -> np.array:
        #this function returns a array
        raise NotImplementedError()



