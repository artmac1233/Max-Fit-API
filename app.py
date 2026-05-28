from flask import Flask
from routes.produtos import produtos_bp
from routes.clientes import clientes_bp

app = Flask(__name__)

app.register_blueprint(produtos_bp)
app.register_blueprint(clientes_bp)

@app.route('/')
def home():
    return "API funcionando"

if (__name__) == '__main__':
    app.run(debug=True)