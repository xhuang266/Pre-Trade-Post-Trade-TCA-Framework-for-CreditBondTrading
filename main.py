import pandas as pd
from src.data_adapter import TradeDataAdapter
from src.tca_core import CreditPreTradeTCA
from src.feedback import PostTradeCalibrationEngine
from src.visualization import generate_visual_report, run_reality_check

# ==============================================================================
# MAIN EXECUTION SCRIPT
# ==============================================================================

# 1. Load Data
file_path = "data/rfq_data.csv"
print(f"Initializing Data Adapter with file: {file_path}")
df = TradeDataAdapter.process(file_path)

if df is not None:
    # 2. Train System
    tca_system = CreditPreTradeTCA()
    print("\n--- Starting TCA System Training ---")
    tca_system.train_model(df)

    # 3. Simulate Live Trading Decision
    print("\n--- Live Trade Opportunity Evaluation ---")
    # Use one historical record as the current market snapshot
    sample_market = df.iloc[0:1].copy() 

    # Example: Portfolio Manager wants to buy $1M, assumes 15bps Alpha
    trade_size = 1000000 
    side = 1      # Buy
    trend = -0.5  # Contrarian Buy (Buy the dip)
    alpha = 15.0 

    result = tca_system.evaluate_trade_opportunity(sample_market, trade_size, side, trend, alpha)

    print(f"Decision: {result['decision']}")
    print(f"Net Edge: {result['net_edge_bps']:.2f} bps")
    print(f"  |-- Theoretical Alpha: {result['alpha_bps']} bps")
    print(f"  |-- Estimated Cost:    {result['cost_bps']:.2f} bps")
    print(f"  |-- Prob of Fill:      {result['prob_fill']*100:.1f}%")

    # 4. Simulate Post-Trade Feedback Loop
    # Scenario: We executed the trade, but realized cost was much higher than predicted,
    # and prices reverted significantly (indicating temporary liquidity impact).
    post_trade_data = pd.DataFrame({
        'predicted_cost_bps': [10, 12, 11],
        'realized_cost_bps': [25, 28, 22], # High realized cost
        'reversion_bps': [20, 25, 18]      # High reversion -> Liquidity Impact
    })

    calibrator = PostTradeCalibrationEngine(tca_system)
    calibrator.analyze_batch(post_trade_data)

    # 5. Generate Visual Reports
    print("\n--- Generating Visual Reports ---")
    generate_visual_report(tca_system, df)

    # 6. Run Reality Check (Stress Test)

    run_reality_check(tca_system, df)
