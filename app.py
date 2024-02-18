import json
from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user,logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

#login view
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user)
            return jsonify({"message":"logado"})
    return jsonify({"message":"Password or username invalid"}), 400

@app.route('/user/<int:id_user>', methods=["DELETE"]) 
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if id_user == current_user.id:
        return jsonify({"message":"You cant delete user logged in"})
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":f"User {id_user} removed"})
    
    return jsonify({"message":"User not found"})

@app.route('/logout', methods=["GET"]) 
@login_required
def logout():
    logout_user()
    return jsonify({"message":"logged out"})

        
@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"

@app.route('/user', methods=["POST"])
@login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return ({"message":f"Cadastro criado com sucesso:{username}"})
    
    return jsonify({"message": "dados invalidas"}), 400

if __name__ == '__main__':
    app.run(debug=True)