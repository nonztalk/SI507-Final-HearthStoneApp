import dash
import plotly
from flask import Flask
from dash.dependencies import Input, Output, State
import sqlite3
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

styles = {
    "H1":{
        "line-height":"2.3rem",
        "letter-spacing":"0.1rem",
        "font-family":"Noto Sans,sans-serif",
        "font-weight":"1000"
    }
}

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/Decks'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/Cards'),
])

decks_layout = html.Div([
    html.Div([
        html.H1('HearthStone Current Decks', style = styles['H1']),
        html.Div([
            dcc.Link('Decks', href = '/Decks', style = {'margin-right':'20px', 'margin-left':'50px'}),
            dcc.Link('Cards', href = '/Cards')
        ], style = {'columnCount':2})

    ]),
    html.Div([
        html.Div([
            html.Hr(style = {"margin-bottom":"1.9rem"}),
            html.H6('Filter by class:'),
            dcc.Dropdown(
                id = 'ClassInput',
                options=[
                    {'label': 'Druid', 'value': 'Druid'},
                    {'label': 'Mage', 'value': 'Mage'},
                    {'label': 'Hunter', 'value': 'Hunter'},
                    {'label': 'Warrior', 'value': 'Warrior'},
                    {'label': 'Warlock', 'value': 'Warlock'},
                    {'label': 'Paladin', 'value': 'Paladin'},
                    {'label': 'Shaman', 'value': 'Shaman'},
                    {'label': 'Priest', 'value': 'Priest'},
                    {'label': 'Rogue', 'value': 'Rogue'}
                ],
                value = None
            ),
            html.Hr(style = {"margin-bottom":"1.9rem"}),
            html.H6('Filter by game mode:'),
            dcc.Dropdown(
                id = "ModeInput",
                options=[
                    {'label': 'Standard', 'value': 'Standard'},
                    {'label': 'Wild', 'value': 'Wild'}
                ],
                value = 'Standard'
            ),
            html.Hr(style = {"margin-bottom":"1.9rem"}),
            html.H6('Order by'),
            html.Div([
                html.Label('Game'),
                dcc.RadioItems(
                    id = 'SortByTotalGames',
                    options = [
                        {'label':'Up', 'value':''},
                        {'label':'Desc', 'value':'DESC'}
                    ],
                    value = 'DESC'
                ),
                html.Label('Win%'),
                dcc.RadioItems(
                    id = 'SortByWinRate',
                    options = [
                        {'label':'Up', 'value':''},
                        {'label':'Desc', 'value':'DESC'}
                    ],
                    value = None
                ),
                html.Label('Time'),
                dcc.RadioItems(
                    id = 'SortByDuration',
                    options = [
                        {'label':'Up', 'value':''},
                        {'label':'Desc', 'value':'DESC'}
                    ],
                    value = None
                ),
                html.Label('Turns'),
                dcc.RadioItems(
                    id = 'SortByTurns',
                    options = [
                        {'label':'Up', 'value':''},
                        {'label':'Desc', 'value':'DESC'}
                    ],
                    value = None
                )
            ], style = {'columnCount':4}),
            html.Hr(style = {"margin-bottom":"1.9rem"}),
            html.H6('Search a deck:'),
            dcc.Input(id = "DeckNameInput", type='text', value = None),
            html.Hr()
        ], className = 'three columns'),

        html.Div(
            id = "DeckTable",
            className = 'nine columns',
            style = {'margin-top':'-3%'}

        )
    ])

])
@app.callback(
    Output('DeckTable', 'children'),
    [Input('ClassInput', 'value'),
     Input('ModeInput', 'value'),
     Input('DeckNameInput', 'value'),
     Input('SortByTotalGames', 'value'),
     Input('SortByWinRate', 'value'),
     Input('SortByDuration', 'value'),
     Input('SortByTurns', 'value')]
)
def print_table(Class, Mode, DeckName, SortByTotalGames, SortByWinRate, SortByDuration, SortByTurns):
    conn = sqlite3.connect('HeartStone.sqlite')
    query = '''
    SELECT DeckName AS Name, DeckClass AS Class, TotalGames, WinRate AS [Win(%)],
    AverageGameTime AS Duration, AverageGameTurns AS Turns, Mode, UId
    FROM Decks
    JOIN DeckDetail ON DeckDetail.DeckId = Decks.NameId
    WHERE NameId > 0 AND Mode = '{}' AND CollectTime = (
        SELECT CollectTime FROM Decks ORDER BY CollectTime DESC LIMIT 1
    )
    ORDER BY TotalGames DESC
    '''.format(Mode)
    if Class is not None:
        query += 'AND Class = \'{}\''.format(Class.upper())
    if DeckName is not None:
        query += 'AND DeckName LIKE \'%{}%\''.format(DeckName)
    if SortByTotalGames is '':
        query.replace('ORDER BY TotalGames DESC', 'ORDER BY TotalGames ')
    if SortByWinRate is not None:
        query += ("AND WinRate " + SortByWinRate)
    if SortByDuration is not None:
        query += ("AND AverageGameTime " + SortByDuration)
    if SortByTurns is not None:
        query += ("AND AverageGameTurns " + SortByTurns)
    df = pd.read_sql_query(query, conn)
    return [
        html.H6('Decks Information'),
        html.Table(
        [html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), 100))]
    )]


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_pages(pathname):
    if pathname == '/Decks':
        return decks_layout
    elif pathname == '/Cards':
        return cards_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
