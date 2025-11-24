import pacai.core.agentinfo
import pacai.util.alias

def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Get the agent information that will be used to create a capture team.
    """

    agent1_info = pacai.core.agentinfo.AgentInfo(name = pacai.util.alias.AGENT_DUMMY.long)
    agent2_info = pacai.core.agentinfo.AgentInfo(name = pacai.util.alias.AGENT_DUMMY.long)

    return [agent1_info, agent2_info]

class MyAgent1(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)

class MyAgent2(pacai.core.agent.Agent):
    """ An agent that just takes random (legal) action. """

    def get_action(self, state: pacai.core.gamestate.GameState) -> pacai.core.action.Action:
        """ Choose a random action. """

        legal_actions = state.get_legal_actions()
        return self.rng.choice(legal_actions)
