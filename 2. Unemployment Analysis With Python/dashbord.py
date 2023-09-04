from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("Unemployment in India.csv")
df.drop('Frequency', axis=1, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

def make_line_with(
        title,
        colName,
        region='all',
        area='all',
        year='all',
        month='all'):

    ndf = df.copy()

    if region != 'all':
        ndf = ndf[ ndf['Region'] == region ]
        title+=f' in {region}'

    if area != 'all':
        ndf = ndf[ ndf['Area'] == area ]
        title+=f', {area}'

    if year != 'all':
        ndf = ndf[ ndf['Year'] == year ]
        title+=f' in ({year}'

    if month != 'all':
        ndf = ndf[ndf['Month'] == int(month)]
        if year == 'all': title += f' In Month {month}'
        else :
            title+=f', {month})'
    else:
        if year and year!= 'all':
            title+=f')'


    line = px.line(
    ndf,
    x='Date',
    y=colName,
    color='Area',
    title=title,
    labels={colName:'Rate (%)'},
    markers=True

    )
    return line


init_estimated_unemployment_rate_graph = make_line_with(title='Estimated Unemployment Rate',
                                                        colName='Estimated Unemployment Rate (%)',
                                                        region='Andhra Pradesh')

init_estimated_labour_participation_rate = make_line_with(title='Estimated Labour Participation Rate',
                                                          colName='Estimated Labour Participation Rate (%)',
                                                          region='Andhra Pradesh')


color = '#9A9AE8'

app = Dash(__name__)

app.layout = html.Div(children=[

    html.H1('UNEMPLOYMENT Dashboard ANALYSIS WITH PYTHON'.title(),
            style={
                'background-color':color,
                'padding':'10px',
                'textAlign':'center',
                'margin':'auto',
                'width':'55%',
               "box-shadow": "8px 8px"
            }),

    html.Br(),

    # input Dropdowns
    html.Div(
        children=[

        # region input
        html.Div(
            children=[
            'Region',
            dcc.Dropdown(
                id='in-region',
                options=['all'] + df['Region'].unique().tolist(),
                value='Andhra Pradesh',
                style={
                    'width':220,
                    'margin-left':10,
                    'font-size':25
                }

            )
        ],
            style={'display':'flex',
           'font-size':30,
           'margin':'10px'}),

        # area input
        html.Div(
            children=[
                'Area',
                dcc.Dropdown(
                    id='in-area',
                    options=['all'] + df['Area'].unique().tolist(),
                    value='all',
                    style={
                        'width': 150,
                        'margin-left': 10,
                        'font-size': 25
                    }
                )
            ],
            style={'display': 'flex',
                   'font-size': 30,
                   'margin': '10px'}),

        # year input
        html.Div(
            children=[
            'Year',
            dcc.Dropdown(
                id='in-year',
                options=['all'] + df['Year'].unique().tolist(),
                value='all',
                style={
                    'width':120,
                    'margin-left':10,
                    'font-size':25
                }
            )
        ],
            style={'display':'flex',
               'font-size':30,
               'margin':'10px'})
        ,
        # month input
        html.Div(
            children=[
            'Month',
            dcc.Dropdown(
                id='in-month',
                options=['all'] + sorted(df['Month'].unique().tolist()),
                value='all',
                style={
                    'width': 100,
                    'margin-left':10,
                    'font-size':25
                }

            )
        ],
            style={'display':'flex',
               'font-size':30,
               'margin':'10px'})

    ],
        style={'display':'flex',
               'flex-wrap':'wrap',
               'justify-content':'space-around',
               'background-color': color,
               'margin': 'auto',
               "box-shadow": "8px 8px",
               'width':'95%'
               }
    ),

    html.Br(),

    # graphs container
    html.Div(
        children=[
            dcc.Graph(
                id='estimated_unemployment_rate_graph',
                figure=init_estimated_unemployment_rate_graph,
                style={
                    'width':"49%",
                    'margin':'5px 0 5px 5px'
                }
            ),
            dcc.Graph(
                id='estimated_labour_participation_rate_graph',
                figure=init_estimated_labour_participation_rate,
                style={
                    'width':"49%",
                    'margin':'5px 5px 5px 0px'
                }
            ),
        ],
        style={
            'display':'flex',
            'flex-wrap':'wrap',
            'justify-content':'space-around',
            'background-color': color,
            'margin': 'auto',
            "box-shadow": "8px 8px",
            'width':'95%'
             }
    )
])


@callback(
    Output('estimated_unemployment_rate_graph', 'figure'),
    [
        Input('in-region', 'value'),
        Input('in-area', 'value'),
        Input('in-year', 'value'),
        Input('in-month', 'value'),
    ]
)
def update_eur(region, area, year, month):
    return make_line_with(region=region,
                          area=area,
                          year=year,
                          month=month,
                          title='Estimated Unemployment Rate',
                          colName='Estimated Unemployment Rate (%)')


@callback(
    Output('estimated_labour_participation_rate_graph', 'figure'),
    [
        Input('in-region', 'value'),
        Input('in-area', 'value'),
        Input('in-year', 'value'),
        Input('in-month', 'value'),
    ]
)
def update_elp(region, area, year, month):
    return  make_line_with(title='Estimated Labour Participation Rate',
                           colName='Estimated Labour Participation Rate (%)',
                           region=region,
                           area=area,
                           year=year,
                           month=month)


app.run(debug=True)