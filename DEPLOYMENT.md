# 🚀 Render Deployment Guide for FoodSaver

## Quick Deploy

1. **Connect Repository**: https://github.com/shraddhas-20/FoodSaver.git
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python app.py`
4. **Set Environment Variables** (see below)

## Required Environment Variables

Set these in your Render dashboard:

```bash
SECRET_KEY=your-super-secret-production-key-here
HUGGINGFACE_API_KEY=your-huggingface-api-key
FLASK_ENV=production
PORT=10000
```

## Deployment Settings

- **Branch**: `home`
- **Root Directory**: `/` (files are in root)
- **Auto Deploy**: Yes
- **Runtime**: Python 3

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Set `SECRET_KEY` and `HUGGINGFACE_API_KEY` in Render dashboard
   - Run `python3 test_deployment.py` locally to verify setup

2. **Dependencies Issues**
   - All problematic packages (opencv, sklearn) have been removed
   - Only essential packages remain in requirements.txt

3. **Port Issues**
   - App automatically uses `PORT` environment variable from Render
   - Defaults to 5001 for local development

### Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run deployment test
python3 test_deployment.py

# Start app locally
python3 app.py
```

### Production URLs

After deployment, your app will be available at:
- Main App: `https://your-app-name.onrender.com`
- API Test: `https://your-app-name.onrender.com/test`

## Features Included

✅ AI Food Recognition (Hugging Face Vision API)  
✅ User Authentication & Registration  
✅ Food Inventory Management  
✅ Interactive Chatbot  
✅ Responsive UI with Contact Page  
✅ SQLite Database  
✅ Production-Ready Configuration  

## Security

- Environment variables for sensitive data
- Secure secret keys
- No hardcoded API keys in code
- Production/development mode switching

---

**Ready for deployment!** 🎉
