import numpy as np
from Hiderandseeker1 import Hideseekspec,Hideseekenv
class HidernSeekerimp(Hideseekenv):
    #init function that act as contructor for the class objcets
    def __init__(self, Xcord, Ycord, nh, ns, hidevisibility, seekervisibility, episode, bricks, alpha_rate=0.9):
        #agents = number of hiders+number of seekers.
        self.agents=nh+ns
        # walls to hide
        self.bricks=bricks
        # specification of the game
        self.hideseek_spec = Hideseekspec (self.agents * Xcord * Ycord, 9 , alpha_rate)
        self.episode = episode
        self.step = 0
        #no of hiders
        self.nh = nh
        # no of seekers
        self.ns = ns
        self.Xcord = Xcord
        self.Ycord = Ycord
        #setting the visibility of hider and seeker
        assert hidevisibility*2+1 <= Xcord and hidevisibility*2+1 <=Ycord, "it is very large"
        assert seekervisibility*2+1 <= Xcord and seekervisibility*2+1 <=Ycord, "it is very large"
        #hidevisibility is the visibility of cube of vision
        self.hidevisibility=hidevisibility
        #sekvisibility is visibility of cube of vision
        self.seekervisibility=seekervisibility
        #seeting up the display size of the game
        self.model_env=np.zeros((self.Xcord, self.Ycord))
        self.init_envmodel()
        self.dimensions=[self.agents,self.Xcord,self.Ycord]
        self.dimen_step=self.hideseek_spec.nos

     #function to display game environment model
    def print_envmodel(self):
        print("\n This shows the beginng of game model")
        print("-----------------------------------")
        # the model shows H hider, W as bricks wall, and S as seeker
        for j in range(self.Xcord):
            model=""
            for x in range(self.Ycord):
                options=self.model_env[j][x]
                if options ==0:
                    model += " ."
                elif options == 1:
                    model += "W"
                elif options == 2:
                    model += "H"
                else:
                    model +="S"
            print(model)
        print("----------------------------------")
        print("End of the game model")

    # fucntion to save the state of the model
    def save_envmodel(self, modelfile, episode):
        visibility=[]
        # the model shows H hider, W as bricks wall, and S as seeker
        for j in range(self.Xcord):
            model= " "
            for x in range(self.Ycord):
                options=self.model_env[j][x]
                if options == 0:
                    model +="."
                elif options == 1:
                    model += "W"
                elif options == 2:
                    model += "H"
                else:
                    model += "S"
            visibility.append(model)
        with open(modelfile,"a") as f:
            f.write("\n the episode no %d \n" %(episode))
            f.write(", ".join(visibility))
    # Function to reset the environment and return the position of the hiders and seekers
    def envset(self):
        self.step=0
        self.init_envmodel()
        no_of_hiders, _=self.reward_agent(self.hider_list, self.hidevisibility, type="hider")
        no_of_seeker,_ =self.reward_agent(self.seeker_list,self.seekervisibility, type="seeker")
        return no_of_hiders,no_of_seeker

   #
    def init_envmodel(self):
        #define the model environment for the game, here 0=normal stae, 1=wall,2=hider,3=seeker, 4=unknown, 5=position of the self agaent

        self.numO=6
        # displaying walls in the model environment
        for j in range(self.Xcord):
            for x in range(self.Ycord):
                if j==0 or j==self.Xcord-1 or x==0 or x== self.Ycord-1:
                    self.model_env[j][x]=1
                else:
                    self.model_env[j][x]=0

        #Now we define different types of walls bricks arrangement
        if self.bricks == "none":
            brick_list=[]
        if self.bricks== "two_brick":
            brick_list=[[3,3],[4,3],[5,3],[6,3],[8,8],[7,8],[6,8],[5,8]]
        if self.bricks=="diagonal":
            brick_list=[]
        for brick in brick_list:
            self.model_env[tuple(brick)]=1

        #Function to get the coordinates using random int
        def coordinates():
            Xcoord = np.random.randint(1,self.Xcord-1)
            Ycoord=np.random.randint(1,self.Ycord-1)
            return Xcoord, Ycoord

        #now we place the hinders randomly.
        self.hider_list=[]
        #Placemen t of the hiders in the model environment
        for j in range(self.nh):
            Xcoord, Ycoord=coordinates()
            while self. model_env[Xcoord][Ycoord]!=0:
                Xcoord,Ycoord=coordinates()
            self.model_env[Xcoord][Ycoord]=2
            self.hider_list.append([Xcoord,Ycoord])

        #now place the seker randomly in the environment
        self.seeker_list=[]

        for j in range(self.ns):
            Xcoord,Ycoord=coordinates()
            while self.model_env[Xcoord][Ycoord] !=0:
                Xcoord,Ycoord=coordinates()
            self.model_env[Xcoord][Ycoord]=3
            self.seeker_list.append([Xcoord,Ycoord])
    #function definition for the rewards for both hider and seeker as agent
    def reward_agent(self,agentlist,vis_agent,type="hide"):
        #considering hder as type 2 and and attacker as type 3
        if type =="hide":
            attacker_type=3
            other_type=2
            agentlist=self.hider_list
            attackerlist=self.seeker_list
        else:
            #vice-versa of the above
            attacker_type=2
            other_type=3
            agentlist=self.seeker_list
            attackerlist=self.hider_list
        attackers_total=0
        states_agent=[]

        #Now we get the visibility of each agent in the environmenmt
        for agent in agentlist:
            env_model=np.copy(self.model_env)
            for x in range(self.Xcord):
                for y in range(self.Ycord):
                    if (x < agent[0]-vis_agent or x>agent[0]+vis_agent)\
                        or (y < agent[1]-vis_agent or y>agent[1]+vis_agent):
                       # 4 is assigned as the visiblity of agent its in the model
                        env_model[x][y]=4
            self.showshadow(agent[0],agent[1],vis_agent,env_model)
            states_agent.append(env_model)
        #Visiblity of agent in the model
        agent_model_view=np.ones((self.model_env.shape))
        agent_model_view.fill(4)
        for x in range(self.Xcord):
            for y in range(self.Ycord):
                for visible in states_agent:
                    if visible[x][y] !=4:
                        agent_model_view[x][y]=visible[x][y]
                        break
        #Now we get the states available to agent in one hot encoding
        states_agent_avail=[]
        attackers_total=0
        for agent in agentlist:
            #setting the agent state
            # coordinates to zeros
            states_agent=np.zeros((self.agents,2)).astype(int)
            states_agent.fill(-100)
            agent_coord=agent
            states_agent[0][:]=agent_coord
            encode=1
            for friend in agentlist:
                if friend ==agent:
                    continue
                if agent_model_view[tuple(friend)]==other_type:
                    states_agent[encode][:]=friend
                encode+=1
            for attacker in attackerlist:
                if agent_model_view[tuple(attacker)] == attacker_type:
                    attackers_total +=1
                    states_agent[encode][:]=attacker
                encode +=1
            states_agent_avail.append(states_agent)

        #reward the hider as +1 and seeker as 0 or -1 else reward the seeker as >1 or -1
        if type=="hide":
            reward=1 if attackers_total ==0 else -1
        else:
            reward= 1 if attackers_total >=1 else -1
        return  reward, states_agent_avail

    #The function gives all the model environment quadrant and shadows
    def showshadow(self, Xcoord, Ycoord, visibility, model_env):
        def isshadow(x,y):
            return (model_env[x][y]==4 or model_env[x][y] == 1)
        #define the moves in the model environment
        moveright=min(Xcoord+visibility+1,model_env.shape[0])
        moveleft=max(Xcoord-visibility-1,-1)
        moveup=min(Ycoord+visibility+1, model_env.shape[1])
        movedown=max(Ycoord-visibility-1, -1)
        mask=1337
        #Now assign to see the shadow of h agent that helps in moving in different directions
        #invert indices to protect interference between quadrant calculations
        for j in range(moveleft,moveright):
            if model_env[j][Ycoord]==1:
                model_env[j][Ycoord] = mask

        for x in range(movedown,moveup):
            if model_env[Xcoord][x]==1:
                model_env[Xcoord][x]=mask

        for j in range(Xcoord+1, moveright): #Move up to right
            for x in range (Ycoord+1,moveup):
                if isshadow(j-1,x) or isshadow(j,x-1) or isshadow(j-1,x-1):
                    model_env[j][x]=4
        for j in range(Xcoord-1, moveleft,-1): #Move low to left
            for x in range (Ycoord-1,movedown,-1):
                if isshadow(j+1,x) or isshadow(j,x+1) or isshadow(j+1,x+1):
                    model_env[j][x]=4

        for j in range(Xcoord +1, moveright):  # Move low to right
            for x in range(Ycoord - 1, movedown, -1):
                if isshadow(j- 1, x) or isshadow(j, x + 1) or isshadow(j - 1, x + 1):
                    model_env[j][x] = 4

        for j in range(Xcoord - 1, moveleft,-1):  # Move up to left
            for x in range(Ycoord - 1, moveup):
                if isshadow(j - 1, x) or isshadow(j, x + 1) or isshadow(j - 1, x + 1):
                    model_env[j][x] = 4

     #Now reinvert to do cross vision to protect the agent hider
        for j in range(moveleft, moveright):
            if model_env[j][Ycoord]==mask:
                model_env[j][Ycoord]=1

        for x in range(movedown, moveup):
            if model_env[Xcoord][x]==mask:
                model_env[Xcoord][x]=1

        #all these hide the agent to unknown location
        #Horizontal cross left movement
        for j in range (Xcoord-1,moveleft,-1):
            if isshadow(j+1, Ycoord):
                model_env[j][Ycoord]=4

         # Horizontal cross right movement
        for j in range(Xcoord +1, moveright):
            if isshadow(j - 1, Ycoord):
                 model_env[j][Ycoord] = 4
        # this will move the agent hider to a random location
        # vertical cross down movement
        for x in range(Ycoord - 1, movedown,-1):
            if isshadow(Xcoord,x+1):
                model_env[Xcoord][x] = 4
       # this will move the agent hider to a random location
         # Horizontal cross down movement
        for x in range(Ycoord + 1, moveup):
            if isshadow(Xcoord, x - 1):
                model_env[Xcoord][x] = 4

    def move_possible(self, target):
        return self.model_env[target[0]][target[1]]==0
    # List of all possible actions available to the agent
    def possible_actions(self, action_ag, type="hide"):
        if type =="hide":
            agentlist=self.hider_list
            type=2
        else:
            agentlist=self.seeker_list
            type=3
        for encode in range(len(agentlist)):
            actions=action_ag[encode]
            begin=agentlist[encode]
            target=list(begin)
            #Now we defining different moves for the agent in different direction using the option variable
            if actions==0:
                pass
            #move towards up
            elif actions ==1:
                target[0] -=1
            #move towards right
            elif actions == 2:
                target[1] += 1
            #move towards down
            elif actions == 3:
                target[0] += 1
            #move towrds left
            elif actions == 4:
                target[1] -= 1
            #move to up and right
            elif actions == 5:
                target[0] -= 1
                target[1] += 1
            #move to  low and right
            elif actions == 6:
                target[0] += 1
                target[1] += 1
            #move to low and left
            elif actions == 7:
                target[0] += 1
                target[1] -= 1
            #move to up and left
            elif actions == 8:
                target[0] -= 1
                target[1] -= 1
            if self.move_possible(target):
                self.model_env[tuple(begin)]=0
                self.model_env[tuple(target)]=type
                agentlist[encode]=list(target)
    #This function takes list of actions as input and give output
    #giving actions as input and getting hider states,seekstates,reward(hider and seeker),
    def agent_step(self, move_hider, move_seeker):
         #The agent runs this step and returns no of hiders, sekkers, hider  reward, seeker reward
        assert self.step < self.episode,"No step beyond the episode"
        self.step+=1
        self.possible_actions(move_hider,type="hide")
        self.possible_actions(move_seeker,type="seek")
        no_of_hider, hider=self.reward_agent(self.hider_list,self.hidevisibility,type="hide")
        no_of_seeker,seeker=self.reward_agent(self.seeker_list,self.seekervisibility,type="seek")
        return no_of_hider,no_of_seeker,hider,seeker == self.episode
#Main function to run the program
if __name__ =="__main__":

    epochs=3
    episode=1000
    episode_length=1000
    xcord=12
    ycord=12
    hiders=1
    seekers=2
    h_visi=3
    s_visi=3
    wall="none"

    grid=HidernSeekerimp(xcord,ycord,hiders,seekers,h_visi,s_visi,episode_length,wall)






























