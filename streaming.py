import openai
from flask import Flask, render_template, request, Response

openai.api_key = "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"
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World"


def stream():
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "Write a small poem on of 4 lines",
            }], stream= True, max_tokens=500, temperature=0)
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta']:
            yield chunk['choices'][0]['delta']['content']

@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "GET":
        return Response(stream(), mimetype='text/event-stream')
    else:
        return Response(None, mimetype='text/event-stream')
    
if __name__ == '__main__':
    app.run(debug=True)