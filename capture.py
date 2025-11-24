import pacai.core.agentinfo
import pacai.util.alias
from pacai.search.distance import manhattan_distance
<<<<<<< HEAD
from pacai.search.distance import maze_distance
import pacai.core.gamestate
import pacai.student.singlesearch
=======
import pacai.core.gamestate


>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196


def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Get the agent information that will be used to create a capture team.
    """

    agent1_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.MyAgent1")
    agent2_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.MyAgent2")

    return [agent1_info, agent2_info]


<<<<<<< HEAD
=======

>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196
class MyAgent1(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """


    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """
<<<<<<< HEAD

        
        legal_actions = state.get_legal_actions()
        #print(self.eval_action(state))
        best = self.eval(state)
        return best


        values = []
        max_value = -float('inf')

        for action in legal_actions:
            value = self.eval(state)
            values.append((value, action))
            if value > max_value:
                max_value = value

        for element in values:
            value, action = element
            # return action
            if value == max_value and action != 'STOP':
                print("this is the best", action)
                return action
=======
        
        legal_actions = state.get_legal_actions()
>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196

        return self.rng.choice(legal_actions)
    
    def features(self, state: pacai.core.gamestate.GameState, actions: list[pacai.core.action.Action]):
        """ 
        Creates features for each action and stores them in a dictionairy to later score based on pacman's situation/placement in the environment 
        """

        feature_dict = {}
<<<<<<< HEAD
        pos_pacman = state.get_agent_position()
=======
        pos = state.get_agent_position()
>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196

        for action in actions:
            successor_state = state.generate_successor(action)
            pos_successor = successor_state.get_agent_position()
<<<<<<< HEAD

            enemies = [successor_state.get_agent_position(i) for i in successor_state.get_opponent_positions()]
=======
>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196
            
            # offense (goal is to get food and avoid other team (havent incorporated other team yet))
            # gets closest food
            food = successor_state.get_food()
            food_count = len(food)

            closest_food = 9999
            for f in food:
<<<<<<< HEAD
                m_dist_food = maze_distance(pos_pacman, f, state)
=======
                m_dist_food = manhattan_distance(pos_pacman, f, state)
>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196
                if  m_dist_food < closest_food:
                    closest_food = m_dist_food
            # defense (goal is to search for invaders and eat them)
            # checks the dist of closest invader
<<<<<<< HEAD
            curr_food_distance = min(maze_distance(pos_successor, f, state) for f in food)


            # beased on successor state to eval next action
            invaders = successor_state.get_invader_positions()
            invader_count = len(invaders)
            closest_invader_dist = 9999
            if invaders and not state.is_pacman():
                scared = state.is_scared()
                for i in invaders:
                    pos_i = state.get_agent_position(i)
                    m_dist = maze_distance(pos_successor, pos_i, state)
                    if m_dist < closest_invader_dist:
                        closest_invader_dist = m_dist
            
            run_away = 0
            for enemy in enemies:
                if maze_distance(pos_successor, enemy, state) < 2 and state.is_pacman():
                    run_away = 1
            
            #succ_score = successor_state.score
            
            # populate dict (work in progress, not all is important mostly added the "important" methods on the documentation just because)
            feature_dict[action] = {
                'food_distance' : closest_food,
                #"food_count" : food_count,
                #"team_pos" : state.get_team_positions(1),
                #"opp_pos" : state.get_opponent_positions(),
                #"invader_distance" : closest_invader_dist,
                #"curr_food_distance" : curr_food_distance,
                #"successor_score" : succ_score,
                # "run_away" : run_away
            }
        return feature_dict

    def get_weights(self, state: pacai.core.gamestate.GameState, action: pacai.core.action.Action):
        # added weights to prioritize certain categories
        return {
            #'successor_score': 2,
            'food_distance': -2,
            #'run_away': -100,
        }

    def eval(self, state: pacai.core.gamestate.GameState):
        # scoring actions here to choose best/highest!
        best_value = -9999
        best_action = None

        opposites = {'NORTH':'SOUTH', 'SOUTH':'NORTH', 'EAST':'WEST', 'WEST':'EAST', 'STOP':'STOP'}

        actions = state.get_legal_actions()
        pos_pacman = state.get_agent_position()

        # which action is best loop : have not scored what is good/bad by how much yet
        feature_table = self.features(state, actions)
        for action in actions:
            features = feature_table[action] 
            print(features)
            weights = self.get_weights(state, action)
            value = sum(features[f] * weights[f] for f in features)
        
            last = state.get_last_agent_action()
            print(action, value)

            if last and action == opposites.get(last):
                value -= 5

            if action == 'STOP':
                value -= 10

            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    
    '''def get_action(self, state: pacai.core.gamestate.GameState):

        successor = state.generate_successor(action)
        pos_succ = successor.get_agent_position()
        features = feature_table[action]
        curr_score = 0
        print(action)

        #curr_dist = features["curr_food_distance"]
        next_dist = features["food_distance"]
        #print(curr_dist)
        print(next_dist)
        if next_dist < curr_dist:
            curr_score += 5
        else:
            curr_score -= 1
        # curr_score = 10 - features['food_distance']
        if pos_succ != pos_pacman:
            curr_score += 1
        if curr_score > best_score:
            best_score = curr_score
            best_act = action
        return best_act'''

        
=======

            # beased on successor state to eval next action
            invaders= successor_state.get_invader_positions()
            invader_count = len(invaders)
            if invaders and not state.is_pacman():
                scared = state.is_scared()
                closest_invader_dist = 9999
                for i in invaders:
                    pos_i = state.get_agent_position(index of invader)
                    m_dist = manhattan_distance(pos_pacman, pos_i, state)
                    if m_dist < closest_invader_dist:
                        closest_invader_dist = m_dist
            
            # populate dict (work in progress, not all is important mostly added the "important" methods on the documentation just because)
            feature_dict[action] = {
                'food_distance' : closest_food,
                "food_count" : food_count,
                "team_pos" : state.get_team_positions(),
                "opp_pos" : state.get_opponent_positions(),
                "invader_distance" : closest_invader_dist,
            }
        return feature_dict

    def eval_action(self, state: pacai.core.gamestate.GameState):
        # scoring actions here to choose best/highest!
        best_score = 0.0
        best_act = None

        actions = state.get_legal_actions()
        # which action is best loop : have not scored what is good/bad by how much yet
        feature_table = self.features(state, actions)
        for action in actions:
            features = feature_table[action]
            curr_score = ....
            if curr_score > best_score:
                best_score = curr_score
                best_act = action
        return best_act
        

        

        

>>>>>>> c825e9e128c9da0dc9c2f0c8a8c8a5979e048196

class MyAgent2(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)
