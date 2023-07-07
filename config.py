from flask_pymongo import PyMongo

mongo = PyMongo()
app = ''

def init_app(app):
    app = app
    
    DB_NAME = "shopping_cart"

    app.config["SECRET_KEY"] = 'c5fdc997eb24ae4b56f6f1783608e9eac9e20410'
    app.config['MONGO_URI'] = f"mongodb+srv://hasandev29:ali2001@mongo-cluster.irg3rzx.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"
    
    mongo.init_app(app)