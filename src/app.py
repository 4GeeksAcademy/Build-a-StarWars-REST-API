"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas,Personajes, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



with app.app_context():
    db.create_all()

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = Personajes.query.all()
    result = [personaje.serialize() for personaje in people]
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personajes.query.get(people_id)
    if personaje:
        return jsonify(personaje.serialize()), 200
    return jsonify({'message': 'Personaje not found'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planetas.query.all()
    result = [planeta.serialize() for planeta in planets]
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planetas.query.get(planet_id)
    if planeta:
        return jsonify(planeta.serialize()), 200
    return jsonify({'message': 'Planeta not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify(result), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Obtener los favoritos del usuario actual (por implementar)
    # user_id = obtener_id_del_usuario_actual()
    user_id = 1  # Ejemplo: obtener el id del usuario actual
    user = User.query.get(user_id)
    if user:
        favorites = user.favoritos
        result = [favorite.serialize() for favorite in favorites]
        return jsonify(result), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Añadir un nuevo favorito de planeta al usuario actual (por implementar)
    # user_id = obtener_id_del_usuario_actual()
    user_id = 1  # Ejemplo: obtener el id del usuario actual
    user = User.query.get(user_id)
    if user:
        favorite = Favoritos(usuario_id=user.id, planetas_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite planet added'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Añadir un nuevo favorito de personaje al usuario actual (por implementar)
    # user_id = obtener_id_del_usuario_actual()
    user_id = 1  # Ejemplo: obtener el id del usuario actual
    user = User.query.get(user_id)
    if user:
        favorite = Favoritos(usuario_id=user.id, personajes_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite person added'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Eliminar un favorito de planeta con el id = planet_id (por implementar)
    # user_id = obtener_id_del_usuario_actual()
    user_id = 1  # Ejemplo: obtener el id del usuario actual
    user = User.query.get(user_id)
    if user:
        favorite = Favoritos.query.filter_by(usuario_id=user.id, planetas_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': 'Favorite planet deleted'}), 200
        return jsonify({'message': 'Favorite planet not found'}), 404
    return jsonify({'message': 'User not found'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Eliminar un favorito de personaje con el id = people_id (por implementar)
    # user_id = obtener_id_del_usuario_actual()
    user_id = 1  # Ejemplo: obtener el id del usuario actual
    user = User.query.get(user_id)
    if user:
        favorite = Favoritos.query.filter_by(usuario_id=user.id, personajes_id=people_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': 'Favorite person deleted'}), 200
        return jsonify({'message': 'Favorite person not found'}), 404
    return jsonify({'message': 'User not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
