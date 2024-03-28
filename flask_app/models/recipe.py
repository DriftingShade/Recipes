from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Recipe:
    DB = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_thirty = data["under_thirty"]
        self.create_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        # Text Validator
        if len(form_data["name"]) == 0:
            flash("Please enter name.")
            is_valid = False
        elif len(form_data["description"]) < 3:
            flash("Description must be at least three characters.")
            is_valid = False
        elif len(form_data["instructions"]) < 3:
            flash("Instructions must be at least three characters.")
            is_valid = False

        # Data Validator
        if len(form_data["date_made"]) == 0:
            flash("Please enter date made.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["date_made"], "%Y-%m-%d")
            except:
                flash("Invalid date made.")
                is_valid = False

        # Radio Button Validator
        if "under_thirty" not in form_data:
            flash("Please choose Yes or No for under 30 minutes.")
            is_valid = False
        elif form_data["under_thirty"] not in ["0", "1"]:
            flash("Please choose Yes or No for under 30 minutes.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"""
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            recipes.append(recipe)
        return recipes

    @classmethod
    def find_all_with_users(cls):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"""

        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            user_data = {
                "id": each_dict["id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["created_at"],
                "updated_at": each_dict["updated_at"],
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)
        return recipes

    @classmethod
    def find_by_id(cls, recipe_id):
        query = """SELECT * FROM recipes WHERE id = %(recipe_id)s"""
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        recipe = Recipe(list_of_dicts[0])
        return recipe

    @classmethod
    def find_by_id_with_user(cls, recipe_id):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id 
        WHERE recipes.id = %(recipe_id)s"""

        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        recipe = Recipe(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        recipe.user = User(user_data)
        return recipe

    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO recipes
        (name, description, instructions, date_made, under_thirty, user_id)
        VALUES
        (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s, 
        %(user_id)s)"""
        recipe_id = connectToMySQL(Recipe.DB).query_db(query, form_data)
        return recipe_id

    @classmethod
    def update(cls, form_data):
        query = """UPDATE recipes
        SET
        name=%(name)s,
        description=%(description)s,
        instructions=%(instructions)s,
        date_made=%(date_made)s,
        under_thirty=%(under_thirty)s
        WHERE id = %(recipe_id)s;"""
        connectToMySQL(Recipe.DB).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, recipe_id):
        query = """DELETE FROM recipes WHERE id = %(recipe_id)s;"""
        data = {"recipe_id": recipe_id}
        connectToMySQL(Recipe.DB).query_db(query, data)
        return
