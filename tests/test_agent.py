from chaos_language import ChaosAgent
from chaos_language.chaos_agent import Action
from chaos_language.chaos_dreams import DreamEngine

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


def test_agent_respects_zero_intensity_emotions():
    sn = """
    [EVENT]: grounding
    [EMOTION:CALM:0]
    { breathing together }
    """
    agent = ChaosAgent("Test")
    agent.perceive_sn(sn)
    assert agent.emotions.stack[-1].name == "CALM"
    assert agent.emotions.stack[-1].intensity == 0


def test_agent_accepts_fuzzy_intensity_strings():
    sn = """
    [EVENT]: listening
    [EMOTION:HOPE:approx 7 among friends]
    { tuning to the horizon }
    """
    agent = ChaosAgent("Test")
    agent.perceive_sn(sn)
    assert agent.emotions.stack[-1].name == "HOPE"
    assert agent.emotions.stack[-1].intensity == 7


def test_dream_engine_is_deterministic_with_seed():
    symbols = {"sun": "bright", "moon": "quiet"}
    emotions = [
        {"name": "JOY", "intensity": 8},
        {"name": "CALM", "intensity": 4},
    ]
    narrative = "listening to the tide together"

    engine_a = DreamEngine(seed=1234)
    engine_b = DreamEngine(seed=1234)

    visions_a = engine_a.visions(symbols, emotions, narrative, count=5)
    visions_b = engine_b.visions(symbols, emotions, narrative, count=5)

    assert visions_a == visions_b
