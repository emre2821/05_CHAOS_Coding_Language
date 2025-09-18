from chaos_emotion import ChaosEmotionStack

def test_emotion_triggers_and_transition():
    es = ChaosEmotionStack()
    es.trigger_from_text("warmth in the dark, thinking of momma")
    assert es.current() is not None
    prev = es.current().name
    es.transition()
    assert es.current().name == prev or es.current().name in ("HOPE","LOVE","GRIEF","WISDOM")
