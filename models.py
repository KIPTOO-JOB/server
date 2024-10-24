from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import func
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

recipe_ingredient = db.Table('recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ("-category.recipes", "-reviews.recipe", "-ingredients.recipes", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    instructions = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Foreign Key and Relationships
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship('Category', back_populates='recipes')

    # Add cascade="all, delete-orphan" to ensure reviews are deleted when a recipe is deleted
    reviews = db.relationship('Review', back_populates='recipe', cascade="all, delete-orphan")

    ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, back_populates='recipes')


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    serialize_rules = ("-recipes.category",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String(250))

    recipes = db.relationship('Recipe', back_populates='category')


class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'ingredients'

    serialize_rules = ("-recipes.ingredients",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Ingredient type (e.g., spice, dairy)
    type = db.Column(db.String)
    calories = db.Column(db.Integer, nullable=True)

    recipes = db.relationship('Recipe', secondary=recipe_ingredient, back_populates='ingredients')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ("-recipe.reviews", "-user.reviews")

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(450))

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"))
    recipe = db.relationship('Recipe', back_populates='reviews')

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', back_populates='reviews')


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-reviews.user", "-created_at", "-updated_at")

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    reviews = db.relationship('Review', back_populates='user')
    
    @validates('email')
    def validate_email(self, key, value):
        if "@" not in value:
            raise ValueError("Invalid email address")        
        return value
    
    # Password hashing
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=func.now())