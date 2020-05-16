import pandas as pd

dataset = pd.read_excel("covid_aggregated_filtered_2.xls")

dataset = main_df2.fillna(0)

dataset.rename(columns={'Unnamed: 0':'index'})
dataset['index'] = dataset['index'].replace({'United Kingdom':'UK'})

dataset=dataset[['index',
 #'Active',
 'Confirmed',
 'Deaths',
 #'FIPS',
 #'Lat',
 #'Latitude',
 #'Long_',
 #'Longitude',
 'Recovered',
 'record_date',
 'Population(m)',
 'Population density /sq mi']].copy()

dataset['Confirmed/million']=dataset['Confirmed']/dataset['Population(m)']
dataset['Deaths/million']=dataset['Deaths']/dataset['Population(m)']

#Function
years = main_df2['record_date'].unique()

t_positions=["top right","bottom left"]

colors = {}
colors_2 = [
    '#2f4f4f',
    '#006400',
    '#b8860b',
    '#cd5c5c',
    '#7f007f',
    '#ff0000',
    '#00ced1',
    '#ffff00',
    '#00ff00',
    '#0000ff',
    '#ff00ff',
    '#6495ed',
    '#98fb98',
    '#ffe4c4'
]


# make list of continents
countries = []
for country in dataset["index"]:
    if country not in countries:
        countries.append(country)

c=0
for i in countries:
    colors['{}'.format(i)]=['{}'.format(colors_2[c])]
    c=c+1

def create_animation(x_axis_column, y_axis_column, size_column):
    
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["yaxis"] = {"range": [-5, max(dataset[x_axis_column])+100], "title": "{}".format(x_axis_column)}
    fig_dict["layout"]["xaxis"] = {"range": [0, max(dataset[y_axis_column])+100], "title": "{}".format(y_axis_column)}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 38,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            #"prefix": "Date:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    year = years[0]
    for country in countries:
        dataset_by_year = dataset[dataset["record_date"] == year]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["index"] == country]

        data_dict = {
            "y": dataset_by_year_and_cont[x_axis_column],
            "x": dataset_by_year_and_cont[y_axis_column],
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["index"]),
            "marker": {
                "sizemode": "area",
                #"sizeref": 200,
                "size": list(dataset_by_year_and_cont[size_column])
            },
            "name": country
        }
        fig_dict["data"].append(data_dict)


    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for country in countries:
            dataset_by_year = dataset[dataset["record_date"] == year]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["index"] == country]

            data_dict = {
                "y": dataset_by_year_and_cont[x_axis_column],
                "x": dataset_by_year_and_cont[y_axis_column],
                "mode": "markers+text",
                "text": list(dataset_by_year_and_cont["index"]),
                "textposition": "top center",
                "marker": {
                    "sizemode": "area",
                    "opacity":0.5,
                    #"sizeref": 200,
                    "size": list(dataset_by_year_and_cont[size_column]),
                    "line":dict(
                        color='Black',
                        width=2
                    )
                },
                "name": country,
                "showlegend": True,            
            }


            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)


        slider_step = {"args": [
            [year],
            {"frame": {"duration": 0, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 30}}
        ],
            "label": year.strftime('%d %b'),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)
    fig.update_layout(template="plotly_white",
        autosize=False,
        width=1050,
        height=800,
        #paper_bgcolor="LightSteelBlue",
        title="Covid-19 - Deaths vs. Population density - US & top 10 countries"
    )

    return fig

#Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "https://codepen.io/chriddyp/pen/brPBPO.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

#available_indicators = df['Indicator Name'].unique()
available_x_axis = [
    'Confirmed',
    'Recovered',
    'Confirmed/million'
]

available_y_axis = [
    'Deaths',
    'Recovered',
    'Deaths/million'
]

available_z_axis = [
 'Population(m)',
 'Population density /sq mi'
]

app.layout = html.Div([
    html.Div([

        html.Div([
            html.Label(["X-axis"]),
            dcc.Dropdown(
                id='x-axis-selection', #'crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_x_axis],
                value='Confirmed/million'
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            html.Label(["Y-axis"]),
            dcc.Dropdown(
                id='y-axis-selection', #'crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_y_axis],
                value='Deaths/million'
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label(["Bubble size"]),
            dcc.Dropdown(
                id='z-axis-selection', #'crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_z_axis],
                value='Population(m)'
            ),
        ], style={'width': '20%', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        html.Div([
            dcc.Graph(
                id='bubble-animation',
                #hoverData={'points': [{'customdata': 'Japan'}]}
            )  
        ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        
        html.Div([
            
        ])
        ])
        

])

@app.callback(
    dash.dependencies.Output('bubble-animation', 'figure'),
    [dash.dependencies.Input('x-axis-selection', 'value'),
     dash.dependencies.Input('y-axis-selection', 'value'),
     dash.dependencies.Input('z-axis-selection', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, zaxis_column_name):
    created_fig = create_animation(xaxis_column_name, yaxis_column_name, zaxis_column_name)

    return created_fig

if __name__ == '__main__':
    app.run_server(debug=False)

