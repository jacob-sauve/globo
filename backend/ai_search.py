import os
from dotenv import load_dotenv
from openai import OpenAI
from flight_finder import scrape, DRIVER, ORDERED_CSV_HEADERS
import csv



# CREATE CLIENT
load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)



def search(client=client, prompt=None, budget=None, origin_airport=None):
    # do the scraping
    try:
        results = scrape(driver=DRIVER, origin_airport=origin_airport, budget=budget)
    except ValueError:
        try:
            # most frequently flown airport ==> Atlanta
            results = scrape(driver=DRIVER, origin_airport="ATL", budget=budget)
        except:
            results = scrape(driver=DRIVER, origin_airport="ATL", budget=None)

    # ai filter
    destination_filter = client.chat.completions.create(
        model="openai/gpt-oss-120b:fastest",
        messages=[
            {
                "role": "user",
                "content": f"You are a travel agent. You will receive 2 inputs: (1) a prompt from a user from near airport"
                           f" {origin_airport} who is trying to plan a trip and generate a list of regions/countries/cities"
                           f" which would correspond to their travel needs; and (2) a list of possible destinations. Your job"
                           f" is to select the top {min(10, len(results)) or 1} destinations from the list. Answer ONLY a comma-separated list of the chosen"
                           f" destinations, named exactly (character-perfect) as they are in the provided list (2). Here are the inputs, in order:"
                           f" (1) 'Take me somewhere {prompt}'; (2) Possible destinations: {",".join(d.get("Destination", "") for d in results)}"
            }
        ],
    ).choices[0].message.content.split(",")
    destination_filter = [d.upper().strip() for d in destination_filter]
    print(destination_filter)

    filtered_results = [d for d in results if d.get("Destination").upper().strip() in destination_filter]
    airport_codes = client.chat.completions.create(
        model="openai/gpt-oss-120b:fastest",
        messages=[
            {
                "role": "user",
                "content": f"Turn the following ordered list of destinations into an list of corresponding nearest"
                           f" airport codes in the same order. Answer ONLY as a comma-separated list of 3-letter"
                           f" airport codes. The destinations, in order, are: {",".join(d.get("Destination", "") for d in filtered_results)}"
            }
        ],
    ).choices[0].message.content.split(",")
    for i, result in enumerate(filtered_results):
        print(result)
        result["Destination"] = airport_codes[i].upper().strip()

    # write to csv
    with open("../frontend/results.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ORDERED_CSV_HEADERS)
        writer.writeheader()
        for entry in filtered_results:
            writer.writerow(entry)

    return "../../frontend/results.csv"



# TESTING
if __name__ == "__main__":
    print(search(prompt="I can dream", budget=99, origin_airport="ORY"))