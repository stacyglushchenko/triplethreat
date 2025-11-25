<<<<<<< HEAD
import typing

# import pacai.agents.greedy
# import pacai.core.action
# import pacai.core.agent
# import pacai.core.gamestate
# import pacai.core.features
# import pacai.search.distance
=======
import pacai.core.agentinfo
import pacai.util.alias
from pacai.search.distance import manhattan_distance
from pacai.search.distance import maze_distance
import pacai.core.gamestate
import pacai.student.singlesearch
>>>>>>> 250cffd214ab53b30356f40d7ace16dd76372e23

GHOST_IGNORE_RANGE: float = 2.5

def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Get the agent information that will be used to create a capture team.
    """

    agent1_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.DefensiveAgent")
    agent2_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.OffensiveAgent")

    return [agent1_info, agent2_info]


<<<<<<< HEAD
class DefensiveAgent(pacai.agents.greedy.GreedyFeatureAgent):
    """
    A capture agent that prioritizes defending its own territory.
    """

    def __init__(self,
            override_weights: dict[str, float] | None = None,
            **kwargs: typing.Any) -> None:
        kwargs['feature_extractor_func'] = _extract_baseline_defensive_features
        super().__init__(**kwargs)

        self._distances: pacai.search.distance.DistancePreComputer = pacai.search.distance.DistancePreComputer()
        """ Precompute distances. """

        # Set base weights.
        self.weights['on_home_side'] = 100.0
        self.weights['stopped'] = -100.0
        self.weights['reverse'] = -2.0
        self.weights['num_invaders'] = -1000.0
        self.weights['distance_to_invader'] = -30.0
        self.weights['food_count'] = -10.0
        self.weights['capsules'] = -5.0


        if (override_weights is None):
            override_weights = {}

        for (key, weight) in override_weights.items():
            self.weights[key] = weight

    def game_start(self, initial_state: pacai.core.gamestate.GameState) -> None:
        self._distances.compute(initial_state.board)

class OffensiveAgent(pacai.agents.greedy.GreedyFeatureAgent):
    """
    A capture agent that prioritizes defending its own territory.
    """

    def __init__(self,
            override_weights: dict[str, float] | None = None,
            **kwargs: typing.Any) -> None:
        kwargs['feature_extractor_func'] = _extract_baseline_offensive_features
        super().__init__(**kwargs)

        self._distances: pacai.search.distance.DistancePreComputer = pacai.search.distance.DistancePreComputer()
        """ Precompute distances. """

        # Set base weights.
        self.weights['score'] = 100.0
        self.weights['distance_to_food'] = -1.0

        if (override_weights is None):
            override_weights = {}

        for (key, weight) in override_weights.items():
            self.weights[key] = weight

    def game_start(self, initial_state: pacai.core.gamestate.GameState) -> None:
        self._distances.compute(initial_state.board)
=======
class MyAgent1(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """
>>>>>>> 250cffd214ab53b30356f40d7ace16dd76372e23

def _extract_baseline_defensive_features(
        state: pacai.core.gamestate.GameState,
        action: pacai.core.action.Action,
        agent: pacai.core.agent.Agent | None = None,
        **kwargs: typing.Any) -> pacai.core.features.FeatureDict:
    agent = typing.cast(DefensiveAgent, agent)
    state = typing.cast(pacai.capture.gamestate.GameState, state)

<<<<<<< HEAD
    features: pacai.core.features.FeatureDict = pacai.core.features.FeatureDict()
=======
    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        
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
>>>>>>> 250cffd214ab53b30356f40d7ace16dd76372e23

    current_position = state.get_agent_position(agent.agent_index)
    if (current_position is None):
        # We are dead and waiting to respawn.
        return features

    # Note the side of the board we are on.
    features['on_home_side'] = int(state.is_ghost(agent_index = agent.agent_index))

    # Prefer moving over stopping.
    features['stopped'] = int(action == pacai.core.action.STOP)

    # Prefer not turning around.
    # Remember that the state we get is already a successor, so we have to look two actions back.
    agent_actions = state.get_agent_actions(agent.agent_index)
    if (len(agent_actions) > 1):
        features['reverse'] = int(action == state.get_reverse_action(agent_actions[-2]))

    # We don't like any invaders on our side.
    invader_positions = state.get_invader_positions(agent_index = agent.agent_index)
    features['num_invaders'] = len(invader_positions)

    # Hunt down the closest invader!
    if (len(invader_positions) > 0):
        invader_distances = [agent._distances.get_distance(current_position, invader_position) for invader_position in invader_positions.values()]
        features['distance_to_invader'] = min(distance for distance in invader_distances if (distance is not None))
    
    
