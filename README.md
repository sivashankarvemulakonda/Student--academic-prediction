# Student Performance Predictor

A web application that predicts student academic performance (Low/Medium/High) based on gadget usage patterns using machine learning.

## Project Structure

```
prudhvi--1/
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # CSS styling
│   └── script.js           # JavaScript frontend logic
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── paper.ipynb            # Jupyter notebook with ML model
└── README.md              # This file
```

## Features

- **Interactive Form**: User-friendly input fields for all gadget usage data
- **Real-time Prediction**: Instant academic performance prediction
- **Professional UI**: Modern, responsive design with smooth animations
- **Sample Data**: Pre-loaded sample profiles for easy testing
- **Error Handling**: Comprehensive error messages and validation
- **Backend API**: RESTful API endpoint for predictions

## Input Features

### Educational Usage
- YouTube Learning Hours
- Coursera Hours
- Udemy Hours
- Google Classroom Hours
- Khan Academy Hours
- Byjus Hours

### Gaming & Entertainment
- Game Hours
- Educational Game Hours

### Social Media Usage
- Instagram Hours
- Snapchat Hours
- WhatsApp Hours
- YouTube Social Hours
- Telegram Hours
- Twitter Hours
- Facebook Hours

### Social Interaction
- Daily Social Interactions

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js (optional, for development tools)
- Modern web browser

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the backend server:**
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Open the frontend in your browser:**
   
   - Simply open `frontend/index.html` in your web browser
   - Or use a live server extension in VS Code

2. **Alternative: Use Python's built-in server:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   
   Then access `http://localhost:8000`

## Usage

### Method 1: Manual Input
1. Fill in all the input fields with your data
2. Click "🔮 Predict Performance"
3. View the prediction result

### Method 2: Sample Data
1. Click "📝 Load Sample Data" to fill with example data
2. Click "🔮 Predict Performance"
3. View the prediction result

### Method 3: Reset Form
- Click "🔄 Reset Form" to clear all fields and start over

## API Endpoints

### POST /predict
Predicts academic performance based on input data.

**Request Body:**
```json
{
  "youtube_learning": 2.5,
  "coursera": 1.8,
  "udemy": 1.2,
  "google_classroom": 2.0,
  "khan_academy": 1.5,
  "byjus": 1.0,
  "game_hours": 0.5,
  "educational_games": 0.8,
  "instagram": 0.3,
  "snapchat": 0.2,
  "whatsapp": 0.5,
  "youtube_social": 0.4,
  "telegram": 0.1,
  "twitter": 0.1,
  "facebook": 0.1,
  "social_interactions": 8
}
```

**Response:**
```json
{
  "prediction": "High",
  "confidence": 0.85,
  "probabilities": {
    "High": 0.85,
    "Medium": 0.12,
    "Low": 0.03
  },
  "score": 2.1,
  "features": {
    "education_hours": 10.0,
    "gaming_hours": 1.3,
    "social_media_hours": 1.6,
    "daily_usage": 12.9,
    "social_interactions": 8
  }
}
```

### GET /health
Health check endpoint.

### GET /features
Returns information about all required features.

## Model Information

The prediction model uses the following logic:

**Score Calculation:**
```
score = (education_hours * 0.6) 
        - (gaming_hours * 0.2) 
        - (social_media_hours * 0.2) 
        - (daily_usage_hours * 0.1) 
        + (social_interactions * 0.1)
```

**Performance Categories:**
- **High**: Score ≥ 1.5
- **Medium**: 0.5 ≤ Score < 1.5
- **Low**: Score < 0.5

## Development

### Running in Development Mode

1. **Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Frontend:**
   - Use VS Code Live Server extension
   - Or any other development server

### Customization

- **Styling**: Modify `frontend/styles.css`
- **Logic**: Update `frontend/script.js`
- **API**: Change `backend/app.py`
- **Model**: Update the notebook or model files

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the backend is running and CORS is enabled
2. **Connection Refused**: Check if the backend server is running on port 5000
3. **Invalid Input**: Ensure all fields are filled with valid numbers
4. **Model Not Found**: The app will use mock predictions if the model file is missing

### Debug Mode

Enable debug mode by setting:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is for educational purposes only.

## Contributing

Feel free to submit issues and enhancement requests!
