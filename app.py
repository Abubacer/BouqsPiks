""" Sets up a Flask server to handle incoming requests """

from flask import Flask, render_template, request, jsonify
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
import numpy as np
import json


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

port = 5000
host = '0.0.0.0'


def read_flower_data_from_json():
    """ Reads flower data from the JSON file """
    with open('flower_data.json', 'r') as file:
        flower_data = json.load(file)
    return flower_data


def fit_label_encoders(flower_data):
    """ Encodes categorical features using sl LabelEncoder """
    le_occasion = LabelEncoder()
    le_personality = LabelEncoder()

    for flower in flower_data:
        flower['occasion'] = le_occasion.fit_transform([flower['occasion']])[0]
        flower['personality'] = le_personality.fit_transform([flower['personality']])[0]
    return le_occasion, le_personality, flower_data


def parse_user_budget(budget_option):
    """ Converts budget options to numerical values """
    budgets = {
        "under 25": 25,
        "25-200": (25, 200),
        "over 200": 200
    }
    try:
        return budgets[budget_option]
    except KeyError:
        # Handle invalid budget option
        raise ValueError(f"Invalid budget option: {budget_option}")


def train_model(flower_data):
    """ Trains the KNN model using feature arrays and prices """
    features = []
    prices = []
    for flower in flower_data:
        features.append([flower['occasion'], flower['gender'], flower['personality']])
        prices.append(flower['price'])

    X = np.concatenate([np.array(features), np.array(prices).reshape(-1, 1)], axis=1)

    knn_model, le_occasion, le_personality, flower_data = fit_label_encoders(flower_data)
    knn_model = NearestNeighbors(n_neighbors=5)
    # knn_model.fit(X)
    return knn_model, le_occasion, le_personality


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
    Retrieves user inputs, encodes them, and generates recommendations.
    """
    gender = request.form.get('gender')
    personality = request.form.get('personality')
    occasion = request.form.get('occasion')
    budget_option = request.form.get('budget')

    flower_data = read_flower_data_from_json()
    fit_label_encoders(flower_data)

    knn_model, le_occasion, le_personality = train_model(flower_data)

    try:
        min_budget, max_budget = parse_user_budget(budget_option)
    except ValueError as error:
        return render_template('error.html', error=error), 400

    user_features = np.array([
        le_occasion.transform([occasion])[0],
        gender,
        le_personality.transform([personality])[0],
        min_budget,
        max_budget
    ]).reshape(1, -1)

    _, indices = knn_model.kneighbors(user_features)

    matched_flowers = [flower_data[i] for i in indices[0]]

    return render_template('recommendations.html', flowers=matched_flowers)


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
