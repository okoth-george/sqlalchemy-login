from flask import Flask,Blueprint, render_template, request, redirect, url_for, flash,get_flashed_messages
from flask_restx import Api, Resource, fields,Namespace
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, session,sessionmaker

app=Flask(__name__)
app.secret_key='your-secret-key'
engine = create_engine("sqlite:///users.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'new_user'
    id = Column(Integer, primary_key=True)
    name = Column(String ,unique=True ,nullable=False)
    password = Column(String ,nullable=False)

Base.metadata.create_all(engine)

Auth_bp = Blueprint('auth', __name__)

Auth_api = Api(Auth_bp, title="Auth API", description="API for User AUTH", doc='/Auth')

# define user model for  login 
user_model =Auth_api.model('user',{
   'name': fields.String(required=True, description="User's username"),
    'password': fields.String(required=True, description="User's password")
})

Auth_ns = Auth_api.namespace('auth', description="Authentications API Endpoints")
 

@Auth_ns.route('/register' )
class RegisterApi(Resource):
    @Auth_api.expect(user_model)
    def post(self):
        data=Auth_api.payload
        name=data.get('name')
        password=data.get('password')

         # Hash the password before storing
        if not  name.replace(" ", "").isalpha():
            return {"error": "Username should contain only letters"}, 400  
        if  not password or not password.isdigit()or len(password) !=4:
           return {"error": "password should contain four digits "}, 400
            
        hashed_password=generate_password_hash(password)
        with SessionLocal() as db:
            existing_user = db.query(User).filter_by(name=name).first()
            if existing_user:
            
                
                return {"username exist enter anoher username"}
                

            new_user = User(name=name, password=hashed_password)
            db.add(new_user)
            db.commit()
            flash("User registered successfully! Please login.", "success")
            return redirect(url_for('auth.login'))
            
        

@Auth_ns.route('/login')
class LoginApi(Resource):
    @Auth_api.expect(user_model)
    def post(self):
        data=Auth_api.payload
        name=data.get('name')
        password=data.get('password')

        with SessionLocal() as db:
            user = db.query(User).filter_by(name=name).first()
            if user and check_password_hash(user.password, password):
               flash(f"Welcome back, {name}!", "success")
               return redirect(url_for('home'))  # or wherever you want
            flash("Invalid username or password", "error")
        return render_template('login.html')

        

app.register_blueprint(Auth_bp, url_prefix='/api')         
if __name__ == '__main__':
    app.run(debug=True)

