---
name: wait-what
description: "Stop. That last message did not land: re-pitch it."
disable-model-invocation: true
---

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the canonical terms from `$CLAUDE_PLUGIN_ROOT/context/CONTEXT.md`. `$CLAUDE_PLUGIN_ROOT` is not a real environment variable — resolve it from this skill's own **"Base directory for this skill"** path (shown above) by walking upward to the directory containing `.claude-plugin/plugin.json`; if that file genuinely isn't reachable, fall back to plain clear English without it rather than blocking on it.
