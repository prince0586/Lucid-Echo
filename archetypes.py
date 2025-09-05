class ArchetypeInterpreter:
    def interpret(self, dream_text: str):
        # Local lightweight archetype cues - used as fallback when model not available
        cues = []
        text = dream_text.lower()
        if 'water' in text:
            cues.append('Water often relates to emotions and the unconscious.')
        if 'chase' in text:
            cues.append('Chasing can indicate pursuit or avoidance in waking life.')
        if 'fall' in text:
            cues.append('Falling often connects to loss of control or anxiety.')
        if not cues:
            cues.append('This dream contains rich imagery; consider what emotions it stirred.')
        return cues
