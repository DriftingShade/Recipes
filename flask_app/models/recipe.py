from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Recipe:
    DB = "recipes_db"

    def __init__(self, data):

        self.id = data["id"]
        self.name = data["name"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_thirty = data["under_thirty"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def create_recipe(cls, data):
        query = """INSERT INTO heroes (name, instructions, date_made, under_thirty, created_at,
        updated_at, user_id) VALUES (%(name)s, %(instructions)s, %(date_made)s, %(under_thirty)s, NOW(),
        NOW(), %(user_id)s)"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results
