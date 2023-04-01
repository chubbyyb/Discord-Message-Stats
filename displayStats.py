import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import json

def displayStats():
    df = pd.read_csv(r'data\df1.csv')
    topUsers = pd.read_pickle(r'data\topUsers.pickle')
    x_values = topUsers[0][-11:]
    y_values = topUsers[2][-11:]
    f = open(r'data\word_counts.json')
    topWords = json.load(f)


    # Extract all the key-value pairs and sort them based on the values in descending order
    sorted_items = sorted(topWords.items(), key=lambda x: x[1], reverse=True)

    # Extract the top 3 items
    top_items = sorted_items[:10]

    # Create an empty dictionary to store the top 3 key-value pairs
    top_dict = {}

    # Add the top 3 key-value pairs to the dictionary using a for loop
    for item in top_items:
        key = item[0]
        value = item[1]
        top_dict[key] = value



    topWordKeys = list(top_dict.keys())
    topWordVals = list(top_dict.values())





    fig = go.Figure(
        data=go.Scatter(x=df['Timestamp'],y=df['Messages']),
        layout=go.Layout(
            title="Mt Bruno Elevation",
            width=2500,
            height=500,
        ))

    fig1 = go.Figure(
            go.Bar(
                x=x_values,
                y=y_values,
                orientation='h',),
            layout=go.Layout(title='',width=1250,height=500)
                
            )

    fig2 = go.Figure(
            go.Bar(
                x=topWordKeys,
                y=topWordVals,
                orientation='v',),
            layout=go.Layout(title='',width=1250-22,height=500)
                
            )

    fig.update_layout(template='plotly_dark', title="Messages Overtime")
    fig1.update_layout(template='plotly_dark', title="Top Users")
    fig2.update_layout(template='plotly_dark', title="Top Words")



    app = dash.Dash(
            meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )

    app.layout = html.Div(children=[
        html.H1('Discord Stats', style={'color': 'black', 'text-align': 'center'}),
        
        html.Div(className='row', children=[
            html.Div(className='col', children=[
                dcc.Graph(id='top-graph', figure=fig),
            ], style={'float': 'left', 'width': '100%'}),
        ]),
        
        html.Div(className='row', children=[
            html.Div(className='col', children=[
                dcc.Graph(id='bottom-left-graph', figure=fig1),
            ], style={'float': 'left', 'width': '50%'}),
            
            html.Div(className='col', children=[
                dcc.Graph(id='bottom-right-graph', figure=fig2),
            ], style={'float': 'left', 'width': '50%'}),
        ])
    ])


    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
