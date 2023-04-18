import math
import pickle
from constants import *
from run import GameController 
import sys

class State:
    def __init__(self, p1):
        self.state = []
        self.p1 = p1
        self.isEnd = False
        self.finalScore = 0
        self.closeDistance = 80
    
    def availableDirections(self, pacman):
        return pacman.validDirections()

    # Returns the direction of the closest ghost relative to pacman
    # if the ghost is within a certain range. Else, returns None.
    def getGhostDirections(self, ghosts, pacman_target):
        directions = []
        for ghost in ghosts:
            distance = math.sqrt((pacman_target[0] - ghost.position.x)**2 + (pacman_target[1] - ghost.position.y)**2)
          
            vec = (ghost.position.x - pacman_target[0], ghost.position.y - pacman_target[1])

            
            convertedDistance = 5
            if(distance <= 25):
                convertedDistance = 0
            elif distance <= 50:
                convertedDistance = 1
            elif distance <= 75:
                convertedDistance = 2
            elif distance <= 100:
                convertedDistance = 3
            elif distance <= 150:
                convertedDistance = 4
            
            vec = (ghost.position.x - pacman_target[0], ghost.position.y - pacman_target[1])
            if abs(vec[1]) >= abs(vec[0]): 
                if vec[1] >= 0:
                    directions.append((DOWN, convertedDistance))
                else:
                    directions.append((UP, convertedDistance))
            else: 
                if vec[0] >= 0:
                   directions.append((RIGHT, convertedDistance))
                else:
                    directions.append((LEFT, convertedDistance))

        return directions
    
    def getClosestPellet(self, pellets, pacman_target):
        closest_pellet = None
        closest_distance = sys.maxsize
        for pellet in pellets.pelletList:
            distance = math.sqrt((pacman_target[0] - pellet.position.x)**2 + (pacman_target[1] - pellet.position.y)**2)
            if closest_pellet is None or distance < closest_distance:
                closest_pellet = pellet
                closest_distance = distance

        if closest_pellet:
            convertedDistance = 5
            if(closest_distance <= 25):
                convertedDistance = 0
            elif closest_distance <= 50:
                convertedDistance = 1
            elif closest_distance <= 75:
                convertedDistance = 2
            elif closest_distance <= 100:
                convertedDistance = 3
            elif closest_distance <= 150:
                convertedDistance = 4
            
            vec = (closest_pellet.position.x - pacman_target[0], closest_pellet.position.y - pacman_target[1])
            if abs(vec[1]) >= abs(vec[0]): 
                if vec[1] >= 0:
                    return DOWN, convertedDistance
                else:
                    return UP, convertedDistance
            else: 
                if vec[0] >= 0:
                    return RIGHT, convertedDistance
                else:
                    return LEFT, convertedDistance    
        else:
            return None, -1
       
        
        
    def getClosestGhostDirection(self, ghosts, pacman_target):
        closest_ghost = None
        closest_distance = 0
        for ghost in ghosts:
            distance = math.sqrt((pacman_target[0] - ghost.position.x)**2 + (pacman_target[1] - ghost.position.y)**2)
            if closest_ghost is None or distance < closest_distance:
                closest_ghost = ghost
                closest_distance = distance
        
        if closest_distance <= self.closeDistance:
            vec = (closest_ghost.position.x - pacman_target[0], closest_ghost.position.y - pacman_target[1])
            if abs(vec[1]) >= abs(vec[0]): 
                if vec[1] >= 0:
                    return DOWN
                else:
                    return UP
            else: 
                if vec[0] >= 0:
                    return RIGHT
                else:
                    return LEFT
        else: 
            return None

    # Updates the state with the current game world's information.
    def updateState(self, ghosts, pacman_target, pellets):
        curGhostDirections = self.getGhostDirections(ghosts, pacman_target)
        closestPelletDir, closestPelletDist = self.getClosestPellet(pellets, pacman_target)
        #print(closestPelletDir, closestPelletDist)
        self.state = [int(pacman_target[0]), int(pacman_target[1]), curGhostDirections[0][0], curGhostDirections[0][1], curGhostDirections[1][0], curGhostDirections[1][1], curGhostDirections[2][0], curGhostDirections[2][1], curGhostDirections[3][0], curGhostDirections[3][1], closestPelletDir, closestPelletDist]
    
    # Apply the chosen action (direction) to the game.
    def applyAction(self, game, direction, isRendering):
        game.pacman.learntDirection = direction
        game.update(isRendering)
    
    # Checks if game is over i.e. level completed or all lives lost.
    def gameEnded(self, game):
        if game.lives <= 0 :
            self.isEnd = True
            self.finalScore = game.score
            return 0
        if game.level > self.level:
            return 1
        else:
            return None
    
    # Checks if game is paused i.e. after one life is lost or at the
    # beginning of new game. If it is, resumes it.
    def gamePaused(self, game):
        if game.pause.paused:
            if game.pacman.alive:
                game.pause.setPause(playerPaused=True)
                if not game.pause.paused:
                    game.textgroup.hideText()
                    game.showEntities()

    # Main method for training.
    def play(self, iterations=100):
        isRendering = True
        for i in range(iterations):
            if i % 1 == 0:
                print("Iterations {}".format(i))
            if i % 50 == 0:
                p1.savePolicy()
            game = GameController()
            game.startGame()
            game.update(isRendering)
            pacman_target = game.nodes.getPixelsFromNode(game.pacman.target)
            self.updateState(game.ghosts, pacman_target, game.pellets)
            self.level = game.level
            lastAliveStatus = True
            while not self.isEnd:
                currentAliveStatus = game.pacman.alive
                died = False
                if not currentAliveStatus and lastAliveStatus:
                    died = True
                lastAliveStatus = currentAliveStatus

                possible_directions = self.availableDirections(game.pacman)
                p1_action = self.p1.getAction(self.state, possible_directions, game.score, died, currentAliveStatus)
                # take action and update board state
                self.applyAction(game, p1_action, isRendering)
                pacman_target = game.nodes.getPixelsFromNode(game.pacman.target)
                self.updateState(game.ghosts, pacman_target, game.pellets)

                # check board status if it is end
                self.gamePaused(game)
                result = self.gameEnded(game)
                if result is not None:
                    self.p1.final(self.state, game.score)
                    game.restartGame()
                    del game
                    self.isEnd = False
                    break

                else:
                    # next frame iteration
                    continue



if __name__ == "__main__":
    #### PARAMETERS:
    # ALPHA -> Learning Rate
    # controls how much influence the current feedback value has over the stored Q-value.

    # GAMMA -> Discount Rate
    # how much an action’s Q-value depends on the Q-value at the state (or states) it leads to.

    # RHO -> Randomness of Exploration
    # how often the algorithm will take a random action, rather than the best action it knows so far.

    # NU: The Length of Walk
    # number of iterations that will be carried out in a sequence of connected actions.
    
    exploration_rho=0.3
    lr_alpha=0.2
    discount_rate_gamma=0.9
    walk_len_nu = 0.2
    
    # training
    from player import *
    p1 = Player("p1", exploration_rho, lr_alpha, discount_rate_gamma, walk_len_nu)
    st = State(p1)

    # # # TRAINING
    print("Training...")
    st.play(5000)
    p1.savePolicy()

    # DEMO
    #demo_p1 = Player("demo", exploration_rho=0, lr_alpha=0)
    #demo_p1.loadPolicy("trained_controller_01")
    #stDemo = State(demo_p1)
    #stDemo.play()