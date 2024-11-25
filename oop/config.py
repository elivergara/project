import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "oopusers.csv")
RECIPES_DIR = os.path.join(BASE_DIR, "recipes")


print(f"Base directory: {BASE_DIR}, \nData File: {USER_FILE}, \nRecipes file: {RECIPES_DIR}")