import streamlit as st 
from project_function import * 

st.sidebar.title(" Recipe Dashboard")
choice = st.sidebar.radio(
    
    "📋 Choose an option:",
    (
        "➕ Add a new recipe",
        "🔍 Search by ingredient",
        "📖 View all recipes",
        "🎲 Random recipe",
        "⭐ Rate recipe",
        "📊 Sort by rating",
        "📏 Scale Ingredients",
        "🛒 Shopping list"
    )
)

if choice == "➕ Add a new recipe":
    st.title(" Create New Recipe")
    st.markdown("Fill in the details below to add your recipe 📚")
    st.divider()
    
    with st.form("recipe_form", clear_on_submit=True):
        name = st.text_input("📝 Recipe Name")
        ingredients = st.text_area("🧂 Ingredients", placeholder="Enter ingredients separated by commas")
        col1, col2 = st.columns(2)
        number_of_servings = st.number_input("Number of servings",min_value=0)
        with col1:
            prep_time = st.number_input("⏱️ Preparation time (minutes)", min_value=0)
        with col2:
            difficulty = st.selectbox("📊 Difficulty level", ["Easy", "Medium", "Hard"])
        instructions = st.text_area("👨‍🍳 Instructions", placeholder="Write each step on a new line...")
        category = st.selectbox("🍽️ Category", ["Breakfast", "Lunch", "Dinner", "Dessert"])
        st.divider()
        
        if st.form_submit_button("✅ Add Recipe"):
            df=read()
            name=name.strip().lower() 
            ingredients=ingredients.strip() 
            instructions=instructions.strip() 
            if name == "" or ingredients == "" or prep_time == 0 or instructions == "" or number_of_servings==0:
                st.error("⚠️ Please fill in all the required fields before submitting.")
            elif name in df['name'].str.lower().values:  
                st.error(f"⚠️ '{name}' already exists! Please choose a different name.")
            else:
                add_recipe(name, category, ingredients, prep_time, instructions, difficulty,number_of_servings)
                st.success("🎉 Recipe added successfully!")

                
if choice == "🔍 Search by ingredient":
    st.title("🔍 Search by ingredient")
    st.markdown("Find recipes that use a specific ingredient.")
    st.divider()
    ingredient = st.text_input("Enter an ingredient")
    if st.button("🔎 Search"):
        result = search_by_ingredients(ingredient)
        if len(result) == 0:
            st.warning("⚠️ No recipes found with this ingredient.")
        else:
            st.success(f"✅ Found {len(result)} recipe(s)!")
            st.dataframe(result)
    st.divider()      


if choice == "📖 View all recipes":
    result = view_all_recipes()
    if len(result) == 0:
        st.warning("⚠️ No recipes found yet. Add your first recipe! ")
    else:
        st.dataframe(result)


        
if choice == "🎲 Random recipe":
    st.title("🎲 Random Recipe Suggestion")
    st.markdown("Not sure what to cook? Let us surprise you! 🍽️")
    st.divider()
    if st.button("🎲 Surprise Me!"):
        result = random_recipe()
        if len(result) == 0:
            st.warning("⚠️ No recipes found yet. Add your first recipe! ")
        else:
            st.dataframe(result)
            
       

if choice == "⭐ Rate recipe":
    st.title("⭐ Rate a Recipe")
    st.markdown("Give this recipe a rating 🌟")
    st.divider()
    df = read()
    name = st.selectbox("🍴 Choose a recipe", df["name"])
    rating = st.slider("⭐ Rating (1 to 5)", min_value=1, max_value=5)
    st.divider()
    if st.button("✅ Submit Rating"):
        rate_recipe(name, rating)
        st.success("🎉 Rating saved successfully!")


if choice == "📊 Sort by rating":
    st.title("📊 Ratings Overview")
    st.markdown("See the top-rated recipes and category performance 🌟")
    st.divider()

    tab1, tab2 = st.tabs(["📊 All Sorted", "📈 Category Stats"])

    with tab1:
        result = sort_by_rating()
        if len(result) == 0:
            st.warning("⚠️ No recipes found yet. Add your first recipe! ")
        else:
            st.dataframe(result)
    with tab2:
        result = category_stats()
        st.dataframe(result)


if choice == "📏 Scale Ingredients":
    st.title("📏 Scale a Recipe")
    st.markdown("Adjust ingredient amounts based on servings 🍽️")
    st.divider()
    df = read()
    name = st.selectbox("🍴 Choose a recipe", df["name"])
    desired_servings = st.number_input("👥 Desired number of servings", min_value=1)
    st.divider()
    if st.button("✅ Apply Scaling"):
        new_ingredients = scale_ingredients(name, desired_servings)
        st.success("🎉 Ingredients scaled successfully!")
        st.write(new_ingredients)



        
if choice == "🛒 Shopping list":
    st.title("🛒 Shopping List")
    st.markdown("Pick your recipes and get a combined shopping list 📝")
    st.divider()
    df = read()
    selected_recipes = st.multiselect("🍴 Choose recipes", df["name"])
    st.divider()
    if st.button("✅ Generate List"):
        if len(selected_recipes) == 0:
            st.warning("⚠️ Please select at least one recipe.")
        else:
            st.session_state.shopping_result = shopping_list(selected_recipes)
    if "shopping_result" in st.session_state:
        st.subheader("📝 Your Shopping List")
        for item in st.session_state.shopping_result:
            st.checkbox(item.capitalize())
