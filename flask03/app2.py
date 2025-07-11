from flask import Flask, request, render_template
import shodan

app = Flask(__name__)

# Shodan API 키를 설정합니다.
SHODAN_API_KEY = 'Z2soDBnFLLNRKZsamG9hUQLtBBh9GTwH'
api = shodan.Shodan(SHODAN_API_KEY)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    product = None

    if request.method == 'POST':
        product = request.form.get('product')
        query = f'product:{product}'

        try:
            # Shodan 검색을 수행합니다.
            shodan_results = api.search(query)
            results = shodan_results['matches'][:5]
        except shodan.APIError as e:
            results = []    

    return render_template('search.html', results=results, product=product)

if __name__ == '__main__':
    app.run(debug=True)
