# 📷 Label Decoder - AI-Powered Product Label Analyzer

An intelligent Streamlit application that uses Google Gemini AI to analyze product labels and provide detailed insights about ingredients, health impacts, allergens, and nutritional information.

## 🌐 **Try It Live!**
**🚀 Access the app directly:** [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)

*No installation required! Just upload a product label image and get instant AI-powered analysis.*

## 🌟 Features

- **📸 Image Capture**: Take photos directly from your camera or upload image files
- **🤖 AI Analysis**: Powered by Google Gemini for accurate label interpretation
- **💾 Database Storage**: Automatic storage of images and analysis results
- **📊 Health Ratings**: Get health scores and recommendations for products
- **⚠️ Allergen Detection**: Identify potential allergens and warnings
- **📈 Analysis History**: Track your previous analyses
- **🎨 User-Friendly Interface**: Clean, intuitive Streamlit web interface

## 🏗️ Project Structure

```
Google-Gemma3n-ImpactChallenge-Project/
├── README.md                   # This file
└── LabelDecoder/              # Main application directory
    ├── app.py                 # Main Streamlit application
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Environment variables (your API key)
    ├── .env.example          # Environment variables template
    ├── config/
    │   └── settings.py       # Application configuration
    ├── database/
    │   └── db_manager.py     # Database operations
    ├── utils/
    │   ├── gemini_analyzer.py # Google Gemini AI integration
    │   └── image_handler.py  # Image processing utilities
    └── uploads/              # Uploaded images storage
        └── thumbnails/       # Generated thumbnails
```

## 🚀 Quick Start

### 🌐 **Option 1: Use the Live App (Recommended)**
**Simply visit:** [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)
- No installation required
- No API key setup needed
- Ready to use immediately
- Upload any product label image and get instant analysis

### 🛠️ **Option 2: Run Locally (For Developers)**

#### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Internet connection for AI analysis

#### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShashwatDubey11/Google-Gemma3n-ImpactChallenge-Project.git
   cd Google-Gemma3n-ImpactChallenge-Project/LabelDecoder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   - Edit the `.env` file in the `LabelDecoder` directory
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ENVIRONMENT=development
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start analyzing product labels!

### Manual Installation

If you prefer manual setup:

```bash
# Navigate to the project directory
cd LabelDecoder

# Install dependencies
pip install streamlit pillow google-generativeai python-dotenv

# Create directories (if needed)
mkdir -p uploads database

# Add your API key to .env file
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Run the app
streamlit run app.py
```

## 📖 How to Use

### 🌐 **Using the Live App** (Easiest Way)
1. **Visit the app:** [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)
2. **Upload an image:** Use either "Take Photo" or "Upload File" tabs
3. **Analyze:** Click "Analyze This Label" button
4. **View results:** Get detailed analysis including health ratings and recommendations

### 🛠️ **For Local Development**

#### 1. **Get Your API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file in the `LabelDecoder` directory

#### 2. **Upload an Image**
   - Use the "Take Photo" tab to capture images directly
   - Or use "Upload File" to select images from your device
   - Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

#### 3. **Analyze the Label**
   - Click the "Analyze This Label" button
   - Wait for AI processing (usually 10-30 seconds)
   - View detailed results including health ratings and recommendations

#### 4. **Review Results**
   - Health rating (1-10 scale)
   - Key ingredients breakdown
   - Allergen warnings
   - Detailed analysis report
   - Storage in analysis history

## 🔧 How It Works

### Application Components

1. **Frontend (Streamlit)**
   - User interface for image upload
   - Results display and visualization
   - Configuration management

2. **Database (SQLite)**
   - Stores uploaded image metadata
   - Saves analysis results
   - Tracks user history

3. **AI Integration (Google Gemini)**
   - Processes product label images
   - Extracts text and analyzes content
   - Provides health and safety insights

4. **Image Processing**
   - Validates uploaded files
   - Handles image storage
   - Optimizes images for AI processing

### Data Flow

```
User Upload → Image Validation → Storage → AI Analysis → Results Display → Database Storage
```

