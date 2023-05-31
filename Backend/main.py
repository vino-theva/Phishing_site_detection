from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

model = xgb.XGBClassifier(n_estimators=1000)
model.load_model('phisingclassify.bin')


@app.route('/backend/endpoint', methods=['POST'])
def handle_upload():
    url = request.json['url']
    # Preprocess the input URL
    df = pd.DataFrame({'url': [url]})
    length_of_url = []
    number_of_letters = []
    number_of_digits = []
    count_of_dotcom = []
    count_of_codot = []
    count_of_dotnet = []
    count_of_forward_slash = []
    count_of_percentage = []
    count_of_upper_case = []
    count_of_lower_case = []
    count_of_dot = []
    count_of_dot_info = []
    count_of_https = []
    count_of_www_dot = []
    count_of_not_alphanumeric = []
    
    for item in df['url']:
        try:
            length_of_url.append(len(item))
        except:
            length_of_url.append(0)
    
        try:
            number_of_letters.append(sum(c.isalpha() for c in item))
        except:
            number_of_letters.append(0)
    
        try:
            number_of_digits.append(sum(c.isdigit() for c in item))
        except:
            number_of_digits.append(0)
    
        try:
            count_of_dotcom.append(item.count(".com"))
        except:
            count_of_dotcom.append(0)
    
        try:
            count_of_codot.append(item.count(".co."))
        except:
            count_of_codot.append(0)
    
        try:
            count_of_dotnet.append(item.count(".net"))
        except:
            count_of_dotnet.append(0)
    
        try:
            count_of_forward_slash.append(item.count("/"))
        except:
            count_of_forward_slash.append(0)
    
        try:
            count_of_percentage.append(item.count("%"))
        except:
            count_of_percentage.append(0)
    
        try:
            count_of_dot.append(item.count("."))
        except:
            count_of_dot.append(0)
    
        try:
            count_of_upper_case.append(sum(c.isupper() for c in item))
        except:
            count_of_upper_case.append(0)
    
        try:
            count_of_lower_case.append(sum(c.islower() for c in item))
        except:
            count_of_lower_case.append(0)
    
        try:
            count_of_dot_info.append(item.count(".info"))
        except:
            count_of_dot_info.append(0)
    
        try:
            count_of_https.append(item.count("https"))
        except:
            count_of_https.append(0)
    
        try:
            count_of_www_dot.append(item.count("www."))
        except:
            count_of_www_dot.append(0)
    
        try:
            count_of_not_alphanumeric.append(sum(not c.isalnum() for c in item))
        except:
            count_of_not_alphanumeric.append(0)
    
    df['length_of_url'] = length_of_url
    df['number_of_letters'] = number_of_letters
    df['number_of_digits'] = number_of_digits
    df['count_of_dotcom'] = count_of_dotcom
    df['count_of_codot'] = count_of_codot
    df['count_of_dotnet'] = count_of_dotnet
    df['count_of_forward_slash'] = count_of_forward_slash
    df['count_of_upper_case'] = count_of_upper_case
    df['count_of_lower_case'] = count_of_lower_case
    df['count_of_dot'] = count_of_dot
    df['count_of_dot_info'] = count_of_dot_info
    df['count_of_https'] = count_of_https
    df['count_of_www_dot'] = count_of_www_dot
    df['count_of_not_alphanumeric'] = count_of_not_alphanumeric
    df['count_of_percentage'] = count_of_percentage
    
    # Amount of symbols to letters ratio
    df['not_alphanumeric_to_letters_ratio'] = df['count_of_not_alphanumeric'] / df['number_of_letters']
    
    # Amount of '%' to length ratio
    df['percentage_to_length_ratio'] = df['count_of_percentage'] / df['length_of_url']
    
    # Amount of '/' to length ratio
    df['forwards_slash_to_length_ratio'] = df['count_of_forward_slash'] / df['length_of_url']
    
    # Amount capitalized vs. non-capitalized
    df['upper_case_to_lower_case_ratio'] = df['count_of_upper_case'] / df['count_of_lower_case']
    
    # Select features for prediction
    X = df[['length_of_url', 'number_of_letters', 'number_of_digits', 'count_of_dotcom', 'count_of_codot',
            'count_of_dotnet', 'count_of_forward_slash', 'count_of_upper_case', 'count_of_lower_case', 'count_of_dot',
            'count_of_dot_info', 'count_of_https', 'count_of_www_dot', 'count_of_not_alphanumeric',
            'count_of_percentage', 'percentage_to_length_ratio', 'forwards_slash_to_length_ratio']]
    
    # Make the prediction
    prediction = model.predict(X)
    
    # Return the prediction
    
    # The analysis returns a boolean value
    is_malicious = False
    
    if prediction == 1:
        is_malicious = True
    else:
        is_malicious = False

    # Return the result as JSON
    return jsonify({'isMalicious': is_malicious})

if __name__ == '__main__':
    app.run(debug=True)
