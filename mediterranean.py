#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:43:39 2023

@author: wakaba
"""

import json
import difflib

# Function to read recipe data from a JSON file
def read_recipe_data(file_path):
    with open(file_path) as jsonfile:
        recipes_data = json.load(jsonfile)
    return recipes_data

# Function to find a recipe recipe by name
def find_recipe_by_name(recipes_data, target_recipe):
    for recipe in recipes_data:
        similarity = difflib.SequenceMatcher(None, recipe['name'], target_recipe).ratio()
        if similarity >= 0.6:
            return recipe
    return None

# Function to find recipes containing specific ingredients
def find_recipes_by_ingredients(recipes_data, target_ingredients):
    matching_recipes = []
    for recipe in recipes_data:
        recipe_ingredients_lower = [ingredient.lower() for ingredient in recipe['ingredients']]
        for target_ingredient in target_ingredients:
            closest_match = difflib.get_close_matches(target_ingredient.lower(), recipe_ingredients_lower, n=1)
            if closest_match and closest_match[0] in recipe_ingredients_lower:
                matching_recipes.append(recipe)
                break
    return matching_recipes

# Main function to interact with the user and execute the program
def main():
    file_path = "mediterrarean_recipes.json"  # Replace with the path to your JSON file
    recipes_data = read_recipe_data(file_path)

    print()
    print("MEDITERRANEAN RECIPE FINDER:")
    print()
    print("'1' Recipe Search")
    print("'2' Ingredients Search")
    print("'3' Recipe List (in alphabetical order)")
    print("'4' Ingredients List (in alphabetical order)")    
    print("'0' Exit")
    print()

    while True:
        user_choice = input("Enter your choice (0-4): ")

        if user_choice == '1':
            # Option 1: Get a specific recipe recipe by name.
            recipe_name = input("Enter the name of the recipe: ").lower()
            recipe = find_recipe_by_name(recipes_data, recipe_name)
            if recipe:
                print()
                print(f"Recipe for {recipe['name'].upper()}:")
                print()
                print("INGREDIENTS:")
                for ingredient, quantity in recipe['ingredients'].items():
                    print(f"- {ingredient}: {quantity}")
                print()
                print("INSTRUCTIONS:")
                instructions_list = recipe['instructions'].split('. ')
                if instructions_list[-1].endswith('.'):
                    instructions_list[-1] = instructions_list[-1][:-1]
                for idx, sentence in enumerate(instructions_list, 1):
                    print(f"- {sentence.strip()}")
                print()
                break
            else:
                print("Recipe not found.")
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() != 'y':
                    break

        elif user_choice == '2':
            # Option 2: Find recipes containing specific ingredients
            ingredients_list = input("Enter recipe ingredients (comma-separated): ")
            target_ingredients = [ingredient.strip() for ingredient in ingredients_list.split(',')]
            matching_recipes = find_recipes_by_ingredients(recipes_data, target_ingredients)
            if matching_recipes:
                print()
                print("Recipes that contain the specified ingredients:")
                print()
                for idx, recipe in enumerate(matching_recipes, 1):
                    print(f"{idx}. {recipe['name']}")
                print()
                while True:
                    choice = input("Enter the number(s) associated with the recipe of interest (or 'b' to go back): ")
                    if choice.lower() == 'b':
                        break
                    elif choice.isdigit():
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(matching_recipes):
                            chosen_recipe = matching_recipes[choice_idx]
                            print()
                            print(f"Recipe for {chosen_recipe['name'].upper()}:")
                            print()
                            print("INGREDIENTS:")
                            for ingredient, quantity in chosen_recipe['ingredients'].items():
                                print(f"- {ingredient}: {quantity}")
                            print()
                            print("INSTRUCTIONS:")
                            instructions_list = chosen_recipe['instructions'].split('. ')
                            if instructions_list[-1].endswith('.'):
                                instructions_list[-1] = instructions_list[-1][:-1]
                            for idx, sentence in enumerate(instructions_list, 1):
                                print(f"- {sentence.strip()}")
                            print()
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("No recipes found with the specified ingredients.")
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() != 'y':
                    break

        elif user_choice == '3':
            # Option 3: List all recipes in alphabetical order
            print()
            display_alphabetical_order(recipes_data)
            print()
            while True:
                recipe_name = input("Enter the name of the recipe: ").lower()
                recipe = find_recipe_by_name(recipes_data, recipe_name)
                if recipe:
                    print()
                    print(f"Recipe for {recipe['name'].upper()}:")
                    print()
                    print("INGREDIENTS:")
                    for ingredient, quantity in recipe['ingredients'].items():
                        print(f"- {ingredient}: {quantity}")
                    print()
                    print("INSTRUCTIONS:")
                    instructions_list = recipe['instructions'].split('. ')
                    if instructions_list[-1].endswith('.'):
                        instructions_list[-1] = instructions_list[-1][:-1]
                    for idx, sentence in enumerate(instructions_list, 1):
                        print(f"- {sentence.strip()}")
                    print()
                    break
                else:
                    print("Recipe not found.")
                    try_again = input("Would you like to try again? (y/n): ")
                    if try_again.lower() != 'y':
                        break

        elif user_choice == '4':
            # Option 4: List all possible recipe ingredients in alphabetical order
            print()
            print("Recipe Ingredients in Alphabetical Order:")
            print()
            all_ingredients = set()
            for recipe in recipes_data:
                all_ingredients.update(recipe['ingredients'].keys())
            sorted_ingredients = sorted(all_ingredients)
            for idx, ingredient in enumerate(sorted_ingredients, 1):
                print(f"{idx}. {ingredient}")
            print()
            selected_ingredients = input("Enter the number(s) associated with the ingredient(s) of interest (comma-separated): ")
            selected_numbers = [int(num.strip()) for num in selected_ingredients.split(',')]
            selected_ingredients = [sorted_ingredients[num - 1] for num in selected_numbers if 1 <= num <= len(sorted_ingredients)]
            if not selected_ingredients:
                print("Invalid input. Please try again.")
            else:
                # Print the selected ingredients
                print()
                print("Recipes that contain:")
                print()
                for ingredient in selected_ingredients:
                    print(f"- {ingredient}")
                print()
                matching_recipes = find_recipes_by_ingredients(recipes_data, selected_ingredients)
                if matching_recipes:
                    print("are:")
                    print()
                    for idx, recipe in enumerate(matching_recipes, 1):
                        print(f"{idx}. {recipe['name']}")
                    print()

                    # Prompt for either a recipe number or exit
                    while True:
                        choice = input("Enter the recipe number whose recipe you wish to see (or type 'e' to exit): ")
                        if choice.lower() == 'e':
                            break
                        elif choice.isdigit():
                            choice_idx = int(choice) - 1
                            if 0 <= choice_idx < len(matching_recipes):
                                chosen_recipe = matching_recipes[choice_idx]
                                print()
                                print(f"Recipe for {chosen_recipe['name'].upper()}:")
                                print()
                                print("INGREDIENTS:")
                                for ingredient, quantity in chosen_recipe['ingredients'].items():
                                    print(f"- {ingredient}: {quantity}")
                                print()
                                print("INSTRUCTIONS:")
                                instructions_list = chosen_recipe['instructions'].split('. ')
                                if instructions_list[-1].endswith('.'):
                                    instructions_list[-1] = instructions_list[-1][:-1]
                                for idx, sentence in enumerate(instructions_list, 1):
                                    print(f"- {sentence.strip()}")
                                print()
                                break
                            else:
                                print("Invalid choice. Please try again.")
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("No recipes found with the selected ingredients.")
                    try_again = input("Would you like to try again? (y/n): ")
                    if try_again.lower() != 'y':
                        break
            break

        elif user_choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Function to display recipe names in alphabetical order
def display_alphabetical_order(recipes_data):
    recipe_names = [recipe['name'] for recipe in recipes_data]
    sorted_recipes = sorted(recipes_data, key=lambda x: x['name'])  # Sort the recipes by name
    for idx, recipe in enumerate(sorted_recipes, 1):
        print(f"{idx}. {recipe['name']}")


if __name__ == "__main__":
    main()

