# SmartCLV Deployment Guide

## 🚀 Deploy to Streamlit Community Cloud

Follow these steps to deploy your SmartCLV dashboard online for free.

---

## Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Create new repository**:
   - Repository name: `SmartCLV`
   - Description: `AI-Powered Customer Lifetime Value Prediction System`
   - Visibility: **Public** (required for free Streamlit hosting)
   - ✅ Do NOT initialize with README (we already have one)
3. **Click "Create repository"**

---

## Step 2: Push Code to GitHub

Open PowerShell in your project directory and run:

```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"

# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SmartCLV project"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/SmartCLV.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 3: Deploy to Streamlit Community Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the deployment form**:
   - **Repository**: `YOUR_USERNAME/SmartCLV`
   - **Branch**: `main`
   - **Main file path**: `dashboard/app.py`
   - **App URL** (optional): Choose a custom subdomain like `smartclv-demo`

5. **Advanced settings** (click to expand):
   - Python version: `3.9` (or your version)
   - Add secrets if needed (not required for this project)

6. **Click "Deploy!"**

---

## Step 4: Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- Build time: ~2-5 minutes
- You'll see build logs in real-time

---

## Step 5: Access Your Live Dashboard

Once deployed, your app will be available at:

```
https://YOUR_USERNAME-smartclv-dashboard-app-xxxxx.streamlit.app
```

Or your custom URL:
```
https://smartclv-demo.streamlit.app
```

---

## 📝 Important Notes

### Data Handling
Since the database file (`data/smartclv.db`) is excluded from Git, you need to:

**Option A**: Generate data on first run
- The app will run `generate_synthetic_data.py` automatically if database is missing
- Already configured in the deployment

**Option B**: Include pre-generated data
- Uncomment the data files in `.gitignore`
- Push the CSV files to GitHub
- The app will load from CSV instead of database

### Model Files
- Model files in `models/` folder are included in Git
- If they're too large (>100MB), use Git LFS or regenerate on deployment

---

## 🔧 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Ensure Python version compatibility
- Check build logs for specific errors

### App Crashes
- Check if data files are available
- Verify all imports work
- Check Streamlit logs in the dashboard

### Database Issues
- The app uses SQLite which works on Streamlit Cloud
- Ensure database is created on first run
- Check file paths are relative, not absolute

---

## 🔄 Updating Your Deployed App

To update your live app:

```powershell
# Make changes to your code
git add .
git commit -m "Update description"
git push
```

Streamlit will automatically redeploy within 1-2 minutes!

---

## 📊 Monitoring

- **View logs**: Click "Manage app" → "Logs" in Streamlit Cloud
- **Restart app**: Click "Reboot app" if needed
- **Analytics**: View usage stats in Streamlit Cloud dashboard

---

## 🎯 Your Deployment Checklist

- [ ] Create GitHub account (if needed)
- [ ] Create new repository on GitHub
- [ ] Push code to GitHub
- [ ] Sign up for Streamlit Community Cloud
- [ ] Deploy app
- [ ] Test live URL
- [ ] Share with others!

---

## 🌐 Alternative: Quick Demo with ngrok

For a quick temporary URL (no GitHub needed):

```powershell
# Download ngrok from https://ngrok.com/download
# Extract and run:
ngrok http 8501
```

You'll get a temporary URL like: `https://xxxx.ngrok-free.app`

**Note**: This URL expires when you close ngrok.

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Report issues in your repository

---

**Ready to deploy?** Follow the steps above and your SmartCLV dashboard will be live in minutes! 🚀
