from flask import Flask
from flask_cors import CORS
from config import init_app
from app.routes.products import products_bp
from app.routes.category import categories_bp
from app.routes.cart import cart_Bp

app = Flask(__name__)
cors = CORS(app)

init_app(app)
 
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(cart_Bp)

if __name__ == '__main__':
    app.run(debug=True)