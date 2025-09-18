from chaos_agent import ChaosAgent, Action

def test_agent_step_minimal():
    sn = '''
    [EVENT]: memory
    [EMOTION:JOY:7]
    { A bright spark. }
    '''
    agent = ChaosAgent("Test")
    rep = agent.step(text="ocean warmth", sn=sn)
    assert isinstance(rep.emotions, list)
    assert isinstance(rep.symbols, dict)
    assert rep.action is None or isinstance(rep.action, Action)
    assert isinstance(rep.dreams, list)
