from app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import DB_SQL as db
from pages.partials import navbar

layout_employee = html.Div([
    navbar.content,
    html.Div(
        id='outerPSDiv',
        children=[
            dcc.Location(id='homePage', refresh=True),
            html.Div([
                html.H2('Select your identity:'),
                dcc.Dropdown(
                    id="UserSelection",
                    options= db.manualLogIn,
                    value= db.selectedUser,
                    persistence=True,
                    persistence_type='session'
                )
            ],style={
                'display': 'grid',
                'grid-template-rows': '50% 50%'
            }),
            html.Div(
                id="pageSelection",
                children=[
                    html.H2("PACEV Travel & Training"),
                    html.Div(
                        id="selectionPageBox",
                        children=[
                            html.A('New Request Form', href='/New-Request'),
                            html.Br(),
                            html.Br(),
                            html.A('View Your Requests', href='/My-Requests'),
                        ]
                    ),
                    html.Br(),
                    html.Div(id='dummy')
                ]
            )
        ]
    )
])

layout_manager = html.Div([
    navbar.content,
    html.Div(
        id='outerPSDiv',
        children=[
            dcc.Location(id='homePage', refresh=True),
            html.Div([
                html.H2('Select your identity:'),
                dcc.Dropdown(
                    id="UserSelection",
                    options= db.manualLogIn,
                    value= db.selectedUser,
                    persistence=True,
                    persistence_type='session'
                )
            ],style={
                'display': 'grid',
                'grid-template-rows': '50% 50%'
            }),
            html.Div(
                id="pageSelection",
                children=[
                    html.H2("PACEV Travel & Training"),
                    html.Div(
                        id="selectionPageBox",
                        children=[
                            html.A('New Request Form', href='/New-Request'),
                            html.Br(),
                            html.Br(),
                            html.A('View Your Requests', href='/My-Requests'),
                            html.Br(),
                            html.Br(),
                            html.A('Admin Control Panel', href='/admin'),
                        ]
                    ),
                    html.Br(),
                    html.Div(id='dummy')
                ]
            )
        ]
    )
])

layout_customer = html.Div([
    navbar.content,
    html.Div(
        id='outerPSDiv',
        children=[
            dcc.Location(id='homePage', refresh=True),
            html.Div([
                html.H2('Select your identity:'),
                dcc.Dropdown(
                    id="UserSelection",
                    options= db.manualLogIn,
                    value= db.selectedUser,
                    persistence=True,
                    persistence_type='session'
                )
            ],style={
                'display': 'inline'
            }),
            html.Div(
                id="pageSelection",
                children=[
                    html.H2("PACEV Travel & Training"),
                    html.Div(
                        id="selectionPageBox",
                        children=[
                            html.A('Admin Control Panel', href='/admin'),
                        ]
                    ),
                    html.Br(),
                    html.Div(id='dummy')
                ]
            )
        ]
    )
])

layout_loggedOut = html.Div([
    navbar.content,
    html.Div(
        id='outerPSDiv',
        children=[
            dcc.Location(id='homePage', refresh=True),
            html.Div([
                html.H2('Select your identity:'),
                dcc.Dropdown(
                    id="UserSelection",
                    options= db.manualLogIn,
                    value= db.selectedUser,
                    persistence=True,
                    persistence_type='session'
                )
            ],style={
                'display': 'grid',
                'grid-template-rows': '50% 50%'
            }),
            html.Div(
                id="pageSelection",
                children=[
                    html.H2("PACEV Travel & Training"),
                    html.Div(
                        id="selectionPageBox",
                        children=[
                            html.Br(),
                            html.Br(),
                            html.A('Select Your Identity and Click Here to Refresh', href='/'),
                            html.Br(),
                            html.Br(),
                        ]
                    ),
                    html.Br(),
                    html.Div(id='dummy')
                ]
            )
        ]
    )
])

@app.callback(Output('homePage', 'pathname'),
              Input('UserSelection', 'value'),
              Input('homePage', 'pathname'))

def storeUser(userSelection, pathname):
    if userSelection is not None:
        if pathname == '/':
            if userSelection != db.selectedUser:
                db.selectedUser = userSelection
                db.selectedUserRole = db.getRole(userSelection)
                return "/home"
            else:
                raise PreventUpdate
        elif pathname == '/home':
            if userSelection != db.selectedUser:
                db.selectedUser = userSelection
                db.selectedUserRole = db.getRole(userSelection)
                return "/"
            else:
                raise PreventUpdate
    else:
        raise PreventUpdate