from dash import html, dcc
from dash.dependencies import Input, Output
import DB_SQL as db
from app import app

content = html.Div(id='navBarUpdate')

@app.callback(
    Output('navBarUpdate', 'children'),
    Input('navBarUpdate', 'value'),
)

def appLayoutReload(navBar):
    if db.getRole(db.selectedUser) == 'E':
        return html.Div([
            html.Div(
                id="page-content-nav",
                    children=[
                        html.Ul([
                            html.Li(html.A('New Request Form', href='/New-Request')),
                            html.Li( html.A('View Your Requests', href='/My-Requests')),
                            html.Li(html.A('Home', href='/home'), 
                            style={
                                'float': 'right',
                            })
                        ]),
                    ]
            )
        ])
    elif db.getRole(db.selectedUser) == 'C':
        return html.Div([
            html.Div(
                id="page-content-nav",
                    children=[
                        html.Ul([
                            html.Li(html.A('Admin Control Panel', href='/admin')),
                            html.Li(html.A('Home', href='/home'), 
                            style={
                                'float': 'right',
                            })
                        ]),
                    ]
            )
        ])
    elif db.getRole(db.selectedUser) == 'M':
        return html.Div([
            html.Div(
                id="page-content-nav",
                    children=[
                        html.Ul([
                            html.Li(html.A('New Request Form', href='/New-Request')),
                            html.Li( html.A('View Your Requests', href='/My-Requests')),
                            html.Li(html.A('Admin Control Panel', href='/admin')),
                            html.Li(html.A('Home', href='/home'), 
                            style={
                                'float': 'right',
                            })
                        ]),
                    ]
            )
        ])
    elif db.getRole(db.selectedUser) == 'S':
        return html.Div([
            html.Div(
                id="page-content-nav",
                    children=[
                        html.Ul([
                            html.Li(html.A('New Request Form', href='/New-Request')),
                            html.Li( html.A('View Your Requests', href='/My-Requests')),
                            html.Li(html.A('Admin Control Panel', href='/admin')),
                            html.Li(html.A('User Access Panel', href='/userAccess')),
                            html.Li(html.A('Home', href='/home'), 
                            style={
                                'float': 'right',
                            })
                        ]),
                    ]
            )
        ])
    else:
        return html.Div([
            html.Div(
                id="page-content-nav",
                    children=[
                        html.Ul([
                            html.Li(html.A('Home', href='/home'), 
                            style={
                                'float': 'right',
                            })
                        ]),
                    ]
            )
        ])

