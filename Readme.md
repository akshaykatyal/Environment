I tried to build a simple game environment using Q-learning in reinforcement learning, here the blue represent player, green is for the food, and red is the killer. So, here the player is to reach the food and be safe from the red attacker. I have made grid of 10*10 for the observations, for the end goal of the player is to reach the food and be safe from the killer. The game players, killer and food will be represented by circle colurs. The code has play.action method which user the play.move method, the q-table is then shown, then we display the envoronment as cv2 image, then also show rewards per 3000 episodes, the all the epiodes with rewards are given at the end, at last from graph we infer the maximum episode has lease -ve reward. 

To run the code:
Just run the environment.py file and agen will be start training.

I have also started working on the hider and seeker game, and will push that as soon as I will finish.