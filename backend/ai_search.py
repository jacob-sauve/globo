import os
from dotenv import load_dotenv
from openai import OpenAI



# CREATE CLIENT
load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)



def search(client=client, prompt=None, budget=None):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:fastest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    print(completion)
    return completion



# TESTING
if __name__ == "__main__":
    print(search(prompt="what's up broski").choices[0].message)