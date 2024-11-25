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

f = Figlet(font="small")

###### User Management ######
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register(cls):
        """Creates a new user or redirects to login if username already exists"""
        users_data = cls.load_users()

        while True:
            username = input("Enter a username: ").lower().strip()

            if username in users_data:
                print("Username already exists. Redirecting to login...")
                # Redirect to the login process for the existing username
                user = cls.login(existing_user=username)
                if user:
                    # If login is successful, return the user to proceed directly to the recipes
                    return user
            else:
                # If username doesn't exist, proceed to register
                password = getpass.getpass(f"Enter a password for {username}: ").strip()

                if not os.path.exists(USER_FILE):
                    with open(USER_FILE, mode="w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=["user", "password"])
                        writer.writeheader()

                with open(USER_FILE, "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["user", "password"])
                    writer.writerow({"user": username, "password": password})

                print(f"User {username} has been registered successfully!")
                return cls(username, password)

    @staticmethod
    def load_users():
        """Load all users from CSV"""
        users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    users[row["user"]] = row["password"]
        return users

    @classmethod
    def login(cls, existing_user=None):
        """Authenticate user login"""
        users_data = cls.load_users()
        attempts = 0
        while attempts < 3:
            if existing_user:
                username = existing_user
            else:
                username = input("Enter your username: ").lower().strip()

            password = getpass.getpass("Enter your password: ").strip()

            if username in users_data and users_data[username] == password:
                print(f"Welcome, {username}!")
                return cls(username, password)
            else:
                attempts += 1
                print(f"Invalid credentials. Attempts left: {3 - attempts}")

        print("Failed to login after 3 attempts.")
        return None


##### Recipe ######
class Recipe:
    def __init__(self, category, name, ingredients, directions):
        self.category = category
        self.name = name
        self.ingredients = ingredients
        self.directions = directions

    def to_dict(self):
        return {
            "Meal Category": self.category,
            "Dish Name": self.name,
            "Ingredients": self.ingredients,
            "Cooking Directions": self.directions,
        }

###### Recipe Book ######
class RecipeBook:
    def __init__(self, username):
        self.username = username
        self.recipes = self.load_user_recipes()

    def load_user_recipes(self):
        filename = Path(RECIPES_DIR) / f"{self.username}.csv"
        recipes = []
        if filename.exists():
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    recipes.append(row)
        return recipes

    def save_user_recipes(self):
        filename = Path(RECIPES_DIR) / f"{self.username}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Meal Category", "Dish Name", "Ingredients", "Cooking Directions"])
            writer.writeheader()
            writer.writerows(self.recipes)

    def add_recipe(self):
        category = input("Enter Meal Category: ").strip()
        name = input("Enter Dish Name: ").strip()
        ingredients = input("Enter Ingredients (comma-separated): ").strip()
        directions = input("Enter Cooking Directions: ").strip()

        recipe = Recipe(category, name, ingredients, directions)
        self.recipes.append(recipe.to_dict())
        self.save_user_recipes()
        print("Recipe added successfully!")

    def edit_recipe(self):
        self.list_recipes()
        try:
            choice = int(input("Enter the number of the recipe to edit: ")) - 1
            if 0 <= choice < len(self.recipes):
                recipe = self.recipes[choice]
                recipe["Meal Category"] = input(f"Enter new Meal Category (current: {recipe['Meal Category']}): ").strip() or recipe["Meal Category"]
                recipe["Dish Name"] = input(f"Enter new Dish Name (current: {recipe['Dish Name']}): ").strip() or recipe["Dish Name"]
                recipe["Ingredients"] = input(f"Enter new Ingredients (current: {recipe['Ingredients']}): ").strip() or recipe["Ingredients"]
                recipe["Cooking Directions"] = input(f"Enter new Cooking Directions (current: {recipe['Cooking Directions']}): ").strip() or recipe["Cooking Directions"]
                self.save_user_recipes()
                print("Recipe updated successfully!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

    def delete_recipe(self):
        self.list_recipes()
        try:
            choice = int(input("Enter the number of the recipe to delete: ")) - 1
            if 0 <= choice < len(self.recipes):
                del self.recipes[choice]
                self.save_user_recipes()
                print("Recipe deleted successfully!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

    def list_recipes(self):
        if self.recipes:
            headers = ["No.", "Meal Category", "Dish Name", "Ingredients", "Cooking Directions"]
            rows = []
            for idx, recipe in enumerate(self.recipes, start=1):
                wrapped_ingredients = "\n".join(textwrap.wrap(recipe.get("Ingredients", ""), width=25))
                wrapped_directions = "\n".join(textwrap.wrap(recipe.get("Cooking Directions", ""), width=40))
                rows.append([idx, recipe.get("Meal Category", ""), recipe.get("Dish Name", ""), wrapped_ingredients, wrapped_directions])
            print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))
        else:
            print("No recipes found.")

###### Recipe Book App (flow) ######
class RecipeBookApp:
    @staticmethod
    def main_menu():
        print(f.renderText("Welcome to your digital Recipe Book"))
        while True:
            choice = input("1 to Register, 2 to Login, 3 to Exit: ").strip()
            if choice == "1":
                user = User.register()
                if user:
                    RecipeBookApp.recipes_menu(user)  # Proceed directly to recipes after registration or successful login
            elif choice == "2":
                user = User.login()
                if user:
                    RecipeBookApp.recipes_menu(user)  # Proceed directly to recipes after successful login
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

    @staticmethod
    def recipes_menu(user):
        recipe_book = RecipeBook(user.username)
        while True:
            choice = input("\n1 - Add Recipe, 2 - Edit Recipe, 3 - Delete Recipe, 4 - View Recipes, 5 - Logout: ").strip()
            if choice == "1":
                recipe_book.add_recipe()
            elif choice == "2":
                recipe_book.edit_recipe()
            elif choice == "3":
                recipe_book.delete_recipe()
            elif choice == "4":
                recipe_book.list_recipes()
            elif choice == "5":
                print("Logging out...")
                exit_choice = input("Do you want to exit the program? (y/n): ").strip().lower()
                if exit_choice == "y":
                    print("Goodbye!")
                    exit()  # Exit the program entirely
                elif exit_choice == "n":
                    print("Returning to your recipes menu...")
                    continue  # Stay in the recipes menu
                else:
                    print("Invalid input, returning to your recipes menu...")
            else:
                print("Invalid option.")

# Entry point
if __name__ == "__main__":
    RecipeBookApp.main_menu()
