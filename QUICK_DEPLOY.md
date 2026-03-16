# Quick Deployment Setup - SmartCLV

## ⚠️ Git Not Installed

Git is not installed on your system. Here are two options to deploy:

---

## Option 1: Install Git and Use Command Line (Recommended)

### Step 1: Install Git
1. Download Git from: https://git-scm.com/download/win
2. Run the installer (use default settings)
3. Restart PowerShell

### Step 2: Run These Commands
```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"

git init
git add .
git commit -m "Initial commit - SmartCLV project"
git branch -M main

# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/SmartCLV.git
git push -u origin main
```

---

## Option 2: Use GitHub Desktop (Easier - No Command Line)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in with your GitHub account

### Step 2: Create Repository
1. Open GitHub Desktop
2. Click "File" → "Add local repository"
3. Browse to: `c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV`
4. Click "Create repository"
5. Click "Publish repository" button
6. Repository name: `SmartCLV`
7. ✅ Keep "Public" checked
8. Click "Publish repository"

### Step 3: Your code is now on GitHub! ✅

---

## Option 3: Manual Upload (Quick but Less Flexible)

### Step 1: Create ZIP File
1. Go to: `c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV`
2. Select all files EXCEPT:
   - `venv` folder
   - `data/smartclv.db` file
   - `__pycache__` folders
3. Right-click → "Send to" → "Compressed (zipped) folder"
4. Name it: `SmartCLV.zip`

### Step 2: Upload to GitHub
1. Go to: https://github.com/new
2. Repository name: `SmartCLV`
3. Make it **Public**
4. Click "Create repository"
5. Click "uploading an existing file"
6. Drag and drop your `SmartCLV.zip`
7. Click "Commit changes"

---

## Next: Deploy to Streamlit Cloud

Once your code is on GitHub (using any option above):

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Fill in**:
   - Repository: `YOUR_USERNAME/SmartCLV`
   - Branch: `main`
   - Main file: `dashboard/app.py`
5. **Click** "Deploy!"

**Your live URL will be**:
```
https://YOUR_USERNAME-smartclv-dashboard-app-xxxxx.streamlit.app
```

---

## ✅ Files Ready for Deployment

I've prepared these files:
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.gitignore` - Excludes unnecessary files
- ✅ `DEPLOYMENT_INSTRUCTIONS.md` - Full guide
- ✅ `requirements.txt` - All dependencies
- ✅ `README.md` - Project documentation

---

## 🎯 Recommended: GitHub Desktop

**Why?**
- ✅ No command line needed
- ✅ Visual interface
- ✅ Easy to update later
- ✅ Free and beginner-friendly

**Download**: https://desktop.github.com/

---

## 📞 Need Help?

If you get stuck:
1. Check `DEPLOYMENT_INSTRUCTIONS.md` for detailed steps
2. GitHub Desktop tutorial: https://docs.github.com/en/desktop
3. Streamlit deployment docs: https://docs.streamlit.io/streamlit-community-cloud

---

**Choose your preferred option above and your SmartCLV dashboard will be live in 10 minutes!** 🚀
