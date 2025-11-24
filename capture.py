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

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """
        
        legal_actions = state.get_legal_actions()

        return self.rng.choice(legal_actions)
    
    def features(self, state: pacai.core.gamestate.GameState):
        feature_dict = {}
        pos = state.get_agent_position()

        actions = state.get_legal_actions(pos)
        for action in actions:
            feature_dict[action] = {
                'food' : state.get_food(),
                "food_count" : state.food_count(),
                "team_pos" : state.get_team_positions(),
                "opp_pos" : state.get_opponent_positions(),
                "invader_pos" : state.get_invader_positions(),
            }
        return feature_dict

    def eval_action(self, state: pacai.core.gamestate.GameState, action: pacai.core.action.Action):
        # offense
        food = state.get_food()
        

        # defense
        pos_pacman = state.get_agent_position()

        invaders= state.get_invader_positions()
        if invaders and not state.is_pacman():
            scared = state.is_scared()
            closest_dist = 9999
            for i in invaders:
                pos_i = state.get_agent_position(index of invader)
                m_dist = manhattan_distance(pos_pacman, pos_i, state)
                if m_dist < closest_dist:
                    closest_dist = m_dist


        


class MyAgent2(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)
