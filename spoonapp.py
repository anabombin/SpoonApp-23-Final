import streamlit as st 
import requests
import pandas as pd
import numpy as np
import re

api = '2426ceb1eb174b7ba23ae522c36329be'

st.title("Find a recipe with ingredients you already have!")
ingredients = st.text_input("What's in your fridge?")

base_url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api}&addRecipeInformation=true'

while ingredients:
    url = f'{base_url}&includeIngredients={ingredients}'

    response = requests.get(url)

    if response.ok:
        results = response.json()

        if results['results']:
            # if we got results, break out of the loop and continue processing
            recipes = results['results']
            break
        else:
            # if we didn't get any results, remove the first ingredient and try again
            ingredients = ','.join(ingredients.split(',')[1:])
            print(f"No results found for ingredients: {ingredients}. Trying again without {ingredients.split(',')[0]}.")
    else:
        # handle errors
        print(f"Error fetching results: {response.status_code} {response.reason}")
        break

if not ingredients:
    print("No results found.")

# Loop over each recipe in the recipes data
for recipe in recipes:
    # Extract the recipe name, image URL, and recipe URL
    name = recipe['title']
    image_url = recipe['image']
    recipe_url = recipe['spoonacularSourceUrl']
    minutes = recipe['readyInMinutes']
    servings = recipe['servings']
    summary = recipe['summary']
    #ingredients_missing = recipe['missedIngredients']['name']

    # Display the recipe name, image, link, servings, minutes, and summary to the recipe
    st.subheader(name)
    st.image(image_url, width=725)
    

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"[Link to Recipe]({recipe_url})")

    with col2:
        st.metric("Minutes", minutes)

    with col3:
        st.metric("Servings", servings)
    
    st.write(summary)
    #st.write(ingredients_missing)
   


