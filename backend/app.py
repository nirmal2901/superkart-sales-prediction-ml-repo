
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_api = Flask("SuperKart Sales Prediction API")

# Load the trained machine learning pipeline
model = joblib.load("Superkart_sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "✅ Welcome to the SuperKart Sales Prediction API! Use POST /v1/sales to predict."

# Define an endpoint for single sales prediction (POST request)
@superkart_sales_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload with product and store details,
    and returns the predicted sales value as JSON.
    """
    input_data = request.get_json()

    # Construct a sample input row with required fields
    sample = {
        'Product_Weight': input_data['Product_Weight'],
        'Product_Sugar_Content': input_data['Product_Sugar_Content'],
        'Product_Allocated_Area': input_data['Product_Allocated_Area'],
        'Product_Type': input_data['Product_Type'],
        'Product_MRP': input_data['Product_MRP'],
        'Store_Establishment_Year': input_data['Store_Establishment_Year'],
        'Store_Size': input_data['Store_Size'],
        'Store_Location_City_Type': input_data['Store_Location_City_Type'],
        'Store_Type': input_data['Store_Type'],
        'Product_Id': 'P0000',  # dummy
        'Store_Id': 'S000',     # dummy
        'Product_Store_Sales_Total': 0  # dummy
    }

    input_df = pd.DataFrame([sample])
    predicted_sales = model.predict(input_df)[0]
    predicted_sales = round(float(predicted_sales), 2)

    return jsonify({'Predicted sales (in dollars)': predicted_sales})

# Define an endpoint for batch sales prediction (CSV file upload)
@superkart_sales_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file with multiple product-store records,
    and returns predicted sales as a dictionary.
    """
    file = request.files['file']
    input_df = pd.read_csv(file)

    # Make predictions
    predicted_sales = model.predict(input_df)
    predicted_sales = [round(float(val), 2) for val in predicted_sales]

    # Assume 'Product_Id' + 'Store_Id' combination for unique key
    keys = (input_df['Product_Id'] + '_' + input_df['Store_Id']).tolist()
    results = dict(zip(keys, predicted_sales))

    return jsonify(results)

# Run the Flask application
if __name__ == '__main__':
    superkart_sales_api.run(debug=True)
