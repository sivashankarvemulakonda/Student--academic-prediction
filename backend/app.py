from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins

# Global variables for model and preprocessing components
model = None
scaler = None
selector = None
pca = None
label_encoders = {}
feature_columns = []

def load_model_and_components():
    """Load the trained model and preprocessing components"""
    global model, scaler, selector, pca, label_encoders, feature_columns
    
    try:
        # Load the trained ensemble model
        model_path = os.path.join(os.path.dirname(__file__), '..', 'student_performance_ensemble.pkl')
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print("Model loaded successfully")
        else:
            print("Model file not found. Using mock predictions.")
            model = None
        
        # Initialize preprocessing components (these would be saved in a real deployment)
        scaler = StandardScaler()
        selector = SelectKBest(score_func=f_classif, k=10)
        pca = PCA(n_components=0.95)
        
        # Define feature columns based on the notebook
        feature_columns = [
            'youtube_learning', 'coursera', 'udemy', 'google_classroom', 'khan_academy', 'byjus',
            'game_hours', 'educational_games', 'instagram', 'snapchat', 'whatsapp', 'youtube_social',
            'telegram', 'twitter', 'facebook', 'social_interactions'
        ]
        
        print("Backend components initialized")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

def preprocess_input(data):
    """Preprocess input data to match model requirements"""
    try:
        # Create a DataFrame with the input data
        input_df = pd.DataFrame([data])
        
        # Add derived features (matching notebook logic)
        education_cols = ['youtube_learning', 'coursera', 'udemy', 'google_classroom', 'khan_academy', 'byjus']
        gaming_cols = ['game_hours', 'educational_games']
        social_media_cols = ['instagram', 'snapchat', 'whatsapp', 'youtube_social', 'telegram', 'twitter', 'facebook']
        
        input_df['Time_on_Education'] = input_df[education_cols].sum(axis=1)
        input_df['Time_on_Gaming'] = input_df[gaming_cols].sum(axis=1)
        input_df['Time_on_Social_Media'] = input_df[social_media_cols].sum(axis=1)
        input_df['Daily_Usage_Hours'] = input_df[education_cols + gaming_cols + social_media_cols].sum(axis=1)
        input_df['Family_Communication'] = input_df['social_interactions']
        
        # Add dummy columns for features not in frontend (would be handled by proper preprocessing)
        dummy_features = [
            'ID', 'Name', 'Age', 'Gender', 'Gadget_Name', 'Gadget_Checks_Per_Day', 'Apps_Used_Daily',
            'Anxiety_Level', 'Depression_Level', 'Parental_Control', 'Screen_Time_Before_Bed',
            'Night_Usage', 'Notification_Frequency', 'Distraction_Level', 'Addiction_Level'
        ]
        
        for feature in dummy_features:
            if feature not in input_df.columns:
                # Use median values from the original dataset
                if feature in ['ID']:
                    input_df[feature] = 1500  # Median ID
                elif feature in ['Age']:
                    input_df[feature] = 16  # Median age
                elif feature in ['Gadget_Checks_Per_Day']:
                    input_df[feature] = 83  # Median checks
                elif feature in ['Apps_Used_Daily']:
                    input_df[feature] = 13  # Median apps
                elif feature in ['Anxiety_Level', 'Depression_Level']:
                    input_df[feature] = 5  # Median levels
                elif feature in ['Parental_Control']:
                    input_df[feature] = 1  # Most common
                elif feature in ['Screen_Time_Before_Bed']:
                    input_df[feature] = 1.0  # Median hours
                elif feature in ['Addiction_Level']:
                    input_df[feature] = 8.8  # Median addiction
                else:
                    input_df[feature] = 0  # Default for categorical
        
        return input_df
        
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

