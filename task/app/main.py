from task.app.client import DialClient
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role

DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."
DIAL_ENDPOINT = "https://ai-proxy.lab.epam.com/openai/deployments/{model}/chat/completions"


def run(
        deployment_name: str,
        print_request: bool = True,
        print_only_content: bool = False,
        user_message: str = None,
        **kwargs
) -> None:
    client = DialClient(
        endpoint=DIAL_ENDPOINT,
        deployment_name=deployment_name,
    )
    conversation = Conversation()
    conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))

    # If user_message is provided, send it once and exit
    if user_message:
        conversation.add_message(Message(Role.USER, user_message))
        ai_message = client.get_completion(
            messages=conversation.get_messages(),
            print_request=print_request,
            print_only_content=print_only_content,
            **kwargs
        )
        conversation.add_message(ai_message)
        return

    # Interactive mode
    print("Type your question or 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
    
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
    
        conversation.add_message(Message(Role.USER, user_input))

        print("AI:")
        ai_message = client.get_completion(
            messages=conversation.get_messages(),
            print_request=print_request,
            print_only_content=print_only_content,
            **kwargs
        )
        conversation.add_message(ai_message)
