""" Sets up a Flask server to handle incoming requests """

from flask import Flask, render_template, request, jsonify
from dummy_data import dummy_flower_data
import os


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

port = 5000
host = '0.0.0.0'


def filter_flowers(data, gender, personality, occasion, price_range):
    """ Implement logic to filter data based on user input """
    filtered_data = [flower for flower in data if
                     flower['gender'] == gender and
                     flower['personality'] == personality and
                     flower['occasion'] == occasion and
                     flower['price_range'] == price_range]

    return filtered_data


@app.route('/')
def home():
    """ Serves the landing page """
    return render_template('index.html')


@app.route('/contact')
def contact():
    """ Serves the contact page """
    return render_template('contact.html')


@app.route('/flower_recommender')
def flower_recommender():
    """ Serves the flower recommender page """
    return render_template('flower_recommender.html')
    

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    Retrieves user inputs from the form, and Generates a prompt for the ChatGPT
    API to get recommendations.
    """
    gender = request.form.get('gender')
    personality = request.form.get('personality')
    occasion = request.form.get('occasion')
    price_range = request.form.get('priceRange')
    # Filter dummy flower data based on user input
    filtered_flowers = filter_flowers(dummy_flower_data, gender, personality, occasion, price_range)
    # Extract flower names for recommendations
    recommendations = [flower['name'] for flower in filtered_flowers]
    # Render the recommendations on the webpage recommendations=recommendations
    return render_template('recommendations.html', recommendations=recommendations, flower_data=filtered_flowers)


@app.errorhandler(404)
def page_not_found(error):
    """ Error handlers for 404 errors """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """ Error handlers for 500 errors """
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
