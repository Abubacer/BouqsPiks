""" Sets up a Flask server to handle incoming requests """

from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

port = 5000
host = '0.0.0.0'


# Loads flower data from the JSON file
with open('flowers.json') as file:
    flower_data = json.load(file)["flowerlist"]


def get_flower_details_by_id(flower_id, flower_data):
    """Get flower details based on the flower ID."""
    for flower in flower_data:
        if flower["productId"] == flower_id:
            return flower
    return None


@app.route('/')
def home():
    """ Serves the landing html page """
    return render_template('index.html')


@app.route('/contact')
def contact():
    """ Serves the contact page """
    return render_template('contact.html')


@app.route('/flower_recommender')
def flower_recommender():
    """ Serves the flower recommender page """
    return render_template('flower_recommender.html')


@app.route('/product-details/<int:flower_id>')
def flower_details(flower_id):
    """ Serves the flower product details page """
    flower = get_flower_details_by_id(flower_id, flower_data)

    if flower is not None:
        return render_template('product-details.html', flower=flower)
    else:
        return render_template('404.html')


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    Retrieves user inputs, encodes them, and generates recommendations.
    """
    gender = request.form.get('gender')
    personality = request.form.get('personality')
    occasion = request.form.get('occasion')
    budget_option = request.form.get('budget')

    print("Received Form Values:")
    print("Gender:", gender)
    print("Personality:", personality)
    print("Occasion:", occasion)
    print("Budget:", budget_option)

    filtered_flowers = filter_flowers(gender, personality, occasion, budget_option)

    return render_template('recommendations.html', flowers=filtered_flowers)


@app.errorhandler(404)
def page_not_found(error):
    """ Error handlers for 404 errors """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """ Error handlers for 500 errors """
    return render_template('500.html'), 500


def filter_flowers(gender, personality, occasion, budget_option):
    """ Filters flowers data based on user input """
    filtered_flowers = []
    for flower in flower_data:
        if (
            (gender is None or flower['gender'] == gender) and
            (personality is None or flower['personality'] == personality) and
            (occasion is None or flower['occasion'] == occasion) and
            (budget_option is None or flower['price'] <= float(budget_option))
        ):
            filtered_flowers.append(flower)

    return filtered_flowers


if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
