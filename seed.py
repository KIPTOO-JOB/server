from app import app
from models import * 
from datetime import datetime

with app.app_context():

    # Clear out existing data
    db.session.query(recipe_ingredient).delete()
    Recipe.query.delete()
    Category.query.delete()
    Ingredient.query.delete()
    Review.query.delete()
    User.query.delete()

    # Create categories
    category_1 = Category(name='Dessert', description='Sweet treats')
    category_2 = Category(name='Main Course', description='Hearty meals')

    # Create recipes with image_url
    now = datetime.utcnow() 
    recipe_1 = Recipe(
        title='Chocolate Cake',
        description='Delicious chocolate cake.',
        instructions='Mix and bake.',
        category=category_1,
        image_url='https://example.com/images/chocolate_cake.jpg',  # Image URL added
        created_at=now,
        updated_at=now
    )
    recipe_2 = Recipe(
        title='Grilled Chicken',
        description='Tasty grilled chicken.',
        instructions='Grill and serve.',
        category=category_2,
        image_url='https://example.com/images/grilled_chicken.jpg',  # Image URL added
        created_at=now,
        updated_at=now
    )

    # Create ingredients
    ingredient_1 = Ingredient(name='Chicken', type='Protein', calories=200)
    ingredient_2 = Ingredient(name='Flour', type='Grain', calories=300)
    ingredient_3 = Ingredient(name='Wheat', type='Grain', calories=300)
    ingredient_4 = Ingredient(name='Oil', type='Fat', calories=300)

    # Assign ingredients to recipes
    recipe_1.ingredients.append(ingredient_2) 
    recipe_1.ingredients.append(ingredient_3) 
    recipe_1.ingredients.append(ingredient_4)

    # Create users with current datetime for created_at and updated_at
    now = datetime.utcnow()  
    user_1 = User(
        full_name='John Doe',
        username='johndoe',
        email='john@example.com',
        password='hashedpassword',
        created_at=now,
        updated_at=now
    )
    user_2 = User(
        full_name='Jane Doe',
        username='janedoe',
        email='jane@example.com',
        password='hashedpassword',
        created_at=now,
        updated_at=now
    )

    # Create reviews
    review_1 = Review(
        recipe=recipe_1,
        user=user_1,
        rating=5,
        comment='Amazing cake!'
    )
    review_2 = Review(
        recipe=recipe_2,
        user=user_2,
        rating=4,
        comment='Great chicken!'
    )

    # Add all objects to the session and commit to the database
    db.session.add_all([
        category_1, category_2,
        recipe_1, recipe_2,
        ingredient_1, ingredient_2,
        ingredient_3, ingredient_4,
        user_1, user_2,
        review_1, review_2
    ])

    db.session.commit()

print("Database seeded successfully!")
