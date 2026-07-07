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
    df["ingredients"] = df["ingredients"].astype(str)
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
    recipe = df[df["name"] == name]
    if recipe.empty:
        return "Recipe not found"
    ingr = recipe["ingredients"].iloc[0]
    original_servings = recipe["number_of_servings"].iloc[0]
    scale_factor = desired_servings / original_servings
    items = pd.Series(ingr.split(','))
    items = items.str.strip()
    parts = items.str.split(n=1, expand=True)
    quantities = parts[0].astype(float)
    rest = parts[1]
    scaled_quantities = quantities * scale_factor
    new_items = scaled_quantities.round(2).astype(str) + " " + rest
    return ", ".join(new_items)


def shopping_list(recipe_names):
    df = read()
    selected = df[df["name"].isin(recipe_names)]
    ingredients = selected["ingredients"].str.split(",")
    all_ingredients = ingredients.sum()
    result = pd.Series(all_ingredients).str.strip()
    result = result.str.replace(
    r"^\d+/?\d*\.?\d*\s*"
    r"\b(tablespoons|tablespoon|tbsp|teaspoons|teaspoon|tsp|cups|cup|cloves|clove|slices|slice|pieces|piece|ml|g|kg|l|oz|lb|pinch)\b\s*",
    "", regex=True, case=False)
    result = result.drop_duplicates()
    return result









 