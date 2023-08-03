from app import app
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State, ALL
from datetime import date
from dash.exceptions import PreventUpdate
import DB_SQL as db
import time
from pages.partials import navbar

@app.callback(
    Output('adminConfirmURL', 'pathname'),
    Input('adminConfirmURL', 'pathname'),
    Input('confirmApprove', 'submit_n_clicks'),
    Input('confirmReject', 'submit_n_clicks'),
    Input('confirmResendEmail', 'submit_n_clicks'),
    prevent_initial_call=True
)

def confirmButton(pathname, confirmApprove, confirmReject, confirmResendEmail):
    try: ## Try for approval/reject
        splitString = str(pathname).lower().split('&urid=')
        uRid = splitString[1].split('&confirm=')[0]
        if(confirmApprove):
            db.approveRow(uRid)
            print('Row Approved')
        if(confirmReject):
            db.rejectRow(uRid)
            print('Row Rejected')
        if(confirmResendEmail):
            db.resendEmail(uRid)
            print('Email Resent')
        raise PreventUpdate
    except:
        raise PreventUpdate


@app.callback(
    Output('url', 'pathname'),
    Output('confirmApprove', 'displayed'),
    Output('confirmReject', 'displayed'),
    Output('confirmResendEmail', 'displayed'),
    Input('url', 'pathname'),
    Input({'type': 'dyn-btn', 'index': ALL}, 'n_clicks'),
    Input({'type': 'dyn-btn-reject', 'index': ALL}, 'n_clicks'),
    Input({'type': 'expandRequestBTN', 'index': ALL}, 'n_clicks'),
    Input({'type': 'editRequestBTN', 'index': ALL}, 'n_clicks'),
    Input({'type': 'updateRequestBTN', 'index': ALL}, 'n_clicks'),
    Input({'type': 'resendEmailBTN', 'index': ALL}, 'n_clicks'),
    Input('adminLookupEmployeeName', 'value'),
    prevent_initial_call=True
)

def buttonPressedAdmin(pathname, approveBtn, rejectBtn, expandInfoBtn, editInfoBtn, updateRequestBtn, resendEmailBtn, employeeName):
    if('redirectLog'.lower() in str(pathname).lower()):
        try:
            userLogIn = str(pathname).lower().split('redirectlog=')[1]
            if '&URID='.lower() in userLogIn.lower():
                userLogIn = userLogIn.split('&URID=')[0]
            if '&Confirm='.lower() in userLogIn.lower():
                userLogIn = userLogIn.split('&Confirm=')[0]
            
            db.selectedUser = db.getUserWithDBID(userLogIn)
            db.selectedUserRole = db.getRole(db.selectedUser)
        except:
            None
        
    if('/admin'.lower() in str(pathname).lower()):
        if(db.getRole(db.selectedUser) == 'E' or db.getRole(db.selectedUser) is None): #Prevents employees from entering admin room
            return "/home", False, False, False
    if(str(pathname).lower() == '/admin'.lower() or '&URID='.lower() in str(pathname).lower()):
        if('&URID='.lower() in str(pathname).lower()):
            splitString = str(pathname).lower().split('&urid=')
            uRid = splitString[1].split('&confirm=')[0]
            confirm = splitString[1].split('&confirm=')[1]
            if(confirm == 'true'):
                return splitString[0], True, False, False
            elif(confirm == 'false'):
                return splitString[0], False, True, False
            elif(confirm == 'resend'):
                return splitString[0], False, False, True
        results = db.loadRequests(employeeName)
        for i in range(len(approveBtn)):
            if approveBtn[i] is not None:
                selected = results[i]
                # db.approveRow(selected[0])
                return pathname + f"&URID={selected[0]}&Confirm=True", False, False, False
        for i in range(len(rejectBtn)):
            if rejectBtn[i] is not None:
                selected = results[i]
                # db.rejectRow(selected[0])
                return pathname + f"&URID={selected[0]}&Confirm=False", False, False, False
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/moreInfo/request={selected[0]}", False, False, False
        for i in range(len(editInfoBtn)):
            if editInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/editRequest/request={selected[0]}", False, False, False
    if(str(pathname).lower() == '/admin/activerequests'.lower()):
        results = db.loadActiveRequests(employeeName)
        for i in range(len(approveBtn)):
            if approveBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=True", False, False, False
        for i in range(len(rejectBtn)):
            if rejectBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=False", False, False, False
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/moreInfo/request={selected[0]}", False, False, False
        for i in range(len(editInfoBtn)):
            if editInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/editRequest/request={selected[0]}"
    if(str(pathname).lower() == '/admin/rejected'.lower()):
        results = db.loadRejectedRequests(employeeName)
        for i in range(len(approveBtn)):
            if approveBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=True", False, False, False
        for i in range(len(rejectBtn)):
            if rejectBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=False", False, False, False
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/moreInfo/request={selected[0]}", False, False, False
        for i in range(len(editInfoBtn)):
            if editInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/editRequest/request={selected[0]}", False, False, False
    if(str(pathname).lower() == '/admin/approved'.lower()):
        results = db.loadApprovedRequests(employeeName)
        for i in range(len(approveBtn)):
            if approveBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=True", False, False, False
        for i in range(len(rejectBtn)):
            if rejectBtn[i] is not None:
                selected = results[i]
                return pathname + f"&URID={selected[0]}&Confirm=False", False, False, False
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/moreInfo/request={selected[0]}", False, False, False
        for i in range(len(editInfoBtn)):
            if editInfoBtn[i] is not None:
                selected = results[i]
                return f"/admin/editRequest/request={selected[0]}", False, False, False
    if('/admin/editRequest'.lower() in str(pathname).lower()):
        for i in range(len(updateRequestBtn)):
            if updateRequestBtn[i] is not None:
                time.sleep(1)
                return "/admin", False, False, False
    if('/admin/lookup'.lower() in str(pathname).lower()):
        selectedID = str(pathname).lower().split('lookup=')[1]
        selectedID = selectedID.split('&')[0]
        for i in range(len(approveBtn)):
            if approveBtn[i] is not None:
                return pathname + f"&URID={selectedID}&Confirm=True", False, False, False
        for i in range(len(rejectBtn)):
            if rejectBtn[i] is not None:
                return pathname + f"&URID={selectedID}&Confirm=False", False, False, False
        for i in range(len(expandInfoBtn)):
            if expandInfoBtn[i] is not None:
                return f"/admin/moreInfo/request={selectedID}", False, False, False
    if('/admin/moreInfo'.lower() in str(pathname).lower()):
        for i in range(len(resendEmailBtn)):
            if resendEmailBtn[i] is not None:
                selected = str(pathname).lower().split('request=')[1]
                return pathname + f"&URID={selected}&Confirm=Resend", False, False, False
        
    raise PreventUpdate


