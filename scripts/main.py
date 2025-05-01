from sys import argv
from llm_alpha_mini.llm import Gemini
from llm_alpha_mini.dialogue_manager.dialogue_manager import DialogueManager
from llm_alpha_mini.tasks.registry import print_registered_tasks
from alpha_mini_rug.speech_to_text import SpeechToText

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):

    # Alpha mini introduces itself.
    yield session.call("rom.optional.behavior.play", name='BlocklyStand')
    session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")

    # Gemini setup
    gemini = Gemini(model="gemini-2.0-flash", api_key=argv[1])
    dialogue_manager = DialogueManager(session=session, llm=gemini)

    # Call the Automatic Speech Recognition Module
    yield automatic_speech_recognition(session, dialogue_manager)

    # Close the connection with the robot
    session.leave()



@inlineCallbacks
def automatic_speech_recognition(session, dialogue_manager):
    """
    Function for Automatic Speech Recognition and Text Processing.

    Args:
        session (session): Session object.
        dialogue_manager (dialogue_manager.DialogueManager): DialogueManager object.
    """
    # Setup ASR module.
    audio_processor = SpeechToText()

    # Time of silence before the robot stops recording.
    audio_processor.silence_time = 0.5
    audio_processor.silence_threshold2 = 100
    audio_processor.logging = False

    # Setup dialogue types
    info = yield session.call("rom.sensor.hearing.info")
    print(info)
    yield session.call("rom.sensor.hearing.sensitivity", 1650)
    # Language
    yield session.call("rie.dialogue.config.language", lang="en")
    # Greeting
    yield session.call("rie.dialogue.say", text="Hello! My name is R.O.B.")
    print("listening to audio")
    yield session.subscribe(audio_processor.listen_continues, "rom.sensor.hearing.stream")
    yield session.call("rom.sensor.hearing.stream")
    while True:
        # In case the conversation partner is still speaking.
        if not audio_processor.new_words:
            yield sleep(0.5)  # VERY IMPORTANT, OTHERWISE THE PROGRAM MIGHT CRASH
        # Otherwise process the audio and return the processed string.
        else:
            word_array = audio_processor.give_me_words()
            # Pass the string to the dialogue manager.
            dialogue_manager.listen(word_array)
            audio_processor.words = []
        audio_processor.loop()

# Robot connection setup
# IMPORTANT: CHANGE REALM TO THE SPECIFIC ROBOT.
wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.680f74dd29c04006ecc06a97",
)
wamp.on_join(main)



if __name__ == "__main__":
    run([wamp])