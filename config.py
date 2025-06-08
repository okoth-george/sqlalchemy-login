from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages

from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, session,sessionmaker

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # needed for flashing messages
#app.register_blueprint()

engine = create_engine("sqlite:///users.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'new_user'
    id = Column(Integer, primary_key=True)
    name = Column(String ,unique=True ,nullable=False)
    password = Column(String ,nullable=False)

Base.metadata.create_all(engine)


@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('home.html')
   # return "<h1>Welcome!</h1>" + "<br>".join([f"{cat}: {msg}" for cat, msg in messages])
@app.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if not name.replace(" ", "").isalpha():
            flash("Username must contain only letters", "error")
            return render_template('register.html')

        if not password.isdigit() or len(password) != 4:
            flash("Password must be exactly 4 digits", "error")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        with SessionLocal() as db:
            existing_user = db.query(User).filter_by(name=name).first()
            if existing_user:
                flash("User already exists", "error")
                return render_template('register.html')
            new_user = User(name=name, password=hashed_password)
            db.add(new_user)
            db.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('login_form'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        with SessionLocal() as db:
            user = db.query(User).filter_by(name=name).first()
            if user and check_password_hash(user.password, password):
                flash(f"Welcome back, {name}!", "success")
                return redirect(url_for('home'))
            flash("Invalid credentials", "error")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
