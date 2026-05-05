# 🚀 Student Performance Predictor - Deployment Guide

## 📋 Prerequisites
- Python 3.8+ installed
- Node.js (optional, for production deployment)
- Git (optional, for version control)
- Text editor (VS Code recommended)

---

## 🗂️ Project Structure
```
prudhvi--1/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   └── predictor.html
└── DEPLOYMENT_GUIDE.md
```

---

## 🔧 Step 1: Backend Deployment

### 1.1 Install Python Dependencies
```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt

# Or install manually if requirements.txt doesn't exist
pip install flask flask-cors numpy pandas scikit-learn joblib imbalanced-learn
```

### 1.2 Start Backend Server
```bash
# Start Flask development server
python app.py

# Server will run on: http://localhost:5000
# API endpoint: http://localhost:5000/predict
```

### 1.3 Verify Backend is Working
Open browser and visit: `http://localhost:5000/health`
You should see: `{"status": "healthy", "model_loaded": false, "version": "1.0.0"}`

---

## 🌐 Step 2: Frontend Deployment

### Option A: Simple Local Deployment (Recommended for testing)

#### 2.1 Start HTTP Server
```bash
# Navigate to frontend directory
cd frontend

# Start Python HTTP server
python -m http.server 8000

# Frontend will run on: http://localhost:8000
```

#### 2.2 Access Application
Open browser and visit: `http://localhost:8000/predictor.html`

### Option B: Using Live Server (VS Code)
1. Install "Live Server" extension in VS Code
2. Right-click on `predictor.html`
3. Select "Open with Live Server"
4. Application opens in browser automatically

### Option C: Node.js Server (Production-ready)
```bash
# Install http-server globally
npm install -g http-server

# Navigate to frontend directory
cd frontend

# Start server
http-server -p 8000

# Access: http://localhost:8000/predictor.html
```

---

## 🧪 Step 3: Test the Application

### 3.1 Test Backend API
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test prediction endpoint with sample data
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_learning": 2.5,
    "coursera": 1.5,
    "udemy": 1.0,
    "google_classroom": 2.0,
    "khan_academy": 1.5,
    "byjus": 0.5,
    "game_hours": 1.0,
    "educational_games": 0.5,
    "instagram": 2.0,
    "snapchat": 1.5,
    "whatsapp": 2.5,
    "youtube_social": 1.0,
    "telegram": 0.5,
    "twitter": 1.0,
    "facebook": 0.5,
    "social_interactions": 10
  }'
```

### 3.2 Test Frontend
1. Open `http://localhost:8000/predictor.html`
2. Click "Load Sample Data" button
3. Click "Predict Performance" button
4. Verify prediction result appears

---

## 🌍 Step 4: Production Deployment Options

### Option A: PythonAnywhere (Free)
1. Create account at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload project files
3. Install requirements in web tab
4. Configure web app to run `app.py`
5. Upload frontend files to static directory

### Option B: Heroku (Free Tier)
1. Install Heroku CLI
2. Create `Procfile` in root:
   ```
   web: python backend/app.py
   ```
3. Create `requirements.txt` in root
4. Deploy:
   ```bash
   heroku create
   git add .
   git commit -m "Deploy app"
   git push heroku main
   ```

### Option C: Vercel/Netlify (Frontend only)
1. Deploy frontend to Vercel/Netlify
2. Use backend API as separate service
3. Update frontend API URL in JavaScript

### Option D: Self-hosted VPS
1. Rent VPS (DigitalOcean, Vultr, etc.)
2. Install nginx, Python, supervisor
3. Configure nginx reverse proxy
4. Set up SSL certificate with Let's Encrypt

---

## 🔧 Step 5: Configuration

### 5.1 Environment Variables (Production)
Create `.env` file in backend directory:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 5.2 Update API URL in Frontend
In `predictor.html`, update the backend URL:
```javascript
// Find this line in the JavaScript code
const backendUrl = 'http://your-domain.com:5000'; // Update to your backend URL
```

### 5.3 CORS Configuration
In `backend/app.py`, update CORS settings for production:
```python
CORS(app, resources={r"/*": {"origins": ["https://your-domain.com"]}})
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Backend Issues:
1. **Port already in use**
   ```bash
   # Find process using port 5000
   netstat -ano | findstr :5000
   # Kill the process
   taskkill /PID <PID> /F
   ```

2. **Module not found**
   ```bash
   # Install missing module
   pip install <module-name>
   ```

3. **CORS errors**
   - Check if backend is running
   - Verify CORS configuration
   - Check browser console for specific error

#### Frontend Issues:
1. **404 errors**
   - Ensure frontend server is running
   - Check file paths in HTML

2. **API connection errors**
   - Verify backend is accessible
   - Check API URL in JavaScript
   - Test API endpoint directly

3. **Styling issues**
   - Ensure CSS is loaded
   - Check browser developer tools
   - Verify file paths

---

## 📱 Step 6: Mobile Testing

### Test on Different Devices:
1. **Responsive Design**: Resize browser window
2. **Mobile Emulators**: Use Chrome DevTools device emulation
3. **Real Devices**: Test on actual smartphones/tablets

### Mobile-specific Checks:
- Touch interactions work
- Form inputs are accessible
- Layout adapts to screen size
- Performance is acceptable

---

## 🔒 Step 7: Security Considerations

### Basic Security:
1. **Input Validation**: Backend validates all inputs
2. **HTTPS**: Use SSL in production
3. **Environment Variables**: Store secrets securely
4. **Rate Limiting**: Implement API rate limiting
5. **CORS**: Restrict to specific domains

### Advanced Security:
1. **Authentication**: Add user authentication
2. **Database Security**: Use parameterized queries
3. **Logging**: Monitor for suspicious activity
4. **Updates**: Keep dependencies updated

---

## 📊 Step 8: Monitoring & Maintenance

### Health Checks:
- Backend: `/health` endpoint
- Frontend: Check page loads without errors
- Database: Monitor connection status

### Performance Monitoring:
- Response times
- Error rates
- Resource usage
- User activity

### Regular Maintenance:
- Update dependencies
- Backup data
- Review logs
- Optimize performance

---

## 🚀 Quick Start Summary

For immediate testing:
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
cd frontend
python -m http.server 8000

# Browser: Visit http://localhost:8000/predictor.html
```

---

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review error messages
3. Test components individually
4. Search online for specific error messages
5. Check project documentation

---

## 🎯 Success Criteria

✅ Backend running on port 5000  
✅ Frontend accessible on port 8000  
✅ Prediction form working  
✅ Results displaying correctly  
✅ Responsive design working  
✅ No console errors  

Your Student Performance Predictor is now deployed and ready to use! 🎉
