from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
