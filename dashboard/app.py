import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import logging
from utils import build_layout, register_callbacks

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load and preprocess datasets
def load_data():
    try:
        df_txn = pd.read_csv('data/transactions.csv', parse_dates=['Date'])
        df_prod = pd.read_csv('data/products.csv')
        df_ret = pd.read_csv('data/returns.csv', parse_dates=['Date'])

        df_txn = df_txn.merge(df_prod, on='ProductID', how='left')
        df_txn['Month'] = df_txn['Date'].dt.to_period('M')

        df_ret = df_ret.merge(df_txn[['SaleID', 'Store', 'Category', 'SaleValue']], on='SaleID', how='left')

        logger.info("✅ Data loaded and merged successfully.")
        return df_txn, df_prod, df_ret
    except Exception as e:
        logger.error("❌ Failed to load data: %s", e)
        raise

# Initialize Dash app
app = dash.Dash(__name__, title="Retail KPI Dashboard", suppress_callback_exceptions=True)
server = app.server

# Load and preprocess data
df_txn, df_prod, df_ret = load_data()

# Define layout
app.layout = build_layout(df_txn, df_prod, df_ret)

# Register app callbacks
register_callbacks(app, df_txn, df_prod, df_ret)

# Launch server
if __name__ == '__main__':
    logger.info("🚀 Starting dashboard server...")
    app.run_server(debug=True)
