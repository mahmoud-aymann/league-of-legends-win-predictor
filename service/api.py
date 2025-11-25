from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
PIPELINE_PATH = ARTIFACT_DIR / "lol_win_pipeline.joblib"
METADATA_PATH = ARTIFACT_DIR / "metadata.json"

if not PIPELINE_PATH.exists() or not METADATA_PATH.exists():
    raise FileNotFoundError(
        "Artifacts not found. Run lol_full_pipeline.ipynb to generate the trained pipeline."
    )

PIPELINE = joblib.load(PIPELINE_PATH)
METADATA = json.loads(METADATA_PATH.read_text())
FEATURE_ORDER = METADATA["feature_order"]


def _prepare_features(payload: Dict[str, Any]) -> np.ndarray:
    missing = [feature for feature in FEATURE_ORDER if feature not in payload]
    if missing:
        raise ValueError(f"Missing required features: {missing}")
    try:
        ordered = [float(payload[feature]) for feature in FEATURE_ORDER]
    except (TypeError, ValueError) as exc:
        raise ValueError("All feature values must be numeric.") from exc
    return np.array(ordered, dtype=float).reshape(1, -1)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/")
    def index() -> Any:
        return render_template(
            "index.html",
            feature_order=FEATURE_ORDER,
            metadata=METADATA,
            response_model="Logistic Regression",
        )

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok", "features": FEATURE_ORDER})

    @app.post("/predict")
    def predict() -> Any:
        payload = request.get_json(force=True) or {}
        try:
            feature_array = _prepare_features(payload)
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

        win_probability = float(PIPELINE.predict_proba(feature_array)[0, 1])
        prediction = int(win_probability >= 0.5)
        response = {
            "win_probability": win_probability,
            "prediction": prediction,
            "threshold": 0.5,
            "metadata": {
                "model": "logistic_regression",
                "metrics": METADATA.get("test_metrics"),
            },
        }
        return jsonify(response)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

