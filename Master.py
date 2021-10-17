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
key_input = dbc.FormGroup(
    [
        html.Div(dbc.Label("Places API Key", html_for="api_key"), style={'text-align': 'center'}),
        dbc.Input(id="api_key", placeholder="API key"),
        dbc.FormText(
            ["Don't have an API key? Get one ",
             dcc.Link('here', target="_blank",href='https://developers.google.com/maps/documentation/places/web-service/overview'), ],
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
limit_exceeded_message = dbc.Alert("Daily quota exceeded for this API!", color="warning", )

# ----------------------------------------------------------------------------------------------------------------------------

index_page = dbc.Container(
    [

        html.Div(html.Img(src=app.get_asset_url('EA_logo_resized.png')),
                 style={'padding-left': '20px', 'padding-top': '20px'}),
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        html.B("Lead Generation"),
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
@app.callback([Output('link-to-search-page', 'children'),
               Output('api-key-storage', 'data'),
               Output('verify-button', 'n_clicks')],

              [State('api_key', 'value'),
               Input('verify-button', 'n_clicks')])
def verify(api_key, n_clicks):
    if n_clicks is None or api_key == None:
        raise PreventUpdate
    else:
        if APIcheck(api_key)=='success':
            return success_message, api_key, 0
        elif APIcheck(api_key)=='OVER_QUERY_LIMIT':
            return limit_exceeded_message, api_key, 0
        return failure_message, api_key, 0


# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
location_input = dbc.FormGroup([
    dbc.Label('Location'),
    dbc.Input(id='input-location', placeholder='Eg. Ambattur, Chennai', debounce=True)
])
keyword_input = dbc.FormGroup([
    dbc.Label('Keyword'),
    dbc.Input(id='input-keyword', placeholder='Eg. Industry')
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
                {"label": "Open Now?", "value": 'opening_hours'},
                {"label": "Email (takes longer)", "value": 'email'},
            ],
            value=['formatted_phone_number', 'formatted_address', 'website'],
            id="switches-input",
            switch=True,
        ),
    ]
)
search_button = dbc.FormGroup([
    html.Div(dbc.Button('Search', id='search-button', n_clicks=0, color='primary'), style={'text-align': 'center'})
])

geo_map = html.Div(dbc.Card(dcc.Graph(id='graph')), id='graph-display', style={'display': 'None'})


@app.callback([Output('graph', 'figure'),
               Output('graph-display', 'style')],
              [State('api-key-storage', 'data'),
               Input('input-location', 'value')])
def location_update(api_key, location):
    if location == '':
        raise PreventUpdate
    return plot_location(api_key, location), {'display': 'block'}


input_box = dbc.Card([

    html.Div(dbc.Form([
        location_input,
        keyword_input,
        switches,
        search_button
    ]), style={'width': '80%', 'height': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'padding-top': '25px'}),
    html.Div(id='search-page-api-error')
],style={'width':'35vh'})

loading = dcc.Loading(
    id="loading",
    children=[html.Div([html.Div(id="loading-output")])],
    type="circle",
)

table = html.Div(html.Div(dbc.Card([
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
        }
        ,
        style_cell={
            'text-align': 'left', 'fontSize': 12, 'font-family': 'verdana'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        id='table',
        columns=[],
        export_format='csv',
        sort_action="native",
        sort_mode='multi',
        export_headers='display',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current=0,
    ),
]), id='table-box', style={'display': 'None'}),id='table-box2', style={'display': 'None'})

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
    html.Div(html.Img(src=app.get_asset_url('EA_logo_resized.png')),
             style={'padding-left': '20px', 'padding-top': '20px'}),

    html.H2(
        html.B("Lead Generation"),
        className="text-center mt-4 mb-5",
        style={"color": "Black", "text-decoration": "None", },
    ),
    dbc.Row([

        html.Br(),
        html.Br(),
        dbc.Col([dbc.Row([html.Br(), html.Br(), input_box]),
                 dbc.Row(html.Div(dcc.Link('<-Use different API key', href='/', style={'font-size': '15px'})))
                 ], width='auto'),
        dbc.Col(geo_map, width='auto')
    ], justify='center'),
    html.Br(),
    html.Div(loading, style={'text-align': 'center'}),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(table, width={'size': 10, 'offset': 1}),
    ], justify='center')
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
    [State(component_id='api-key-storage', component_property='data'),
     State(component_id='input-location', component_property='value'),
     State(component_id='input-keyword', component_property='value'),
     State(component_id='switches-input', component_property='value'),
     Input(component_id='search-button', component_property='n_clicks')]
)
def update_table(api_key, location, keyword, fields_list, n_clicks):
    if n_clicks == 0 or location is None or keyword is None:
        raise PreventUpdate
    if APIcheck(api_key) !='success':
        return location, keyword, 0, search_page_api_error, None, None, None, {'display': 'None'}
    else:
        df = get_details(api_key, location, keyword, fields_list)
        columns = [{'name': col, 'id': col , 'deletable': True} for col in df.columns]
        data = df.to_dict(orient='records')
        return location, keyword, 0, '', columns, data, None, {'display': 'Block'}


@app.callback(Output('table-box2','style'),[Input('table-box','style'),Input('search-button','n_clicks')])
def remove_table(style,n_clicks):
    if n_clicks==0 or style=={'display': 'None'}:
        return {'display':'Block'}
    else:
        return {'display': 'None'}
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------


app.layout = html.Div([
    dcc.Store(id='api-key-storage', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dcc.Link('FEEDBACK FORM', href='https://forms.gle/BRHXfLUpk8bdNk52A', target="_blank", style={'font-size': '15px'}), style={'text-align': 'center'})
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
