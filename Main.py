from flask import Flask
from flask_jwt_extended import JWTManager
from auth.auth_controller import auth_blueprint
from insurance.insurance_controller import insurance_blueprint
from claims.claim_controller import claim_blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Set a secure, unique secret key
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(insurance_blueprint)
app.register_blueprint(claim_blueprint)

if __name__ == '__main__':
    app.run(debug=True)