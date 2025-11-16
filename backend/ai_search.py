import os
from dotenv import load_dotenv
from openai import OpenAI
from flight_finder import scrape, DRIVER



# CREATE CLIENT
load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)



def search(client=client, prompt=None, budget=None, origin_airport=None):
    spiel = client.chat.completions.create(
        model="openai/gpt-oss-120b:fastest",
        messages=[
            {
                "role": "user",
                "content": f"You are a travel agent. Take the following prompt from a user from near airport"
                f" {origin_airport} who is trying to plan a trip and generate a list of regions/countries/cities"
                f" which would correspond to their travel needs (budge of around {budget} CAD):"
                f" 'Take me somewhere {prompt}'"
            }
        ],
    )
    airportCodeList = client.chat.completions.create(
        model="openai/gpt-oss-120b:fastest",
        messages=[
            {
                "role": "user",
                "content": "Take the following text from a travel agent and generate ONLY a comma-separated"\
                " list of relevant 3-letter airport codes corresponding to the mentioned regions/countries/cities"\
                f": '{spiel.choices[0].message.content}'"
            }
        ],
    ).choices[0].message.content.split(",")

    try:
        scrape(driver=DRIVER, origin_airport=origin_airport, budget=budget, destination_filter=airportCodeList)
    except ValueError:
        try:
            scrape(driver=DRIVER, origin_airport="ATL", budget=budget, destination_filter=airportCodeList)
        except:
            scrape(driver=DRIVER, origin_airport="ATL", budget=None, destination_filter=airportCodeList)

    print(airportCodeList)

    return "../../frontend/results.csv"



# TESTING
if __name__ == "__main__":
    print(search(prompt="I can dream", budget=99, origin_airport="ORY"))