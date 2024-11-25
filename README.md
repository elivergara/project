
# Digital Recipe Book

#### Video Demo: <https://youtu.be/mppi3EwoVFc?si=q0S8czQY-w_ydXLF>

#### Description
The **Digital Recipe Book** is a command-line Python program developed as the final project for the CS50P course. This project aims to create a personalized digital repository where users can save, edit, and manage recipes. Designed for simplicity and user-friendliness, it applies basic to intermediate programming concepts in Python, such as file handling, user authentication, and text-based interfaces. Although initially designed for cooking recipes, this project can be adapted for any instructions or notes that users might want to save and organize.

## Project Overview

**Course:** CS50P: Introduction to Programming with Python - Harvard University.<br>
**Author:** Eli Vergara (GitHub: [elivergara](https://github.com/elivergara)).<br>
**Date:** October 30, 2024<br>


### Features and Components

1. **User Authentication**:
   - **Description**: The `main_menu` and `create_user` functions implement a login and registration system, ensuring each user has a separate file for storing recipes. This promotes data integrity by limiting access to individual recipe books.
   - **Design Choice**: Chose a simple text-based login system with password handling using `getpass` to keep passwords secure during entry. Usernames and passwords are stored in `users.csv`, making it easy to look up and verify credentials.

2. **Recipe Management**:
   - **Core Functionality**: The program offers four main recipe actions (Add, Edit, Delete, View), implemented in the functions `add_recipe`, `edit_recipe`, `delete_recipe`, and `print_recipes`.
   - **Files Created**: Each user’s recipes are stored in a CSV file named after their username, allowing for user-specific recipe management. This structure also makes it easier to load, display, and edit recipe data.
   - **Design Consideration**: Instead of storing all recipes in one file, each user has an individual CSV, simplifying recipe organization and making it easier to handle potential expansion to a database in future versions.

3. **Logout System**:
   - **Description**: Users can safely exit their session with the `Logout` option, which clears the session data and returns the user to the main login menu. This helps maintain a clean workflow, especially if multiple users access the program on the same device.

### File Descriptions

- **project.py**
  - The main script containing all the functionality for the Digital Recipe Book. This file includes functions for user management, recipe operations, and file handling, making it the core of the application.

- **users.csv**
  - A CSV file storing registered users’ login credentials. Each entry consists of a `user` and `password`, separated by commas. It’s managed using Python’s `csv` module and helps authenticate users while respecting basic data privacy.

- **User-specific recipe files** (e.g., `username.csv`)
  - Each registered user has a unique CSV file named after their username. This file contains the user's recipes, with fields like "Meal Category," "Dish Name," "Ingredients," and "Cooking Directions." Using CSV files simplifies adding, editing, and deleting recipes while allowing easy viewing and formatting with the `tabulate` library.

### Program Flow and Execution

1. **Installation Requirements**:
   - Python 3.12+
   - Libraries: `csv`, `os`, `textwrap`, `tabulate`, `pyfiglet`

   To install the required libraries, run:
   ```bash
   pip install tabulate pyfiglet
   ```

2. **How to Run**:
   - Clone the repository:
     ```bash
     git clone https://github.com/elivergara/project.git
     ```
   - Navigate to the project directory:
     ```bash
     cd project
     ```
   - Run the main program file:
     ```bash
     python project.py
     ```

### Usage Instructions

Upon launching, the program welcomes users to the **Digital Recipe Book**. Users must first log in or register. After logging in, they can:

1. **Add Recipes**: Fill in meal category, dish name, ingredients, and cooking directions. This information is stored and can be displayed in a tabular format using `tabulate`.
2. **Edit Recipes**: View a list of recipes, select one, and update its details. Only specified fields are modified, and all changes are saved automatically.
3. **Delete Recipes**: Permanently removes a recipe from the user’s recipe book, allowing for easy organization.
4. **View Recipes**: Lists recipes in a formatted table, with wrapped text for readability.

### Design Choices

- **CSV File Handling**: CSV files were chosen for simplicity and ease of manipulation. Using a unique CSV per user offers a clear separation of data and reduces complexity in managing multiple users.
- **Command-line Interface**: The CLI format was intentional for this course project, allowing focus on Python fundamentals without the added complexity of a graphical interface.
- **Libraries**:
   - `getpass`: Secures password entry by hiding typed characters.
   - `tabulate`: Provides a clean, tabular display for recipes, improving the user experience.
   - `pyfiglet`: Adds ASCII art to the UI, making the interface more welcoming and visually appealing.

### Future Enhancements

The next step is to introduce a **Graphical User Interface (GUI)** using **Tkinter**, making the program more accessible to users unfamiliar with the command line. With a GUI, the recipe book could also incorporate search, filter, and sorting functionalities, enhancing the user experience.

### Motivation and Acknowledgments

This project was inspired by my wife’s request for a digital recipe book to organize her recipes. I utilized concepts learned from CS50P, including file handling, user authentication, and CLI design. This project has been a rewarding way to consolidate my programming knowledge, and I hope users find the **Digital Recipe Book** helpful in managing their culinary creations.

### Contact

For questions or feedback, feel free to reach out via GitHub: [elivergara](https://github.com/elivergara).

Thank you for exploring the **Digital Recipe Book**!
