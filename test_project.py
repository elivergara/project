from project import load_users, add_recipe, delete_recipe, load_user_recipes

def test_load_users():
    """Test if load_users correctly loads user data."""
    users = load_users()
    assert "elivergara" in users, "User 'elivergara' not loaded from file"
    assert users["elivergara"] == "password123"

def test_add_recipe():
    """Test if add_recipe correctly adds a recipe."""
    username = "elivergara"
    recipes = []
    
    new_recipe = {
        "Meal Category": "Lunch",
        "Dish Name": "Sandwich",
        "Ingredients": "Bread, Cheese",
        "Cooking Directions": "Assemble ingredients"
    }


    add_recipe(username, recipes, recipe=new_recipe)
    
    updated_recipes = load_user_recipes(username)
    assert updated_recipes[-1] == new_recipe

def test_delete_recipe():
    """Test if delete_recipe correctly removes a recipe."""
    username = "elivergara"
    recipes = []

    recipe_to_add_and_delete = {
        "Meal Category": "Dinner",
        "Dish Name": "Pasta",
        "Ingredients": "Pasta, Sauce",
        "Cooking Directions": "Boil pasta, add sauce"
    }
    add_recipe(username, recipes, recipe=recipe_to_add_and_delete)
    
    updated_recipes = load_user_recipes(username)
    initial_count = len(updated_recipes)
    assert updated_recipes[-1] == recipe_to_add_and_delete
    
    delete_recipe(username, recipes, recipe_index=len(recipes) - 1)
    
    updated_recipes = load_user_recipes(username)
    assert len(updated_recipes) == initial_count - 1
    assert recipe_to_add_and_delete not in updated_recipes