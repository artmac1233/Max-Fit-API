from flask import Flask
from routes.produtos import produtos_bp

app = Flask(__name__)

app.register_blueprint(produtos_bp)

@app.route('/')
def home():
    return "API funcionando"

if (__name__) == '__main__':
    app.run(debug=True)