from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Created basic configuration for getting started!"

if __name__ == "__main__":
    app.run(debug=True)

