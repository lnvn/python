from flask import Flask, request, Response

app = Flask(__name__)

def check_auth(username, password):
    """Verify username and password."""
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'} # The HTTP WWW-Authenticate response header advertises the HTTP authentication methods (or challenges) that might be used to gain access to a specific resource.
    )

@app.route('/protected-resource')
def protected_resource():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f"Hello, {auth.username}!"

if __name__ == '__main__':
    app.run()