<<<<<<< HEAD
    return features

def _extract_baseline_offensive_features(
        state: pacai.core.gamestate.GameState,
        action: pacai.core.action.Action,
        agent: pacai.core.agent.Agent | None = None,
        **kwargs: typing.Any) -> pacai.core.features.FeatureDict:
    agent = typing.cast(OffensiveAgent, agent)
    state = typing.cast(pacai.capture.gamestate.GameState, state)

    features: pacai.core.features.FeatureDict = pacai.core.features.FeatureDict()
    features['score'] = state.get_normalized_score(agent.agent_index)

    # Note the side of the board we are on.
    features['on_home_side'] = int(state.is_ghost(agent_index = agent.agent_index))

    # Prefer moving over stopping.
    features['stopped'] = int(action == pacai.core.action.STOP)

    # Prefer not turning around.
    # Remember that the state we get is already a successor, so we have to look two actions back.
    agent_actions = state.get_agent_actions(agent.agent_index)
    if (len(agent_actions) > 1):
        features['reverse'] = int(action == state.get_reverse_action(agent_actions[-2]))

    current_position = state.get_agent_position(agent.agent_index)
    if (current_position is None):
        # We are dead and waiting to respawn.
        return features

    food_positions = state.get_food(agent_index = agent.agent_index)
    if (len(food_positions) > 0):
        food_distances = [agent._distances.get_distance(current_position, food_position) for food_position in food_positions]
        features['distance_to_food'] = min(distance for distance in food_distances if (distance is not None))
    else:
        # There is no food left, give a large score.
        features['distance_to_food'] = -100000

    ghost_positions = state.get_nonscared_opponent_positions(agent_index = agent.agent_index)
    if (len(ghost_positions) > 0):
        ghost_distances = [agent._distances.get_distance(current_position, ghost_position) for ghost_position in ghost_positions.values()]
        features['distance_to_ghost'] = min(distance for distance in ghost_distances if (distance is not None))
        if (features['distance_to_ghost'] > GHOST_IGNORE_RANGE):
            features['distance_to_ghost'] = 1000

        features['distance_to_ghost_squared'] = features['distance_to_ghost'] ** 2
    else:
        features['distance_to_ghost'] = 0

    # pellet_positions = state.get_position()
    # distance_to_markers = [agent._distances.get_distance(current_position, pellet_position) for pellet in pellet_position()]
    # features['capsules'] = min(distance for distance in distance_to_markers if (distance is not None))

    return features
=======
    def features(self, state: pacai.core.gamestate.GameState, actions: list[pacai.core.action.Action]):
        """ 
        Creates features for each action and stores them in a dictionairy to later score based on pacman's situation/placement in the environment 
        """

        feature_dict = {}
        pos_pacman = state.get_agent_position()

        for action in actions:
            successor_state = state.generate_successor(action)
            pos_successor = successor_state.get_agent_position()

            enemies = [successor_state.get_agent_position(i) for i in successor_state.get_opponent_positions()]
            
            # offense (goal is to get food and avoid other team (havent incorporated other team yet))
            # gets closest food
            food = successor_state.get_food()
            food_count = len(food)

            closest_food = 9999
            for f in food:
                m_dist_food = maze_distance(pos_pacman, f, state)
                if  m_dist_food < closest_food:
                    closest_food = m_dist_food
            # defense (goal is to search for invaders and eat them)
            # checks the dist of closest invader
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

        

class MyAgent2(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)
>>>>>>> 250cffd214ab53b30356f40d7ace16dd76372e23
