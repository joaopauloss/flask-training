import datetime
from functools import wraps

import jwt
from flask import (Flask, current_app, jsonify, make_response, redirect,
                   render_template, request, session, url_for)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_raw_jwt
)

from users import Users, token_exception_messages

app = Flask(__name__)

# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# receives POST requests directly from an HTML form
app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)

# Variable for page2 functions
last_content = 'Default'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # username = request.json.get('username', None)
        username = request.form['txtUsr']
        # password = request.json.get('password', None)
        password = request.form['txtPwd']
        if username != 'test' or password != 'test':
            return jsonify({'login': False}), 401

        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        print('\033[91m' + access_token + '\033[0m')
        refresh_token = create_refresh_token(identity=username)
        print('\033[91m' + refresh_token + '\033[0m')

        # Set the JWTs and the CSRF double submit protection cookies
        # in this response
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return render_template(
            'index.html', csrf_token=(get_raw_jwt() or {}).get("csrf")
            )
        
        # return resp, 200
    return render_template("login.html")


@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route('/api/example', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(username)}), 200

# @app.route('/protected', methods=['GET', 'POST'])
# @jwt_required
# def protected():
#   if request.method == "GET":
#       return render_template(
#           "form.html", csrf_token=(get_raw_jwt() or {}).get("csrf")
#       )
#   else:
#     # handle POST request
#     current_user = get_jwt_identity()


@app.route('/', methods=['POST', 'GET'])
@jwt_required
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        # handle POST request
        current_user = get_jwt_identity()

    
    
@app.route('/login2', methods=["POST"])
def login2():
    if request.form['txtUsr'] and request.form['txtPwd'] == 'password':

        token = jwt.encode({'user': request.form['txtUsr'],
            'user': request.form['txtUsr'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        },
        app.config['SECRET_KEY'])

        response = make_response(render_template("index.html"))
        # token = rba_controller.refresh_token(current_user)

        return response
        # return jsonify({'token': token})
        # return render_template('index.html')
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})

@app.route('/page1', methods=('POST', 'GET'))
@jwt_required
def page1():
    return render_template('page1.html')


@app.route('/page2', methods=('POST', 'GET'))
@jwt_required
def page2():
    global last_content
    if request.method == 'POST':
        if request.form["submit_button"] == "write":
            content = request.form['content']
            last_content = content
            return render_template('page2.html', content=content)

        elif request.form["submit_button"] == "read":
            return render_template('page2.html', content=last_content)
            
    else:
        return render_template('page2.html', content='Nothing to show')


@app.route('/page3',methods=('POST', 'GET'))
@jwt_required
def page3():
    return render_template('page3.html')


@app.route('/subpage1', methods=['GET','POST'])
def subpage1():
    return render_template('subpage1.html')


@app.route('/subpage2', methods=['GET','POST'])
def subpage2():
    return render_template('subpage2.html')

    
if __name__ == "__main__":
    app.run(debug=True)



# if __name__ == '__main__':
#     app.run(host="localhost", port=8000, debug=True)
#     app.run(host="localhost", port=8001, debug=True)




# def authentication_required():
#     def authentication(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             token = None

#             # if 'Authorization' in request.headers:
#             if 'x-access-tokens' in request.headers:
#                 token = request.headers['x-access-tokens']
#                 print('\033[91m' + token + '\033[0m')

#             if not token:  # TODO: enhance this check for empty tokens as "" or undefined
#                 return jsonify({"error": "unauthorized access"}), 401

#             try:
#                 payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms="HS256")

#             except jwt.ExpiredSignatureError:
#                 return token_exception_messages.get('expired'), 401
#             except jwt.InvalidTokenError:
#                 return token_exception_messages.get('invalid'), 401

#             return func(current_user=payload['user_name'], *args, **kwargs)

#         return wrapper

#     return authentication


# def check_for_token(func):
#     @wraps(func)
#     def wrapped(*args, **kwargs):
#         token = None
#         if 'token' in request.headers:
#             token =  request.headers['token']
#         if not token:
#             return jsonify({'message': 'Missing token'}), 401
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message': 'Invalid token'}), 401
#         return func(*args, **kwargs)
#     return wrapped


# @app.route('/login', methods=["POST"])
# def login():
#     if request.form['txtUsr'] and request.form['txtPwd'] == 'password':
#         session['logged_in'] = True
#         token = jwt.encode({'user': request.form['txtUsr'],
#             'user': request.form['txtUsr'],
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
#         },
#         app.config['SECRET_KEY'])

#         response = make_response(render_template("index.html")
#         # token = rba_controller.refresh_token(current_user)
#         response.headers['token'] = token.decode()

#         return response
#         # return jsonify({'token': token})
#         # return render_template('index.html')
#     else:
#         session['logged_in'] = False
#         return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})