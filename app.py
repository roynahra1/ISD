from flask import Flask, render_template

app = Flask(__name__)

def get_max(a, b):
    return max(a, b)

@app.route('/')
def index():
    a, b = 10, 20
    result = get_max(a, b)
    return render_template('index.html', max_value=result)

if __name__ == '__main__':
    app.run(debug=True)