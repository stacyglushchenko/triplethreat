import typing

import pacai.agents.greedy
import pacai.core.action
import pacai.core.agent
import pacai.core.board
import pacai.core.gamestate
import pacai.core.features
import pacai.search.distance
import pacai.pacman.board
import pacai.capture.gamestate

GHOST_IGNORE_RANGE: float = 2.5

def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Get the agent information that will be used to create a capture team.
    """

    agent1_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.DefensiveAgent")
    agent2_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.OffensiveAgent")

    return [agent1_info, agent2_info]


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
        self.weights['on_home_side'] = 120.0
        self.weights['stopped'] = -100.0
        self.weights['reverse'] = 0.0
        self.weights['num_invaders'] = -1000.0
        self.weights['distance_to_invader'] = -40.0
        self.weights['distance_to_ghost_squared'] = 0.0
        self.weights['food_count'] = -10.0
        self.weights['capsules'] = 0
        # self.weights['dist_to_mid'] = 1.0
        self.weights['distance_to_food'] = -1.0
        self.weights['eaten_food'] = 100.0

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
        self.weights['distance_to_food'] = -1.2
        self.weights['distance_to_ghost'] = 8.0
        self.weights['distance_to_ghost_squared'] = 0.0
        self.weights['capsules'] = 20.0
        # self.weights['on_home_side'] = -5.0
        self.weights['distance_to_invader'] = -5.0
        self.weights['distance_to_scared_ghost'] = 4.0

        if (override_weights is None):
            override_weights = {}

        for (key, weight) in override_weights.items():
            self.weights[key] = weight

    def game_start(self, initial_state: pacai.core.gamestate.GameState) -> None:
        self._distances.compute(initial_state.board)

def _extract_baseline_defensive_features(
        state: pacai.core.gamestate.GameState,
        action: pacai.core.action.Action,
        agent: pacai.core.agent.Agent | None = None,
        **kwargs: typing.Any) -> pacai.core.features.FeatureDict:
    agent = typing.cast(DefensiveAgent, agent)
    state = typing.cast(pacai.capture.gamestate.GameState, state)
    successor = state.generate_successor(action)

    features: pacai.core.features.FeatureDict = pacai.core.features.FeatureDict()

    current_position = state.get_agent_position(agent.agent_index)
    if (current_position is None):
        # We are dead and waiting to respawn.
        return features

    # Note the side of the board we are on.
    features['on_home_side'] = int(state.is_ghost(agent_index = agent.agent_index))

    # Prefer moving over stopping.
    features['stopped'] = int(action == pacai.core.action.STOP)

    # COMMENtED out since it could be benificial to turning around and running away!!
    # # Prefer not turning around.
    # # Remember that the state we get is already a successor, so we have to look two actions back.
    # agent_actions = state.get_agent_actions(agent.agent_index)
    # if (len(agent_actions) > 1):
    # features['reverse'] = int(action == state.get_reverse_action(agent_actions[-2]))

    # We don't like any invaders on our side.
    invader_positions = state.get_invader_positions(agent_index = agent.agent_index)
    features['num_invaders'] = len(invader_positions)

    # Hunt down the closest invader!
    if (len(invader_positions) > 0):
        invader_distances = [agent._distances.get_distance(current_position, invader_position) for invader_position in invader_positions.values()]
        features['distance_to_invader'] = min(distance for distance in invader_distances if (distance is not None))
    
    # keeping defense hovering around our capsule so opps dont eat it and make us vulnerable to being scared
    all_capsule_positions = state.board.get_marker_positions(pacai.pacman.board.MARKER_CAPSULE)
    team_mod = state._team_modifier(agent.agent_index)
    our_caps = []
    for c in all_capsule_positions:
        if team_mod == state._team_side(agent.agent_index, c):
            our_caps.append(c)
    if (len(our_caps) > 0):
        distances_to_caps = []
        for capsule_pos in our_caps:
            distances_to_caps.append(agent._distances.get_distance(current_position, capsule_pos))
        features["capsules"] = min(capsule for capsule in distances_to_caps if (capsule is not None))
    
    # # wall positions
    # wall_positions = state.board.get_marker_positions(pacai.core.board.MARKER_WALL)
    # agent_actions = state.get_agent_actions(agent.agent_index)
    # for act in agent_actions:
    # if
    food_positions = state.get_food(agent_index = agent.agent_index)
    next_food_positions = successor.get_food(agent_index = agent.agent_index)
    if (len(food_positions) > 0):
        food_distances = [agent._distances.get_distance(current_position, food_position) for food_position in food_positions]
        features['distance_to_food'] = min(distance for distance in food_distances if (distance is not None))
    
    # keep track of where food was eaten, and defend that place
    old_food = food_positions
    new_food = next_food_positions

    eaten_food = None
    for f in old_food:
        if f not in new_food:
            eaten_food = f
            break

    if eaten_food is not None:
        dist = agent._distances.get_distance(current_position, eaten_food)
        # prefer closer distance
        features['eaten_food'] = -dist
    else:
        features['eaten_food'] = 0

    return features

def _extract_baseline_offensive_features(
        state: pacai.core.gamestate.GameState,
        action: pacai.core.action.Action,
        agent: pacai.core.agent.Agent | None = None,
        **kwargs: typing.Any) -> pacai.core.features.FeatureDict:
    agent = typing.cast(OffensiveAgent, agent)
    state = typing.cast(pacai.capture.gamestate.GameState, state)
    # parameter to make sure if off is pac or no
    pacman = state.is_pacman(agent_index = agent.agent_index)
    features: pacai.core.features.FeatureDict = pacai.core.features.FeatureDict()
    features['score'] = state.get_normalized_score(agent.agent_index)

    # Note the side of the board we are on.
    features['on_home_side'] = int(state.is_ghost(agent_index = agent.agent_index))

    # Prefer moving over stopping.
    features['stopped'] = int(action == pacai.core.action.STOP)

    # COMMENtED out since it could be benificial to turning around and running away!!
    # # Prefer not turning around.
    # # Remember that the state we get is already a successor, so we have to look two actions back.
    # agent_actions = state.get_agent_actions(agent.agent_index)
    # if (len(agent_actions) > 1):
    #     features['reverse'] = int(action == state.get_reverse_action(agent_actions[-2]))

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
    if pacman:
        ghost_positions = state.get_nonscared_opponent_positions(agent_index = agent.agent_index)
        if (len(ghost_positions) > 0):
            ghost_distances = [agent._distances.get_distance(current_position, ghost_position) for ghost_position in ghost_positions.values()]
            features['distance_to_ghost'] = min(distance for distance in ghost_distances if (distance is not None))
            if (features['distance_to_ghost'] > GHOST_IGNORE_RANGE):
                features['distance_to_ghost'] = 100

            features['distance_to_ghost_squared'] = features['distance_to_ghost'] ** 2
        else:
            features['distance_to_ghost'] = 0
    else:
        opp_pos = state.get_invader_positions(agent_index = agent.agent_index)
        if (len(opp_pos) > 0):
            opp_dists = [agent._distances.get_distance(current_position, op) for op in opp_pos.values()]
            features['distance_to_invader'] = min(distance for distance in opp_dists if (distance is not None))

    # get opponent capsules otherwise offense will hover on its own! Get opp then eat so enemy is ghost
    all_capsule_positions = state.board.get_marker_positions(pacai.pacman.board.MARKER_CAPSULE)
    team_mod = state._team_modifier(agent.agent_index)
    opp_caps = []
    for c in all_capsule_positions:
        if team_mod != state._team_side(agent.agent_index, c):
            opp_caps.append(c)
    if (len(opp_caps) > 0):
        distance_to_markers = [agent._distances.get_distance(current_position, capsule_position) for capsule_position in opp_caps]
        valid_capsule = [d for d in distance_to_markers if d is not None]
        if valid_capsule:
            # closer capusiles give larger feature*weight.
            features['capsules'] = -min(valid_capsule)
    else:
        # all finished big reward
        features['capsules'] = 1000
    
    # make it less scared of scared ghosts when on opps side
    if pacman:
        scared_ghost_positions = state.get_scared_opponent_positions(agent_index = agent.agent_index)
        ghost_positions = state.get_nonscared_opponent_positions(agent_index = agent.agent_index)
        if (len(scared_ghost_positions) > 0):
            scared_ghost_distances = [
                agent._distances.get_distance(current_position, scared_ghost_pos)
                for scared_ghost_pos in scared_ghost_positions.values()
            ]
            features['distance_to_scared_ghost'] = min(distance for distance in scared_ghost_distances if (distance is not None))
            if (features['distance_to_scared_ghost'] > GHOST_IGNORE_RANGE):
                features['distance_to_scared_ghost'] = 100
        else:
            features['distance_to_scared_ghost'] = 0
            
    return features
