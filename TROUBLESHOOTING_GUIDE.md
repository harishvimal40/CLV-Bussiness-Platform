# SmartCLV - Complete Setup & Troubleshooting Guide

## ✅ SYSTEM STATUS CHECK

**Date**: February 14, 2026
**Status**: ALL SYSTEMS OPERATIONAL ✅

### Environment Verification:
- ✅ Python Version: 3.14.0
- ✅ Virtual Environment: Active
- ✅ Database: smartclv.db exists
- ✅ All Core Packages: Installed
- ✅ Data Validation: PASSED

### Package Status:
```
✅ pandas 2.3.3
✅ numpy 2.4.2
✅ scikit-learn 1.8.0
✅ xgboost 3.2.0
✅ streamlit 1.54.0
✅ plotly 6.5.2
✅ shap 0.50.0
✅ matplotlib 3.10.8
✅ seaborn 0.13.2
```

### Data Validation Results:
```
✅ customers: 10,000 records
✅ transactions: 62,284 records
✅ behavioral_data: 276,588 records
✅ engagement_data: 550,501 records
✅ feedback: 5,986 records
✅ Data integrity: PASSED
✅ All validation checks: PASSED
```

---

## 🚀 HOW TO RUN THE PROJECT (3 SIMPLE STEPS)

### **Step 1: Open PowerShell**
Press `Windows + X` → Select "Windows PowerShell" or "Terminal"

### **Step 2: Navigate and Activate**
```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
.\venv\Scripts\activate
```

### **Step 3: Run the Program**

**Option A: Run Complete Pipeline**
```powershell
python src\main_pipeline.py
```
This runs all 8 phases (~70 seconds)

**Option B: Launch Dashboard Only** (if pipeline already ran)
```powershell
streamlit run dashboard\app.py
```
Opens at: http://localhost:8501

---

## 📋 COMPLETE EXECUTION COMMANDS

### Full Workflow (Copy & Paste All):
```powershell
# Navigate to project
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"

# Activate virtual environment
.\venv\Scripts\activate

# Run complete pipeline
python src\main_pipeline.py

# Launch dashboard
streamlit run dashboard\app.py
```

**That's it!** Your dashboard will open automatically.

---

## 🔧 TROUBLESHOOTING GUIDE

### Problem 1: "Virtual environment not found"

**Solution:**
```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### Problem 2: "Module not found" errors

**Solution:**
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

**For specific missing packages:**
```powershell
pip install pandas numpy scikit-learn xgboost streamlit plotly shap
```

---

### Problem 3: "Database not found"

**Solution:**
```powershell
python scripts\setup_database.py
python scripts\generate_synthetic_data.py
```

---

### Problem 4: "Port 8501 already in use"

**Solution A: Kill existing process**
```powershell
# Find process using port 8501
netstat -ano | findstr :8501

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Solution B: Use different port**
```powershell
streamlit run dashboard\app.py --server.port=8502
```

---

### Problem 5: Dashboard shows errors

**Solution:**
```powershell
# Clear Streamlit cache
streamlit cache clear

# Restart dashboard
streamlit run dashboard\app.py
```

---

### Problem 6: "Permission denied" errors

**Solution:**
Run PowerShell as Administrator:
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Navigate to project and run commands

---

### Problem 7: Models not found

**Solution:**
```powershell
# Retrain models
python src\model_training\trainer.py
python src\model_training\churn_trainer.py
```

---

### Problem 8: Data files missing

**Solution:**
```powershell
# Run complete pipeline to regenerate all files
python src\main_pipeline.py
```

---

## 🧪 TESTING & VALIDATION

### Validate System Health:
```powershell
# Check data integrity
python scripts\validate_data.py

# Run unit tests
pytest tests\

# Verify all imports
python -c "import pandas, numpy, sklearn, xgboost, streamlit, shap; print('OK')"
```

---

## 📁 VERIFY FILE STRUCTURE

Your project should have these folders:

```
SmartCLV/
├── config/          ✅ Configuration files
├── dashboard/       ✅ Streamlit app
├── data/            ✅ Database and processed files
├── docs/            ✅ Documentation
├── models/          ✅ Trained models
├── scripts/         ✅ Utility scripts
├── src/             ✅ Source code
├── tests/           ✅ Unit tests
├── venv/            ✅ Virtual environment
└── requirements.txt ✅ Dependencies
```

**Check if folder exists:**
```powershell
dir "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
```

---

## 🎯 QUICK DIAGNOSTICS

