import pandas as pd

def read():
    return pd.read_csv("recipee.csv")
    
def add_recipe(name, category, ingredients, prep_time, instructions, difficulty, number_of_servings):
    df = read()
    new_recipe = {
        "name": name,
        "category": category,
        "ingredients": ingredients,
        "prep_time": prep_time,
        "instructions": instructions,
        "difficulty": difficulty,
        "rating": None,
        "number_of_servings":number_of_servings
        }
    df = pd.concat([df, pd.DataFrame([new_recipe])], ignore_index=True)
    df.to_csv("recipee.csv", index=False)


def search_by_ingredients(ingredient):
    df = read()
    result = df[df["ingredients"].str.contains(ingredient, case=False)]
    return result  
    
def view_all_recipes():
    df = read()
    result = df[["name", "prep_time"]]
    return result

def random_recipe():
    df = read()
    result = df.sample()
    return result

def rate_recipe(name, rating):
    df = read()
    df.loc[df["name"] == name, "rating"] = rating
    df.to_csv("recipee.csv", index=False)

def sort_by_rating():
    df = read()
    result = df.sort_values(by="rating", ascending=False)
    return result


def category_stats():
    df = read()
    df["rating"] = df["rating"].astype(float)
    result = df.groupby("category")["rating"].agg(["count", "mean"])
    return result



def scale_ingredients(name, desired_servings):
    df = read()
    ingr = df.loc[df["name"] == name, "ingredients"].values[0]
    original_servings = df.loc[df["name"] == name, "number_of_servings"].values[0]
    scale_factor = desired_servings / original_servings
    items = pd.Series(ingr.split(',')).str.strip()
    numbers = items.str.split().str[0]
    rest_of_text = items.str.split().str[1:].str.join(' ')
    quantities = numbers.astype(float)
    scaled_quantities = quantities * scale_factor
    new_items = scaled_quantities.round(2).astype(str) + " " + rest_of_text
    return ", ".join(new_items)


def shopping_list(recipe_names):
    df = read()
    selected = df[df["name"].isin(recipe_names)]
    ingredients = selected["ingredients"].str.split(",")
    all_ingredients = ingredients.sum()
    result = pd.Series(all_ingredients).str.strip()
    result = result.str.replace(r"^\d+/?\d*\.?\d*\s*", "", regex=True)
    result = result.str.replace(
r"^\b(tablespoons|tablespoon|tbsp|teaspoons|teaspoon|tsp|cups|cup|cloves|clove|slices|slice|pieces|piece|ml|g|kg|l|oz|lb|pinch)\b\s*",
        "", regex=True, case=False)
    result = result.str.lower().str.strip().drop_duplicates()
    return result


import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

def get_secret(name):
    value = os.getenv(name)

    if value:
        return value.strip()

    try:
        value = st.secrets[name]

        if value:
            return str(value).strip()

    except Exception:
        pass

    return None

client = OpenAI(
    api_key=get_secret("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
)



def import_recipe_from_api(dish_name):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"

    try:
        response = requests.get(url, params={"s": dish_name}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    data = response.json()
    meals = data.get("meals")

    if not meals:
        return None

    meal = meals[0]
    ingredients = []

    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")

        if ingredient and ingredient.strip():
            text = f"{measure.strip()} {ingredient.strip()}" if measure else ingredient.strip()
            ingredients.append(text)

    return {
        "name": meal.get("strMeal", ""),
        "category": meal.get("strCategory", "Dinner"),
        "ingredients": ", ".join(ingredients),
        "instructions": meal.get("strInstructions", ""),
        "image": meal.get("strMealThumb")
    }


def smart_chef_suggestion(available_ingredients, dietary_restriction=""):

    if dietary_restriction.strip():
        prompt = f"""
        Here are the available ingredients:

        {available_ingredients}

        Make the recipe suitable for: {dietary_restriction}

        Give substitutions in the following format:

        Original -> Replment (Reason)
        """
    else:
        prompt = f"""
        Create one realistic recipe using mainly these ingredients:

        {available_ingredients}

        Format:

        Titleace

        Ingredients

        Numbered Steps
        """

    try:
        response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500 )

        return response.choices[0].message.content

    except Exception:
        return "⚠️ Unable to generate recipe suggestion."