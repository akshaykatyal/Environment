import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

GRID_SIZE = 10  # 10*10 GRID FOR DISCRETE MAPPING
TOT_EPISODES = 25000
PENALTY_MOVE = 1
PENALTY_KILLER = 300
REWARD_FOOD = 25
# PARAMETERS FOR Q-LEARNING BASED FORMULA
EPSILON = 0.9
DECAY_RATE = 0.9998
DISPLAY_EVERY = 3000
qq_table = None  # give the q table or any file that contains q table for selcting the maximum value from that table
#learning and discount rate
ALPHA_LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.95
# PLAYER, food and killer FOR THE GAME ENVIRONMENT
GAME_PLAYER_N = 1
GAME_FOOD_N = 2
GAME_KILLER_N = 3
# CREATING A DICTIONARY FOR THE COLOUR VALUES OF PLAYERS IN THE GAME
d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)}

#creating a class for game play
class Game_Play:
    def __init__(self):
        # THE a and b dimension initialization for the Grid of the game using
        self.a = np.random.randint(0, GRID_SIZE)
        self.b = np.random.randint(0, GRID_SIZE)

    # Return the dimension of the random X and Y
    def __str__(self):
        return "{},{}".format(self.a, self.b)

    # Subtraction function for the x and the difference
    def __sub__ (self, difference):
        return (self.a - difference.a, self.b - difference.b)

    # Now we define the actions for the agents there are 4 choices that the agent have 0,1,2,3
    # cordinates move for different action uusing move function
    def agent_action(self, option):
        if option == 0:
            self.agent_move(a=1, b=1)  # cordinates move for different action
        elif option == 1:
            self.agent_move(a=-1, b=-1)  # cordinates move for different action
        elif option == 2:
            self.agent_move(a=-1, b=1)  # cordinates move for different action
        elif option == 3:
            self.agent_move(a=1, b=-1)  # cordinates move for different action

    # Now define the moves for the agent
    def agent_move(self, a=False, b=False):
        # if no value is given for 'a' then given random value else give the difference
        if not a:
            self.a += np.random.randint(-1, 2)
        else:
            self.a += a
        # if no value is given for 'b' then given random value else give the difference
        if not b:
            self.b += np.random.randint(-1, 2)
        else:
            self.b += b
			
        # If the agent goes out of boudaries of the grid
        if self.a < 0:
            self.a = 0
        elif self.a > GRID_SIZE - 1:
            self.a = GRID_SIZE - 1
        if self.b < 0:
            self.b = 0
        elif self.b > GRID_SIZE - 1:
            self.b = GRID_SIZE - 1


# Now WE GIVE THE Q-TABEL FOR THE AGAENT TO SELECT THE HIGHEST VALUE
if qq_table is None:
    # Initializing q table
    table_q = {}
    # NOW USING COMPREHENSION LIST TO GENERATE THE Q TABLE
    for a1 in range(-GRID_SIZE + 1, GRID_SIZE):
        for b1 in range(-GRID_SIZE + 1, GRID_SIZE):
            for a2 in range(-GRID_SIZE + 1, GRID_SIZE):
                for b2 in range(-GRID_SIZE + 1, GRID_SIZE):
                    # assigning random value to q- table
                    table_q[((a1, b1), (a2, b2))] = [np.random.uniform(-5, 0) for i in range(4)]
# we can also give the q-table as input file
else:
    with open(qq_table, "rb") as f:
        table_q = pickle.load(f)

