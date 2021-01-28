from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
#     app.run(host="localhost", port=8001, debug=True)
