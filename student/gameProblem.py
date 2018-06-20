#
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None


    # --------------- Common functions to a SearchProblem -----------------
    
    
    def actions(self, state):
        actions = []
        x, y = state[0]
        if(x>0 and self.MAP[x-1][y][0] != 'sea'):
            actions.append('west')
        if(x<9 and self.MAP[x+1][y][0] != 'sea'):
            actions.append('east')
        if(y>0 and self.MAP[x][y-1][0] != 'sea'):
            actions.append('north')
        if(y<3 and self.MAP[x][y+1][0] != 'sea'):
            actions.append('south')     
        return actions
    

    def result(self, state, action):
        x, y = state[0]
        if(action == 'west'):
            x -= 1
        elif(action == 'east'):
            x += 1
        elif(action == 'north'):
            y -= 1
        elif(action == 'south'):
            y += 1          
        goals = list(state[1])
        if (x,y) in goals:
            goals.remove((x,y))
        state_final = (x,y), tuple(goals)
        return state_final 


    def is_goal(self, state):
        return self.GOAL == state 
        
            
    
    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        #I think this is right but IDK why he gave us state2
        #change costs in the config file 
        x,y = state[0]
        return self.MAP[x][y][2]['cost']
        
    
    def heuristic(self, state):
        '''Returns the heuristic for `state'
        '''
        #Manhatan Distance 
        heur = abs(self.INITIAL_STATE[0][0]-state[0][0]) + abs(self.INITIAL_STATE[0][1]-state[0][1])
        for i in state[1]:
            heur += (abs(i[0]-state[0][0])+abs(i[1]-state[0][1]))
        #Euclid Distance
        #heur = sqrt(abs(self.INITIAL_STATE[0][0]-state[0][0])+ (abs(self.INITIAL_STATE[0][1]-state[0][1])**2))
        #for i in state[1]:
        #    heur += sqrt((abs(i[0]-state[0][0]))**2+abs(i[1]-state[0][1])**2)
        return heur 

    def setup (self):
        print ('\nMAP: ', self.MAP, '\n')
        print ('POSITIONS: ', self.POSITIONS, '\n')
        print ('CONFIG: ', self.CONFIG, '\n')

        initial_state = (self.POSITIONS['drone'][0], tuple(self.POSITIONS['goal']))
        final_state = (self.POSITIONS['drone'][0], ()) 

        algorithm = simpleai.search.greedy #the diffrent search algs 
        
        return initial_state,final_state,algorithm

        
    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #
    
    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        
        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
        if self.mapInitialization(map,positions,conf,aiBaseName):
    
            initial_state,final_state,algorithm = self.setup()
            
            self.INITIAL_STATE=initial_state
            self.GOAL=final_state
            self.ALGORITHM=algorithm
            super(GameProblem,self).__init__(self.INITIAL_STATE)
            
            return True
        else:
            return False
        
    # END initializeProblem 


    def mapInitialization(self,map,positions,conf,aiBaseName):
        # Creates lists of positions from the configured map
        # The initial position for the agent is obtained from the first and only aiBaseName tile
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf

        if 'agentInit' in conf.keys():
            self.AGENT_START = tuple(conf['agentInit'])
        else:                    
            if aiBaseName in self.POSITIONS.keys():
                if len(self.POSITIONS[aiBaseName]) == 1:
                    self.AGENT_START = self.POSITIONS[aiBaseName][0]
                else:
                    print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(aiAgentName,mapaPosiciones[aiAgentName]))
                    return False
            else:
                print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(aiBaseName))
                return False
        
        return True
    

