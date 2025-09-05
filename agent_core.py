import datetime
from memory_manager import MemoryManager
from archetypes import ArchetypeInterpreter
from personas import Narrator
from gpt_oss_wrapper import GPTOSSWrapper

class DreamAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.interpreter = ArchetypeInterpreter()
        self.narrator = Narrator()
        # Initialize wrapper (model path can be a local path or HF id)
        self.model = GPTOSSWrapper()

    def process_dream(self, dream_text: str, password: str):
        timestamp = datetime.datetime.now().isoformat()
        dream_id = self.memory.save_dream(dream_text, timestamp, password)

        # Use the model to generate richer interpretations and a story
        prompt_interp = f"Interpret this dream in multiple symbolic perspectives:\n\n{dream_text}\n\nProvide 3 concise interpretations labeled 1., 2., 3.:"
        interp_text = self.model.generate(prompt_interp, max_tokens=200)

        prompt_story = f"Retell the following dream as a short mythic folktale (approx 150-300 words):\n\n{dream_text}\n\nInclude evocative imagery and a gentle moral."
        story_text = self.model.generate(prompt_story, max_tokens=300, temperature=0.9)

        # Fallback to archetype/simple narrator if model returns stub
        if interp_text.startswith("[stub]"):
            interpretations = self.interpreter.interpret(dream_text)
        else:
            # Split lines by numbering if possible
            interpretations = [line.strip() for line in interp_text.split('\n') if line.strip()][:3]

        if story_text.startswith("[stub]"):
            story = self.narrator.retell(dream_text)
        else:
            story = story_text

        result = {
            "dream_id": dream_id,
            "interpretations": interpretations,
            "story": story,
            "timestamp": timestamp
        }
        self.memory.save_result(dream_id, result, password)
        return result

    def get_dream_history(self, password: str):
        return self.memory.load_all(password)
