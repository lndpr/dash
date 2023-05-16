import MetaTrader5 as mt5
import talib
import pandas as pd
import dash
import dash_html_components as html
import dash_table

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=84566681, server="XMGlobal-MT5 4",password="Matary1122@"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on connection status, server name and trading account
print(mt5.terminal_info())
# display data on MetaTrader 5 version
print(mt5.version())

# list of currency pairs to analyze
symbols = ['AUDJPY', 'AUDUSD', 'EURUSD', 'EURCHF', 'EURGBP', 'GBPUSD', 'GBPJPY', 'GOLD',  'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY' ]

# list of timeframes to analyze
timeframes = [mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1]

# initialize data
data = {}
for tf in timeframes:
    data[tf] = []

# process data
for symbol in symbols:
    for tf in timeframes:
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, 1000)
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.drop(["open", "high", "low", "tick_volume", "spread", "real_volume"], axis=1, inplace=True)

        # hitung RSI 14 dan RSI 30
        rsi14 = talib.RSI(df["close"], timeperiod=14)
        rsi30 = talib.RSI(df["close"], timeperiod=30)
        print(f"{symbol} {tf}: RSI14: {rsi14.iloc[-1]}")
        print(f"{symbol} {tf}: RSI30: {rsi30.iloc[-1]}")

        timeframe_map = {
    mt5.TIMEFRAME_M1: 'M1',
    mt5.TIMEFRAME_M2: 'M2',
    mt5.TIMEFRAME_M3: 'M3',
    mt5.TIMEFRAME_M4: 'M4',
    mt5.TIMEFRAME_M5: 'M5',
    mt5.TIMEFRAME_M6: 'M6',
    mt5.TIMEFRAME_M10: 'M10',
    mt5.TIMEFRAME_M12: 'M12',
    mt5.TIMEFRAME_M15: 'M15',
    mt5.TIMEFRAME_M20: 'M20',
    mt5.TIMEFRAME_M30: 'M30',
    mt5.TIMEFRAME_H1: 'H1',
    mt5.TIMEFRAME_H2: 'H2',
    mt5.TIMEFRAME_H3: 'H3',
    mt5.TIMEFRAME_H4: 'H4',
    mt5.TIMEFRAME_H6: 'H6',
    mt5.TIMEFRAME_H8: 'H8',
    mt5.TIMEFRAME_H12: 'H12',
    mt5.TIMEFRAME_D1: 'D1',
    mt5.TIMEFRAME_W1: 'W1',
    mt5.TIMEFRAME_MN1: 'MN1'
}


        # tentukan tren bullish, bearish, atau sideways
        if rsi14.iloc[-1] > rsi30.iloc[-1]:
            trend = "Up"
        elif rsi14.iloc[-1] < rsi30.iloc[-1]:
            trend = "Dn"
        else:
            if 45 <= rsi14.iloc[-1] <= 55 and 45 <= rsi30.iloc[-1] <= 55:
                trend = "Sideways"
            else:
                trend = ""
        print(f"{symbol} {tf}: Trend: {trend}")

        data[tf].append({"Pair": symbol, timeframe_map[tf].upper(): trend})


# buat dataframe dari data
df = pd.DataFrame(data[mt5.TIMEFRAME_M1])

# tambahkan kolom-kolom untuk setiap timeframe
for tf in timeframes[1:]:
    df = df.merge(pd.DataFrame(data[tf]), on="Pair")

# buat table dari dataframe
table = dash_table.DataTable(
    id="table",
    columns=[{"name": col, "id": col} for col in df.columns],
    data=df.to_dict("records"),
    style_cell={
        "textAlign": "center",
        "font_size": "16px",
        "font_family": "Calibri"
    },
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold"
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
        
            "backgroundColor": "rgb(248, 248, 248)"
            
        },
        {
            "if": {"column_id": "Pair"},
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M1",
                "filter_query": "{M1} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M1",
                "filter_query": "{M1} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M5",
                "filter_query": "{M5} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M5",
                "filter_query": "{M5} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M15",
                "filter_query": "{M15} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M15",
                "filter_query": "{M15} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M30",
                "filter_query": "{M30} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "M30",
                "filter_query": "{M30} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "H1",
                "filter_query": "{H1} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "H1",
                "filter_query": "{H1} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "H4",
                "filter_query": "{H4} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "H4",
                "filter_query": "{H4} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "D1",
                "filter_query": "{D1} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "D1",
                "filter_query": "{D1} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "W1",
                "filter_query": "{W1} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "W1",
                "filter_query": "{W1} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "MN1",
                "filter_query": "{MN1} eq 'Up'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "MN1",
                "filter_query": "{MN1} eq 'Dn'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
    ]
)

# buat aplikasi dash
app = dash.Dash(__name__)

# tambahkan table ke dalam layout
app.layout = dash.html.Div([
    dash.html.H1("OUTLOOK HARIAN MATARY", style={"textAlign": "center"}),
    table,
    dash.html.Br(), # tambahkan baris kosong
    dash.html.P("Gunakanlah Outlook harian Matary ini secara bijak, pelajari cara menggunakannya untuk intraday, swing, dan position trading di grup telegram Matary.", style={"textAlign": "center"}),
    dash.html.P("Untuk join grup telegram Matary klik link dibawah ini. ", style={"textAlign": "center"})
],
    style={"max-width": "850px", "margin": "auto"}
)


if __name__ == "__main__":
    app.run_server(debug=True)
