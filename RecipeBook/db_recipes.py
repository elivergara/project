import sqlite3
import os
import getpass
import textwrap
from tabulate import tabulate
from pyfiglet import Figlet
from config import DB_FILE


# Initialize the database
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Create recipes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            directions TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

initialize_database()

f = Figlet(font="small")

###### User Management ######
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register(cls):
        """Creates a new user or redirects to login if username already exists"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        while True:
            username = input("Enter a username: ").lower().strip()
            # Check if username exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                print("Username already exists. Redirecting to login...")
                conn.close()
                return cls.login(existing_user=username)
            else:
                password = getpass.getpass(f"Enter a password for {username}: ").strip()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                print(f"User {username} has been registered successfully!")
                conn.close()
                return cls(username, password)

    @classmethod
    def login(cls, existing_user=None):
        """Authenticate user login"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        attempts = 0
        while attempts < 3:
            if existing_user:
                username = existing_user
            else:
                username = input("Enter your username: ").lower().strip()

            password = getpass.getpass("Enter your password: ").strip()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                print(f"Welcome, {username}!")
                conn.close()
                return cls(username, password)
            else:
                attempts += 1
                print(f"Invalid credentials. Attempts left: {3 - attempts}")

        print("Failed to login after 3 attempts.")
        conn.close()
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
        self.user_id = self.get_user_id()

    def get_user_id(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

    def load_user_recipes(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, category, name, ingredients, directions FROM recipes WHERE user_id = ?", (self.user_id,))
        recipes = [
            dict(zip(["Recipe ID", "Meal Category", "Dish Name", "Ingredients", "Cooking Directions"], row))
            for row in cursor.fetchall()
        ]
        conn.close()
        return recipes

    def add_recipe(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        category = input("Enter Meal Category: ").strip()
        name = input("Enter Dish Name: ").strip()
        ingredients = input("Enter Ingredients (comma-separated): ").strip()
        directions = input("Enter Cooking Directions: ").strip()

        cursor.execute("""
            INSERT INTO recipes (user_id, category, name, ingredients, directions)
            VALUES (?, ?, ?, ?, ?)
        """, (self.user_id, category, name, ingredients, directions))
        conn.commit()
        conn.close()
        print("Recipe added successfully!")

    def edit_recipe(self):
        recipes = self.load_user_recipes()
        self.list_recipes(recipes)

        try:
            choice = int(input("Enter the Recipe ID to edit: "))
            recipe = next((r for r in recipes if r["Recipe ID"] == choice), None)

            if recipe:
                category = input(f"Enter new Meal Category (current: {recipe['Meal Category']}): ").strip() or recipe['Meal Category']
                name = input(f"Enter new Dish Name (current: {recipe['Dish Name']}): ").strip() or recipe['Dish Name']
                ingredients = input(f"Enter new Ingredients (current: {recipe['Ingredients']}): ").strip() or recipe['Ingredients']
                directions = input(f"Enter new Cooking Directions (current: {recipe['Cooking Directions']}): ").strip() or recipe['Cooking Directions']

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE recipes
                    SET category = ?, name = ?, ingredients = ?, directions = ?
                    WHERE id = ? AND user_id = ?
                """, (category, name, ingredients, directions, choice, self.user_id))
                conn.commit()
                conn.close()
                print("Recipe updated successfully!")
            else:
                print("Invalid Recipe ID.")
        except ValueError:
            print("Invalid input.")

    def delete_recipe(self):
        recipes = self.load_user_recipes()
        self.list_recipes(recipes)

        try:
            choice = int(input("Enter the Recipe ID to delete: "))
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = ? AND user_id = ?", (choice, self.user_id))
            conn.commit()
            conn.close()
            print("Recipe deleted successfully!")
        except ValueError:
            print("Invalid input.")

    def list_recipes(self, recipes=None):
        recipes = recipes or self.load_user_recipes()
        if recipes:
            headers = ["Recipe ID", "Meal Category", "Dish Name", "Ingredients", "Cooking Directions"]
            rows = [
                [r["Recipe ID"], r["Meal Category"], r["Dish Name"],
                 "\n".join(textwrap.wrap(r["Ingredients"], 25)),
                 "\n".join(textwrap.wrap(r["Cooking Directions"], 40))]
                for r in recipes
            ]
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
                    RecipeBookApp.recipes_menu(user)
            elif choice == "2":
                user = User.login()
                if user:
                    RecipeBookApp.recipes_menu(user)
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