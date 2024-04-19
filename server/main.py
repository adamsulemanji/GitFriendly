from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
  return "Hello World!"


@app.route("/clean", methods=['POST'])
def clean():
    data = request.json
    url = data.get('url', '')
    print(url)
    return jsonify({"cleanedUrl": "Cleaned URL: " + url})

if __name__ == "__main__":
  app.run(debug=True)