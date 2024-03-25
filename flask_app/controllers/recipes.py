from flask_app import app
from flask import flash, render_template, redirect, request, session
from flask_app.models.recipe import Recipe


@app.get("/recipes/create")
def recipe_create():
    return render_template("create_recipe.html")
