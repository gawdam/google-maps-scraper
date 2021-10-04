import dash
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from GooglePlacesAPIcheck import APIcheck
from GoogleMapsPlotter import plot_location
from GoogleMapsScrapper import get_details

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA])
server = app.server
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
logo_url = 'data:image/png;base64,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'
key_input = dbc.FormGroup(
    [
        html.Div(dbc.Label("Places API Key", html_for="api_key"), style={'text-align': 'center'}),
        dbc.Input(id="api_key", placeholder="API key"),
        dbc.FormText(
            ["Don't have an API key? Get one ",
             dcc.Link('here', href='https://developers.google.com/maps/documentation/places/web-service/overview'), ],
            color="secondary",
        ),

        html.Br(),
        html.Div(dbc.Button('Verify', id='verify-button', n_clicks=0, color='primary'), style={'text-align': 'center'})
    ]
)

form = dbc.Form([key_input])
output = html.Div(id='link-to-search-page')
card = dbc.Card([
    html.Div(dbc.CardImg(src=app.get_asset_url('Google_Maps_logo_icon.png'), top=True),
             style={'width': '50%', 'height': '50%', 'margin-left': 'auto', 'margin-right': 'auto',
                    'padding-top': '25px'}),
    dbc.CardBody([
        # content
        form,
        output
    ])])
index_page = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        html.B("Google Maps: Yellow Pages"),
                        className="text-center mt-4 mb-5",
                        style={"color": "Black", "text-decoration": "None", },
                    )
                )
            ]
        ),
        dbc.Row(
            [dbc.Col(card, width="auto")],
            justify="center",
        ),
    ],
    fluid=True,
)
# ----------------------------------------------------------------------------------------------------------------------------
success_message = dbc.Alert(
    [
        "The API has been verified!\n",
        html.Br()
        ,
        html.A(html.B("Click here to search for places"), href="/search", className="alert-link"),
    ],
    color="success",
)
failure_message = dbc.Alert("This API is invalid!", color="danger", )


# ----------------------------------------------------------------------------------------------------------------------------
@app.callback([Output('link-to-search-page', 'children'),
               Output('api-key-storage', 'data'),
               Output('verify-button', 'n_clicks')],

              [State('api_key', 'value'),
               Input('verify-button', 'n_clicks')])
def verify(api_key, n_clicks):
    if n_clicks is None or api_key == None:
        raise PreventUpdate
    else:
        if APIcheck(api_key):
            return success_message, api_key, 0
        else:
            return failure_message, api_key, 0


# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
location_input = dbc.FormGroup([
    dbc.Label('Location'),
    dbc.Input(id='input-location',placeholder= 'Eg. Ambattur, Chennai',debounce=True)
])
keyword_input = dbc.FormGroup([
    dbc.Label('Keyword'),
    dbc.Input(id='input-keyword',placeholder= 'Eg. Industry')
])
switches = dbc.FormGroup(
    [
        dbc.Label("Select Fields"),
        dbc.Checklist(
            options=[
                {"label": "Phone Number", "value": 'formatted_phone_number'},
                {"label": "Address", "value": 'formatted_address'},
                {"label": "Website", "value": 'website'},
                {"label": "Price Level", "value": 'price_level'},
                {"label": "Google Rating", "value": 'rating'},
                {"label": "Open Now?", "value": 'opening_hours'}
            ],
            value=['formatted_phone_number','formatted_address','website'],
            id="switches-input",
            switch=True,
        ),
    ]
)
search_button = dbc.FormGroup([
    html.Div(dbc.Button('Search', id='search-button', n_clicks=0, color='primary'), style={'text-align': 'center'})
])

geo_map = html.Div(dbc.Card(dcc.Graph(id='graph')),id='graph-display',style={'display':'None'})

@app.callback([Output('graph','figure'),
               Output('graph-display','style')],
              [State('api-key-storage','data'),
                  Input('input-location','value')])
def location_update(api_key,location):
    if location =='':
        raise PreventUpdate
    return plot_location(api_key,location),{'display':'block'}


input_box = dbc.Card([

    html.Div(dbc.Form([
        location_input,
        keyword_input,
        switches,
        search_button
    ]),style={'width':'80%','height':'80%','margin-left':'auto','margin-right':'auto','padding-top':'25px'}),
    html.Div(id='search-page-api-error')
])

loading = dcc.Loading(
                    id="loading",
                    children=[html.Div([html.Div(id="loading-output")])],
                    type="circle",
                )

table = html.Div(dbc.Card([
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
        },
        style_cell_conditional=[
                {'if': {'column_id': 'row_num'},
                 'width': '10%'},
                {'if': {'column_id': 'name'},
                 'width': '20%'},
                {'if': {'column_id': 'formatted_phone_number'},
                                 'width': '20%'},
                {'if': {'column_id': 'formatted_address'},
                                 'width': '50%'},
            ]
        ,
        style_cell={
            'text-align':'left','fontSize':12, 'font-family':'verdana'
        },
        style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
        id='table',
        columns=[],
        export_format='csv',
    ),
]),id='table-box',style= {'display': 'None'})

search_page_api_error = dbc.Alert(
    [
        "This session is invalid!\n",
        html.Br()
        ,
        html.A(html.B("<- Go back"), href="/", className="alert-link"),
    ],
    color="danger",
)

search_page = html.Div([
        html.H2(
            html.B("Google Maps: Yellow Pages"),
            className="text-center mt-4 mb-5",
            style={"color": "Black", "text-decoration": "None", },
        ),
    dbc.Row([

        html.Br(),
        html.Br(),
        dbc.Col([dbc.Row([html.Br(),html.Br(),input_box]),
                 dbc.Row(html.Div(dcc.Link('<-Use different API key',href='/',style={'font-size':'15px'})))
    ],width='auto'),
        dbc.Col(geo_map,width='auto')
    ],justify='center'),
    html.Br(),
    html.Div(loading,style={'text-align':'center'}),

    dbc.Row([
        dbc.Col(table,width={'size':10,'offset':1}),
    ],justify='center')
])

# ------------------------------------------------------------------------
@app.callback(
    [Output(component_id='input-location', component_property='value'),
     Output(component_id='input-keyword', component_property='value'),
     Output(component_id='search-button', component_property='n_clicks'),
     Output(component_id='search-page-api-error', component_property='children'),
     Output(component_id='table', component_property='columns'),
     Output(component_id='table', component_property='data'),
     Output(component_id="loading-output", component_property="children"),
     Output(component_id="table-box", component_property="style")],
    [State(component_id='api-key-storage',component_property='data'),
     State(component_id='input-location', component_property='value'),
     State(component_id='input-keyword', component_property='value'),
     State(component_id='switches-input', component_property='value'),
     Input(component_id='search-button', component_property='n_clicks')]
)
def update_table(api_key,location,keyword, fields_list,n_clicks):
    if n_clicks==0:
        raise PreventUpdate
    if api_key == None:
        return location,keyword,0, search_page_api_error,None,None,None, {'display': 'none'}
    else:
        df = get_details(api_key, location, keyword, fields_list)
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict(orient='records')
        return location, keyword, 0,'' ,columns, data,None , {'display': 'Block'}
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------


app.layout = html.Div([
    dcc.Store(id='api-key-storage',storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/search':
        return search_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
