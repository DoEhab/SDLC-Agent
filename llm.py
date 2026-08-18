import os
import cohere
from dotenv import load_dotenv

load_dotenv()

client = cohere.ClientV2(
    os.getenv("COHERE_API_KEY")
)


def ask_llm(prompt):
    response = client.chat(
        model="command-a-03-2025",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content[0].text