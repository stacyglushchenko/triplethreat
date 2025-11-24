import pacai.core.agentinfo
import pacai.util.alias
from pacai.search.distance import manhattan_distance
import pacai.core.gamestate




def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Get the agent information that will be used to create a capture team.
    """

    agent1_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.MyAgent1")
    agent2_info = pacai.core.agentinfo.AgentInfo(name = f"{__name__}.MyAgent2")

    return [agent1_info, agent2_info]



class MyAgent1(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """
    def manhattan_dist(self, a, b):


    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """
        
        legal_actions = state.get_legal_actions()

        return self.rng.choice(legal_actions)
    
    def features(self, state: pacai.core.gamestate.GameState, action: pacai.core.action.Action):
        feature_dict = {}
        pos = state.get_agent_position()

        for action in actions:
            successor_state = state.generate_successor(action)
            pos_successor = successor_state.get_agent_position()
            
            # offense
            food = successor_state.get_food()
            food_count = len(food)

            closest_food = 9999
            for f in food:
                m_dist_food = manhattan_distance(pos_pacman, f, state)
                if  m_dist_food < closest_food:
                    closest_food = m_dist_food
            # defense
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

        feature_table = self.features(state, actions)
        for action in actions:
            features = feature_table[action]
            curr_score = ....
            if curr_score > best_score:
                best_score = curr_score
                best_act = action
        return best_act
        

        

        


class MyAgent2(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)
