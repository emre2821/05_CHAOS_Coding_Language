# File: tests/test_interpreter.py

from chaos_runtime import run_chaos

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

