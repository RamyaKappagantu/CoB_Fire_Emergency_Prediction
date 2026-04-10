from flask import Flask
from Controllers import VAR_controller, coordinates_controller, prophet_controller, auth_controller, LSTM_PredictionByDate_controller
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from Models.user import User
from database import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
app.register_blueprint(LSTM_PredictionByDate_controller.bp)
# app.register_blueprint(VAR_controller.bp)
app.register_blueprint(coordinates_controller.bp)
app.register_blueprint(prophet_controller.bp)
app.register_blueprint(auth_controller.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost:3306/CBFP'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = '3b98b159d2875f31df9c7f2d3837c6e0d1c5d18e6c8c239b5b929cb939b3d9e7'
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# def add_user(username, password, is_admin=False):
#     with app.app_context():
#         user = User(username=username, is_admin=is_admin)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         print(f"User {username} added successfully!")

if __name__ == '__main__':
    # add_user('admin', '12345', is_admin=True)
    app.run(debug=True, port=5000)
