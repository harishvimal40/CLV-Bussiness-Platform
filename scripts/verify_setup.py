"""
Verification script for Phase 1 setup
Run this to ensure all dependencies are installed correctly
"""

import sys

def verify_imports():
    """Verify all required packages can be imported"""
    
    packages = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning',
        'xgboost': 'Gradient boosting',
        'tensorflow': 'Deep learning',
        'streamlit': 'Dashboard',
        'plotly': 'Visualization',
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical visualization',
        'shap': 'Explainable AI',
        'nltk': 'NLP',
        'textblob': 'Sentiment analysis',
        'flask': 'Web framework',
        'sqlalchemy': 'Database ORM',
    }
    
    print("=" * 60)
    print("SmartCLV Setup Verification")
    print("=" * 60)
    print()
    
    failed = []
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✓ {package:20s} - {description}")
        except ImportError:
            print(f"✗ {package:20s} - {description} [FAILED]")
            failed.append(package)
    
    print()
    print("=" * 60)
    
    if failed:
        print(f"❌ {len(failed)} package(s) failed to import:")
        for pkg in failed:
            print(f"   - {pkg}")
        print("\nRun: pip install -r requirements.txt")
        return False
    else:
        print("✅ All packages imported successfully!")
        print("Phase 1 setup is complete and verified.")
        return True

def check_directory_structure():
    """Verify directory structure exists"""
    import os
    
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/synthetic',
        'models/clv_models',
        'models/churn_models',
        'src/data_preprocessing',
        'src/feature_engineering',
        'src/model_training',
        'dashboard',
        'tests',
        'notebooks',
        'config',
    ]
    
    print("\nDirectory Structure Check:")
    print("-" * 60)
    
    all_exist = True
    for directory in required_dirs:
        exists = os.path.exists(directory)
        status = "✓" if exists else "✗"
        print(f"{status} {directory}")
        if not exists:
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("\n")
    
    # Check directories
    dirs_ok = check_directory_structure()
    
    print("\n")
    
    # Check imports
    imports_ok = verify_imports()
    
    print("\n")
    
    if dirs_ok and imports_ok:
        print("🎉 Phase 1 setup completed successfully!")
        print("You can now proceed to Phase 2: Data Collection")
        sys.exit(0)
    else:
        print("⚠️  Some issues detected. Please fix them before proceeding.")
        sys.exit(1)
