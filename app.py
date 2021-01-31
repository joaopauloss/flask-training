from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/page1', methods=('POST', 'GET'))
def page1():
    return render_template('page1.html')

@app.route('/page2', methods=('POST', 'GET'))
def page2():
    return render_template('page2.html')

@app.route('/page3',methods=('POST', 'GET'))
def page3():
    return render_template('page3.html')


if __name__ == "__main__":
    app.run(debug=True)



# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
#     app.run(host="localhost", port=8001, debug=True)
