import json
from rapidfuzz import fuzz, process

class JSONTool:
    def __init__(self, json_path):
        with open(json_path, 'r') as file:
            self.data = json.load(file)

    def find_closest_product(self, product_name):
        # Extract product names from the data
        product_names = [item["general information"]["name"] for item in self.data]
        # Find closest match using fuzzy matching
        closest_match = process.extractOne(product_name, product_names, scorer=fuzz.ratio)
        if closest_match and closest_match[1] > 60:  # Adjust threshold as needed
            return closest_match[0]
        return None

    def query_product(self, product_name):
        # Find the closest product name match
        closest_product_name = self.find_closest_product(product_name)
        if closest_product_name:
            for item in self.data:
                if item["general information"]["name"] == closest_product_name:
                    return item, closest_product_name
        return None, None

    def query_by_brand(self, brand):
        # Filter products by brand
        filtered_products = [
            item for item in self.data
            if brand.lower() in item["general information"]["brand"].lower()
        ]
        return filtered_products if filtered_products else None

    def get_price_by_product(self, product_name):
        # Get current price for a specific product
        product, closest_product_name = self.query_product(product_name)
        if product:
            original_price = product["general information"].get("original_price", 0)
            discount_price = product["general information"].get("discount_price", 0)
            current_price = original_price - discount_price
            return {
                "product_name": closest_product_name,
                "price": f"{current_price:,} VNĐ" if current_price > 0 else "No valid discount price available."
            }
        return {"error": f"Product '{product_name}' not found."}

    def get_prices_by_brand(self, brand):
        # Get current prices for all products of a brand
        products = self.query_by_brand(brand)
        if products:
            prices = []
            for product in products:
                product_name = product["general information"]["name"]
                original_price = product["general information"].get("original_price", 0)
                discount_price = product["general information"].get("discount_price", 0)
                current_price = original_price - discount_price
                prices.append({
                    "product_name": product_name,
                    "price": f"{current_price:,} VNĐ" if current_price > 0 else "No valid discount price available."
                })
            return prices
        return {"error": f"No products found for brand '{brand}'."}

    def get_technical_specifications(self, product_name):
        # Get technical specifications for a specific product
        product, closest_product_name = self.query_product(product_name)
        if product:
            specs = product.get("technical specifications", {})
            return {
                "product_name": closest_product_name,
                "technical_specifications": specs if specs else "No technical specifications found."
            }
        return {"error": f"Product '{product_name}' not found."}

    def get_promotion(self, product_name):
        # Get promotion for a specific product
        product, closest_product_name = self.query_product(product_name)
        if product:
            promotion = product["general information"].get("promotion", None)
            if promotion:
                return {
                    "product_name": closest_product_name,
                    "promotion": promotion
                }
            return {"error": f"No promotion available for '{closest_product_name}'."}
        return {"error": f"Product '{product_name}' not found."}

    def compare_metadata(self, product_names):
        # Compare metadata for multiple products
        if len(product_names) < 2:
            return {"error": "Please provide at least two product names for comparison."}

        comparison = {}
        unmatched_products = []
        matched_names = []
        for name in product_names:
            product, closest_product_name = self.query_product(name)
            if product:
                matched_names.append(closest_product_name)
                for key, value in product.items():
                    if key not in comparison:
                        comparison[key] = {}
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in comparison[key]:
                                comparison[key][sub_key] = []
                            comparison[key][sub_key].append(sub_value)
                    else:
                        if key not in comparison:
                            comparison[key] = []
                        comparison[key].append(value)
            else:
                unmatched_products.append(name)

        if unmatched_products:
            return {"error": f"The following products were not found: {', '.join(unmatched_products)}"}

        return {"compared_products": matched_names, "comparison": comparison}

class ProductFunctions:
    def __init__(self, json_tool):
        self.json_tool = json_tool

    def get_price_by_product(self, product_name):
        return self.json_tool.get_price_by_product(product_name)

    def get_prices_by_brand(self, brand):
        return self.json_tool.get_prices_by_brand(brand)

    def get_technical_specifications(self, product_name):
        return self.json_tool.get_technical_specifications(product_name)

    def get_promotion(self, product_name):
        return self.json_tool.get_promotion(product_name)

    def compare_metadata(self, product_names):
        return self.json_tool.compare_metadata(product_names)
