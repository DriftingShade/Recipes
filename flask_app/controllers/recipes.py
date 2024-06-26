from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.route("/recipes/all")
def recipes():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipes = Recipe.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    return render_template("all_recipes.html", recipes=recipes, user=user)


@app.get("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("new_recipe.html", user=user)


@app.post("/recipes/create")
def create_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Recipe.form_is_valid(request.form):
        return redirect("/recipes/new")
    Recipe.create(request.form)
    return redirect("/recipes/all")


@app.get("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe = Recipe.find_by_id_with_user(recipe_id)
    user = User.find_by_id(session["user_id"])
    return render_template("recipe_details.html", user=user, recipe=recipe)


@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe = Recipe.find_by_id(recipe_id)
    user = User.find_by_id(session["user_id"])
    return render_template("edit_recipe.html", recipe=recipe, user=user)


@app.post("/recipes/update")
def update_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe_id = request.form["recipe_id"]
    if not Recipe.form_is_valid(request.form):
        return redirect(f"/recipes/{recipe_id}/edit")

    Recipe.update(request.form)
    return redirect("/recipes/all")


@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    Recipe.delete_by_id(recipe_id)
    return redirect("/recipes/all")
