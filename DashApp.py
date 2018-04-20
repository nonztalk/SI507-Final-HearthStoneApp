import dash
import plotly
import ast
from flask import Flask
from dash.dependencies import Input, Output, State
import sqlite3
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


app = dash.Dash(__name__)
server = app.server

# setting styles for app
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

styles = {
    "H1":{
        "line-height":"2.3rem",
        "letter-spacing":"0.1rem",
        "font-family":"Noto Sans,sans-serif",
        "font-weight":"1000"
    }
}

# setting data and functions for app
conn = sqlite3.connect('HeartStone.sqlite')
query = '''
SELECT DeckName AS Name, DeckClass AS Class, TotalGames, WinRate AS [Win(%)],
AverageGameTime AS Duration, AverageGameTurns AS Turns, Mode, UID
FROM Decks
JOIN DeckDetail ON DeckDetail.DeckId = Decks.NameId
WHERE NameId > 0 AND CollectTime = (
    SELECT CollectTime FROM Decks ORDER BY CollectTime DESC LIMIT 1
)
'''
df = pd.read_sql_query(query, conn)

query_card = '''
SELECT Name, Class, Popularity AS [Popularity(%)], UseFrequency AS Frequency,
CardWinRate AS [Win(%)], Rarity, [Set], Copies, Mode, CardsPlay.CardId AS UId FROM CardsPlay
JOIN CardDetail ON CardsPlay.CardId = CardDetail.CardId
WHERE CollectTime = (
SELECT CollectTime FROM CardsPlay ORDER BY CollectTime DESC LIMIT 1
)
'''
df_card = pd.read_sql_query(query_card, conn)
conn.close()

def get_deck_detail(cards_list):
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()
    cards = ast.literal_eval(cards_list)
    string = ''
    for card_id, card_copies in cards:
        query = '''
        SELECT Name FROM CardDetail WHERE CardId = '{}'
        '''.format(card_id)
        cur.execute(query)
        card_name = cur.fetchone()[0]
        string += (card_name + '*' + str(card_copies) + '; ')
    conn.close()
    return string

def cards_in_decks_detail(cards_list):
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()
    cards = ast.literal_eval(cards_list)
    cards_cost = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0}
    cards_attack = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0}
    cards_health = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0}
    for card_id, card_copies in cards:
        query = '''
        SELECT Cost, Attack, Health FROM CardDetail WHERE CardId = '{}'
        '''.format(card_id)
        cur.execute(query)
        cost, attack, health = cur.fetchone()
        if cost >= 7:
            cards_cost['7'] += card_copies
        elif cost < 7:
            cards_cost[str(cost)] += card_copies
        if attack == '':
            pass
        elif attack >= 7:
            cards_attack['7'] += card_copies
        else:
            cards_attack[str(attack)] += card_copies
        if health == '':
            pass
        elif health >= 7:
            cards_health['7'] += card_copies
        else:
            cards_health[str(health)] += card_copies
    conn.close()
    return cards_cost, cards_attack, cards_health

def cards_images(CardId):
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()
    sets = {
    'CORE': 'Base',
    'EXPERT1': 'Core',
    'TGT': 'The Grand Tournament',
    'BRM': 'Blackrock Mountain',
    'GANGS': 'Mean Streets of Gadgetzan',
    'HOF': 'Hall of Fame',
    'NAXX': 'Curse of Naxxramas',
    'GVG': 'Goblins vs Gnomes',
    'HERO_SKINS': 'Heros',
    'ICECROWN': 'Knights of the Frozen Throne',
    'KARA': 'One Night in Karazhan',
    'LOE': 'The League of Explorers',
    'LOOTAPALOOZA': 'Kobolds & Catacombs',
    'OG': 'Whispers of the Old Gods',
    'UNGORO': 'Journey to Un\'Goro',
    'GILNEAS': 'The Witchwood'
    }
    query = '''
    SELECT Name, [Set], ImageLink, ImageGoldLink FROM CardDetail
    JOIN CardImg ON CardDetail.Name = CardImg.CardName
    WHERE CardId = '{}'
    '''.format(CardId)
    cur.execute(query)
    card_name, card_set_abbr, card_Img, card_ImgGold = cur.fetchone()
    card_set = sets[card_set_abbr]
    return card_name, card_set, card_Img, card_ImgGold


