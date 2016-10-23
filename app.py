from flask import Flask
application = Flask(__name__)  # Change assignment here

@application.route("/")        # Change your route statements
def hello():         
    return "Hello World!"

if __name__ == "__main__":         
    application.run()          # Change all other references to 'app'