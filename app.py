from flask import Flask

from views.home import home_bp
from views.search import search_bp

app = Flask(__name__)
app.secret_key = "my secret key"

app.register_blueprint(home_bp)
app.register_blueprint(search_bp)


if __name__ == "__main__":
    app.run(debug=True)