# app layout
app.layout = html.Div([
    html.Div([
        html.H1('HearthStone Data and Statistics', style = styles['H1'])

    ]),

    html.Div([
        html.H6('Decks Information'),
        dt.DataTable(
            rows = df.to_dict('records'),
            sortable = True,
            row_selectable=True,
            filterable=True,
            selected_row_indices=[],
            id = 'DecksTable'
        )
    ], className = 'container'),

    html.Hr(),
    html.Div(id='selected-decks', className = 'container'),
    html.Hr(),

    dcc.Graph(
        id='TotalGameGraph',
        className = 'container'
    ),
    dcc.Graph(
        id='WinRateGraph',
        className = 'container'
    ),
    dcc.Graph(
        id='AverageGameTimeGraph',
        className = 'container'
    ),

    html.Hr(),
    html.Div([
        html.H6('Cards Information'),
        dt.DataTable(
            rows = df_card.to_dict('records'),
            sortable = True,
            row_selectable=True,
            filterable=True,
            selected_row_indices=[],
            id = 'CardsTable'
        )
    ], className = 'container'),

    html.Hr(),
    html.Div(id='selected-cards', className = 'container'),
    html.Hr(),

    dcc.Graph(
        id='PopularityGraph',
        className = 'container'
    ),
    dcc.Graph(
        id='UseFrequencyGraph',
        className = 'container'
    ),
    dcc.Graph(
        id='CardWinRateGraph',
        className = 'container'
    ),
    dcc.Graph(
        id='CopiesGraph',
        className = 'container'
    ),
])

# Interactions
# DECKS
@app.callback(
    Output('DecksTable', 'selected_row_indices'),
    [Input('TotalGameGraph', 'clickData')],
    [State('DecksTable', 'selected_row_indices')])
