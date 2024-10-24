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
    category_1 = Category(name='Dessert', description='Sweet and decadent treats')
    category_2 = Category(name='Main Course', description='Hearty and filling meals')
    category_3 = Category(name='Appetizer', description='Small dishes to start the meal')
    category_4 = Category(name='Vegan', description='Plant-based dishes')

    # Create recipes with more diverse content
    now = datetime.utcnow() 
    recipe_1 = Recipe(
        title='Chocolate Lava Cake',
        description='Rich chocolate cake with a gooey molten center.',
        instructions='Bake at high heat for 12 minutes, ensuring the center stays soft.',
        category=category_1,
        image_url='https://images.unsplash.com/photo-1652561781059-58d5d9ffcb4d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGF2YSUyMGNha2V8ZW58MHx8MHx8fDA%3D',
        created_at=now,
        updated_at=now
    )
    recipe_2 = Recipe(
        title='Lemon Herb Grilled Salmon',
        description='Perfectly grilled salmon with a refreshing lemon herb seasoning.',
        instructions='Marinate in lemon and herbs, then grill for 10 minutes.',
        category=category_2,
        image_url='https://images.unsplash.com/photo-1712334562767-5d366d0c40d9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fHNhbG1vbnxlbnwwfHwwfHx8MA%3D%3D',
        created_at=now,
        updated_at=now
    )
    recipe_3 = Recipe(
        title='Stuffed Mushrooms',
        description='Juicy mushrooms filled with garlic, cheese, and breadcrumbs.',
        instructions='Bake stuffed mushrooms until golden brown.',
        category=category_3,
        image_url='https://images.unsplash.com/photo-1622268805718-ca073548d4ad?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c3R1ZmZlZCUyMG11c2hyb29tc3xlbnwwfHwwfHx8MA%3D%3D',
        created_at=now,
        updated_at=now
    )
    recipe_4 = Recipe(
        title='Vegan Quinoa Salad',
        description='Healthy quinoa with fresh veggies and a light lemon dressing.',
        instructions='Cook quinoa, toss with veggies and dressing.',
        category=category_4,
        image_url='https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cXVpbm9hJTIwc2FsYWR8ZW58MHx8MHx8fDA%3D',
        created_at=now,
        updated_at=now
    )
    recipe_5 = Recipe(
        title='Classic Tiramisu',
        description='A traditional Italian dessert layered with coffee-soaked ladyfingers and mascarpone cream.',
        instructions='Layer ladyfingers with coffee and mascarpone. Chill before serving.',
        category=category_1,
        image_url='https://images.unsplash.com/photo-1710518025175-a3ea35d44e3e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHRpcmFtaXN1fGVufDB8fDB8fHww',
        created_at=now,
        updated_at=now
    )

    # Create ingredients
    ingredient_1 = Ingredient(name='Salmon', type='Protein', calories=200)
    ingredient_2 = Ingredient(name='Chocolate', type='Sweetener', calories=400)
    ingredient_3 = Ingredient(name='Quinoa', type='Grain', calories=220)
    ingredient_4 = Ingredient(name='Mushrooms', type='Vegetable', calories=30)
    ingredient_5 = Ingredient(name='Lemon', type='Fruit', calories=20)
    ingredient_6 = Ingredient(name='Cheese', type='Dairy', calories=100)

    # Assign ingredients to recipes
    recipe_1.ingredients.append(ingredient_2)  # Chocolate Lava Cake
    recipe_2.ingredients.append(ingredient_1)  # Salmon for Lemon Herb Salmon
    recipe_3.ingredients.append(ingredient_4)  # Mushrooms for Stuffed Mushrooms
    recipe_4.ingredients.append(ingredient_3)  # Quinoa for Vegan Salad
    recipe_5.ingredients.append(ingredient_2)  # Chocolate for Tiramisu

    # Create users with richer information
    user_1 = User(
        full_name='Alice Wonderland',
        username='alice123',
        email='alice@example.com',
        password='hashedpassword1',
        created_at=now,
        updated_at=now
    )
    user_2 = User(
        full_name='Bob Builder',
        username='bobthebuilder',
        email='bob@example.com',
        password='hashedpassword2',
        created_at=now,
        updated_at=now
    )
    user_3 = User(
        full_name='Charlie Chaplin',
        username='charlie',
        email='charlie@example.com',
        password='hashedpassword3',
        created_at=now,
        updated_at=now
    )

    # Create reviews with more detailed comments
    review_1 = Review(
        recipe=recipe_1,
        user=user_1,
        rating=5,
        comment='This lava cake was divine! The center was perfectly gooey.'
    )
    review_2 = Review(
        recipe=recipe_2,
        user=user_2,
        rating=4,
        comment='The salmon was very fresh, but I would have liked more seasoning.'
    )
    review_3 = Review(
        recipe=recipe_3,
        user=user_3,
        rating=5,
        comment='These stuffed mushrooms were a hit at my dinner party!'
    )
    review_4 = Review(
        recipe=recipe_4,
        user=user_1,
        rating=4,
        comment='A great vegan option, light and healthy.'
    )
    review_5 = Review(
        recipe=recipe_5,
        user=user_2,
        rating=5,
        comment='Best tiramisu I\'ve had outside of Italy!'
    )

    # Add all objects to the session and commit to the database
    db.session.add_all([
        category_1, category_2, category_3, category_4,
        recipe_1, recipe_2, recipe_3, recipe_4, recipe_5,
        ingredient_1, ingredient_2, ingredient_3, ingredient_4, ingredient_5, ingredient_6,
        user_1, user_2, user_3,
        review_1, review_2, review_3, review_4, review_5
    ])

    db.session.commit()

print("Database seeded successfully!")
