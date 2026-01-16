import json
import os

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

from task.models.message import Message
from task.models.role import Role

# Load environment variables from .env file
load_dotenv()

# Initialize Rich console for markdown rendering
console = Console()


class DialClient:
    _endpoint: str
    _api_key: str

    def __init__(self, endpoint: str, deployment_name: str):
        api_key = os.getenv('DIAL_API_KEY', '')
        if not api_key or api_key.strip() == "":
            raise ValueError(
                "API key cannot be null or empty. Please:\n"
                "1. Create a .env file in the project root\n"
                "2. Add: DIAL_API_KEY=your_actual_api_key\n"
                "3. Get your key from: https://support.epam.com/ess?id=sc_cat_item&table=sc_cat_item&sys_id=910603f1c3789e907509583bb001310c"
            )
        
        # Debug: Check if API key looks valid (print first/last few chars)
        print(f"🔑 API Key loaded: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")

        self._endpoint = endpoint.format(
            model=deployment_name
        )
        self._api_key = api_key

    def get_completion(
            self, messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        """
        Send synchronous request to DIAL API and return AI response.

        Args:
            messages (list[Message]): List of conversation messages
            print_request (bool): If True, pretty print the request data
            print_only_content (bool): If True, only print response content

            **kwargs: Additional OpenAI-compatible parameters:
                temperature (float): Controls the randomness of the output. It's a parameter for balancing creativity and determinism.
                    Range: 0.0 to 2.0
                    Default: 1.0

                top_p (float): An alternative to sampling with temperature, called nucleus sampling.
                    The model considers the results of the tokens with top_p probability mass.
                    Range: 0.0 to 1.0
                    Default: 1.0
                IMPORTANT: **It's generally not recommended to use temperature and top_p together!**
                    According to OpenAI's documentation, you should typically use either temperature or top_p, but not
                    both simultaneously. Here's why:
                        - `temperature` - controls randomness by scaling the probability distribution of all possible next tokens
                        - `top_p` - (nucleus sampling) controls randomness by only considering tokens within a certain probability mass
                    When used together, they can interact in unpredictable ways and make it harder to control the model's behavior.
                    The effects compound and can lead to either overly conservative or overly random outputs.

                    Best practice:
                        - Use `temperature` when you want straightforward control over randomness (0.0 = deterministic, higher = more creative)
                        - Use `top_p` when you want more nuanced control over the diversity of responses while maintaining quality

                n (int): How many chat completion choices to generate for each input message. Note that you will be charged
                    based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs
                    Default: 1

                seed (int): If specified, the system will make a best effort to sample deterministically, such that repeated
                    requests with the same seed and parameters should return the same result. In other words, seed allows
                    us to reduce entropy by making the model's output more deterministic.
                    There's no universally "best" seed - any integer works fine. Common approaches:
                        - For testing: Use simple values like 42, 123, or 1000
                        - For production: Use meaningful numbers like timestamps, user IDs, or content hashes
                        - For experiments: Use the same seed across test runs to isolate other parameter effects
                    Default: None

                max_tokens (int): Sets the maximum length of the AI's response. The AI will stop generating text once it hits this limit.
                    Default: inf

                frequency_penalty (float): Positive values penalize new tokens based on their existing frequency in the text so far,
                    decreasing the model's likelihood to repeat the same line verbatim. Higher values == less repetitive text.
                    Range: -2.0 to 2.0
                    Default: 0.0

                presence_penalty (float): Positive values penalize new tokens based on whether they appear in the text so far,
                    increasing the model's likelihood to talk about new topics. Higher values == more topic diversity.
                    Range: -2.0 to 2.0
                    Default: 0.0

                stop (str or list[str]): Tells the AI to stop generating text when it encounters specific words or phrases.
                    Like setting custom "end of response" triggers.
                    Default: None
        """
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            "messages": [msg.to_dict() for msg in messages],
            **kwargs,
        }

        if print_request:
            self._print_request(request_data, headers)

        response = requests.post(url=self._endpoint, headers=headers, json=request_data, timeout=60)

        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                print("\n" + "="*50 + " RESPONSE " + "="*50)
                
                # Handle multiple choices (when n > 1)
                if len(choices) > 1:
                    print(f"\n📊 **Generated {len(choices)} choices:**\n")
                    for idx, choice in enumerate(choices, 1):
                        content = choice.get("message", {}).get("content")
                        print(f"\n{'─'*70}")
                        print(f"**Choice {idx}/{len(choices)}:**")
                        print(f"{'─'*70}\n")
                        console.print(Markdown(content))
                        if not print_only_content:
                            print(f"\n_Finish Reason: {choice.get('finish_reason', 'N/A')}_")
                    
                    if not print_only_content:
                        print(f"\n{'─'*70}")
                        print(f"\n**Metadata:**")
                        print(f"- Model: {data.get('model', 'N/A')}")
                        print(f"- Total Choices: {len(choices)}")
                        usage = data.get("usage", {})
                        if usage:
                            print(f"- Tokens Used: {usage.get('total_tokens', 'N/A')} (prompt: {usage.get('prompt_tokens', 'N/A')}, completion: {usage.get('completion_tokens', 'N/A')})")
                        print()
                else:
                    # Single choice (n=1 or default)
                    content = choices[0].get("message", {}).get("content")
                    if print_only_content:
                        # Render content as markdown
                        console.print(Markdown(content))
                        print()
                    else:
                        # Display in markdown-friendly format
                        print(f"\n**Model Response:**\n")
                        # Render content as markdown
                        console.print(Markdown(content))
                        print(f"\n**Metadata:**")
                        print(f"- Model: {data.get('model', 'N/A')}")
                        print(f"- Finish Reason: {choices[0].get('finish_reason', 'N/A')}")
                        usage = data.get("usage", {})
                        if usage:
                            print(f"- Tokens Used: {usage.get('total_tokens', 'N/A')} (prompt: {usage.get('prompt_tokens', 'N/A')}, completion: {usage.get('completion_tokens', 'N/A')})")
                        print()
                
                print("="*108)
                # Return the first choice for conversation continuity
                return Message(Role.AI, choices[0].get("message", {}).get("content"))
            raise ValueError("No Choice has been present in the response")
        else:
            # Better error messages for common issues
            if response.status_code == 403:
                raise Exception(
                    f"❌ HTTP 403: Access Denied\n\n"
                    f"This usually means:\n"
                    f"1. You're not connected to EPAM VPN (required!)\n"
                    f"2. Your API key is invalid or expired\n"
                    f"3. Your API key doesn't have access to model: {self._endpoint}\n\n"
                    f"Please verify:\n"
                    f"- EPAM VPN is connected\n"
                    f"- Your API key is correct in the .env file\n"
                    f"- Get a new key if needed: https://support.epam.com/ess?id=sc_cat_item&table=sc_cat_item&sys_id=910603f1c3789e907509583bb001310c\n\n"
                    f"Response: {response.text}"
                )
            elif response.status_code == 401:
                raise Exception(
                    f"❌ HTTP 401: Unauthorized\n\n"
                    f"Your API key is missing or invalid.\n"
                    f"Please check your .env file and ensure DIAL_API_KEY is set correctly.\n\n"
                    f"Response: {response.text}"
                )
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")


    def _print_request(self, request_data: dict, headers: dict):
        """Pretty print the request details."""
        print("\n" + "="*50 + " REQUEST " + "="*50)
        print(f"🔗 Endpoint: {self._endpoint}")

        print("\n📋 Headers:")
        safe_headers = headers.copy()
        if "api-key" in safe_headers:
            api_key = safe_headers["api-key"]
            safe_headers["api-key"] = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"

        for key, value in safe_headers.items():
            print(f"  {key}: {value}")

        print("\n📝 Request Body:")
        messages = request_data.get("messages", [])
        other_params = {k: v for k, v in request_data.items() if k != "messages"}

        if messages:
            print("  Messages:")
            for i, msg in enumerate(messages):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                content_preview = content[:100] + "..." if len(content) > 100 else content
                print(f"    [{i+1}] {role.upper()}: {content_preview}")

        if other_params:
            print("\n  Parameters:")
            for key, value in sorted(other_params.items()):
                print(f"    {key}: {value}")

        print("="*107)
