from flask import Flask, request, make_response, jsonify
from flask_migrate import  Migrate
from models import *
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token,jwt_required, get_jwt_identity, unset_jwt_cookies

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get ('JWT_SECRET_KEY')


# Initialize migration and database
migrate = Migrate(app, db)
CORS(app)
db.init_app(app)

# Initialize JWT Manager
jwt = JWTManager(app)

# Routes
@app.route('/')
def index():
    return "<h1>Hello, welcome to the Kitchen API</h1>"


# User Registration 

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    full_name = data.get('full_name')

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"msg": "Username already exists"}), 400)

    # Create a new user and hash the password
    new_user = User(
        username=username,
        email=email,
        full_name=full_name
    )
    new_user.set_password(password)  # Hash the password here
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({"msg": "User registered successfully"}), 201)



# #User Login

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Query for the user in the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
        if user and user.check_password(password):  # Use check_password to verify
            # Generate access and refresh tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.username)
            return make_response({
                'msg': 'Login successful',
                'tokens': {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }, 200)
        else:
            return make_response(jsonify({"msg": "Invalid username or password"}), 401)
    
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return make_response(jsonify({"msg": "Internal server error"}), 500)



# LogOut 

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"}) 
    unset_jwt_cookies(response)

    return response


    # Recipes Route
@app.route('/recipes', methods=['GET', 'POST'])
# @jwt_required()

def handle_recipes():
    current_user = get_jwt_identity()
    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)

    if request.method == 'GET':
        recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
        return make_response(jsonify(recipes), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get("title"),
            description=data.get("description"),
            instructions=data.get("instructions"),
            category_id=data.get("category_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
        db.session.add(new_recipe)
        db.session.commit()
        return make_response(new_recipe.to_dict(), 201)

@app.route('/recipes/<int:id>', methods=['GET', 'PATCH', 'DELETE'])

@jwt_required()
def recipe_by_id(id):
    current_user = get_jwt_identity()
    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)
    
    recipe = Recipe.query.get(id)
    if not recipe:
        return make_response(jsonify({"message": "Recipe not found"}), 404)

    if request.method == 'GET':
        return make_response(recipe.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(recipe, key, value)
        db.session.commit()
        return make_response(recipe.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(recipe)
        db.session.commit()
        return make_response({"message": "Recipe deleted successfully"}, 200)

# Categories Route
@app.route('/categories', methods=['GET', 'POST'])
# @jwt_required()

def handle_categories():
    current_user = get_jwt_identity()
    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)
    
    if request.method == 'GET':
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(jsonify(categories), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_category = Category(
            name=data.get("name"),
            description=data.get("description")
        )
        db.session.add(new_category)
        db.session.commit()
        return make_response(new_category.to_dict(), 201)

@app.route('/categories/<int:id>', methods=['GET', 'PATCH', 'DELETE'])

# @jwt_required()

def category_by_id(id):
    current_user = get_jwt_identity()

    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)
    
    category = Category.query.get(id)
    if not category:
        return make_response(jsonify({"message": "Category not found"}), 404)

    if request.method == 'GET':
        return make_response(category.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(category, key, value)
        db.session.commit()
        return make_response(category.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return make_response({"message": "Category deleted successfully"}, 200)

# Reviews Route
@app.route('/reviews', methods=['GET', 'POST'])
# @jwt_required()
def handle_reviews():
    current_user = get_jwt_identity()
    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(jsonify(reviews), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_review = Review(
            recipe_id=data.get("recipe_id"),
            user_id=data.get("user_id"),
            rating=data.get("rating")
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
# @jwt_required()
def review_by_id(id):

    current_user = get_jwt_identity()
    
    if not current_user:
        return make_response(jsonify({
            "msg": "Please Login to access "
        }),401)
    
    review = Review.query.get(id)
    if not review:
        return make_response(jsonify({"message": "Review not found"}), 404)

    if request.method == 'GET':
        return make_response(review.to_dict(), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(review, key, value)
        db.session.commit()
        return make_response(review.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        return make_response({"message": "Review deleted successfully"}, 200)

# Start the Flask app
if __name__ == '__main__':
    app.run(port=5555, debug=True)


