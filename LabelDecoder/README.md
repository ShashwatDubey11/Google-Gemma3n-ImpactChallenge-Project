# 📷 Label Decoder - AI-Powered Product Label Analyzer

An intelligent Streamlit application that uses Google Gemini AI to analyze product labels and provide detailed insights about ingredients, health impacts, allergens, and nutritional information.

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
LabelDecoder/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── setup.sh                   # Setup script
├── .env.example               # Environment variables template
├── config/
│   └── settings.py            # Application configuration
├── database/
│   └── db_manager.py          # Database operations
├── utils/
│   ├── gemini_analyzer.py     # Google Gemini AI integration
│   └── image_handler.py       # Image processing utilities
└── uploads/                   # Uploaded images storage
    └── thumbnails/           # Generated thumbnails
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Internet connection for AI analysis

### Installation

1. **Clone or download the project**
   ```bash
   cd LabelDecoder
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

3. **Configure your API key**
   - Edit the `.env` file
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
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
# Install dependencies
pip install streamlit pillow google-generativeai python-dotenv

# Create directories
mkdir -p uploads uploads/thumbnails database

# Copy environment template
cp .env.example .env

# Edit .env file with your API key
nano .env

# Run the app
streamlit run app.py
```

## 📖 How to Use

### 1. **Get Your API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

### 2. **Upload an Image**
   - Use the "Take Photo" tab to capture images directly
   - Or use "Upload File" to select images from your device
   - Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

### 3. **Analyze the Label**
   - Click the "Analyze This Label" button
   - Wait for AI processing (usually 10-30 seconds)
   - View detailed results including health ratings and recommendations

### 4. **Review Results**
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
   - Generates thumbnails

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
DATABASE_URL=sqlite:///database/label_decoder.db
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

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add environment variables in Streamlit Cloud settings
4. Deploy automatically

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔒 Security Notes

- Keep your API key secure and never commit it to version control
- The `.env` file should be in your `.gitignore`
- Images are stored locally and not sent to external services except Google Gemini
- Database contains no personal information

## 🐛 Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**
   - Install missing packages: `pip install -r requirements.txt`

2. **API key errors**
   - Verify your `.env` file has the correct API key
   - Check API key permissions in Google AI Studio

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

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

**Enjoy analyzing product labels with AI! 🎉**
