from flask import Flask, render_template, request, url_for
from search import load_data, search_records

app = Flask(__name__)

# Load JSON data
data = load_data('birth.json')
links_data = load_data('birthlinks.json')

# Home route with search form
@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize variables to handle empty states
    records = []
    antenati_results = []
    surname = None
    year_range = None

    if request.method == 'POST':
        surname = request.form['surname']
        year_range = request.form.get('year_range', None)

        # Perform search, now returns both records and antenati_results
        records, antenati_results = search_records(data, surname, year_range, links_data)

    # Render results
    return render_template(
        'index.html',
        records=records,
        antenati_results=antenati_results,
        surname=surname,
        year_range=year_range
    )


if __name__ == '__main__':
    app.run(debug=True)