1. User uploads an image via Streamlit interface
2. Image is validated and saved to local storage
3. Image metadata is stored in SQLite database
4. Image is sent to Google Gemini for analysis
5. AI response is processed and structured
6. Results are displayed to user
7. Analysis results are saved to database

## 📊 Database Schema

### `uploaded_images` Table
- `id`: Primary key
- `filename`: Generated unique filename
- `original_filename`: User's original filename
- `file_path`: Storage path
- `file_size`: File size in bytes
- `upload_timestamp`: When uploaded
- `analysis_status`: Processing status

### `analysis_results` Table
- `id`: Primary key
- `image_id`: Foreign key to uploaded_images
- `analysis_text`: Raw AI response
- `analysis_json`: Structured data
- `analysis_timestamp`: When analyzed
- `model_used`: AI model version

## 🛠️ Configuration

### Environment Variables (.env)
```env
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=development
```

### Application Settings (config/settings.py)
- API configuration
- File upload limits
- Database settings
- UI customization

## 🤖 AI Analysis Features

The Google Gemini integration provides:

- **Product Identification**: Name, brand, type
- **Ingredient Analysis**: Main components, preservatives, additives
- **Nutritional Information**: Calories, nutrients, serving sizes
- **Health Assessment**: Safety ratings, recommendations
- **Allergen Detection**: Common allergens and warnings
- **Additional Details**: Expiry dates, certifications, storage

## 🚀 Deployment

### 🌐 **Live Production App**
The app is currently deployed and accessible at:
**[labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)**

### 📱 **Mobile Friendly**
The app works perfectly on:
- 📱 Mobile phones
- 📟 Tablets  
- 💻 Desktop computers
- 📷 Camera functionality available on mobile devices

### 🛠️ **For Developers - Local Development**
```bash
cd LabelDecoder
streamlit run app.py
```

### ☁️ **Deploy Your Own Version on Streamlit Cloud**
1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set the main file path to `LabelDecoder/app.py`
4. Add environment variables in Streamlit Cloud settings:
   - `GEMINI_API_KEY`: Your Google Gemini API key
5. Deploy automatically

### 🐳 **Docker Deployment (Optional)**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY LabelDecoder/ .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔒 Security Notes

- Keep your API key secure and never commit it to version control
- The `.env` file should be in your `.gitignore`
- Images are stored locally and not sent to external services except Google Gemini
- Database contains no personal information

## 🐛 Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**
   ```bash
   cd LabelDecoder
   pip install -r requirements.txt
   ```

2. **API key errors**
   - Verify your `.env` file has the correct API key
   - Check API key permissions in Google AI Studio
   - Ensure the `.env` file is in the `LabelDecoder` directory

3. **Image upload failures**
   - Check file size (max 10MB)
   - Verify file format is supported
   - Ensure `uploads` directory exists

4. **Database errors**
   - Check write permissions in project directory
   - Verify `database` directory exists

### Getting Help

- Check the Streamlit logs in your terminal
- Verify all dependencies are installed
- Ensure your API key is valid and has credits

## 📈 Future Enhancements

Potential improvements you could add:

- **Multiple Language Support**: Analyze labels in different languages
- **Batch Processing**: Upload multiple images at once
- **Export Features**: Download analysis results as PDF/Excel
- **User Accounts**: Personal analysis history and preferences
- **Comparison Tool**: Compare multiple products side by side
- **Mobile App**: React Native or Flutter mobile version
- **API Endpoint**: RESTful API for integration with other apps

## 🔗 Links

- **🌐 Live App**: [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)
- **📚 Documentation**: [Streamlit Docs](https://docs.streamlit.io)
- **🔑 Get API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **☁️ Deploy Your Own**: [Streamlit Cloud](https://streamlit.io/cloud)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 🏆 About This Project

This project was created as part of the Google Gemma 3 Impact Challenge, demonstrating the power of AI in helping consumers make informed decisions about the products they consume.

**🌐 Try it now:** [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)

---

**Enjoy analyzing product labels with AI! 🎉**

## 📞 Contact

For questions or support:
- 🌐 Try the live app: [labeldecoder.streamlit.app](https://labeldecoder.streamlit.app)
- 🐛 Report issues: Open an issue on this repository
- 💡 Feature requests: Submit via GitHub issues
