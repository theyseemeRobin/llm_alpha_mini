from sys import argv
from llm_alpha_mini.llm import Gemini
from llm_alpha_mini.dialogue_manager.dialogue_manager import DialogueManager
from llm_alpha_mini.tasks.registry import print_registered_tasks


def main():
    gemini = Gemini(model="gemini-2.0-flash", api_key=argv[1])
    dialogue_manager = DialogueManager(session=None, llm=gemini)
    ret = dialogue_manager.listen("Hello, my name is John.")


if __name__ == "__main__":
    main()