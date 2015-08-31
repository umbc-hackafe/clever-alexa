import cleverbot
import pyalexa
import flask

APP_ID = None

with open(".app_id") as app_file:
    APP_ID = app_file.read().strip()

api = flask.Flask(__name__)
skill = pyalexa.Skill(app_id=APP_ID)
cleverbot = cleverbot.Cleverbot()

@skill.launch
def launch(request):
    return request.response(speech="Hello!", reprompt="Are you there?")

@skill.end
@skill.intent("Bye")
def end(request):
    return request.response(speech="Goodbye.", end=True)

@skill.intent("Chat")
def chat(request):
    if request.slots.get("Text"):
        return request.response(speech=cleverbot.ask(request.slots.get("Text")),
                                reprompt="What?")
    else:
        return request.response(speech="What?", reprompt="What?")

api.add_url_rule('/', 'pyalexa', skill.flask_target, methods=['POST'])
api.run('0.0.0.0', port=8080, debug=True)
