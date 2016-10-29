def lambda_handler(event, context):
    '''
    AWS Lambda Entry Point. JSON body of the request
    is in the event parameter
    '''

    '''Application ID verification'''
    if (event['session']['application']['applicationId'] !=
        "amzn1.echo-sdk-ams.app.bd304b90-xxxx-xxxx-xxxx-1e4fd4772bab"):
        raise ValueError("Invalid Application ID")

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SolvePostfix":
        return solve_postfix_intent_handler(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome!"
    speech_output = "Welcome to the Post-fix notation calculator. " \
                    "Please ask me a math problem using post-fix notation " \
                    "such as one five plus, or four two times."
    equation = "Examples: one five plus, four two times."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me a math problem using post-fix notation " \
                    "such as one five plus, or four two times."
    should_end_session = False
    return build_response(build_speechlet_response(
        card_title, speech_output, equation, reprompt_text, should_end_session))

def solve_postfix_intent_handler(intent):
    opA = int(intent['slots']['OperandA']['value'])
    opB = int(intent['slots']['OperandB']['value'])
    operator = intent['slots']['Operator']['value']

    card_title = 'Postfix Solution'
    should_end_session = False

    solution = None

    if operator == 'plus':
        solution = opA + opB
    elif operator == 'add':
        solution = opA + opB
    elif operator == 'addition':
        solution = opA + opB
    elif operator == 'minus':
        solution = opA - opB
    elif operator == 'subtract':
        solution = opA - opB
    elif operator == 'subtraction':
        solution = opA - opB
    elif operator == 'multiply':
        solution = opA * opB
    elif operator == 'times':
        solution = opA * opB
    elif operator == 'multiplication':
        solution = opA * opB
    elif operator == 'divide':
        solution = opA / opB
    elif operator == 'division':
        solution = opA / opB
    elif operator == 'modulo':
        solution = opA % opB
    elif operator == 'modulus':
        solution = opA % opB

    if solution == None:
        # Handle Error message response building
        speech_output = "I'm not sure what the answer is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what the answer is." \
                        "You can ask me to solve a math problem " \
                        "using post-fix notation."
        equation = speech_output

    else:
        # Normal solution response
        speech_output = "The answer is" + str(solution) + "."
        reprompt_text = "You can ask me to solve a math problem " \
                        "using post-fix notation."
        equation = intent['slots']['OperandA']['value'] + " " + intent['slots']['OperandB']['value'] + " " + intent['slots']['Operator']['value'] + " = " + str(solution)

    speech_response = build_speechlet_response(
        card_title, speech_output, equation, reprompt_text, should_end_session)

    return build_response(speech_response)


def build_response(speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': speechlet_response
    }

def build_speechlet_response(title, output, equation, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + equation
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
