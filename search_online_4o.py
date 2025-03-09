from serpapi import GoogleSearch
import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import time

def load_api_key(api_key):
    load_dotenv()
    return os.getenv(api_key)

def get_data_online(product_name):
    google_api = "Google_API_key"

    # re-make the query in a standard format 
    query = f"{product_name} hoàng hà"

    params = {
        "q": query,
        "api_key": google_api
    }
    # get response from GoogleSearch API with params
    search = GoogleSearch(params)
    results = search.get_dict()
    # with open('search_online_result.json', 'w', encoding='utf-8') as f:
    #    f.write(results)
    # get the first result of searching
    if results:
        first_result = results["organic_results"][0]
        return json.dumps(first_result, indent= 4)
    return None

def search_online(product_name):
    
    # load open api key & OpenAI model
    open_api_key = "OpenAi_key"
    client = OpenAI(api_key = open_api_key)

    # get the result from Google Search
    search_result = get_data_online(product_name = product_name)

    # with open('search_online_result.json', 'w', encoding='utf-8') as f:
    #     f.write(search_result)

    # using gpt to make the response for user
    response = client.chat.completions.create(
        model="gpt-4o",  # using gpt-4o / 4o-mini is acceptable
        messages=[
            {
                "role": "system",
                "content": (f"You are a helpful assistant"
                            f"Here is an information of the searched product: {search_result}."
                            f"The provided information will include the product's link, hence you can access to it and get necessary data"
                            f"You need to provide data (includes name, corresponding price, corresponding product's link)."
                            f"The promotion is also display (it should be the return policy or sale information applied on the product)"
                            f"Some technical specifications of the product maybe displayed if exist."
                            f"The rating and review of product could be display if exist"
                            f"Your answer must be in Vietnamese.")

            },
            {
                "role": "user",
                "content": f"Search for {product_name}."
            }
        ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    product_name = "iphone 13"
    result = search_online(product_name = product_name)
    print(f"Searching result for {product_name}:\n {result}")

# result = search_online("samsung s24 ultra")

# with open('search_online_result.txt', 'w', encoding='utf-8') as f:
#     f.write(result)


