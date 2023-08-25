#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:43:39 2023

@author: wakaba
"""

import json
import difflib

# Function to read cocktail data from a JSON file
def read_cocktail_data(file_path):
    with open(file_path) as jsonfile:
        cocktails_data = json.load(jsonfile)
    return cocktails_data

# Function to find a cocktail recipe by name
def find_cocktail_by_name(cocktails_data, target_cocktail):
    for cocktail in cocktails_data:
        similarity = difflib.SequenceMatcher(None, cocktail['name'], target_cocktail).ratio()
        if similarity >= 0.7:
            return cocktail
    return None

# Function to find cocktails containing specific ingredients
def find_cocktails_by_ingredients(cocktails_data, target_ingredients):
    matching_cocktails = []
    for cocktail in cocktails_data:
        cocktail_ingredients_lower = [ingredient.lower() for ingredient in cocktail['ingredients']]
        for target_ingredient in target_ingredients:
            closest_match = difflib.get_close_matches(target_ingredient.lower(), cocktail_ingredients_lower, n=1)
            if closest_match and closest_match[0] in cocktail_ingredients_lower:
                matching_cocktails.append(cocktail)
                break
    return matching_cocktails

# Main function to interact with the user and execute the program
def main():
    file_path = "cocktails.json"  # Replace with the path to your JSON file
    cocktails_data = read_cocktail_data(file_path)

    print()
    print("Welcome to the Cocktail Recipe Finder!")
    print("Please choose an option from the menu below:")
    print()
    print("'1' Cocktail Search")
    print("'2' Ingredients Search")
    print("'3' Cocktail List (in alphabetical order)")
    print("'4' Ingredients List (in alphabetical order)")    
    print("'0' Exit")
    print()

    while True:
        user_choice = input("Enter your choice (0-4): ")

        if user_choice == '1':
            # Option 1: Get a specific cocktail recipe by name.
            cocktail_name = input("Enter the name of the cocktail: ").lower()
            cocktail = find_cocktail_by_name(cocktails_data, cocktail_name)
            if cocktail:
                print()
                print(f"Recipe for {cocktail['name'].upper()}:")
                print()
                print("INGREDIENTS:")
                for ingredient, quantity in cocktail['ingredients'].items():
                    print(f"- {ingredient}: {quantity}")
                print()
                print("INSTRUCTIONS:")
                instructions_list = cocktail['instructions'].split('. ')
                if instructions_list[-1].endswith('.'):
                    instructions_list[-1] = instructions_list[-1][:-1]
                for idx, sentence in enumerate(instructions_list, 1):
                    print(f"- {sentence.strip()}")
                print()
                break
            else:
                print("Cocktail not found.")
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() != 'y':
                    break

        elif user_choice == '2':
            # Option 2: Find cocktails containing specific ingredients
            ingredients_list = input("Enter cocktail ingredients (comma-separated): ")
            target_ingredients = [ingredient.strip() for ingredient in ingredients_list.split(',')]
            matching_cocktails = find_cocktails_by_ingredients(cocktails_data, target_ingredients)
            if matching_cocktails:
                print()
                print("Cocktails that contain the specified ingredients:")
                print()
                for idx, cocktail in enumerate(matching_cocktails, 1):
                    print(f"{idx}. {cocktail['name']}")
                print()
                while True:
                    choice = input("Enter the number(s) associated with the Cocktail of interest (or 'b' to go back): ")
                    if choice.lower() == 'b':
                        break
                    elif choice.isdigit():
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(matching_cocktails):
                            chosen_cocktail = matching_cocktails[choice_idx]
                            print()
                            print(f"Recipe for {chosen_cocktail['name'].upper()}:")
                            print()
                            print("INGREDIENTS:")
                            for ingredient, quantity in chosen_cocktail['ingredients'].items():
                                print(f"- {ingredient}: {quantity}")
                            print()
                            print("INSTRUCTIONS:")
                            instructions_list = chosen_cocktail['instructions'].split('. ')
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
                print("No cocktails found with the specified ingredients.")
                try_again = input("Would you like to try again? (y/n): ")
                if try_again.lower() != 'y':
                    break

        elif user_choice == '3':
            # Option 3: List all cocktails in alphabetical order
            print()
            display_alphabetical_order(cocktails_data)
            print()
            while True:
                cocktail_name = input("Enter the name of the cocktail: ").lower()
                cocktail = find_cocktail_by_name(cocktails_data, cocktail_name)
                if cocktail:
                    print()
                    print(f"Recipe for {cocktail['name'].upper()}:")
                    print()
                    print("INGREDIENTS:")
                    for ingredient, quantity in cocktail['ingredients'].items():
                        print(f"- {ingredient}: {quantity}")
                    print()
                    print("INSTRUCTIONS:")
                    instructions_list = cocktail['instructions'].split('. ')
                    if instructions_list[-1].endswith('.'):
                        instructions_list[-1] = instructions_list[-1][:-1]
                    for idx, sentence in enumerate(instructions_list, 1):
                        print(f"- {sentence.strip()}")
                    print()
                    break
                else:
                    print("Cocktail not found.")
                    try_again = input("Would you like to try again? (y/n): ")
                    if try_again.lower() != 'y':
                        break

        elif user_choice == '4':
            # Option 4: List all possible cocktail ingredients in alphabetical order
            print()
            print("Cocktail Ingredients in Alphabetical Order:")
            print()
            all_ingredients = set()
            for cocktail in cocktails_data:
                all_ingredients.update(cocktail['ingredients'].keys())
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
                print("Cocktails that contain:")
                print()
                for ingredient in selected_ingredients:
                    print(f"- {ingredient}")
                print()
                matching_cocktails = find_cocktails_by_ingredients(cocktails_data, selected_ingredients)
                if matching_cocktails:
                    print("are:")
                    print()
                    for idx, cocktail in enumerate(matching_cocktails, 1):
                        print(f"{idx}. {cocktail['name']}")
                    print()

                    # Prompt for either a cocktail number or exit
                    while True:
                        choice = input("Enter the cocktail number whose recipe you wish to see (or type 'e' to exit): ")
                        if choice.lower() == 'e':
                            break
                        elif choice.isdigit():
                            choice_idx = int(choice) - 1
                            if 0 <= choice_idx < len(matching_cocktails):
                                chosen_cocktail = matching_cocktails[choice_idx]
                                print()
                                print(f"Recipe for {chosen_cocktail['name'].upper()}:")
                                print()
                                print("INGREDIENTS:")
                                for ingredient, quantity in chosen_cocktail['ingredients'].items():
                                    print(f"- {ingredient}: {quantity}")
                                print()
                                print("INSTRUCTIONS:")
                                instructions_list = chosen_cocktail['instructions'].split('. ')
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
                    print("No cocktails found with the selected ingredients.")
                    try_again = input("Would you like to try again? (y/n): ")
                    if try_again.lower() != 'y':
                        break
            break

        elif user_choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Function to display cocktail names in alphabetical order
def display_alphabetical_order(cocktails_data):
    cocktail_names = [cocktail['name'] for cocktail in cocktails_data]
    sorted_cocktails = sorted(cocktails_data, key=lambda x: x['name'])  # Sort the cocktails by name
    for idx, cocktail in enumerate(sorted_cocktails, 1):
        print(f"{idx}. {cocktail['name']}")


if __name__ == "__main__":
    main()
