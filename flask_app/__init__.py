from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "d8a8cv0a3caklalxcz#23dsaoim232.3i2oida81jds8a"
