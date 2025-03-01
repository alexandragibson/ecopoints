import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_project.settings')
django.setup()

from ecopoints.models import Category, Task, CompletedTask
from django.contrib.auth.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_json = os.path.join(BASE_DIR, "populate/users.json")
category_json = os.path.join(BASE_DIR, "populate/category.json")
task_json = os.path.join(BASE_DIR, "populate/task.json")

if not User.objects.exists():
    with open(user_json, "r") as file:
        users = json.load(file)

    for user_data in users:
        username = user_data["username"]
        email = user_data["email"]
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password="password123"
            )
            print(f"Created user: {username}")
else:
    print("Skipping user population - Users already exist")


# 2. Categories population
if not Category.objects.exists():
    with open(category_json, "r") as file:
        categories = json.load(file)

    for category_data in categories:
        name = category_data["name"]

        if not Category.objects.filter(name=name).exists():
            Category.objects.create(name=name)
            print(f"Created category: {name}")
else:
    print("Skipping category population - Categories already exist")


# 3. Tasks population
if not Task.objects.exists():
    with open(task_json, "r") as file:
        task_data = json.load(file)

    tasks = task_data["tasks"]

    for task in tasks:
        name = task["name"]
        description = task["description"]
        score = task["score"]

        category_name = task["category"]
        try:
            category = Category.objects.get(name=category_name)

            if not Task.objects.filter(name=name).exists():
                Task.objects.create(name=name, description=description, score=score, category=category)
                print(f"Created task: {name}")
        except Category.DoesNotExist:
            print(f"Category '{category_name}' not found for task '{name}'. Make sure categories are populated first.")
else:
    print("Skipping task population - Tasks already exist")
