import pandas as pd
from pkg_resources import Environment
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import shelve
import dataReview
import config
import dash_table



#Grab and Clean Data
data = shelve.open('history.db')
history = data['history']
data.close()
versions = dataReview.orderVersion(history['versions'])


standard_BS = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__, external_stylesheets=[standard_BS])

option = []
for version in versions:
    option.append({"label": version, "value": version})


#Determines if a model has successfully passed and outputs % finished and devices that aren't done
def percentDone(version):
    deviceNumber = len(config.iphones)
    complete = 0
    notComplete = []
    for device in range(len(history[version])):
        if history[version][device]['model'] in config.iphones:
            if history[version][device]['iosReset'] == True and history[version][device]['smartReset'] == True and history[version][device]['fmip']['unlocked'] > 0:
                complete += 1   
            else:
                notComplete.append(device)
    percent = round((complete/deviceNumber),2)
    if percent > 1:
        return "Complete", notComplete
    else:
        #print(len(config.iphones))
        return int(percent*100), notComplete


def unfinishedModels(version): 
    broken = percentDone(version)[1]
    models = []
    for model in range(len(history[version])):
        if 'iPhone' in history[version][model]:
            models.append(history[version][model])
    new = list(set(models) - set(config.iphones))
    total = broken + new 
    print(total)
    return total

#def check(outcome):

def generateTable(df, version):
    df = pd.DataFrame(history[version], columns = ['model', 'smartReset', 'iosReset', 'success', 'fail'])
    return dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records')
    )

app.layout = html.Div([
    html.H1("Blancco UAT Progress", style={'text-align': 'center'}),
    html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id="versions",
                        options=option, 
                        multi=False,
                        value=versions[0]
                        ),
                        width={"size": 3}),
        dbc.Col(
            html.H4(id='head'), width={"size": 2}
                ),
        dbc.Col(id='progress', width={"size": 7}),
    ])]),
    html.Div(id='output_container'),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar', figure={},), width={"size": 4}),
        dbc.Col(dash_table.DataTable(id='table',columns=[{"name": i, "id": i} for i in ['model', 'Total', 'smartReset', 'iosReset', 'Success Rate(%)']]), width={"size": 8}, style={'text-align': 'center'})
    ]),

    ], style = {"width": '100%', "overflow-x": "hidden"})


@app.callback(
    [Output(component_id='head', component_property='children'),
     Output(component_id='progress', component_property='children'),
     Output(component_id='bar', component_property='figure'),
     Output('table', 'data')
     ],
    [Input(component_id='versions', component_property='value')]
    )
def updateDash(versionSelected):
    done = int(percentDone(versionSelected)[0])
    container = "Version : {}\t\t\t".format(versionSelected)
    progress = dbc.Progress("{}%".format(done), value = done)
    
#horizontal bar graph  
    df =  pd.DataFrame(history[versionSelected], columns = ['model', 'success', 'fail'])
    df['Success Rate'] = (round(df['success'] / (df['success'] + df['fail']),2)*100) 
    mask = df['model'].str.contains('iPhone ')
    df2 = df[mask].loc[df['Success Rate'] < 90]
    fig = px.bar(df2, y="model", x='Success Rate', orientation='h', title='Below 90% Success Rate')
#main table
    df3 = pd.DataFrame(history[versionSelected], columns = ['model', 'smartReset', 'iosReset', 'fmip', 'success', 'fail'])
    df3['Total'] = (df3['success'] + df3['fail'])
    df3['Success Rate(%)'] = (round(df3['success'] / (df3['success'] + df3['fail']),2)*100)
    mask1 = df3['model'].str.contains('iPhone ')
    df4 = df3[mask1].loc[(df3['iosReset'] == False) | (df3['smartReset']== False) | (df3['Success Rate(%)'] < 90)]
    table = df4.to_dict('records')
    return container, progress, fig, table



if __name__ == '__main__':
    app.run_server(debug=True)