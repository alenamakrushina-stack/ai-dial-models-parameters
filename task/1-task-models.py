from task.app.main import run

# HINT: All available models you can find here: https://ai-proxy.lab.epam.com/openai/models

# TODO:
#  Try different models (`deployment_name`) with such user request:
#  User message: What LLMs can do?

# Models to try:
# - gpt-4o
# - claude-3-7-sonnet@20250219
# - gemini-2.5-pro

# Test 1: GPT-4o
print("\n" + "="*80)
print("# Test 1: GPT-4o")
print("="*80)
print("**Question:** What LLMs can do?\n")
run(
    deployment_name='gpt-4o',
    user_message='What LLMs can do?',
    print_request=False, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response
)

# Test 2: Claude 3.7 Sonnet
print("\n" + "="*80)
print("# Test 2: Claude 3.7 Sonnet")
print("="*80)
print("**Question:** What LLMs can do?\n")
run(
    deployment_name='anthropic.claude-3-7-sonnet-20250219-v1:0',
    user_message='What LLMs can do?',
    print_request=True,
    print_only_content=False,
)

# Test 3: Gemini 2.5 Pro
print("\n" + "="*80)
print("# Test 3: Gemini 2.5 Pro")
print("="*80)
print("**Question:** What LLMs can do?\n")
run(
    deployment_name='gemini-2.5-pro',
    user_message='What LLMs can do?',
    print_request=False,
    print_only_content=False,
)

print("\n" + "="*80)
print("✅ All models tested successfully!")
print("="*80)

# The main goal of this task is to explore the functional capabilities of DIAL to be able to work with different
# LLMs through unified API
