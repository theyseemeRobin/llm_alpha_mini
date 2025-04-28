from sys import argv
from llm_alpha_mini.llm import Gemini
from llm_alpha_mini.dialogue_manager.dialogue_manager import DialogueManager
from llm_alpha_mini.tasks.registry import print_registered_tasks
from alpha_mini_rug.speech_to_text import SpeechToText

def main():

    # Gemini setup
    gemini = Gemini(model="gemini-2.0-flash", api_key=argv[1])
    session = None
    dialogue_manager = DialogueManager(session=session, llm=gemini)
    text = None
    while text != "quit":
        text = input(f"Response: ")
        dialogue_manager.listen(text)


if __name__ == "__main__":
    main()
