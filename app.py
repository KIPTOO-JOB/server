from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import *
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Initialize migration and database
migrate = Migrate(app, db)
CORS(app)
db.init_app(app)

# Initialize JWT Manager
jwt = JWTManager(app)

# User lookup callback
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none() 

# JWT error handling
@jwt.expired_token_loader
def jwt_expired_token(jwt_header, jwt_data):
    return make_response({'message': "Token has expired", "error": "token_expired"}, 401)

@jwt.invalid_token_loader
def jwt_invalid_token(error):
    return make_response({'message': 'Invalid token', "error": "invalid_token"}, 401)

@jwt.unauthorized_loader
def missing_token(error):
    return make_response({'message': 'Missing token', "error": "missing_token"}, 401)

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    return token is not None

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

    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"msg": "Username already exists"}), 201)

    new_user = User(username=username, email=email, full_name=full_name)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({"msg": "User registered successfully"}), 200)


@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
    return token is not None
 
# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id) 
        refresh_token = create_refresh_token(identity=user.id) 
        return make_response({
            'msg': 'Login successful',
            'tokens': {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }, 200)

    return make_response(jsonify({"msg": "Bad username or password"}), 401)

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# Recipes Route
@app.route('/recipes', methods=['GET', 'POST'])
@jwt_required()
def handle_recipes():
    current_user = get_jwt_identity()

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
@jwt_required()
def handle_categories():
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
@jwt_required()
def category_by_id(id):
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
@jwt_required()
def handle_reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(jsonify(reviews), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_review = Review(
            recipe_id=data.get("recipe_id"),
            user_id=get_jwt_identity(),  # Assuming user ID is obtained from JWT
            rating=data.get("rating")
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def review_by_id(id):
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
