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
print(response)
# use the auto eval Factuality() evaluator

print("calling evaluator")
evaluator = Factuality()
result = evaluator(
    output=response.choices[0]["message"][
        "content"
    ],  # response from waypoint.completion()
    expected="India",  # expected output
    input=question,  # question passed to waypoint.completion
)

print(result)