### Run This to Check Everything:
```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
.\venv\Scripts\activate

# Check Python version
python --version

# Check installed packages
pip list | findstr "pandas numpy scikit-learn xgboost streamlit"

# Validate data
python scripts\validate_data.py

# Test imports
python -c "import pandas, numpy, sklearn, xgboost, streamlit, shap; print('All packages OK!')"
```

If all commands succeed, your system is ready! ✅

---

## 🚨 COMMON ERROR MESSAGES & FIXES

### Error: "UnicodeEncodeError"
**Fix:** Already handled in code (using ASCII characters)

### Error: "Cannot setitem on Categorical"
**Fix:** Already handled in code (type conversion before fillna)

### Error: "Streamlit command not found"
**Fix:**
```powershell
.\venv\Scripts\activate
pip install streamlit
```

### Error: "Database is locked"
**Fix:**
```powershell
# Close all Python processes
taskkill /IM python.exe /F

# Restart
python src\main_pipeline.py
```

---

## 📊 EXPECTED OUTPUT

When you run `python src\main_pipeline.py`, you should see:

```
============================================================
SmartCLV Data Cleaning Pipeline
============================================================
Loading data from database...
Loaded 10000 customers
...
[SUCCESS] Data cleaning complete!

============================================================
SmartCLV Feature Engineering Pipeline
============================================================
...
[SUCCESS] Features saved

[Model Training Output]
XGBoost -> RMSE: 0.02, R²: 0.9995
RandomForest -> F1: 0.8037, AUC: 0.8975

[SUCCESS] Pipeline Completed Successfully!
```

**Total Time**: ~70 seconds

---

## 🌐 DASHBOARD ACCESS

After running `streamlit run dashboard\app.py`:

**Local URL**: http://localhost:8501
**Network URL**: http://192.168.x.x:8501

The dashboard has 5 tabs:
1. 📊 Overview
2. 💰 CLV Analysis
3. 📉 Churn Risk
4. 💡 Decisions
5. 🧠 Explainability

---

## ✅ PRE-FLIGHT CHECKLIST

Before running, verify:

- [ ] PowerShell is open
- [ ] Navigated to project directory
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] Database exists (`data\smartclv.db`)
- [ ] All packages installed (`pip list`)
- [ ] No other Streamlit instances running

---

## 🎓 STEP-BY-STEP FIRST RUN

**For absolute beginners:**

1. **Open PowerShell**
   - Press Windows key
   - Type "PowerShell"
   - Press Enter

2. **Copy and paste this:**
   ```powershell
   cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
   ```
   Press Enter

3. **Copy and paste this:**
   ```powershell
   .\venv\Scripts\activate
   ```
   Press Enter
   (You should see `(venv)` appear)

4. **Copy and paste this:**
   ```powershell
   python src\main_pipeline.py
   ```
   Press Enter
   (Wait ~70 seconds)

5. **Copy and paste this:**
   ```powershell
   streamlit run dashboard\app.py
   ```
   Press Enter
   (Browser opens automatically)

**Done!** 🎉

---

## 📞 SUPPORT

If you encounter issues not covered here:

1. Check `PROGRAM_OUTPUT.md` for expected output
2. Check `EXECUTION_SUMMARY.md` for detailed results
3. Review error messages carefully
4. Ensure all files are in correct locations

---

## 🔄 RESET EVERYTHING (Nuclear Option)

If nothing works, start fresh:

```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"

# Delete virtual environment
Remove-Item -Recurse -Force venv

# Recreate environment
python -m venv venv
.\venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt

# Regenerate database
python scripts\setup_database.py
python scripts\generate_synthetic_data.py

# Run pipeline
python src\main_pipeline.py

# Launch dashboard
streamlit run dashboard\app.py
```

---

## ✅ FINAL STATUS

**Your SmartCLV project is READY TO RUN!**

All systems operational:
- ✅ Python 3.14.0
- ✅ All packages installed
- ✅ Database validated
- ✅ Data integrity confirmed
- ✅ 10,000 customers ready
- ✅ Models can be trained
- ✅ Dashboard ready to launch

**Just run:**
```powershell
cd "c:\New folder (2)\OneDrive\Desktop\Mini project\SmartCLV"
.\venv\Scripts\activate
python src\main_pipeline.py
streamlit run dashboard\app.py
```

**Your SmartCLV system is production-ready!** 🚀

---

*Last Updated: February 14, 2026*
*Status: All Systems Operational ✅*
