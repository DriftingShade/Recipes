from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Recipe:
    DB = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.column1 = data["column1"]
        self.column2 = data["column2"]
        self.column3 = data["column3"]
        self.column4 = data["column4"]
        self.column5 = data["column5"]
        self.create_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        # Text Validator
        if len(form_data["column"]) == 0:
            flash("Please enter column.")
            is_valid = False
        elif len(form_data["column"]) < 3:
            flash("Column must be at least three characters.")
            is_valid = False

        # Data Validator
        if len(form_data["date_column"]) == 0:
            flash("Please enter date_column.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["date_column"], "%Y-%m-%d")
            except:
                flash("Invalid date_column.")
                is_valid = False

        # Radio Button Validator
        if "radio_column" not in form_data:
            flash("Please enter radio_column.")
            is_valid = False
        elif form_data["radio_column"] not in ["choice1", "choice2"]:
            flash("radio_column must be at least three characters.")
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
                "id": each_dict["recipes.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["recipes.created_at"],
                "updated_at": each_dict["recipes.updated_at"],
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
        (column1, column2, column3, column4, column5, user_id)
        VALUES
        (%(column1)s, %(column2)s, %(column3)s, %(column4)s, %(column5)s, 
        %(user_id)s,)"""
        recipe_id = connectToMySQL(Recipe.DB).query_db(query, form_data)
        return recipe_id

    @classmethod
    def update(cls, form_data):
        query = """UPDATE recipes
        SET
        column1=%(column1)s,
        column2=%(column2)s,
        column3=%(column3)s,
        column4=%(column4)s,
        column5=%(column5)s,
        WHERE id = %(recipe_id)s;"""
        connectToMySQL(Recipe.DB).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, recipe_id):
        query = """DELETE FROM recipes WHERE id = %(recipe_id)s;"""
        data = {"recipe_id": recipe_id}
        connectToMySQL(Recipe.DB).query_db(query, data)
        return
