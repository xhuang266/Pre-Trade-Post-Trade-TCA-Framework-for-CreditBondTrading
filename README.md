# Quantitative TCA Framework for Credit Trading

## Overview

This project implements an institutional-grade **Pre-Trade Transaction Cost Analysis (TCA)** system designed for the Credit Bond market. It transitions execution strategy from empirical intuition to a **probability-calibrated framework**. 

By leveraging **Ridge Regression** for cost estimation and **Isotonic Calibrated Logistic Regression** for execution probability, the system quantifies the risk of "blind flying" in OTC markets. It features a robust **Walk-Forward Validation** mechanism to prevent look-ahead bias and includes a **Post-Trade Feedback Loop** that dynamically recalibrates impact models based on realized liquidity conditions.

## Key Features

### 1. Data Engineering & Validation (Module 1)
* **Strict Walk-Forward Validation:** Eliminates look-ahead bias by ensuring feature scaling (StandardScaler) and model training only use data available up to time $T$.
* **Issuer-Level Aggregation:** Solves the sparse data problem in credit markets by aggregating liquidity metrics across an issuer's entire bond curve when specific bond data is missing.
* **VIX Integration:** Enriches trade data with macro volatility signals derived from Yahoo Finance.

### 2. Two-Stage Predictive Engine (Module 2)
* **Cost Model (Ridge Regression):** Uses L2 regularization to handle high multicollinearity among financial features (Spread, Duration, VIX, DTS).
* **Probability Model (Calibrated Classifier):** Uses **Isotonic Regression** to map raw logistic scores to actual statistical fill rates (e.g., a 0.7 score implies a true 70% probability of execution).
* **Market Impact Modeling:** Implements the **Square-Root Law** with an asymmetric "Crowding Penalty" to simulate liquidity evaporation during panic selling or crowded trades.

### 3. Decision Logic & Feedback Loop (Module 3)
* **Value Trap Filter:** Calculates `Net Edge = Alpha - Predicted Cost`. Trades are rejected ("NO_TRADE") if transaction costs erode the theoretical alpha, preventing unprofitable execution.
* **Closed-Loop Calibration:** Analyzes post-trade **Reversion Ratios**. High reversion suggests temporary liquidity impact, triggering an automated increase in the model's impact beta coefficient.

## Project Structure

```text
Credit-Bond-TCA-System/
├── data/
│   └── rfq_data.csv           # Input Data
├── src/
│   ├── __init__.py
│   ├── data_adapter.py        # Data Cleaning, VIX Fetching, Feature Engineering
│   ├── tca_core.py            # Ridge Cost Model & Calibrated Probability Model
│   ├── feedback.py            # Post-Trade Analysis & Parameter Recalibration
│   └── visualization.py       # Visual Reporting & Reality Check Utilities
├── main.py                    # Main Execution Script

└── README.md                  # Project Documentation
