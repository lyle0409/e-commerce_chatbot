import numpy as np
import openai
from embedding_data import get_embedding, resize_embedding, load_json_file
from embedding_data import get_embedding, resize_embedding, load_json_file


# Cosine similarity function
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def filter_by_price(filter_price, products, operator):
    if operator == ">":
        return [product for product in products if product["original_price"] > filter_price]
    elif operator == "<":
        return [product for product in products if product["original_price"] < filter_price]
    elif operator == "<=":
        return [product for product in products if product["original_price"] <= filter_price]
    elif operator == ">=":
        return [product for product in products if product["original_price"] >= filter_price]
    elif operator == "=":
        return [product for product in products if product["original_price"] == filter_price]
        return [product for product in products if product["original_price"] == filter_price]


def search_most_relevance(filtered_data, intention):
    # Generate embedding for the user's intention
    intention_embedding = get_embedding(intention)

    # Lấy chiều dài của embedding đầu tiên (mặc định là embedding của sản phẩm đầu tiên)
    target_size = max(len(product["embedding"]) for product in filtered_data)

    # Resize intention embedding to match the product's embedding size
    if len(intention_embedding) != target_size:
        intention_embedding = resize_embedding(intention_embedding, target_size)

    # Calculate similarity of each product's embedding to the intention embedding
    similarities = []
    for product in filtered_data:
        # Resize product embedding to match intention embedding size
        product_embedding = resize_embedding(product["embedding"], target_size)

        similarity = cosine_similarity(intention_embedding, product_embedding)
        # Resize product embedding to match intention embedding size
        product_embedding = resize_embedding(product["embedding"], target_size)

        similarity = cosine_similarity(intention_embedding, product_embedding)
        similarities.append((product, similarity))

    # Return top 3 most relevant products sorted by similarity score
    return sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
 

def recommend(data, filter_price: float, operator: str, intention: str) -> str:
    
    
    data_filter_bt_price = filter_by_price(filter_price, data, operator)

    filter_by_intention = search_most_relevance(data_filter_bt_price, intention)

    filtered_results = [
        {key: value for key, value in product[0].items() if key != "embedding"} 
        for product in filter_by_intention
    ]

    return filtered_results

# if __name__ == "__main__":
#     data = load_json_file("product_data_with_embeddings.json")

#     # Scenario 1: Looking for a budget-friendly phone within a price range
#     filter_price_1 = 651000
#     operator_1 = "<="
#     intention_1 = "I want a cheap phone with basic features for everyday use."
#     result_1 = recommend(data, filter_price_1, operator_1, intention_1)
#     print("Scenario 1 Results:", result_1)

    # # Scenario 2: Seeking a high-end laptop for professional work within a budget
    # filter_price_2 = 3000
    # operator_2 = "<="
    # intention_2 = "I'm looking for a high-performance laptop suitable for professional work."
    # result_2 = recommend(data, filter_price_2, operator_2, intention_2)
    # print("Scenario 2 Results:", result_2)

    # # Scenario 3: Finding an affordable smartwatch with fitness tracking capabilities
    # filter_price_3 = 300
    # operator_3 = "<="
    # intention_3 = "I need a smartwatch that tracks fitness and heart rate on a budget."
    # result_3 = recommend(data, filter_price_3, operator_3, intention_3)
    # print("Scenario 3 Results:", result_3)

    # # Scenario 4: Looking for a gaming console with good graphics for under $4000
    # filter_price_4 = 4000
    # operator_4 = "<="
    # intention_4 = "I'm looking for a gaming console with excellent graphics and game options."
    # result_4 = recommend(data, filter_price_4, operator_4, intention_4)
    # print("Scenario 4 Results:", result_4)

    # # Scenario 5: Seeking a compact wireless mouse that’s affordable and easy to carry
    # filter_price_5 = 100
    # operator_5 = "<="
    # intention_5 = "I need a small wireless mouse that’s portable and affordable."
    # result_5 = recommend(data, filter_price_5, operator_5, intention_5)
    # print("Scenario 5 Results:", result_5)