# initializing rewards for the episodes in the games
action_epi_reward = []
# loop for episodes in the total 25000 episodes
for epi in range(TOT_EPISODES):
    # Creating agents for the game_play class
    #the game player
    game_player = Game_Play()
    #food that player needs to reach
    food_game = Game_Play()
    #killer, from which player needs to be safe from
    game_killer = Game_Play()
    # Display the episodes after modulus with DISPLAY_EVERY ALSO WE REINITIALIZE the player, food and killer
    if epi % DISPLAY_EVERY == 0:
        print("on #{}, epsilon:{}".format(epi, EPSILON))
        # THE mean is also displayed after every episode for  display_every
        print("{} ep mean {}".format(DISPLAY_EVERY, np.mean(action_epi_reward[-DISPLAY_EVERY:])))
        show = True
    else:
        show = False
    # initialize episode reward ro zero
    epi_reward = 0
    # find observations for the player actions in the game
    for j in range(200):
        observations = (game_player - food_game, game_player - game_killer)
        if np.random.random() > EPSILON:
            # The action is taken from q table
            player_action = np.argmax(table_q[observations])
        else:
            player_action = np.random.randint(0, 4)

        game_player.agent_action(player_action)
        
        # Assigning penalty for different moves
        # if both player and killer perform same action
        if game_player.a == game_killer.a and game_player.b == game_killer.b:
            game_reward = -PENALTY_KILLER
        elif game_player.a == food_game.a and game_player.b == food_game.b:
            game_reward = REWARD_FOOD
        else:
            game_reward = -PENALTY_MOVE
        # Now assignment of new observations after player moves and rewards
        new_observation = (game_player - food_game, game_player - game_killer)
        # q-table for future players
        future_max_q = np.max(table_q[new_observation])
        #save the result in variables
        q_value = table_q[observations][player_action]

        #checking the rewards for the play reaching food or attack by kill er and updating the Q value
        if game_reward == REWARD_FOOD:
            new_q_value = REWARD_FOOD
        elif game_reward == -PENALTY_KILLER:
            new_q_value = -PENALTY_KILLER
        else:
            # Update the q-value using the formula for q-learning
            new_q_value = (1 - ALPHA_LEARNING_RATE) * q_value + ALPHA_LEARNING_RATE * (
                        game_reward + DISCOUNT_RATE * future_max_q)
        # the table is updated
        table_q[observations][player_action] = new_q_value

        # DISPLAYING THE GAME GRID
        if show:
            # The grid is created for the size mentioned
            environment = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=np.uint8)
            # The food is assigned green colour in the game
            environment[food_game.a][food_game.b] = d[GAME_FOOD_N]
            # The player has a blue colour in the game
            environment[game_player.a][game_player.b] = d[GAME_PLAYER_N]
            # The killer has red colour in the game
            environment[game_killer.a][game_killer.b] = d[GAME_KILLER_N]
            # The image is read in the RBG format
            img_disp = Image.fromarray(environment, 'RGB')
            #image display using opencv
            img_disp = img_disp.resize((300, 300))  # reseize to see the agent
            cv2.imshow("image", np.array(img_disp))  # Image display
            if game_reward == REWARD_FOOD or game_reward == -PENALTY_KILLER:
                 #WAITKEY OPEN CV TO MONITOR THE DISPLAY ON THE SCREEN OF THE GAME
                 if cv2.waitKey(500) & 0xFF == ord('q'):
                    break
            else:
                 if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        # the episode reward are added to the game reward
        epi_reward += game_reward
        if game_reward == REWARD_FOOD or game_reward == -PENALTY_KILLER:
            break
    # Now print the episode reward
    #print(epi_reward)
    action_epi_reward.append(epi_reward)
    # Epsilon value is updated
    EPSILON *= DECAY_RATE
# calculating average
final_avg = np.convolve(action_epi_reward, np.ones((DISPLAY_EVERY,)) / DISPLAY_EVERY, mode='valid')

#plot for the episode and rewards
plt.plot([j for j in range(len(final_avg))], final_avg)
plt.ylabel("Reward {}".format(DISPLAY_EVERY))
plt.xlabel("episode #")
plt.show()
# saving the q-table
with open("qtable-{}.pickle", "wb".format(int(time.time()))) as f:
    pickle.dump(table_q, f)