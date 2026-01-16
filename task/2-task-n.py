from task.app.main import run

# TODO:
#  Try the `n` parameter with different models (`deployment_name`). With the parameter `n`, we can configure how many
#       chat completion choices to generate for each input message
#  User message: Why is the snow white?

# Models to try:
# - gpt-4o
# - claude-3-7-sonnet@20250219
# - gemini-2.5-pro

# Test 1: GPT-4o with n=3
print("\n" + "="*80)
print("# Test 1: GPT-4o with n=3")
print("="*80)
print("**Question:** Why is the snow white?")
print("**Parameter:** n=3 (generating 3 different responses)\n")
run(
    deployment_name='gpt-4o',
    user_message='Why is the snow white?',
    n=3,
    print_request=False,
    print_only_content=False,
)

# # Test 2: Claude with n=2
# print("\n" + "="*80)
# print("# Test 2: Claude 3.7 Sonnet with n=2")
# print("="*80)
# print("**Question:** Why is the snow white?")
# print("**Parameter:** n=2 (generating 2 different responses)\n")
# run(
#     deployment_name='claude-3-7-sonnet@20250219',
#     user_message='Why is the snow white?',
#     n=2,
#     print_request=False,
#     print_only_content=False,
# )

# Test 3: Gemini with n=4
print("\n" + "="*80)
print("# Test 3: Gemini 2.5 Pro with n=4")
print("="*80)
print("**Question:** Why is the snow white?")
print("**Parameter:** n=4 (generating 4 different responses)\n")
run(
    deployment_name='gemini-2.5-pro',
    user_message='Why is the snow white?',
    n=4,
    print_request=False,
    print_only_content=False,
)

print("\n" + "="*80)
print("✅ All models tested with different n values!")
print("="*80)

# Pay attention to the number of choices in the response!
# If you have worked with ChatGPT, you have probably seen responses where ChatGPT offers you a choice between two
# responses to select which one you prefer. This is done with the `n` parameter.
