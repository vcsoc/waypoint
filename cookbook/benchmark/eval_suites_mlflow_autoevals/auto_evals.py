import sys

from dotenv import load_dotenv

load_dotenv()

from autoevals.llm import *

import waypoint

###################

# litellm completion call
question = "which country has the highest population"
response = waypoint.completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
)
sys.stdout.write(str(response) + "\n")
# use the auto eval Factuality() evaluator

sys.stdout.write("calling evaluator" + "\n")
evaluator = Factuality()
result = evaluator(
    output=response.choices[0]["message"][
        "content"
    ],  # response from waypoint.completion()
    expected="India",  # expected output
    input=question,  # question passed to waypoint.completion
)

sys.stdout.write(str(result) + "\n")
