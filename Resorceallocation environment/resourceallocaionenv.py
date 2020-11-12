import numpy as np
import gym
from gym import spaces
from addvehicle import Addvehicle
from gym.envs.registration import EnvSpec
#This environment is a base model for vehicular networking resource allocation
# This is the environment for the all the vehicles acting as agents in the the vehicular networking
class MultiAgentresourceallocation(gym.Env):
    metadata ={
        'render.modes':['human','rgb_array']
    }
    def __init__(self,aglist,world,observation=None, policy=0,reset=None,reward=None, info=None, done=None):
        #this is the world
        self.world=world
        #policy the ageent follows
        self.vehicle_policy=policy
        #environment reset parameter
        self.reset=reset
        #the reward parameter
        self.reward=reward
        #this contains the states
        self.observation=observation
        #this is the variable done
        self.done=done
        #this variable containsthe inofmration
        self.info=info
        self.vehicles=[]
        self.no_of_ResourecBlock=20
        self.no_of_vehicles=60

        #self.vehicles= Addvehicle(self.startpos, self.startdirec, self.startvelo)

        #TODO
        #define V2V or V2I for the vehicles communication

        self.sharedreward=world.collaborative if hasattr(world,'collaborative') else False
        #this give no of steps
        self.no_of_step=0
        #this give the action space
        self.action_space=[]
        #this gives the observation space for the states
        self.observation_space=[]
        for vehicles in self.vehicle_policy:
            total_actions=[]

            agent_space=spaces.Discrete(vehicles.action.dim_a)

            total_actions.append(agent_space)

            #checking the condition
            if len(total_actions)>1:
                if all([isinstance(actions,spaces.Discrete) for actions in total_actions]):
                    NotImplementedError
                    #TODO
                    #ADD ACTIONS TO MULTIDISCRETE SPACE
                else:
                    actions=spaces.Tuple(total_actions)
                self.action_space.append(actions)
            else:
                self.action_space.append(total_actions[0])

            #Now also defining the observatuon space for the states
            dimensions=len(observation(vehicles,self.world,step=0))
            self.observation.append(spaces.Box(low=0, high=+np.inf,shape=(dimensions),dtype=np.float32))


     #adding a new vehicle agent based on start position, direction, and the velocity
    def new_vehicle_add(self,startpos,startdirec,startvelo):
        self.vehicles.append(Addvehicle(startpos, startdirec, startvelo))

    def actionstep(self,actions, no_of_step,type="maddpg"):
        observation=[]
        done=[]
        reward_total=[]
        info=[]
        #policy for the vehicles as teh agents
        self.vehicle_policy=self.world.policy
        for x,vehicle_po in(self.vehicle_policy):
            self.actionperform(actions[x],vehicle_po,self.action_space[x])
        # taking action in the world states
        self.world.step(actions)


        for vehicle_po in self.vehicle_policy:
            obser=self.obsperform(vehicle_po,no_of_step)
            observation.append(obser)
            done.append(self.doneperform(vehicle_po))

 #gettring reward, numbers of seteps, delays , loss rate for multiagent approach
            reward,number,delays,lossrate=self.rewardget(type)
            if self.sharedreward and np.size(reward)==1:
                reward_total=[reward] * self.no_of_vehicles
            else:
                reward_total=reward

            #Now we can get the averafge delay for the action
            observation_delay=observation

            return observation_delay, reward_total, done,info,number, delays, lossrate

#This function is used to reset the environment
    def reset(self, training, steps,arglist, test=False,Vehicle_test=None):
        self.reset(self.world, training,steps,arglist,test,Vehicle_test)

        #now rendering for the episodes:
        self.render()
        observation=[]
        self.vehicle_policy=self.world.policy
        Delay=np.zeros(self.world.agent_num)

        for vehicle_agents in self.vehicle_policy:
            Delay[vehicle_agents.id],vehicle_agents.state.loss=self.getdelayeachagent(vehicle_agents,self.world,vehicle_agents.serve_rate)
            vehicle_agents.state.Delay=Delay[vehicle_agents.id]
            observ=self.obsperform(vehicle_agents,steps)
            observation.append(observ)


        self.world.delay=self.getdelays(transmissiondelay, propagationdelay,responsedelay)
        return  observation


    def getdelays(self, transmissiondelay, propagationdelay, reponsedelay):
        #TODO
      #This fuction is used to give total delay in
      #resource allocation due to transmission, control and reponse
        return NotImplementedError()

    def Queue_for_delay(self):

        #Todo
#This function maintains the queue fro the eelayes for esource allocation to the agent
        return NotImplementedError()

    def lossrate(self):
        #TODO
  #tHIS FUNCTION CALCULATE THE LOSS RATE FOR EACH CONTRLLER
      return NotImplementedError()
    #This function gets observation for the vehicle agent
    def obsperform(self,vehicle_agent):
        if self.observation is None:
            return {}
        return self.observation(vehicle_agent,self.world)
   #This gunction gets dones for the vehicle agent
    def doneperform(self, vehicle_agent):
        if self.done is None:
            return {}
        return self.done(vehicle_agent, self.world)

    #This function gets actions for the agent
    def actionperform(self,action,vehicle_agent):
        return NotImplementedError()


#The above is the environment for the vehicular networking for the resource aloocation thiis just a base model for development










