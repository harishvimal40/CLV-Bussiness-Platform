"""
SmartCLV Main Pipeline
Runs the entire data processing and modeling workflow
"""

import subprocess
import sys
from pathlib import Path
import time

BASE_DIR = Path(__file__).parent

def run_script(script_path):
    print(f"\n{'='*50}")
    print(f"Running: {script_path}")
    print(f"{'='*50}\n")
    
    start_time = time.time()
    try:
        # Use the current python interpreter
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False # Let output flow to terminal
        )
        duration = time.time() - start_time
        print(f"\n[OK] Success! (Time: {duration:.2f}s)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Error running {script_path}")
        print(f"Exit Code: {e.returncode}")
        return False

def main():
    print("[START] Starting SmartCLV System Pipeline...\n")
    
    scripts = [
        # Data Pipeline
        # (Assuming database setup is already done)
        # "scripts/generate_synthetic_data.py", 
        
        # Preprocessing
        "src/data_preprocessing/cleaner.py",
        "src/feature_engineering/features.py",
        "src/data_preprocessing/normalizer.py",
        
        # Models
        "src/model_training/trainer.py", # CLV
        "src/prediction/predictor.py",   # CLV Prediction
        "src/model_training/churn_trainer.py", # Churn
        "src/prediction/churn_predictor.py",   # Churn Prediction
        
        # Action
        "src/recommendation/engine.py",
        
        # Explainability
        "src/explainability/shap_explainer.py"
    ]
    
    for script in scripts:
        full_path = BASE_DIR / script
        if not full_path.exists():
            # Try checking if it's in a subdirectory relative to root? 
            # Actually BASE_DIR is 'src/...' if we run from root? 
            # No, BASE_DIR = Path(__file__).parent which is 'src' if main_pipeline is in src?
            # Wait, user put main_pipeline in 'src'.
            # Scripts paths in list are relative to 'SmartCLV' root if we run from root.
            # Let's verify where main_pipeline is.
            pass
            
    # Adjust paths based on execution from ROOT
    root_dir = BASE_DIR.parent
    
    pipeline_steps = [
        root_dir / "src/data_preprocessing/cleaner.py",
        root_dir / "src/feature_engineering/features.py",
        root_dir / "src/data_preprocessing/normalizer.py",
        root_dir / "src/model_training/trainer.py",
        root_dir / "src/prediction/predictor.py",
        root_dir / "src/model_training/churn_trainer.py",
        root_dir / "src/prediction/churn_predictor.py",
        root_dir / "src/recommendation/engine.py",
        root_dir / "src/explainability/shap_explainer.py"
    ]
    
    failed = False
    for step in pipeline_steps:
        if not step.exists():
            print(f"[WARN] Script not found: {step}")
            continue
            
        if not run_script(step):
            failed = True
            break
            
    if not failed:
        print("\n[SUCCESS] Pipeline Completed Successfully!")
    else:
        print("\n[FAIL] Pipeline Failed.")

if __name__ == "__main__":
    main()
