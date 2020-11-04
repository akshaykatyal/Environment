import numpy as np

class HidernSeekerimp(Hideseekenv):
    def __init__(self, Xcord, Ycord, nh, ns, hidevisibility, seekervisibility, episode, bricks, gamma=0.9):
        self.agents=nh+ns
        self.bricks=bricks
        self.spec=Hideseekspec(self.agents * Xcord * Ycord, 9 , gamma)
        self.episode=episode
        self.step=0
        self.nh=nh
        self.ns=ns
        self.Xcord=Xcord
        self.Ycord=Ycord
        #setting the visibility of hider and seeker
        assert hidevisibility*2+1 <= Xcord and hidevisibility*2+1 <=Ycord, "it is very large"
        assert seekervisibility*2+1 <= Xcord and seekervisibility*2+1 <=Ycord, "it is very large"
        self.hidevisibility=hidevisibility
        self.seekervisibility=seekervisibility
        #seeting up the display size of the game
        self.model_env=np.zeros((self.Xcord, self.Ycord))
        self.init_envmodel()
        self.dimensions=[self.agents,self.Xcord,self.Ycord]
        self.dimen_step=self._hideseek_spec.nos


    def print_envmodel(self):
        print("\n This shows the beginng of game model")
        print("-----------------------------------")
        for j in range(self.Xcord):
            model=""
            for x in range(self.Ycord):
                options=self.envmodel[j][x]
                if options ==0:
                    model += " ."
                elif options == 1:
                    model += "W"
                elif options == 2:
                    model +="H"
                else:
                    model +="S"
            print(model)
        print("----------------------------------")
        print("End of the game model")

    def save_envmodel(self,modelfile,episodes):
        visibility=[]
        for j in range(self.Xcord):
            model= " "
            for x in range(self.Ycord):
                options=self.envmodel[j][x]
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
            f.write("\n the episode no %d \n" %(episodes))
            f.write(", ".join(visibility))

    def envset(self):
        self.step=0
        self.init_envmodel()
        no_of_hiders, _=self.agent_reward(self.hider_list, self.hidevisibility, type="hider")
        no_of_seeker,_ =self.agent_reward(self.seeker_list,self.seekervisibility, type="seeker")
        return no_of_hiders,no_of_seeker

    def init_envmodel(self):
        #define the model environment for the game, here 0=normal stae, 1=wall,2=hider,3=seeker, 4=unknown, 5=position of the self agaent
        for j in range(self.Xcord):
            for x in range(self.Ycord):
                if j==0 or j==self.Xcord-1 or x==0 or x== self.Ycord-1:
                    self.envmodel[j][x]=1

                else:
                    self.envmodel[j[x]]=0