@app.callback(
    Output('dummyDiv', 'value'),
    Input({'type': 'updateRequestBTN', 'index': ALL}, 'n_clicks'),
    Input('editInfoID', 'value'),
    Input('editInfoStatus', 'value'),
    Input('editInfoEmployee', 'value'),
    Input('editInfoEmployer', 'value'),
    Input('editInfoProject', 'value'),
    Input('editInfoTrainingTitle', 'value'),
    Input('editInfoTrainingPurpose', 'value'),
    Input('editInfoCertification', 'value'),
    Input('editInfoTravelStart', 'value'),
    Input('editInfoTravelEnd', 'value'),
    Input('editInfoDestination', 'value'),
    Input('editInfoTrainingStart', 'value'),
    Input('editInfoTrainingEnd', 'value'),
    Input('editInfoTotalCost', 'value'),
    Input('editInfoWorkOrderLead', 'value'),
    Input('editInfoCompanySupervisor', 'value'),
    Input('editInfoWorkOrderManager', 'value'),
    Input('editInfoTrainingCost', 'value'),
    Input('editInfoTripMIE', 'value'),
    Input('editInfoLodging', 'value'),
    Input('editInfoLodgingTaxesFees', 'value'),
    Input('editInfoAutoMileage', 'value'),
    Input('editInfoRentalCar', 'value'),
    Input('editInfoGroundTransportation', 'value'),
    Input('editInfoFuelCost', 'value'),
    Input('editInfoAirfare', 'value'),
    Input('editInfoBaggage', 'value'),
    Input('editInfoOther', 'value')
)

