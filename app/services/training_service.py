from app.ml.train_model import train_model


def train_asset(asset):

    model, metrics = train_model(asset)

    return {

        "accuracy": round(metrics["accuracy"] * 100, 2),

        "precision": round(metrics["precision"] * 100, 2),

        "recall": round(metrics["recall"] * 100, 2),

        "f1": round(metrics["f1"] * 100, 2),

        "feature_importance": metrics["feature_importance"].tolist(),

        "feature_names": list(metrics["feature_names"]),

        "confusion_matrix": metrics["confusion_matrix"].tolist()

    }