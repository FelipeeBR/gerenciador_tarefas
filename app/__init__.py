from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#iniciando login
#login = LoginManager(app)
#login.init_app(app)
#login.login_view ='login'

app.secret_key = 'secret_key'


from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)