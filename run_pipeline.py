import argparse
import subprocess

# ------------------ Existing Phase Imports ------------------
from src.phase1_data_cleaning import run_phase1
from src.phase2_feature_engineering import run_phase2
from src.phase3_model_training import run_phase3
from src.phase4_model_evaluation import run_phase4
from src.phase5_explainability import run_phase5

# ------------------ Training Function ------------------
def run_training():
    """Runs the full train_model.py script"""
    subprocess.run(["python", "training/train_model.py"], check=True)

# ------------------ Pipeline Function ------------------
def run_pipeline():
    """Runs the full 5-phase ML pipeline"""
    print("🚀 Starting GrievTech ML Pipeline...\n")

    # Phase 1: Data Cleaning
    df_clean = run_phase1(limit=100000)
    print("✅ Phase 1 complete: Data cleaned")

    # Phase 2: Feature Engineering
    df_features = run_phase2(df_clean)
    print("✅ Phase 2 complete: Features created")

    # Phase 3: Model Training
    model, X_test, y_test, le_borough, le_agency, le_target = run_phase3(df_features)
    print("✅ Phase 3 complete: Model trained")

    # Phase 4: Model Evaluation
    y_pred = run_phase4(model, X_test, y_test, le_borough, le_agency, le_target)
    print("✅ Phase 4 complete: Model evaluated")

    # Phase 5: Explainability
    run_phase5(model, X_test)
    print("✅ Phase 5 complete: Explainability done")

# ------------------ CLI ------------------
def main():
    parser = argparse.ArgumentParser(description="GrievTech ML Pipeline CLI")
    parser.add_argument(
        "--train",
        action="store_true",
        help="Run training pipeline using training/train_model.py"
    )
    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="Run full 5-phase ML pipeline"
    )

    args = parser.parse_args()

    if args.train:
        print("🏋️ Running training script...")
        run_training()
    elif args.pipeline:
        print("🏃 Running full 5-phase ML pipeline...")
        run_pipeline()
    else:
        print("No command specified. Use --train or --pipeline")

if __name__ == "__main__":
    main()