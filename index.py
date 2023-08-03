from dash import html, dcc
from dash.dependencies import Input, Output
from pages import Request_Form as rf, Form_Submitted as fs, admin as admin, Page_Selection as ps, User_Requests as ur
import DB_SQL as db
from app import app
from dash.exceptions import PreventUpdate

server = app.server

app.layout = html.Div([
            dcc.Location(id='url', refresh=True),
            html.Div(id='page-content')
        ])

def getSubDirectory():
    if db.getRole(db.selectedUser) == 'E':
        return html.Div(
            id='SubDir',
            children=[
                html.H2('Available Page Redirects:'),
                html.Br(),
                html.Br(),
                html.A("New Request Form", href="/New-Request"),
                html.Br(),
                html.A("My Requests", href="/My-Requests"),
                html.Br(),
                html.A("Home", href="/home")
            ]
        )
    elif db.getRole(db.selectedUser) == 'C':
        return html.Div(
            id='SubDir',
            children=[
                html.H2('Available Page Redirects:'),
                html.Br(),
                html.Br(),
                html.A("Admin Control Panel", href="/admin"),
                html.Br(),
                html.A("Home", href="/home")
            ]
        )
    elif db.getRole(db.selectedUser) == 'M':
        return html.Div(
            id='SubDir',
            children=[
                html.H2('Available Page Redirects:'),
                html.Br(),
                html.Br(),
                html.A("New Request Form", href="/New-Request"),
                html.Br(),
                html.A("My Requests", href="/My-Requests"),
                html.Br(),
                html.A("Admin Control Panel", href="/admin"),
                html.Br(),
                html.A("Home", href="/home")
            ]
        )
    else:
        return html.Div(
            id='SubDir',
            children=[
                html.H2('Available Page Redirects:'),
                html.Br(),
                html.Br(),
                html.A("Home", href="/home")
            ]
        )


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or str(pathname).lower() == '/home'.lower():
        if db.getRole(db.selectedUser) == 'E':
            return ps.layout_employee
        elif db.getRole(db.selectedUser) == 'C':
            return ps.layout_customer
        elif db.getRole(db.selectedUser) == 'M':
            return ps.layout_manager
        else:
            return ps.layout_loggedOut
    elif str(pathname).lower() == '/New-Request'.lower() or str(pathname).lower() == '/New-Request/'.lower():
        return rf.content
    elif str(pathname).lower() == '/Form-Submitted'.lower() or str(pathname).lower() == '/Form-Submitted/'.lower():
        return fs.layout
    elif str(pathname).lower() == '/admin'.lower() or str(pathname).lower() == '/admin/'.lower() or '&URID='.lower() in str(pathname).lower() or str(pathname).lower() == '/admin/rejected'.lower() or str(pathname).lower() == '/admin/rejected/'.lower() or str(pathname).lower() == '/admin/activerequests'.lower() or str(pathname).lower() == '/admin/activerequests/myapproval'.lower() or str(pathname).lower() == '/admin/activerequests/'.lower() or str(pathname).lower() == '/admin/approved'.lower() or str(pathname).lower() == '/admin/approved/'.lower() or "/admin/moreInfo".lower() in str(pathname).lower() or "/admin/editRequest".lower() in str(pathname).lower() or "/admin/lookup".lower() in str(pathname).lower():
        return admin.layout
    elif ("/My-Requests".lower() in str(pathname).lower()):
        return ur.layout
    elif (str(pathname).lower() == '/login'):
        return dcc.Location(id='urlLogin', refresh=True)
    elif (str(pathname).lower() == '/directory'):
        return getSubDirectory()
    else:
        return html.Div([
            html.A("404: Page Not Found\n\n Click to view available page directory.", href="/directory")
        ])
        


if __name__ == '__main__':
    app.run_server(debug=False)