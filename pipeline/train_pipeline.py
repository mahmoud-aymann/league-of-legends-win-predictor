"""
Utility script to train the League of Legends win predictor pipeline.

The script loads the CSV dataset, splits it into train/test folds, trains a
standardized Logistic Regression classifier, and stores both the fitted
pipeline and a metadata file with feature ordering and evaluation metrics.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "league_of_legends_data_large.csv"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
PIPELINE_PATH = ARTIFACT_DIR / "lol_win_pipeline.joblib"
METADATA_PATH = ARTIFACT_DIR / "metadata.json"


@dataclass
class TrainingConfig:
    test_size: float = 0.2
    random_state: int = 42
    penalty: str = "l2"
    C: float = 1.0
    max_iter: int = 1000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train LoL win probability model.")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="Path to the CSV dataset.",
    )
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=ARTIFACT_DIR,
        help="Directory to store the trained pipeline and metadata.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=TrainingConfig.test_size,
        help="Fraction of the dataset reserved for validation.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=TrainingConfig.random_state,
        help="Random state for the train/test split.",
    )
    parser.add_argument(
        "--C",
        type=float,
        default=TrainingConfig.C,
        help="Inverse regularization strength for Logistic Regression.",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=TrainingConfig.max_iter,
        help="Maximum iterations for Logistic Regression solver.",
    )
    return parser.parse_args()


def load_dataset(path: Path) -> Tuple[pd.DataFrame, List[str], str]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)
    if "win" not in df.columns:
        raise ValueError("Dataset must contain a 'win' target column.")

    target = "win"
    feature_order = [col for col in df.columns if col != target]
    return df, feature_order, target


def build_pipeline(config: TrainingConfig) -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    penalty=config.penalty,
                    C=config.C,
                    max_iter=config.max_iter,
                    solver="lbfgs",
                ),
            ),
        ]
    )


def train(
    df: pd.DataFrame,
    features: List[str],
    target: str,
    config: TrainingConfig,
    test_size: float,
    random_state: int,
) -> Dict[str, Any]:
    X = df[features].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    pipeline = build_pipeline(config)
    pipeline.fit(X_train, y_train)

    proba = pipeline.predict_proba(X_test)[:, 1]
    preds = (proba >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
    }

    return {"pipeline": pipeline, "metrics": metrics}


def save_artifacts(
    pipeline: Pipeline,
    metrics: Dict[str, float],
    features: List[str],
    target: str,
    artifact_dir: Path,
) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, artifact_dir / "lol_win_pipeline.joblib")

    metadata = {
        "feature_order": features,
        "target": target,
        "test_metrics": metrics,
    }
    (artifact_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))


def main() -> None:
    args = parse_args()
    config = TrainingConfig(
        test_size=args.test_size,
        random_state=args.random_state,
        C=args.C,
        max_iter=args.max_iter,
    )
    df, features, target = load_dataset(args.dataset)
    result = train(
        df=df,
        features=features,
        target=target,
        config=config,
        test_size=args.test_size,
        random_state=args.random_state,
    )
    save_artifacts(
        pipeline=result["pipeline"],
        metrics=result["metrics"],
        features=features,
        target=target,
        artifact_dir=args.artifact_dir,
    )
    print(f"Artifacts saved to {args.artifact_dir}")
    print(f"Validation metrics: {json.dumps(result['metrics'], indent=2)}")


if __name__ == "__main__":
    main()

