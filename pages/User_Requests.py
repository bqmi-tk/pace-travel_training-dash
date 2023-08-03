from app import app
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State, ALL
from datetime import date
from dash.exceptions import PreventUpdate
import DB_SQL as db
import time
from pages.partials import navbar

@app.callback(
    Output('requestsURL', 'pathname'),
    Input('requestsURL', 'pathname'),
    Input({'type': 'expandRequestBTN', 'index': ALL}, 'n_clicks'),
    Input({'type': 'backBTN', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)

def buttonPressedMyRequests(pathname, expandInfoBtn, backBtn):
    if('/My-Requests'.lower() in str(pathname).lower()):
        results = db.loadRequestsDESC(db.selectedUser)
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                selected = results[i]
                return f"/My-Requests/moreInfo/request={selected[0]}"
        for i in range(len(backBtn)):
            if backBtn[i] is not None:
                selected = results[i]
                return f"/My-Requests"
    raise PreventUpdate

@app.callback(
    Output('userRequests', 'children'),
    Input('url', 'pathname')
)

def displayUserRequests(pathname):
    tableResults = []
    if('/My-Requests'.lower() in str(pathname).lower()):
        employee = db.selectedUser
        results = []
        results = db.loadRequestsDESC(employee)
        tableResults = []
        if(results is not None):
            for row in results:
                tableResults.append(
                    html.Div(
                        id="myRequestsTableTop",
                        children=[
                            html.Button(
                                'More Info',
                                id={
                                    'type': 'expandRequestBTN',
                                    'index': 'expandRequest'
                                },
                                style={
                                    "background-color": "Gray"
                                }
                            ),
                            html.Div(
                                id="myRequestsTable",
                                children=[
                                    html.Table(
                                        id=f'myRequestspprovalTable{row[0]}',
                                        children=[
                                            html.Thead(
                                                html.Tr(
                                                    [
                                                        html.Th("Approval Status"),
                                                        html.Th("Name"),
                                                        html.Th("Email"),
                                                        html.Th("Employeer"),
                                                        html.Th("Training Title"),
                                                        html.Th("Request Purpose"),
                                                        html.Th("Certification"),
                                                        html.Th("Travel Start Date"),
                                                        html.Th("Travel End Date"),
                                                        html.Th("Travel Destination"),
                                                        html.Th("Training Start Date"),
                                                        html.Th("Training End Date"),
                                                        html.Th("Total Cost"),
                                                        html.Th("Work Order Lead"),
                                                        html.Th("Company Supervisor"),
                                                        html.Th("Work Order Manager")
                                                    ]
                                                )
                                            ),
                                            html.Tbody(
                                                html.Tr(
                                                    [
                                                        html.Td(row[2]), #Approval Status
                                                        html.Td(row[3]), #Name
                                                        html.Td(row[4]), #Email
                                                        html.Td(row[5]), #Employer
                                                        html.Td(row[7]), #Training Title
                                                        html.Td(row[8]), #Purpose
                                                        html.Td(row[9]), #Certification?
                                                        html.Td(row[10]), #Travel Start Date
                                                        html.Td(row[11]), #Travel End Date
                                                        html.Td(row[12]), #Travel Destination
                                                        html.Td(row[13]), #Training Start Date
                                                        html.Td(row[14]), #Training End Date
                                                        html.Td(row[15]), #Total Cost
                                                        html.Td(row[16]), #Work Order Lead
                                                        html.Td(row[17]), #Company Supervisor
                                                        html.Td(row[18]), #Work Order Manager
                                                    ]
                                                )
                                            )
                                        ]
                                    ),
                                ]
                            )
                        ]
                    )
                )
    if('/My-Requests/moreInfo'.lower() in str(pathname).lower()):
        results = []
        results = db.expandRow(pathname.split('request=')[1])
        tableResults = []
        tableResults.append(
            html.Div(
                id='Back',
                children=[
                    html.Button(
                        'Back',
                        id={
                            'type': 'backBTN',
                            'index': 'backBTN'
                        },
                        style={
                            "background-color": "Gray"
                        }
                    ),
                    html.Div(
                        id="infoGrid",
                        children=[
                            html.Div(
                                id='expandedLeftSide',
                                children=[
                                    html.H3('Request ID:'),
                                    html.H3('Date Created:'),
                                    html.H3('Approval Status:'),
                                    html.H3('Employee Name:'),
                                    html.H3('Employee Email:'),
                                    html.H3('Employer:'),
                                    html.H3('Project Code:'),
                                    html.H3('Training Title:'),
                                    html.H3('Training Purpose:'),
                                    html.H3('Certification:'),
                                    html.H3('Travel Start Date:'),
                                    html.H3('Travel End Date:'),
                                    html.H3('Destination:'),
                                    html.H3('Training Start Date:'),
                                    html.H3('Training End Date:'),
                                    html.H3('Total Cost:'),
                                    html.H3('Work Order Lead:'),
                                    html.H3('Company Supervisor:'),
                                    html.H3('Work Order Manager:'),
                                    html.H3('Training Cost:'),
                                    html.H3('Trip M&IE:'),
                                    html.H3('Trip Lodging:'),
                                    html.H3('Trip Lodging Taxes & Fees:'),
                                    html.H3('Round Trip Auto Mileage Cost:'),
                                    html.H3('Rental Car Place:'),
                                    html.H3('Ground Transportation Fees:'),
                                    html.H3('Estimated Fuel Cost:'),
                                    html.H3('Estimated Airfare Cost:'),
                                    html.H3('Baggage Fees:'),
                                    html.H3('Other Costs:')
                                ]
                            ),
                            html.Div(
                                id='expandedRightSide',
                                children=[
                                    html.H3(f'{results[0]}'),
                                    html.H3(f'{results[1]}'),
                                    html.H3(f'{results[2]}'),
                                    html.H3(f'{results[3]}'),
                                    html.H3(f'{results[4]}'),
                                    html.H3(f'{results[5]}'),
                                    html.H3(f'{results[6]}'),
                                    html.H3(f'{results[7]}'),
                                    html.H3(f'{results[8]}'),
                                    html.H3(f'{results[9]}'),
                                    html.H3(f'{results[10]}'),
                                    html.H3(f'{results[11]}'),
                                    html.H3(f'{results[12]}'),
                                    html.H3(f'{results[13]}'),
                                    html.H3(f'{results[14]}'),
                                    html.H3(str(f"${'{0:.2f}'.format(results[15])}")),
                                    html.H3(f'{results[16]}'),
                                    html.H3(f'{results[17]}'),
                                    html.H3(f'{results[18]}'),
                                    html.H3(str(f"${'{0:.2f}'.format(results[19])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[20])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[21])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[22])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[23])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[24])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[25])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[26])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[27])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[28])}")),
                                    html.H3(str(f"${'{0:.2f}'.format(results[29])}")),
                                ]
                            )
                        ],
                        style={
                            'display': 'grid',
                            'grid-template-columns': '50% 50%'
                        }
                    ) 
                ]
            )
        )
    if tableResults:
        return tableResults
    else:
        return html.Div([
            html.H1("You have not made any requests."),
            html.Br(),
            html.H3("Travel and Training requests made under your name will appear here.")
        ])
        
layout = html.Div([
    navbar.content,
    html.Div(
        id="userRequestsOuterDiv",
        children=[
            dcc.Location(id='requestsURL', refresh=True),
            html.Div(
                id="userRequests"
            )
        ]
    )
])
