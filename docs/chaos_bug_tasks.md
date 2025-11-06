# CHAOS Bug Task List

- [x] **DreamEngine ignored deterministic seeds.** Wire the internal random selection through a `random.Random` instance so the optional seed parameter produces repeatable visions.
- [x] **Continuation build emitted invalid escape warnings.** Switch the module docstring to a raw string to avoid noisy `SyntaxWarning` messages during compilation.

These fixes keep DreamEngine outputs stable for testing and ensure the build helper runs without warning chatter.
