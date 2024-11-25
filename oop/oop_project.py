import csv
import os
import getpass
import textwrap
from tabulate import tabulate
from pyfiglet import Figlet
from pathlib import Path
from config import USER_FILE, RECIPES_DIR

if not os.path.exists(RECIPES_DIR):
    os.makedirs(RECIPES_DIR)


f = Figlet(font='small')
user_file = USER_FILE 

class User():
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def register(self):
        """Creates new username and password, and creates a recipes file for the newly registered user."""
        self.username = input("Enter a username: ").lower().strip()
        self.password = getpass.getpass(f"Enter a password for {self.username}: ").strip()
        
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["user", "password"])
                writer.writeheader()

        with open(user_file, "a") as file:
            writer = csv.DictWriter(file, fieldnames=["user", "password"])
            writer.writerow({"user": self.username, "password": self.password})


        user_recipe_file = Path(RECIPES_DIR) / f"{self.username}.csv"
        with open(user_recipe_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Meal Category", "Dish Name", "Servings", "Ingredients", "Cooking Directions"])

        print(f"User {self.username} has been registred!")

def load_users():
    """Load users from a CSV file and return a dictionary of username: password."""
    users = {}
    if os.path.exists(user_file):
        with open(user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  
                    username, password = row
                    users[username] = password
    return users

newuser = User().register()



class RecipeBook():
    def __init__(self, recipe):
        ...

class Recipe():
    def __init__(self, name: str, ingredients: list[str], steps: list[str]):
        ...

