import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Layout builder
def build_layout(df_txn, df_prod, df_ret):
    categories = sorted(df_txn['Category'].dropna().unique())
    stores = sorted(df_txn['Store'].dropna().unique())

    return html.Div([
        html.H1("📊 Comprehensive Retail Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

        html.Div([
            html.Div([
                html.Label("Select Store:"),
                dcc.Dropdown(
                    id='store-dropdown',
                    options=[{'label': s, 'value': s} for s in stores],
                    value=stores[0],
                    clearable=False
                )
            ], style={'width': '40%', 'padding': '10px'}),
        ]),

        dcc.Graph(id='category-sales-bar'),
        dcc.Graph(id='monthly-trends-line'),
        dcc.Graph(id='return-reason-pie'),

        html.H3("📋 Transaction Records", style={'marginTop': '30px'}),
        dash_table.DataTable(
            id='transaction-table',
            columns=[{'name': col, 'id': col} for col in df_txn.columns],
            data=df_txn.to_dict('records'),
            page_size=15,
            style_table={'overflowX': 'scroll'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': '#f5f5f5', 'fontWeight': 'bold'}
        )
    ])

# Callback registration
def register_callbacks(app, df_txn, df_prod, df_ret):
    @app.callback(
        Output('category-sales-bar', 'figure'),
        Input('store-dropdown', 'value')
    )
    def update_category_sales(store):
        filtered = df_txn[df_txn['Store'] == store]
        agg = filtered.groupby('Category')['SaleValue'].sum().reset_index()
        return px.bar(
            agg, x='Category', y='SaleValue', color='Category', text_auto='.2s',
            title=f"💰 Sales by Category – {store}"
        )

    @app.callback(
        Output('monthly-trends-line', 'figure'),
        Input('store-dropdown', 'value')
    )
    def update_monthly_sales(store):
        filtered = df_txn[df_txn['Store'] == store]
        trend = filtered.groupby('Month')['SaleValue'].sum().reset_index()
        trend['Month'] = trend['Month'].astype(str)
        return px.line(
            trend, x='Month', y='SaleValue', markers=True,
            title=f"📈 Monthly Revenue Trend – {store}"
        )

    @app.callback(
        Output('return-reason-pie', 'figure'),
        Input('store-dropdown', 'value')
    )
    def update_return_pie(store):
        filtered = df_ret[df_ret['Store'] == store]
        pie = filtered.groupby('Reason').size().reset_index(name='Count')
        return px.pie(
            pie, names='Reason', values='Count', hole=0.4,
            title=f"🔁 Return Reasons Breakdown – {store}"
        )

    @app.callback(
        Output('transaction-table', 'data'),
        Input('store-dropdown', 'value')
    )
    def update_table_data(store):
        return df_txn[df_txn['Store'] == store].to_dict('records')
