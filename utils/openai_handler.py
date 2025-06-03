import os
import openai
from dotenv import load_dotenv

# Load the OpenAI API key from environment variable
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_kubectl_command(prompt: str, context: str) -> str:
    system_prompt = """
You are a Kubernetes command-line assistant. Your role is to translate natural language requests into safe, valid, and concise kubectl commands.

Rules:

- Respond with only the final kubectl command—no explanations, no additional text.
- Use `kubectl run` to create and immediately run a simple pod from an image (e.g., nginx). This is preferred for one-off or demo-style pods.
- Use `kubectl create` only if the user specifically asks for a manifest file, YAML generation, or requests a resource that requires more complex setup.
- Do not generate commands that delete or modify existing resources unless explicitly requested by the user.
- Default to the `default` namespace unless the user specifies a different one.
- Include flags like `--restart=Never` for jobs or ephemeral pods if relevant.
- Always validate resource names and types based on standard Kubernetes CLI behavior.
- If the request is ambiguous or unsafe (e.g., mass deletion), assume no action should be taken.
- Never hallucinate or fabricate resources, flags, or API behaviors. Stick strictly to the Kubernetes CLI.
    """.strip()

    user_message = f"{prompt}. Context: {context}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2,
            max_tokens=100
        )

        command = response.choices[0].message['content'].strip()

        # Optionally append the context if not present
        if "--context" not in command:
            command += f" --context {context}"

        return command

    except Exception as e:
        raise RuntimeError(f"OpenAI error: {str(e)}")
