from task.app.main import run

# TODO:
#  Try `frequency_penalty` parameter.
#  Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's
#  likelihood to repeat the same line verbatim. Higher values == less repetitive text.
#       Range: -2.0 to 2.0
#       Default: 0.0
#  User massage: Explain the water cycle in simple terms for children

run(
    deployment_name='gpt-4o',
    print_only_content=True,
    user_message='I work in EPAM for SwissRe and i want to offer AI enablment to the project. How should i start? ',
    # frequency_penalty=-2.0,
    # generate several results (n=4)
    # n=4,

    # temperature=2, # 0.0 - deterministic, 2.0 - random
    # max_tokens=10, # 100 - max length of the response
    # top_p=0.5, # 0.0 - deterministic, 1.0 - random
    # n=4, # 1 - single response, 4 - 4 responses
    # seed=42, # 42 - random, 123 - random, 1000 - random
    # frequency_penalty=-2.0, # -2.0 - less repetitive, 2.0 - more repetitive
    # presence_penalty=2.0, # 2.0 - more topic diversity, -2.0 - less topic diversity
    # stop='stop', # 'stop' - stop the response, 'stop1' - stop the response after 1 word, 'stop2' - stop the response after 2 words
    # TODO:
    #  Use `frequency_penalty` parameter with different range (-2.0 to 2.0).
)

# Pay attention that when we set for `gpt-4o` frequency_penalty as -2.0 - the request is running too long,
# and in the result we can get something strange (such as repetitive words in the end).
# Copy the results and then check with separate request and ask LLM where is more repetitive blocks in texts.
# For Anthropic and Gemini this parameter will be ignored