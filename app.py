from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
import threading

app = Flask(__name__)
api = Api(app)

# Créer une liste de dictionnaires pour simuler une base de données d'utilisateurs
users = [
    {"id": 1, "username": "john_doe", "password": "secret"},
    {"id": 2, "username": "jane_smith", "password": "12345"},
]

# Parser pour analyser les arguments dans les demandes POST
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Username is required.")
parser.add_argument('password', type=str, required=True, help="Password is required.")

# Classe de ressource pour gérer les demandes POST (pour créer un utilisateur) et GET (pour obtenir les détails de l'utilisateur)
class UserResource(Resource):
    def get(self, user_id):
        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            return user
        return {"message": "User not found"}, 404

    def post(self):
        args = parser.parse_args()
        new_user = {
            "id": len(users) + 1,
            "username": args['username'],
            "password": args['password']
        }
        users.append(new_user)
        return new_user, 201

# Ajouter la ressource à l'API avec un chemin d'accès
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/login', methods=['POST'])
def login():
    # Récupérer le nom d'utilisateur et le mot de passe depuis le formulaire
    username = request.form['username']
    password = request.form['password']

    # Traitez les données (par exemple, vérifiez les informations d'identification)
    # ...

    # Rediriger l'utilisateur vers une autre page ou afficher un message de succès
    return f"Welcome, {username}! You are logged in successfully."

def serve_app():
    app.run(debug=False)

if __name__ == '__main__':
    # Utiliser threading pour exécuter l'application Flask en parallèle
    t = threading.Thread(target=serve_app)
    t.daemon = True
    t.start()

    # Vous pouvez également exécuter certaines autres tâches ici s'il y a lieu.

    # Joindre le thread principal pour éviter que le programme se termine
    t.join()
