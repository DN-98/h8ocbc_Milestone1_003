import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)
# print(connex_app.__dict__)

# Get the underlying Flask app instance
app = connex_app.app
# print(app.__dict__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mwbciteaunhwxy:4fff8dafe80958892b2bc61d3e32a0131537d54920a4716c87545b979d9a7418@ec2-54-80-123-146.compute-1.amazonaws.com:5432/d5fdsb8j2eqf8p'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)