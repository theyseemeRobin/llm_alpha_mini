# LLM Alpha Mini
This is a package for integrating LLMs (currently only Gemini) into the Alpha Mini robot to allows human-robot interaction for social robots.

## Installation
To install this package (tested on python 3.12):
```
pip install git+https://github.com/theyseemeRobin/llm_alpha_mini.git
```

## usage
Following the installation, you can run one of the scripts in the [scripts](scripts) directory as follows:
```
python main.py [YOUR_GEMINI_API_KEY]
python gemini_only.py [YOUR_GEMINI_API_KEY]
```
You can obtain a gemini api key from [Google AI Studio](https://aistudio.google.com/app/apikey).

the `main.py` script will attempt to connect with an Alpha Mini Robot (note this requires proper setup as instructed in the documentation). the `gemini_only.py` script skips the robot, and simply interacts through text-only. This script will ask for a user response, and will print Gemini's output.
