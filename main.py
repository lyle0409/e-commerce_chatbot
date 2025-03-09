from typing import Union

from fastapi import FastAPI

from recommend import recommend
from json_tool import JSONTool, ProductFunctions
from embedding_data import get_embedding, resize_embedding, flatten_json, prepare_data, load_json_file, embedding_data
from typing import List
from pydantic import BaseModel
from search_online_4o import search_online


JSON_PATH = "product_data_3_pages_hoangha.json"
# Load and prepare data, generating embeddings on the fly
raw_data = load_json_file(JSON_PATH)  # Load raw product data
flattened_data = flatten_json(raw_data)  # Flatten nested fields, if any
data_with_embeddings = prepare_data(flattened_data)  # Generate embeddings for the data

app = FastAPI()

# Initialize JSONTool and ProductFunctions
json_tool = JSONTool(JSON_PATH)
product_functions = ProductFunctions(json_tool)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{name}")
def read_item(name: str):
    return {"name": name, "price": "14.000.000"}

## Embedding data
# data = embedding_data(JSON_PATH)
data = load_json_file("product_data_with_embeddings.json") # Demo với data đã embedding

@app.get("/recommend/")
def recommend_prod(filter_price: float, operator: str, intention: str) -> str:
    return str(recommend(data_with_embeddings, filter_price, operator, intention))

# Endpoint to get current price by product name
@app.get("/get_current_price_by_product/")
def get_current_price_by_product(product_name: str):
    return {"price": product_functions.get_price_by_product(product_name=product_name)}

# Endpoint to get current price by brand
@app.get("/get_current_price_by_brand/")
def get_current_price_by_brand(brand: str):
    return {"prices": product_functions.get_prices_by_brand(brand=brand)}

# Endpoint to get technical specifications
@app.get("/get_technical_specifications/")
def get_technical_specifications(product_name: str):
    return {"technical_specifications": product_functions.get_technical_specifications(product_name=product_name)}

# Endpoint to get promotion information
@app.get("/get_promotion/")
def get_promotion(product_name: str):
    return {"promotion": product_functions.get_promotion(product_name=product_name)}

@app.get("/search_online/")
def search_online_by_name(product_name: str) -> str:
    return str(search_online(product_name=product_name))

class ProductComparisonRequest(BaseModel):
    product_names: List[str]

@app.post("/compare_metadata/")
def compare_metadata(request: ProductComparisonRequest):
    return {"comparison": product_functions.compare_metadata(request.product_names)}