from flask import Flask, request, redirect, render_template
import string
import random

app = Flask(__name__)

# In-memory storage (HashMap)
url_mapping = {}

# Function to generate short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']

        # Generate unique short code
        short_code = generate_short_code()
        while short_code in url_mapping:
            short_code = generate_short_code()

        url_mapping[short_code] = long_url
        short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in url_mapping:
        return redirect(url_mapping[short_code])
    return "URL not found!"

if __name__ == '__main__':
    app.run(debug=True)