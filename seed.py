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
    category_5 = Category(name='Breakfast', description='Start your day right with these dishes')
    category_6 = Category(name='Snack', description='Light bites for any time of day')

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
    
    # Additional Recipes
    recipe_6 = Recipe(
        title='Avocado Toast',
        description='Smashed avocado on toasted bread, topped with salt, pepper, and chili flakes.',
        instructions='Toast bread, mash avocado, and spread on top.',
        category=category_5,
        image_url='https://images.unsplash.com/photo-1526151271220-4d68c0f33f44?w=500&auto=format&fit=crop&q=60',
        created_at=now,
        updated_at=now
    )
    recipe_7 = Recipe(
        title='Caprese Salad',
        description='Fresh mozzarella, tomatoes, and basil drizzled with balsamic glaze.',
        instructions='Layer mozzarella and tomatoes, sprinkle with basil, and drizzle with glaze.',
        category=category_3,
        image_url='https://images.unsplash.com/photo-1514516877562-6ac4d72ab2cf?w=500&auto=format&fit=crop&q=60',
        created_at=now,
        updated_at=now
    )
    recipe_8 = Recipe(
        title='Pasta Primavera',
        description='Pasta with fresh vegetables and a light garlic sauce.',
        instructions='Cook pasta, sauté vegetables, and toss with pasta and sauce.',
        category=category_2,
        image_url='https://images.unsplash.com/photo-1589927986089-3581c1e4571c?w=500&auto=format&fit=crop&q=60',
        created_at=now,
        updated_at=now
    )
    recipe_9 = Recipe(
        title='Spicy Chickpea Stew',
        description='A hearty stew made with chickpeas, tomatoes, and spices.',
        instructions='Simmer chickpeas with tomatoes and spices until thick.',
        category=category_4,
        image_url='https://images.unsplash.com/photo-1603791448208-b4f0c3a4b45f?w=500&auto=format&fit=crop&q=60',
        created_at=now,
        updated_at=now
    )
    recipe_10 = Recipe(
        title='Banana Pancakes',
        description='Fluffy pancakes made with ripe bananas and topped with syrup.',
        instructions='Mix ingredients, pour on skillet, and cook until golden.',
        category=category_5,
        image_url='https://images.unsplash.com/photo-1587240822973-90d4c52eb236?w=500&auto=format&fit=crop&q=60',
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
    ingredient_7 = Ingredient(name='Avocado', type='Fruit', calories=160)
    ingredient_8 = Ingredient(name='Tomato', type='Vegetable', calories=18)
    ingredient_9 = Ingredient(name='Pasta', type='Grain', calories=200)
    ingredient_10 = Ingredient(name='Chickpeas', type='Protein', calories=164)
    ingredient_11 = Ingredient(name='Banana', type='Fruit', calories=105)

    # Assign ingredients to recipes
    recipe_1.ingredients.append(ingredient_2)  # Chocolate Lava Cake
    recipe_2.ingredients.append(ingredient_1)  # Salmon for Lemon Herb Salmon
    recipe_3.ingredients.append(ingredient_4)  # Mushrooms for Stuffed Mushrooms
    recipe_4.ingredients.append(ingredient_3)  # Quinoa for Vegan Salad
    recipe_5.ingredients.append(ingredient_2)  # Chocolate for Tiramisu
    recipe_6.ingredients.append(ingredient_7)  # Avocado for Avocado Toast
    recipe_7.ingredients.append(ingredient_8)  # Tomatoes for Caprese Salad
    recipe_8.ingredients.append(ingredient_9)  # Pasta for Pasta Primavera
    recipe_9.ingredients.append(ingredient_10) # Chickpeas for Spicy Chickpea Stew
    recipe_10.ingredients.append(ingredient_11) # Banana for Banana Pancakes

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
    review_6 = Review(
        recipe=recipe_6,
        user=user_1,
        rating=5,
        comment='Simple and delicious! Perfect for breakfast.'
    )
    review_7 = Review(
        recipe=recipe_7,
        user=user_2,
        rating=4,
        comment='Fresh and tasty, but I prefer more basil.'
    )
    review_8 = Review(
        recipe=recipe_8,
        user=user_3,
        rating=5,
        comment='A colorful and flavorful dish!'
    )
    review_9 = Review(
        recipe=recipe_9,
        user=user_1,
        rating=5,
        comment='Hearty and full of flavor!'
    )
    review_10 = Review(
        recipe=recipe_10,
        user=user_2,
        rating=4,
        comment='Fluffy and sweet, just the way I like it.'
    )

    # Add all objects to the session and commit to the database
    db.session.add_all([
        category_1, category_2, category_3, category_4, category_5, category_6,
        recipe_1, recipe_2, recipe_3, recipe_4, recipe_5,
        recipe_6, recipe_7, recipe_8, recipe_9, recipe_10,
        ingredient_1, ingredient_2, ingredient_3, ingredient_4, ingredient_5, ingredient_6,
        ingredient_7, ingredient_8, ingredient_9, ingredient_10, ingredient_11,
        user_1, user_2, user_3,
        review_1, review_2, review_3, review_4, review_5,
        review_6, review_7, review_8, review_9, review_10
    ])

    db.session.commit()

print("Database seeded successfully!")