def make_mock_prediction(data):
    """Make a mock prediction based on input patterns"""
    # Calculate derived features
    education_hours = sum([
        data.get('youtube_learning', 0), data.get('coursera', 0), data.get('udemy', 0),
        data.get('google_classroom', 0), data.get('khan_academy', 0), data.get('byjus', 0)
    ])
    
    gaming_hours = data.get('game_hours', 0) + data.get('educational_games', 0)
    
    social_media_hours = sum([
        data.get('instagram', 0), data.get('snapchat', 0), data.get('whatsapp', 0),
        data.get('youtube_social', 0), data.get('telegram', 0), data.get('twitter', 0),
        data.get('facebook', 0)
    ])
    
    daily_usage = education_hours + gaming_hours + social_media_hours
    social_interactions = data.get('social_interactions', 0)
    
    # Simple scoring system (matching the notebook logic)
    score = (
        education_hours * 0.6
        - gaming_hours * 0.2
        - social_media_hours * 0.2
        - daily_usage * 0.1
        + social_interactions * 0.1
    )
    
    # Determine prediction
    if score >= 1.5:
        prediction = 'High'
        confidence = min(0.95, 0.7 + (score - 1.5) * 0.1)
    elif score >= 0.5:
        prediction = 'Medium'
        confidence = 0.6 + (score - 0.5) * 0.2
    else:
        prediction = 'Low'
        confidence = max(0.5, 0.8 - abs(score) * 0.1)
    
    # Generate mock probabilities
    if prediction == 'High':
        probabilities = {'High': confidence, 'Medium': (1 - confidence) * 0.6, 'Low': (1 - confidence) * 0.4}
    elif prediction == 'Medium':
        probabilities = {'High': (1 - confidence) * 0.3, 'Medium': confidence, 'Low': (1 - confidence) * 0.7}
    else:
        probabilities = {'High': (1 - confidence) * 0.2, 'Medium': (1 - confidence) * 0.3, 'Low': confidence}
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'probabilities': probabilities,
        'score': score,
        'features': {
            'education_hours': education_hours,
            'gaming_hours': gaming_hours,
            'social_media_hours': social_media_hours,
            'daily_usage': daily_usage,
            'social_interactions': social_interactions
        }
    }

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'youtube_learning', 'coursera', 'udemy', 'google_classroom', 'khan_academy', 'byjus',
            'game_hours', 'educational_games', 'instagram', 'snapchat', 'whatsapp', 'youtube_social',
            'telegram', 'twitter', 'facebook', 'social_interactions'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        if model is not None:
            # Use actual model (would require proper preprocessing)
            result = make_mock_prediction(data)  # Fallback to mock for now
        else:
            # Use mock prediction
            result = make_mock_prediction(data)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'version': '1.0.0'
    })

@app.route('/features', methods=['GET'])
def get_features():
    """Get information about required features"""
    return jsonify({
        'features': [
            {
                'name': 'youtube_learning',
                'label': 'YouTube Learning Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on YouTube for educational content'
            },
            {
                'name': 'coursera',
                'label': 'Coursera Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Coursera courses'
            },
            {
                'name': 'udemy',
                'label': 'Udemy Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Udemy courses'
            },
            {
                'name': 'google_classroom',
                'label': 'Google Classroom Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Google Classroom'
            },
            {
                'name': 'khan_academy',
                'label': 'Khan Academy Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Khan Academy'
            },
            {
                'name': 'byjus',
                'label': 'Byjus Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Byjus learning platform'
            },
            {
                'name': 'game_hours',
                'label': 'Game Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent playing games'
            },
            {
                'name': 'educational_games',
                'label': 'Educational Game Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on educational games'
            },
            {
                'name': 'instagram',
                'label': 'Instagram Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Instagram'
            },
            {
                'name': 'snapchat',
                'label': 'Snapchat Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Snapchat'
            },
            {
                'name': 'whatsapp',
                'label': 'WhatsApp Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on WhatsApp'
            },
            {
                'name': 'youtube_social',
                'label': 'YouTube Social Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on YouTube for entertainment'
            },
            {
                'name': 'telegram',
                'label': 'Telegram Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Telegram'
            },
            {
                'name': 'twitter',
                'label': 'Twitter Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Twitter'
            },
            {
                'name': 'facebook',
                'label': 'Facebook Hours',
                'type': 'number',
                'min': 0,
                'max': 5,
                'description': 'Hours spent on Facebook'
            },
            {
                'name': 'social_interactions',
                'label': 'Daily Social Interactions',
                'type': 'number',
                'min': 0,
                'max': 20,
                'description': 'Number of social interactions per day'
            }
        ]
    })

if __name__ == '__main__':
    load_model_and_components()
    app.run(debug=True, host='0.0.0.0', port=5000)
