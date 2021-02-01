from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/page1', methods=('POST', 'GET'))
def page1():
    return render_template('page1.html')

@app.route('/page2', methods=('POST', 'GET'))
def page2():

    if request.method == 'POST':
        if request.form["submit_button"] == "write":
            content = request.form['content']
            return render_template('page2.html', content=content)

        elif request.form["submit_button"] == "read":
            return render_template('page2.html', content='Read button pressed')
            
    else:
        return render_template('page2.html', content='Nothing to show')

@app.route('/page3',methods=('POST', 'GET'))
def page3():
    return render_template('page3.html')


if __name__ == "__main__":
    app.run(debug=True)



# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
#     app.run(host="localhost", port=8001, debug=True)