def updateRequest(updateBtn, ID, status, employee, employer, projectCode, trainingTitle, trainingPurpose, certification, travelStart, travelEnd, destination, trainingStart, trainingEnd, totalCost, workOrderLead, companySupervisor, workOrderManager, trainingCost, tripMIE, lodging, lodgingTaxFee, autoMileage, rentalCar, groundTransportation, fuelCost, airfare, baggage, other):
    for i in range(len(updateBtn)):
        if updateBtn[i] is not None:
            db.updateRow(ID, status, employee, employer, projectCode, trainingTitle, trainingPurpose, certification, travelStart, travelEnd, destination, trainingStart, trainingEnd, totalCost, workOrderLead, companySupervisor, workOrderManager, trainingCost, tripMIE, lodging, lodgingTaxFee, autoMileage, rentalCar, groundTransportation, fuelCost, airfare, baggage, other)

    raise PreventUpdate


@app.callback(
    Output('adminApproval', 'children'),
    Input('url', 'pathname'),
    Input('adminLookupEmployeeName', 'value'),
)

def displayRequests(pathname, employeeName):
    tableResults = []
    if(db.selectedUserRole == 'M' or db.selectedUserRole == 'S'):
        if(str(pathname).lower() == '/admin'.lower() or '&URID='.lower() in str(pathname).lower()):
            results = []
            results = db.loadRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                html.Button(
                                    'Edit Request',
                                    id={
                                        'type': 'editRequestBTN',
                                        'index': 'editRequest'
                                    },
                                    style={
                                        "background-color": "Gray"
                                    }
                                ),
                                html.Div(
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    )
            
        if(str(pathname).lower() == '/admin/rejected'.lower()):
            results = []
            results = db.loadRejectedRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                html.Button(
                                    'Edit Request',
                                    id={
                                        'type': 'editRequestBTN',
                                        'index': 'editRequest'
                                    },
                                    style={
                                        "background-color": "Gray"
                                    }
                                ),
                                html.Div(
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
        if(str(pathname).lower() == '/admin/activerequests'.lower()):
            results = []
            results = db.loadActiveRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                html.Button(
                                    'Edit Request',
                                    id={
                                        'type': 'editRequestBTN',
                                        'index': 'editRequest'
                                    },
                                    style={
                                        "background-color": "Gray"
                                    }
                                ),
                                html.Div(
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if(str(pathname).lower() == '/admin/activerequests/myapproval'.lower()):
            results = []
            results = db.loadRequestsForMyApprovals(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                html.Button(
                                    'Edit Request',
                                    id={
                                        'type': 'editRequestBTN',
                                        'index': 'editRequest'
                                    },
                                    style={
                                        "background-color": "Gray"
                                    }
                                ),
                                html.Div(
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
            else:
                tableResults.append(html.Div([
                    html.H1("You have no current requests needing approval."),
                    html.Br(),
                    html.H3("Travel and Training requests with your name as an approver will appear here.")
                ]))
        if(str(pathname).lower() == '/admin/approved'.lower()):
            results = []
            results = db.loadApprovedRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if('/admin/lookup'.lower() in str(pathname).lower()):
            results = []
            rowID = str(pathname).lower().split('lookup=')[1]
            rowID = rowID.split('&')[0]
            results = db.lookupRow(rowID)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if('/admin/moreInfo'.lower() in str(pathname).lower() and '&Confirm=Resend'.lower() not in str(pathname).lower()):
            results = []
            results = db.expandRow(pathname.split('request=')[1])
            tableResults = []
            tableResults.append(
                html.Div(
                    id='expandedInfo',
                    children=[
                        html.Button(
                            'Resend Approval Email',
                            id={
                                'type': 'resendEmailBTN',
                                'index': 'resendEmail'
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
        
        if('/admin/editRequest'.lower() in str(pathname).lower()):
            results = []
            results = db.expandRow(pathname.split('request=')[1])
            tableResults = []
            tableResults.append(
                html.Div(
                    id='editInfo',
                    children=[
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Request ID:'),
                                dcc.Input(
                                    id="editInfoID",
                                    value= f"{results[0]}",
                                    disabled=True
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Approval Status:'),
                                dcc.Dropdown(
                                    id="editInfoStatus",
                                    options= ['Rejected', 'Awaiting Approval Process', 'Awaiting Work Order Lead Approval', 'Awaiting Company Supervisor Approval', 'Awaiting Financial Approval', 'Awaiting Work Order Manager Approval', 'Awaiting Primary Approval', 'Awaiting Project Manager Approval', 'Request Approved'],
                                    value= f'{results[2]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Employee:'), # Results[4] Gone
                                dcc.Dropdown(
                                    id="editInfoEmployee",
                                    options= db.employeeList,
                                    value= f'{results[3]}, {results[4]}'

                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Employer'),
                                dcc.Dropdown(
                                    id="editInfoEmployer",
                                    options= db.employerList,
                                    value= f'{results[5]}'

                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Project Code:'),
                                dcc.Dropdown(
                                    id="editInfoProject",
                                    options= db.projectCodes,
                                    value= f'{results[6]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Title:'),
                                dcc.Input(
                                    id="editInfoTrainingTitle",
                                    value= f'{results[7]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Purpose:'),
                                dcc.Input(
                                    id="editInfoTrainingPurpose",
                                    value= f'{results[8]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Certification:'),
                                dcc.Input(
                                    id="editInfoCertification",
                                    value= f'{results[9]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Travel Start Date:'),
                                dcc.Input(
                                    id="editInfoTravelStart",
                                    value= f'{results[10]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Travel End Date:'),
                                dcc.Input(
                                    id="editInfoTravelEnd",
                                    value= f'{results[11]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Destination:'),
                                dcc.Input(
                                    id="editInfoDestination",
                                    value= f'{results[12]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Start Date:'),
                                dcc.Input(
                                    id="editInfoTrainingStart",
                                    value= f'{results[13]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training End Date:'),
                                dcc.Input(
                                    id="editInfoTrainingEnd",
                                    value= f'{results[14]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Total Cost:'),
                                dcc.Input(
                                    id="editInfoTotalCost",
                                    value= f"${'{0:.2f}'.format(results[15])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Work Order Lead:'),
                                dcc.Dropdown(
                                    id="editInfoWorkOrderLead",
                                    options= db.managerList,
                                    value= f'{results[16]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Company Supervisor:'),
                                dcc.Dropdown(
                                    id="editInfoCompanySupervisor",
                                    options= db.managerList,
                                    value= f'{results[17]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Work Order Manager:'),
                                dcc.Dropdown(
                                    id="editInfoWorkOrderManager",
                                    options= db.customerList,
                                    value= f'{results[18]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Cost:'),
                                dcc.Input(
                                    id="editInfoTrainingCost",
                                    value= f"${'{0:.2f}'.format(results[19])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip M&IE:'),
                                dcc.Input(
                                    id="editInfoTripMIE",
                                    value= f"${'{0:.2f}'.format(results[20])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip Lodging:'),
                                dcc.Input(
                                    id="editInfoLodging",
                                    value= f"${'{0:.2f}'.format(results[21])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip Lodging Taxes and Fees:'),
                                dcc.Input(
                                    id="editInfoLodgingTaxesFees",
                                    value= f"${'{0:.2f}'.format(results[22])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Round Trip Auto Mileage Cost:'),
                                dcc.Input(
                                    id="editInfoAutoMileage",
                                    value= f"${'{0:.2f}'.format(results[23])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Rental Car Cost:'),
                                dcc.Input(
                                    id="editInfoRentalCar",
                                    value= f"${'{0:.2f}'.format(results[24])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Ground Transportation Fees:'),
                                dcc.Input(
                                    id="editInfoGroundTransportation",
                                    value= f"${'{0:.2f}'.format(results[25])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Estimated Fuel Cost:'),
                                dcc.Input(
                                    id="editInfoFuelCost",
                                    value= f"${'{0:.2f}'.format(results[26])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Estimated Airfare Cost:'),
                                dcc.Input(
                                    id="editInfoAirfare",
                                    value= f"${'{0:.2f}'.format(results[27])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Baggage Fees:'),
                                dcc.Input(
                                    id="editInfoBaggage",
                                    value= f"${'{0:.2f}'.format(results[28])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Other Costs:'),
                                dcc.Input(
                                    id="editInfoOther",
                                    value= f"${'{0:.2f}'.format(results[29])}"
                                )
                            ]
                        ),
                        html.Div(
                            id="editInfoUpdateButton",
                            children=[
                                html.Button(
                                    'Click to Update Request',
                                    id={
                                        'type': 'updateRequestBTN',
                                        'index': 'updateRequest'
                                    },
                                    style={
                                        "background-color": "white",
                                        "font-size": "60px",
                                        "color": "black",
                                        "border-color": "white",
                                    }
                                )
                            ]
                        )
                    ]
                )
            )
    else:
        if(str(pathname).lower() == '/admin'.lower() or '&URID='.lower() in str(pathname).lower()):
            results = []
            results = db.loadRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    )
            
        if(str(pathname).lower() == '/admin/rejected'.lower()):
            results = []
            results = db.loadRejectedRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
        if(str(pathname).lower() == '/admin/activerequests'.lower()):
            results = []
            results = db.loadActiveRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if(str(pathname).lower() == '/admin/activerequests/myapproval'.lower()):
            results = []
            results = db.loadRequestsForMyApprovals(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
            else:
                tableResults.append(html.Div([
                    html.H1("You have no current requests needing approval."),
                    html.Br(),
                    html.H3("Travel and Training requests with your name as an approver will appear here.")
                ]))
        if(str(pathname).lower() == '/admin/approved'.lower()):
            results = []
            results = db.loadApprovedRequests(employeeName)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if('/admin/lookup'.lower() in str(pathname).lower()):
            results = []
            rowID = str(pathname).lower().split('lookup=')[1]
            rowID = rowID.split('&')[0]
            results = db.lookupRow(rowID)
            tableResults = []
            if(results is not None):
                for row in results:
                    tableResults.append(
                        html.Div(
                            id="adminTableTop",
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
                                    id="adminTable",
                                    children=[
                                        html.Button(
                                            '✓',
                                            id={
                                                'type': 'dyn-btn',
                                                'index': 'approveRequest'
                                            },
                                            style={
                                                "background-color": "#4CAF50"
                                            }
                                        ),
                                        html.Table(
                                            id=f'adminApprovalTable{row[0]}',
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
                                    html.Button(
                                            '✘',
                                            id={
                                                'type': 'dyn-btn-reject',
                                                'index': 'rejectRequest'
                                            },
                                            style={
                                                "background-color": "#f44336"
                                            }
                                        ),
                                        
                                    ]
                                )
                            ]
                        )
                    )
        if('/admin/moreInfo'.lower() in str(pathname).lower()):
            results = []
            results = db.expandRow(pathname.split('request=')[1])
            tableResults = []
            tableResults.append(
                html.Div(
                    id='expandedInfo',
                    children=[
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
        
        if('/admin/editRequest'.lower() in str(pathname).lower()):
            results = []
            results = db.expandRow(pathname.split('request=')[1])
            tableResults = []
            tableResults.append(
                html.Div(
                    id='editInfo',
                    children=[
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Request ID:'),
                                dcc.Input(
                                    id="editInfoID",
                                    value= f"{results[0]}",
                                    disabled=True
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Approval Status:'),
                                dcc.Dropdown(
                                    id="editInfoStatus",
                                    options= ['Rejected', 'Awaiting Approval Process', 'Awaiting Work Order Lead Approval', 'Awaiting Company Supervisor Approval', 'Awaiting Financial Approval', 'Awaiting Work Order Manager Approval', 'Awaiting Primary Approval', 'Awaiting Project Manager Approval', 'Request Approved'],
                                    value= f'{results[2]}'

                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Employee:'), # Results[4] Gone
                                dcc.Dropdown(
                                    id="editInfoEmployee",
                                    options= db.employeeList,
                                    value= f'{results[3]}, {results[4]}'

                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Employer'),
                                dcc.Dropdown(
                                    id="editInfoEmployer",
                                    options= db.employerList,
                                    value= f'{results[5]}'

                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Project Code:'),
                                dcc.Dropdown(
                                    id="editInfoProject",
                                    options= db.projectCodes,
                                    value= f'{results[6]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Title:'),
                                dcc.Input(
                                    id="editInfoTrainingTitle",
                                    value= f'{results[7]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Purpose:'),
                                dcc.Input(
                                    id="editInfoTrainingPurpose",
                                    value= f'{results[8]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Certification:'),
                                dcc.Input(
                                    id="editInfoCertification",
                                    value= f'{results[9]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Travel Start Date:'),
                                dcc.Input(
                                    id="editInfoTravelStart",
                                    value= f'{results[10]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Travel End Date:'),
                                dcc.Input(
                                    id="editInfoTravelEnd",
                                    value= f'{results[11]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Destination:'),
                                dcc.Input(
                                    id="editInfoDestination",
                                    value= f'{results[12]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Start Date:'),
                                dcc.Input(
                                    id="editInfoTrainingStart",
                                    value= f'{results[13]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training End Date:'),
                                dcc.Input(
                                    id="editInfoTrainingEnd",
                                    value= f'{results[14]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Total Cost:'),
                                dcc.Input(
                                    id="editInfoTotalCost",
                                    value= f"${'{0:.2f}'.format(results[15])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Work Order Lead:'),
                                dcc.Dropdown(
                                    id="editInfoWorkOrderLead",
                                    options= db.managerList,
                                    value= f'{results[16]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Company Supervisor:'),
                                dcc.Dropdown(
                                    id="editInfoCompanySupervisor",
                                    options= db.managerList,
                                    value= f'{results[17]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Work Order Manager:'),
                                dcc.Dropdown(
                                    id="editInfoWorkOrderManager",
                                    options= db.customerList,
                                    value= f'{results[18]}'
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Training Cost:'),
                                dcc.Input(
                                    id="editInfoTrainingCost",
                                    value= f"${'{0:.2f}'.format(results[19])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip M&IE:'),
                                dcc.Input(
                                    id="editInfoTripMIE",
                                    value= f"${'{0:.2f}'.format(results[20])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip Lodging:'),
                                dcc.Input(
                                    id="editInfoLodging",
                                    value= f"${'{0:.2f}'.format(results[21])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Trip Lodging Taxes and Fees:'),
                                dcc.Input(
                                    id="editInfoLodgingTaxesFees",
                                    value= f"${'{0:.2f}'.format(results[22])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Round Trip Auto Mileage Cost:'),
                                dcc.Input(
                                    id="editInfoAutoMileage",
                                    value= f"${'{0:.2f}'.format(results[23])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Rental Car Cost:'),
                                dcc.Input(
                                    id="editInfoRentalCar",
                                    value= f"${'{0:.2f}'.format(results[24])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Ground Transportation Fees:'),
                                dcc.Input(
                                    id="editInfoGroundTransportation",
                                    value= f"${'{0:.2f}'.format(results[25])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Estimated Fuel Cost:'),
                                dcc.Input(
                                    id="editInfoFuelCost",
                                    value= f"${'{0:.2f}'.format(results[26])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Estimated Airfare Cost:'),
                                dcc.Input(
                                    id="editInfoAirfare",
                                    value= f"${'{0:.2f}'.format(results[27])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Baggage Fees:'),
                                dcc.Input(
                                    id="editInfoBaggage",
                                    value= f"${'{0:.2f}'.format(results[28])}"
                                )
                            ]
                        ),
                        html.Div(
                            className='editLeftSideItem',
                            children=[
                                html.H3('Other Costs:'),
                                dcc.Input(
                                    id="editInfoOther",
                                    value= f"${'{0:.2f}'.format(results[29])}"
                                )
                            ]
                        ),
                        html.Div(
                            id="editInfoUpdateButton",
                            children=[
                                html.Button(
                                    'Click to Update Request',
                                    id={
                                        'type': 'updateRequestBTN',
                                        'index': 'updateRequest'
                                    },
                                    style={
                                        "background-color": "white",
                                        "font-size": "60px",
                                        "color": "black",
                                        "border-color": "white",
                                    }
                                )
                            ]
                        )
                    ]
                )
            )
    return tableResults

layout = html.Div([
    dcc.Location(id='adminConfirmURL', refresh=True),
    navbar.content,
    dcc.ConfirmDialog(
        id='confirmApprove',
        message="Click 'OK' to confirm approval.",
    ),
    dcc.ConfirmDialog(
        id='confirmReject',
        message="Click 'OK' to confirm rejection.",
    ),
    dcc.ConfirmDialog(
        id='confirmResendEmail',
        message="Click 'OK' to resend email to current approver.",
    ),
    html.Div(
        id="adminOuterDiv",
        children=[
            html.Div(
                id='adminNavBar',
                children=[
                    html.Ul([
                        html.Li(html.A('All Requests', href='/admin')),
                        html.Li(html.A('All Requests Needing Approval', href='/admin/activerequests')),
                        html.Li(html.A('Requests Needing My Approval', href='/admin/activerequests/myapproval')),
                        html.Li(html.A('Rejected Requests', href='/admin/rejected')),
                        html.Li(html.A('Approved Requests', href='/admin/approved'))
                    ]),
                
                    
                ]
            ),
            html.Div(
                id='nameSearch',
                children=[
                    html.H2('Form Lookup By Name:'),
                    dcc.Dropdown(
                        id="adminLookupEmployeeName",
                        options= db.employeeList,
                        placeholder="Employee Name"
                    ),
                ]
            ),
            html.Div(
                id="adminApproval"
            ),
            html.Div(
                id="dummyDiv"
            )
        ]
    )
])