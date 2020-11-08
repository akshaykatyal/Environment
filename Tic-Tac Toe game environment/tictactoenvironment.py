import gym
import numpy
import itertools
import copy
#defining parameters to be used in the game
BOARD_STATE=[['','',''],['','',''],['','','']]
REWARD_WIN=1.0
REWARD_LOOSE=-1.0
DRAW_GAME=0.0
REWARD_ZERO=0.0
#The game environment is for the game TicTacToe this has two players with 'o' or 'x'symbols.The tic tac toe game has o and x symbol

#defining the class for tic tac toe environment
class GameTictactoe(gym.Env):
    metadata={'render.modes':['human']}
    # this function is called by the objects and is used to initialise the parameters
    def __init__(self,player1,player2):
        self.board=BOARD_STATE
        self.done=False
        self.player1=player1
        self.player2=player2

#this function displays the tic tac toe board
    def display_board(self):
        #This function is used to display board
        print('\n')
        print(self.board[0][0] + '|' + self.board[0][1] + '|' + self.board[0][2])
        print("----------------------")
        print(self.board[1][0] + '|' + self.board[1][1] + '|' + self.board[1][2])
        print("----------------------")
        print(self.board[2][0] + '|' + self.board[2][1] + '|' + self.board[2][2])
        print('\n')
    #This function display board with both the players
    def states(self):
        return (self.board)

    def gamestatus(self):
        #The game status s by 1:Player 1 wins the game or
#2 player 2 wins the game , -1 if it draws
        if ((self.board[0][0]==self.board[0][1]==self.board[0][2]==self.player1)or
                (self.board[1][0]==self.board[1][1]==self.board[1][2]==self.player1)or
                (self.board[2][0]==self.board[2][1]==self.board[2][2]==self.player1)or
                (self.board[0][0]==self.board[1][0]==self.board[2][0]==self.player1)or
                (self.board[0][1]==self.board[1][1]==self.board[2][1]==self.player1)or
                (self.board[0][2] == self.board[1][2] == self.board[2][2] == self.player1) or
                (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.player1) or
                (self.board[0][2] == self.board[1][1] == self.board[2][0] == self.player1)):
            return (1)
        elif ((self.board[0][0]==self.board[0][1]==self.board[0][2]==self.player1)or
                (self.board[1][0]==self.board[1][1]==self.board[1][2]==self.player1)or
                (self.board[2][0]==self.board[2][1]==self.board[2][2]==self.player1)or
                (self.board[0][0]==self.board[1][0]==self.board[2][0]==self.player1)or
                (self.board[0][1]==self.board[1][1]==self.board[2][1]==self.player1)or
                (self.board[0][2] == self.board[1][2] == self.board[2][2] == self.player1) or
                (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.player1) or
                (self.board[0][2] == self.board[1][1] == self.board[2][0] == self.player1)):
            return (2)
        elif(''in list(itertools.chain.from_iterable(self.board))):
            return (-1)
        else:
            return (0)

    #The function now give the step of the game when the suer plays the game, this is called when the player perfrom any move
    def step(self,action,play,current_play):
        if self.done:
            return (self.states(),0,True,None)

        self.board[action[0]][action[1]]=current_play
        reward=REWARD_ZERO
        status=self.gamestatus()

        if (status>=0):
            self.gameend=True
            if(play==self.player1):
                reward =REWARD_WIN if status==1 else REWARD_LOOSE if status==2 else DRAW_GAME
            elif(play==self.player2):
                reward = REWARD_WIN if status == 1 else REWARD_LOOSE if status == 2 else DRAW_GAME
        return (self.states(),reward,self.gameend,None)

    #This function is use to reset the environment of the game, this reserts the environment of tic tac toe game environment
    def reset(self):
        self.board=copy.deepcopy(BOARD_STATE)
        self.gameend=False
        return (self.states())

    #This function is use to refresh and display the screen, this render displays the current state on the screen
    def render(self):
        self.display_board()





