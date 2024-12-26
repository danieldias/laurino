from flask import Flask, render_template, request, url_for
from search import load_data, search_records

app = Flask(__name__)

# Load JSON data
data = load_data('birth.json')

@app.route('/test-static')
def test_static():
    # Use url_for to reference the static image
    image_url = url_for('static', filename='images/Natti 1866-75/Indice di Nati Decennale 1866-75 _cover.jpg')
    return f'<img src="{image_url}">'

# Home route with search form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        surname = request.form['surname']
        year_range = request.form.get('year_range', None)

        # Perform search
        records = search_records(data, surname, year_range)

        # Render results
        return render_template('index.html', records=records, surname=surname, year_range=year_range)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
