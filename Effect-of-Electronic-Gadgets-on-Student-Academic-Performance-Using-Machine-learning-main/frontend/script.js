// Student Performance Predictor - Frontend JavaScript

class StudentPerformancePredictor {
    constructor() {
        this.form = document.getElementById('predictionForm');
        this.predictBtn = document.getElementById('predictBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.resultSection = document.getElementById('resultSection');
        this.predictionResult = document.getElementById('predictionResult');
        this.confidenceScore = document.getElementById('confidenceScore');
        this.loadingSection = document.getElementById('loadingSection');
        this.errorSection = document.getElementById('errorSection');
        this.errorMessage = document.getElementById('errorMessage');
        
        this.apiEndpoint = 'http://localhost:5000/predict'; // Backend API endpoint
        
        this.initializeEventListeners();
        this.loadSampleData();
    }
    
    initializeEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handlePrediction();
        });
        
        // Reset button
        this.resetBtn.addEventListener('click', () => {
            this.resetForm();
        });
        
        // Input validation
        const inputs = this.form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateInput(input);
            });
        });
    }
    
    validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        
        if (value < min || value > max) {
            input.setCustomValidity(`Value must be between ${min} and ${max}`);
        } else {
            input.setCustomValidity('');
        }
    }
    
    collectFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        // Collect all form values
        for (let [key, value] of formData.entries()) {
            data[key] = parseFloat(value);
        }
        
        // Calculate derived features (matching the notebook logic)
        const educationHours = [
            data.youtube_learning,
            data.coursera,
            data.udemy,
            data.google_classroom,
            data.khan_academy,
            data.byjus
        ].reduce((sum, hours) => sum + hours, 0);
        
        const gamingHours = data.game_hours + data.educational_games;
        
        const socialMediaHours = [
            data.instagram,
            data.snapchat,
            data.whatsapp,
            data.youtube_social,
            data.telegram,
            data.twitter,
            data.facebook
        ].reduce((sum, hours) => sum + hours, 0);
        
        const dailyUsageHours = educationHours + gamingHours + socialMediaHours;
        
        // Return the data structure expected by the backend
        return {
            ...data,
            Time_on_Education: educationHours,
            Time_on_Gaming: gamingHours,
            Time_on_Social_Media: socialMediaHours,
            Daily_Usage_Hours: dailyUsageHours,
            Family_Communication: data.social_interactions
        };
    }
    
    async handlePrediction() {
        try {
            this.showLoading();
            this.hideResults();
            
            const data = this.collectFormData();
            
            // Validate data
            if (!this.validateData(data)) {
                throw new Error('Please fill in all fields with valid values');
            }
            
            // Send prediction request
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.displayResult(result);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    validateData(data) {
        // Check if all required fields are filled
        const requiredFields = [
            'youtube_learning', 'coursera', 'udemy', 'google_classroom',
            'khan_academy', 'byjus', 'game_hours', 'educational_games',
            'instagram', 'snapchat', 'whatsapp', 'youtube_social',
            'telegram', 'twitter', 'facebook', 'social_interactions'
        ];
        
        for (let field of requiredFields) {
            if (isNaN(data[field]) || data[field] < 0) {
                return false;
            }
        }
        
        return true;
    }
    
    displayResult(result) {
        const { prediction, confidence, probabilities } = result;
        
        // Set prediction result with appropriate styling
        this.predictionResult.textContent = `Prediction: ${prediction}`;
        this.predictionResult.className = `prediction-result ${prediction.toLowerCase()}`;
        
        // Display confidence score
        this.confidenceScore.textContent = `Confidence: ${(confidence * 100).toFixed(1)}%`;
        
        // Show result section with animation
        this.resultSection.classList.remove('hidden');
        this.resultSection.classList.add('show');
        
        // Scroll to result
        setTimeout(() => {
            this.resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
        
        // Log detailed results for debugging
        console.log('Prediction Results:', {
            prediction,
            confidence,
            probabilities
        });
    }
    
    showLoading() {
        this.loadingSection.classList.remove('hidden');
        this.predictBtn.disabled = true;
        this.predictBtn.textContent = '⏳ Predicting...';
    }
    
    hideLoading() {
        this.loadingSection.classList.add('hidden');
        this.predictBtn.disabled = false;
        this.predictBtn.textContent = '🔮 Predict Performance';
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorSection.classList.remove('hidden');
        
        // Scroll to error
        this.errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.errorSection.classList.add('hidden');
        }, 5000);
    }
    
    hideResults() {
        this.resultSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
    }
    
    resetForm() {
        this.form.reset();
        this.hideResults();
        
        // Clear any validation states
        const inputs = this.form.querySelectorAll('input');
        inputs.forEach(input => {
            input.setCustomValidity('');
        });
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    loadSampleData() {
        // Add sample data button for testing
        const sampleBtn = document.createElement('button');
        sampleBtn.type = 'button';
        sampleBtn.className = 'btn-secondary';
        sampleBtn.textContent = '📝 Load Sample Data';
        sampleBtn.style.marginRight = '10px';
        
        sampleBtn.addEventListener('click', () => {
            this.fillSampleData();
        });
        
        // Insert before predict button
        this.predictBtn.parentNode.insertBefore(sampleBtn, this.predictBtn);
    }
    
    fillSampleData() {
        // Sample data representing different student profiles
        const sampleProfiles = [
            {
                name: 'High Performer',
                data: {
                    youtube_learning: 2.5,
                    coursera: 1.8,
                    udemy: 1.2,
                    google_classroom: 2.0,
                    khan_academy: 1.5,
                    byjus: 1.0,
                    game_hours: 0.5,
                    educational_games: 0.8,
                    instagram: 0.3,
                    snapchat: 0.2,
                    whatsapp: 0.5,
                    youtube_social: 0.4,
                    telegram: 0.1,
                    twitter: 0.1,
                    facebook: 0.1,
                    social_interactions: 8
                }
            },
            {
                name: 'Medium Performer',
                data: {
                    youtube_learning: 1.0,
                    coursera: 0.5,
                    udemy: 0.3,
                    google_classroom: 0.8,
                    khan_academy: 0.5,
                    byjus: 0.2,
                    game_hours: 1.5,
                    educational_games: 0.5,
                    instagram: 1.2,
                    snapchat: 0.8,
                    whatsapp: 1.0,
                    youtube_social: 1.5,
                    telegram: 0.3,
                    twitter: 0.5,
                    facebook: 0.4,
                    social_interactions: 5
                }
            },
            {
                name: 'Low Performer',
                data: {
                    youtube_learning: 0.2,
                    coursera: 0.1,
                    udemy: 0.0,
                    google_classroom: 0.1,
                    khan_academy: 0.0,
                    byjus: 0.0,
                    game_hours: 3.0,
                    educational_games: 0.2,
                    instagram: 2.5,
                    snapchat: 1.8,
                    whatsapp: 2.0,
                    youtube_social: 2.8,
                    telegram: 0.8,
                    twitter: 1.2,
                    facebook: 1.0,
                    social_interactions: 2
                }
            }
        ];
        
        // Randomly select a profile
        const profile = sampleProfiles[Math.floor(Math.random() * sampleProfiles.length)];
        
        // Fill form with sample data
        Object.entries(profile.data).forEach(([key, value]) => {
            const input = document.getElementById(key);
            if (input) {
                input.value = value;
            }
        });
        
        // Show notification
        this.showNotification(`Loaded sample data for: ${profile.name}`);
    }
    
    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            font-weight: 500;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentPerformancePredictor();
});

// Add some utility functions
function formatHours(hours) {
    return `${hours.toFixed(1)} hours`;
}

function calculateTotalHours(data) {
    const educationFields = ['youtube_learning', 'coursera', 'udemy', 'google_classroom', 'khan_academy', 'byjus'];
    const gamingFields = ['game_hours', 'educational_games'];
    const socialFields = ['instagram', 'snapchat', 'whatsapp', 'youtube_social', 'telegram', 'twitter', 'facebook'];
    
    const education = educationFields.reduce((sum, field) => sum + (data[field] || 0), 0);
    const gaming = gamingFields.reduce((sum, field) => sum + (data[field] || 0), 0);
    const social = socialFields.reduce((sum, field) => sum + (data[field] || 0), 0);
    
    return {
        education,
        gaming,
        social,
        total: education + gaming + social
    };
}

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StudentPerformancePredictor, formatHours, calculateTotalHours };
}
