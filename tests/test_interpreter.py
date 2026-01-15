# File: tests/test_interpreter.py

from chaos_language import run_chaos

def test_interpreter_env_keys():
    src = '''
    [EVENT]: memory
    [EMOTION:JOY:7]
    { Warm day. }
    '''
    env = run_chaos(src)
    assert set(env.keys()) == {"structured_core", "emotive_layer", "chaosfield_layer"}

def test_interpreter_emotion_payload():
    src = '[EMOTION:HOPE:5]'
    env = run_chaos(src)
    assert any(e.get("type") == "HOPE" or e.get("name") == "HOPE" for e in env["emotive_layer"])


def test_structured_core_preserves_relation_box():
    with open("artifacts/corpus_sn/relation_box.sn", "r", encoding="utf-8") as handle:
        src = handle.read()
    env = run_chaos(src)
    structured = env.get("structured_core", {})
    assert structured.get("EVENT") == "relation"
    assert structured.get("OBJECT:BOX") == "ATTRIBUTE:WOOD"
    assert structured.get("OBJECT:GIFT") == "ATTRIBUTE:SMALL"
