from app.ml.train_model import train_model
from app.ml.predict import predict_signal

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


def show_models():

    st.title("🤖 Machine Learning Models")
    st.markdown("Train, evaluate and compare trading models.")
    st.divider()

    # ============================================================
    # Model Selection
    # ============================================================

    model_name = st.selectbox(

        "Select Model",

        [

            "XGBoost",

            "Random Forest",

            "LSTM",

            "LightGBM",

            "Prophet",

            "ARIMA"

        ]

    )

    asset = st.selectbox(

        "Select Asset",

        [

            "AAPL",

            "AMZN",

            "GOOGL",

            "META",

            "MSFT",

            "NVDA",

            "TSLA",

            "BTC-USD",

            "ETH-USD",

            "SOL-USD"

        ]

    )

    st.divider()

    # ============================================================
    # Buttons
    # ============================================================

    c1, c2 = st.columns(2)

    train = c1.button(

        "🚀 Train Model",

        width="stretch"

    )

    predict = c2.button(

        "📈 Predict",

        width="stretch"

    )

    # ============================================================
    # Train
    # ============================================================

    if train:

        try:

            with st.spinner("Training model..."):

                trained_model, metrics = train_model(asset)

                st.session_state["metrics"] = metrics

            st.success(f"{asset} model trained successfully.")

        except Exception as e:

            st.error(str(e))

    # ============================================================
    # Predict
    # ============================================================

    if predict:

        try:

            signal, confidence = predict_signal(asset)

            st.success(f"Prediction : {signal}")

            st.info(

                f"Confidence : {confidence:.2%}"

            )

        except Exception as e:

            st.error(str(e))

    st.divider()

    # ============================================================
    # Performance Metrics
    # ============================================================

    st.subheader("Model Performance")

    c1, c2, c3, c4 = st.columns(4)

    if "metrics" in st.session_state:

        metrics = st.session_state["metrics"]

        c1.metric(

            "Accuracy",

            f"{metrics['accuracy']:.2%}"

        )

        c2.metric(

            "Precision",

            f"{metrics['precision']:.2%}"

        )

        c3.metric(

            "Recall",

            f"{metrics['recall']:.2%}"

        )

        c4.metric(

            "F1 Score",

            f"{metrics['f1']:.2%}"

        )

    else:

        c1.metric("Accuracy", "--")

        c2.metric("Precision", "--")

        c3.metric("Recall", "--")

        c4.metric("F1 Score", "--")

    st.divider()

    # ============================================================
    # Feature Importance
    # ============================================================

    st.subheader("Feature Importance")

    if "metrics" in st.session_state:

        metrics = st.session_state["metrics"]

        feature_df = pd.DataFrame(

            {

                "Feature": metrics["feature_names"],

                "Importance": metrics["feature_importance"]

            }

        )

        fig = px.bar(

            feature_df,

            x="Importance",

            y="Feature",

            orientation="h",

            color="Importance"

        )

        fig.update_layout(

            template="plotly_dark",

            height=450

        )

        st.plotly_chart(

            fig,

            width="stretch"

        )

    else:

        st.info("Train a model to view feature importance.")
    st.divider()

    # ============================================================
    # Confusion Matrix
    # ============================================================

    st.subheader("Confusion Matrix")

    if "metrics" in st.session_state:

        metrics = st.session_state["metrics"]

        cm = metrics["confusion_matrix"]

        cm_df = pd.DataFrame(

            cm,

            index=[

                "Actual Sell",

                "Actual Buy"

            ],

            columns=[

                "Predicted Sell",

                "Predicted Buy"

            ]

        )

        st.dataframe(

            cm_df,

            width="stretch",

            hide_index=False

        )

    else:

        st.info("Train a model to view the confusion matrix.")

    st.divider()

    # ============================================================
    # Saved Models
    # ============================================================

    st.subheader("Saved Models")

    models_dir = Path("models")

    if models_dir.exists():

        files = sorted(

            [f.name for f in models_dir.glob("*.pkl")]

        )

        if files:

            models_df = pd.DataFrame(

                {

                    "Saved Models": files

                }

            )

            st.dataframe(

                models_df,

                width="stretch",

                hide_index=True

            )

        else:

            st.info("No trained models found.")

    else:

        st.info("Models folder not found.")

    st.divider()

    # ============================================================
    # Model Information
    # ============================================================

    st.subheader("Model Information")

    info = pd.DataFrame(

        {

            "Property": [

                "Selected Model",

                "Selected Asset",

                "Prediction Task",

                "Algorithm"

            ],

            "Value": [

                model_name,

                asset,

                "Next-Day Direction",

                model_name

            ]

        }

    )

    st.dataframe(

        info,

        width="stretch",

        hide_index=True

    )

    st.success("✅ Machine Learning Module Ready")