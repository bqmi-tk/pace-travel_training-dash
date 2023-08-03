##
#
# THIS PAGE IS NOW DEPRECIATED AND IS NO LONGER USED BY THE PACE Travel Training Tool
#
##

from app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import date
from dash.exceptions import PreventUpdate
import DB_SQL as db
from pages.partials import navbar

rf_passedData = []

layout = html.Div([
    navbar.content,
    html.Div(
        id="Full-Form-FS",
        children=[
            html.H2("A Travel and Training form was submitted with the following information:"),
            html.Div(
                id="form-Callback-Info"
            )
        ]
    )
])

def populateForm(ID):
    global rf_passedData
    if(rf_passedData):
        rf_passedData.clear()
        rf_passedData = db.lookupRow(ID)
        print(rf_passedData)
        print('\n\n\n\n')
    else:
        rf_passedData = db.lookupRow(ID)
        print(rf_passedData)
        print('\n\n\n\n')

@app.callback(Output('form-Callback-Info', 'children'),
            Input('url', 'pathname')
            )
def formConfirm(pathname):
    if pathname == '/Form-Submitted':
        return html.Div(
            html.Table(
                id='fs_OutputTable',
                children=[
                    html.Thead(
                        html.Tr(
                            [
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
                            [ # rf_passedData[i] = passed Data from Request Form | 0-14 Matches Table Headers
                                html.Td(rf_passedData[0]), #Employee Name
                                html.Td(rf_passedData[1]), #Employee Email
                                html.Td(rf_passedData[2]), #Employer
                                html.Td(rf_passedData[3]), #Training Title
                                html.Td(rf_passedData[4]), #Request Purpose
                                html.Td(rf_passedData[5]), #Certification (Y/N)
                                html.Td(rf_passedData[6]), #Travel Start Date
                                html.Td(rf_passedData[7]), #Travel End Date
                                html.Td(rf_passedData[8]), #Travel Destination
                                html.Td(rf_passedData[9]), #Training Start Date
                                html.Td(rf_passedData[10]), #Training End Date
                                html.Td(str(f"${'{0:.2f}'.format(rf_passedData[11])}")), #Total Cost
                                html.Td(rf_passedData[12]), #Work Order Lead
                                html.Td(rf_passedData[13]), #Company Supervisor
                                html.Td(rf_passedData[14]) #Work Order Manager
                            ]
                        )
                    )
                ]
            )
        )