def update_selected_row_indices_decks(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

@app.callback(
    Output('TotalGameGraph', 'figure'),
    [Input('DecksTable', 'rows'),
     Input('DecksTable', 'selected_row_indices')])
def update_figure_totalGame(rows, selected_row_indices):
    layout = dict(title = 'Total Games', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Game Counts'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT TotalGames, CollectTime FROM Decks WHERE UId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['TotalGames'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('WinRateGraph', 'figure'),
    [Input('DecksTable', 'rows'),
     Input('DecksTable', 'selected_row_indices')])
def update_figure_WinRate(rows, selected_row_indices):
    layout = dict(title = 'Deck Win Rate', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Rate (%)'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT WinRate, CollectTime FROM Decks WHERE UId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['WinRate'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('AverageGameTimeGraph', 'figure'),
    [Input('DecksTable', 'rows'),
     Input('DecksTable', 'selected_row_indices')])
def update_figure_AverageGameTime(rows, selected_row_indices):
    layout = dict(title = 'Play Time', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Seconds'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT AverageGameTime, CollectTime FROM Decks WHERE UId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['AverageGameTime'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('selected-decks', 'children'),
    [Input('DecksTable', 'rows'),
     Input('DecksTable', 'selected_row_indices')]
)
def update_deck_detail(rows, selected_row_indices):
    content = []
    if selected_row_indices is []:
        return content
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        cur = conn.cursor()
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT CardsIncluded FROM Decks WHERE UId = '{0}' AND Mode = '{1}'
            AND CollectTime = (
                SELECT CollectTime FROM Decks ORDER BY CollectTime DESC LIMIT 1
            )
            '''.format(UId, mode)
            cur.execute(query)
            cards_list_string = cur.fetchone()[0]
            content.append(
                html.Div(children = name + ": " + get_deck_detail(cards_list_string))
            )
            cost, attack, health = cards_in_decks_detail(cards_list_string)
            fig = plotly.tools.make_subplots(rows = 1, cols = 3, subplot_titles = ('Cost', 'Attack', 'Health'))
            trace_cost = go.Bar(
                x = list(cost.keys()),
                y = list(cost.values()),
                marker = dict(color = 'rgb(79, 143, 263)')
            )
            trace_attack = go.Bar(
                x = list(attack.keys()),
                y = list(attack.values()),
                marker = dict(color = 'rgb(209, 142, 77)')
            )
            trace_health = go.Bar(
                x = list(health.keys()),
                y = list(health.values()),
                marker = dict(color = 'rgb(214, 20, 28)')
            )
            fig.append_trace(trace_cost, 1, 1)
            fig.append_trace(trace_attack, 1, 2)
            fig.append_trace(trace_health, 1, 3)
            fig['layout'].update(showlegend = False)
            content.append(
                dcc.Graph(id = 'cards-in-deck-{}'.format(UId), figure = fig)
            )
            content.append(html.Br())
        conn.close()
        return content


# Cards
@app.callback(
    Output('CardsTable', 'selected_row_indices'),
    [Input('PopularityGraph', 'clickData')],
    [State('CardsTable', 'selected_row_indices')])
def update_selected_row_indices_cards(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

@app.callback(
    Output('PopularityGraph', 'figure'),
    [Input('CardsTable', 'rows'),
     Input('CardsTable', 'selected_row_indices')])
def update_figure_Popularity(rows, selected_row_indices):
    layout = dict(title = 'Popularity', xaxis = dict(title = 'Date Time'), yaxis = dict(title = '%% deck use this card'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT Popularity, CollectTime FROM CardsPlay WHERE CardId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['Popularity'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('UseFrequencyGraph', 'figure'),
    [Input('CardsTable', 'rows'),
     Input('CardsTable', 'selected_row_indices')])
def update_figure_Popularity(rows, selected_row_indices):
    layout = dict(title = 'Use Frequency', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Counts'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT UseFrequency, CollectTime FROM CardsPlay WHERE CardId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['UseFrequency'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('CardWinRateGraph', 'figure'),
    [Input('CardsTable', 'rows'),
     Input('CardsTable', 'selected_row_indices')])
def update_figure_Popularity(rows, selected_row_indices):
    layout = dict(title = 'Win Rate (decks have this card)', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Rate (%)'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT CardWinRate, CollectTime FROM CardsPlay WHERE CardId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['CardWinRate'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('CopiesGraph', 'figure'),
    [Input('CardsTable', 'rows'),
     Input('CardsTable', 'selected_row_indices')])
def update_figure_Popularity(rows, selected_row_indices):
    layout = dict(title = 'Card Copies in Decks', xaxis = dict(title = 'Date Time'), yaxis = dict(title = 'Copies'))
    data = []
    if selected_row_indices is []:
        fig = dict(data=data, layout=layout)
        return fig
    else:
        conn = sqlite3.connect('HeartStone.sqlite')
        for i in selected_row_indices:
            UId = rows[i]['UId']
            name = rows[i]['Name'] + ' ' + rows[i]['Mode']
            mode = rows[i]['Mode']
            query = '''
            SELECT Copies, CollectTime FROM CardsPlay WHERE CardId = '{0}' AND Mode = '{1}'
            '''.format(UId, mode)
            df_plot = pd.read_sql_query(query, conn)
            df_plot['CollectTime'] = pd.to_datetime(df_plot['CollectTime'], format = '%m-%d %H:%M')
            df_plot['CollectTime'] = df_plot['CollectTime'].apply(lambda dt: dt.replace(year=2018))
            trace = go.Scatter(
                x = df_plot['CollectTime'],
                y = df_plot['Copies'],
                mode = 'lines+markers',
                name = name
            )
            data.append(trace)
        fig = dict(data=data, layout=layout)
        conn.close()
        return fig

@app.callback(
    Output('selected-cards', 'children'),
    [Input('CardsTable', 'rows'),
     Input('CardsTable', 'selected_row_indices')]
)
def update_cards_image(rows, selected_row_indices):
    content = []
    already_shown = []
    if selected_row_indices is []:
        return content
    else:
        for i in selected_row_indices:
            UId = rows[i]['UId']
            if UId in already_shown:
                continue
            else:
                card_name, card_set, card_Img, card_ImgGold = cards_images(UId)
                content.append(
                    html.Div(children = card_name + " from " + card_set)
                )
                content.append(
                    html.Div([
                        html.Img(src = card_Img),
                        html.Img(src = card_ImgGold)
                    ], style = {'columnCounts': 2})
                )
                content.append(html.Br())
                already_shown.append(UId)
        return content

if __name__ == '__main__':
    app.run_server(debug=True)
