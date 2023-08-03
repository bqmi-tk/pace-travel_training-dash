from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from datetime import date, datetime
import time
from dash.exceptions import PreventUpdate
import DB_SQL as db
from app import app
from pages import Form_Submitted as fs
from functions import email
from pages.partials import navbar

@app.callback( # Used for Enabling / Disabling the Submit Button
    Output('submit-btn', 'disabled'),
    Input('Employee-Name', 'value'),
    Input('Employer-Name', 'value'),
    Input('Work-Order-Lead-List', 'value'),
    Input('Company-Supervisor-List', 'value'),
    Input('Work-Order-Manager-List', 'value'),
    Input('Purpose-For-Request', 'value'),
    Input('submit-btn', 'n_clicks'),
    Input('confirmSubmit', 'cancel_n_clicks'),
)
def unlock_Submit_Button(employeeName, employerName, workOrderLeadList, companySupervisorList, workOrderManagerList, purposeForRequest, submit_button, cancelSubmit):
    if (cancelSubmit):
        return False
    if submit_button:
        print("Submit Button Clicked")
        return True
    if (employeeName == None):
        return True
    elif (employerName == None):
        return True
    elif (workOrderLeadList == None):
        return True
    elif (companySupervisorList == None):
        return True
    elif (workOrderManagerList == None):
        return True
    elif (purposeForRequest == None):
        return True
    else:
        return False

@app.callback( # Used for Calculating and Outputting costs
    Output('Travel-Total-out', 'children'),
    Output('Total-Cost-out', 'children'),
    Input('Training-Cost', 'value'),
    Input('Calc-Lodge', 'value'),
    Input('Calc-MIE', 'value'),
    Input('Est-Lodge-Tax-Fees', 'value'),
    Input('Round-Mileage-Cost', 'value'),
    Input('Est-Ground-Trans-Fees', 'value'),
    Input('Est-Airfare-Price', 'value'),
    Input('Baggage-Fees', 'value'),
    Input('Est-Car-Rental-Price', 'value'),
    Input('Est-Fuel-Cost', 'value'),
    Input('Other-Cost', 'value')
)
def update_cost_calc(trainingCost, estLodge, calcMIE, estLodgeTaxFees, roundMileageCost, estGroundTransFees, estAirfarePrice, baggageFees, estCarRentalPrice, estFuelCost, otherCost): 
    if(trainingCost == None):
        trainingCost = 0.00
    if(estLodge == None): 
        estLodge = 0.00 
    if(calcMIE == None):
        calcMIE = 0.00
    if(estLodgeTaxFees == None):
        estLodgeTaxFees = 0.00
    if(roundMileageCost == None):
        roundMileageCost = 0.00
    if(estGroundTransFees == None):
        estGroundTransFees = 0.00
    if(estAirfarePrice == None):
        estAirfarePrice = 0.00
    if(baggageFees == None):
        baggageFees = 0.00
    if(estCarRentalPrice == None):
        estCarRentalPrice = 0.00
    if(estFuelCost == None):
        estFuelCost = 0.00
    if(otherCost == None):
        otherCost = 0.00

    travelCosts = float(calcMIE + estLodge + estLodgeTaxFees + roundMileageCost + estGroundTransFees + estAirfarePrice + baggageFees + estCarRentalPrice + estFuelCost + otherCost) 

    totalCosts = round(travelCosts + trainingCost, 2)
    

    if(travelCosts != None and totalCosts != None):
        return f"${'{0:.2f}'.format(travelCosts)}", f"${'{0:.2f}'.format(totalCosts)}"
    else:
        raise PreventUpdate


@app.callback(
    Output('SevenFive-MIE-Rate', 'value'),
    Input('MIE-Rate', 'value')
)
def calcDailySevenFive(MIE):
    if (MIE == None):
        return None
    else:
        MIE75 = MIE*.75
        return (MIE75)

@app.callback(
    Output('Calc-MIE', 'value'),
    Input('MIE-Rate', 'value'),
    Input('Travel-Start-Date', 'date'),
    Input('Travel-End-Date', 'date')
)
def calcTripMIE(MIE, travelStart, travelEnd):
    date_format = "%Y-%m-%d"
    if(travelEnd == None or travelStart == None):
        travelDays = 0
    try:
        totalDays = datetime.strptime(travelEnd, date_format) - datetime.strptime(travelStart, date_format)
        travelDays = totalDays.days + 1
        
        if (MIE == None):
            MIE = 0
        MIE75 = MIE*.75
        return ((MIE75 * 2) + ((travelDays - 2)*MIE))
    except:
        print("Start and End Travel Date Required")



@app.callback(
    Output('Calc-Lodge', 'value'),
    Output('Est-Lodge-Tax-Fees', 'value'),
    Input('Lodging-Rate', 'value'),
    Input('Travel-Start-Date', 'date'),
    Input('Travel-End-Date', 'date')
)
def calcTripLodging(lodgingRate, travelStart, travelEnd):
    date_format = "%Y-%m-%d"
    if(travelEnd == None or travelStart == None):
        travelDays = 0
    try:
        totalDays = datetime.strptime(travelEnd, date_format) - datetime.strptime(travelStart, date_format)
        travelDays = totalDays.days
        if (lodgingRate == None):
            lodgingRate = 0
        calcLodge = (lodgingRate * travelDays)
        return (calcLodge), (calcLodge * .08)
    except:
        raise PreventUpdate

@app.callback(
    Output('requestFormURL', 'pathname'),
    Input('requestFormURL', 'pathname'),
    Input('confirmSubmit', 'submit_n_clicks'),
    Input('Employee-Name', 'value'),
    Input('Employer-Name', 'value'),
    Input('Project-Code', 'value'),
    Input('Work-Order-Lead-List', 'value'),
    Input('Company-Supervisor-List', 'value'),
    Input('Work-Order-Manager-List', 'value'),
    Input('Purpose-For-Request', 'value'),
    Input('Training-Title', 'value'),
    Input('Training-Start-Date', 'date'),
    Input('Training-End-Date', 'date'),
    Input('Certification', 'value'),
    Input('Travel-City', 'value'),
    Input('Travel-State', 'value'),
    Input('Travel-Start-Date', 'date'),
    Input('Travel-End-Date', 'date'),
    Input('Training-Cost', 'value'),
    Input('SevenFive-MIE-Rate', 'value'),
    Input('MIE-Rate', 'value'),
    Input('Lodging-Rate', 'value'),
    Input('Calc-MIE', 'value'),
    Input('Calc-Lodge', 'value'),############
    Input('Est-Lodge-Tax-Fees', 'value'),
    Input('Round-Mileage-Cost', 'value'),
    Input('Est-Ground-Trans-Fees', 'value'),
    Input('Est-Airfare-Price', 'value'),
    Input('Baggage-Fees', 'value'),
    Input('Est-Car-Rental-Price', 'value'),
    Input('Est-Fuel-Cost', 'value'),
    Input('Other-Cost', 'value'),
    prevent_initial_call=True
)

def confirmButton(pathname, confirmApprove, employeeName, employerName, projectCode, workOrderLead, companySupervisor, workOrderManager, purposeForRequest, trainingTitle, trainingStartDate, trainingEndDate, certification, travelCity, travelState, travelStartDate, travelEndDate, trainingCost, MIE75, MIE, lodgingRate, calcMIE, estLodge, estLodgeTaxFees, roundMileageCost, estGroundTransFees, estAirfarePrice, baggageFees, estCarRentalPrice, estFuelCost, otherCost):
    try:
        if(confirmApprove):
            if(trainingCost == None):
                trainingCost = 0.00
            if(MIE75 == None):
                MIE75 = 0.00
            if(MIE == None):
                MIE = 0.00
            if(lodgingRate == None):
                lodgingRate = 0.00
            if(calcMIE == None):
                calcMIE = 0.00
            if(estLodge == None): ###########
                estLodge = 0.00 ###########
            if(estLodgeTaxFees == None):
                estLodgeTaxFees = 0.00
            if(projectCode == None):
                projectCode = 'N/A'
            if(roundMileageCost == None):
                roundMileageCost = 0.00
            if(estGroundTransFees == None):
                estGroundTransFees = 0.00
            if(estAirfarePrice == None):
                estAirfarePrice = 0.00
            if(baggageFees == None):
                baggageFees = 0.00
            if(estCarRentalPrice == None):
                estCarRentalPrice = 0.00
            if(estFuelCost == None):
                estFuelCost = 0.00
            if(otherCost == None):
                otherCost = 0.00
            if(travelCity == None):
                travelCity = 'N/A'
            if(travelState == None):
                travelState = 'N/A'
            if not certification:
                certification = 'No'
            elif(certification[0] == 'Certification'):
                certification = 'Yes'
            if(trainingTitle == None):
                trainingTitle = 'N/A'
            # Spacer
            travelCosts = float(calcMIE + estLodge + estLodgeTaxFees + roundMileageCost + estGroundTransFees + estAirfarePrice + baggageFees + estCarRentalPrice + estFuelCost + otherCost) #################
            # Spacer
            totalCosts = round(travelCosts + trainingCost, 2)
            travelLocation = '' + travelCity + ', ' + travelState
            if (", " in employeeName):
                employeeEmail = employeeName.split(", ")[1]
                employeeName = employeeName.split(", ")[0]
            else:
                employeeEmail = "N/A"
                employeeName = employeeName
            if(travelStartDate != None):
                date_object = date.fromisoformat(travelStartDate)
                travelStartDate = date_object.strftime('%B %d, %Y')
            else:
                travelStartDate = "N/A"

            if(travelEndDate != None):
                date_object = date.fromisoformat(travelEndDate)
                travelEndDate = date_object.strftime('%B %d, %Y')
            else:
                travelEndDate = "N/A"

            if(trainingStartDate != None):
                date_object = date.fromisoformat(trainingStartDate)
                trainingStartDate = date_object.strftime('%B %d, %Y')
            else:
                trainingStartDate = "N/A"

            if(trainingEndDate != None):
                date_object = date.fromisoformat(trainingEndDate)
                trainingEndDate = date_object.strftime('%B %d, %Y')
            else:
                trainingEndDate = "N/A"
    # Spacer
            today = date.today()
            # YYYY-mm-dd
            dateCreated = today.strftime("%Y-%m-%d")
            # Spacer
            db.submit_New_Request(dateCreated=dateCreated, employeeName=employeeName, employeeEmail=employeeEmail, employerName=employerName, projectCode=projectCode, trainingTitle=trainingTitle, trainingPurpose=purposeForRequest, certification=certification, travelStartDate=travelStartDate, travelEndDate=travelEndDate, destination=travelLocation, trainingStartDate=trainingStartDate, trainingEndDate=trainingEndDate, totalCost=totalCosts, workOrderLead=workOrderLead, companySupervisor=companySupervisor, workOrderManager=workOrderManager, trainingCost=trainingCost, tripMIE=calcMIE, tripLodging=estLodge, lodgingTF=estLodgeTaxFees, autoMileage=roundMileageCost, carRental=estCarRentalPrice, groundTrans=estGroundTransFees, estFuel=estFuelCost, estAirFare=estAirfarePrice, baggage=baggageFees, other=otherCost)
            requestID = db.getNewRequestID(employeeName)
    # Used to populate confirm table, data transfer was slow, now sends user to '/My-Requests', with newest request on top.
            # requestID = db.getNewRequestID(employeeName) Form-Submitted Page Causes slow page load times// Temp send to My-Requests
            # fs.populateForm(requestID)
    # Spacer
            email.sendRequestApprovalConfirm(employeeName=employeeName, employeeEmail=employeeEmail, employerName=employerName, trainingTitle=trainingTitle, requestPurpose=purposeForRequest, certification=certification, travelStartDate=travelStartDate, travelEndDate=travelEndDate, destination=travelLocation, trainingStartDate=trainingStartDate, trainingEndDate=trainingEndDate, totalCost=totalCosts, workOrderLead=workOrderLead, companySupervisor=companySupervisor, workOrderManager=workOrderManager, trainingCost=trainingCost, projectCode=projectCode, requestID=requestID)
            email.sendRequestApprovalInitial(employeeName=employeeName, employeeEmail=employeeEmail, employerName=employerName, trainingTitle=trainingTitle, requestPurpose=purposeForRequest, certification=certification, travelStartDate=travelStartDate, travelEndDate=travelEndDate, destination=travelLocation, trainingStartDate=trainingStartDate, trainingEndDate=trainingEndDate, totalCost=totalCosts, workOrderLead=workOrderLead, companySupervisor=companySupervisor, workOrderManager=workOrderManager, trainingCost=trainingCost, projectCode=projectCode, requestID=requestID)
            # # Spacer
            confirmApprove = 0
            return "/My-Requests"
        raise PreventUpdate
    except:
        raise PreventUpdate


@app.callback(
    Output('url', 'href'),
    Output('confirmSubmit', 'displayed'),
    Input('reset-btn', 'n_clicks'),
    Input('submit-btn', 'n_clicks')
)
def pageChange(reset_button, submit_button):
    if reset_button:
        print("Reset Button Clicked")
        return "/New-Request", False
    if submit_button:
        print("Submit Button Clicked")
        return None, True
    raise PreventUpdate


@app.callback(
    Output('totalTravelDays', 'children'),
    Input('Travel-Start-Date', 'date'),
    Input('Travel-End-Date', 'date')
)
def calcTravelDays(travelStart, travelEnd):
    date_format = "%Y-%m-%d"
    if(travelEnd == None or travelStart == None):
        return f"Total Days of Travel: 0"
    totalDays = datetime.strptime(travelEnd, date_format) - datetime.strptime(travelStart, date_format)
    travelDays = totalDays.days + 1
    return f"Total Days of Travel: {travelDays}"

@app.callback(
    Output('googleMapsLink', 'children'),
    Input('Travel-City', 'value'),
    Input('Travel-State', 'value')
)
def updateGoogleMapsLink(travelCity, travelState):
    if(travelCity == None or travelState == None):
        return dcc.Link(html.Button('Google Maps', id='googleMapsBTN'), href='https://www.google.com/maps/', target='_blank')
    else:
        travelCity = travelCity.replace(" ", "+")
        travelState = travelState.replace(" ", "+")
        return dcc.Link(html.Button('Google Maps', id='googleMapsBTN'), href=f'https://www.google.com/maps/place/{travelCity},+{travelState}', target='_blank')

content = html.Div([
    navbar.content,
    dcc.ConfirmDialog(
        id='confirmSubmit',
        message="Click 'OK' to submit your request.",
    ),
    dcc.Location(id='requestFormURL', refresh=True),
    html.Div(
        id="Full-Form",
        children=[
            html.Div(
                id="Form-Left",
                children=[
                    html.Div(
                        id="Form-Left-Top",
                        children=[
                            html.H1("Requests"),
                            dcc.Dropdown(
                                id="Employee-Name",
                                options= db.employeeList,
                                placeholder="Employee Name"
                            ),
                            dcc.Dropdown(
                                id="Employer-Name",
                                options= db.employerList,
                                placeholder="Employer Name"
                            ),
                            dcc.Dropdown(
                                id="Work-Order-Lead-List",
                                options= db.managerList,
                                placeholder="Work Order Lead"
                            ),
                            dcc.Dropdown(
                                id="Company-Supervisor-List",
                                options= db.managerList,
                                placeholder="Company Supervisor"
                            ),
                            dcc.Dropdown(
                                id="Work-Order-Manager-List",
                                options= db.customerList,
                                placeholder="Work Order Manager"
                            ),
                            html.Div(
                                id='WOM-Not-Found-Note',
                                children=[
                                    html.P('If your Work Order Manager is not in the list, please contact:'),
                                    html.P('Melissa Mongalier, melissa.j.mongalier@nasa.gov')
                                ]    
                            ),
                            dcc.Dropdown(
                                id="Project-Code",
                                options= db.projectCodes,
                                placeholder="Project Work Code"
                            ),
                            dcc.Textarea(
                                id="Purpose-For-Request",
                                placeholder="Purpose For Request..."
                            )
                        ]
                    ),
                    html.Div(
                        id="Form-Left-Bottom",
                        children=[
                            html.Div(
                                children=[
                                    html.H1("Training"),
                                    dcc.Input(
                                        id="Training-Title",
                                        type="text",
                                        placeholder="Training Title"
                                    ),
                                    dcc.DatePickerSingle(
                                        id="Training-Start-Date",
                                        placeholder="Start Date"
                                    ),
                                    dcc.DatePickerSingle(
                                        id="Training-End-Date",
                                        placeholder="End Date"
                                    ),
                                    html.Div(
                                        dcc.Checklist(
                                            id="Certification",
                                            options=["Certification"]
                                        )
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.H1("Travel"),
                                    dcc.Input(
                                        id="Travel-City",
                                        type="text",
                                        placeholder="City"
                                    ),
                                    dcc.Input(
                                        id="Travel-State",
                                        type="text",
                                        placeholder="State"
                                    ),
                                    dcc.DatePickerSingle(
                                        id="Travel-Start-Date",
                                        placeholder="Start Date"
                                    ),
                                    dcc.DatePickerSingle(
                                        id="Travel-End-Date",
                                        placeholder="End Date"
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                id="Right-Form",
                children=[
                    html.H1("Training Cost"),
                    dcc.Input(
                        id="Training-Cost",
                        type="number",
                        placeholder="$0.00"
                    ),
                    html.H2("Itemized Travel Costs"),
                    html.Div(
                        id="Right-Form-Top-Buttons",
                        children= [
                            dcc.Link(
                                html.Button('Search Per Diem Rates', id='perDiemRate'), href='https://www.gsa.gov/travel/plan-book/per-diem-rates', target="_blank"
                            ),

                            html.Div(
                                id="googleMapsLink"
                            ),

                            html.H3(id="totalTravelDays")
                        ]
                    ),
                    html.Div(
                        id="Right-Form-Block",
                        children=[
                            html.Div(
                                id="Sub-Right-Form",
                                children=[
                                    html.P("Daily M&IE Rate"),
                                    html.P("Daily Lodging Rate"),
                                    html.P("Daily 75% M&IE Rate"),
                                    dcc.Input(
                                        id="MIE-Rate",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="Lodging-Rate",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="SevenFive-MIE-Rate",
                                        type="number",
                                        placeholder="$0.00",
                                        disabled=True
                                    ),
                                    
                                    html.P("Calculated Trip \nM&IE Total"),
                                    html.P("Calculated Trip \nLodging Total"),
                                    html.P("Calculated Lodging \nTaxes and Fees"),
                                    dcc.Input(
                                        id="Calc-MIE",
                                        type="number",
                                        placeholder="$0.00",
                                        disabled=True
                                    ),
                                    dcc.Input(
                                        id="Calc-Lodge",
                                        type="number",
                                        placeholder="$0.00",
                                        disabled=True
                                    ),
                                    dcc.Input(
                                        id="Est-Lodge-Tax-Fees",
                                        type="number",
                                        placeholder="$0.00",
                                        disabled=True
                                    ),
                                    html.P("Estimated Roundtrip \nAuto Mileage Cost"),
                                    html.P("Estimated Car \nRental Price"),
                                    html.P("Estimated Ground \nTransportation Fees"),
                                    dcc.Input(
                                        id="Round-Mileage-Cost",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="Est-Car-Rental-Price",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="Est-Ground-Trans-Fees",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    html.P("Estimated Fuel Cost"),
                                    html.P("Estimated Airfare Price"),
                                    html.P("Baggage Fees"),
                                    dcc.Input(
                                        id="Est-Fuel-Cost",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="Est-Airfare-Price",
                                        type="number",
                                        placeholder="$0.00"
                                    ),
                                    dcc.Input(
                                        id="Baggage-Fees",
                                        type="number",
                                        placeholder="$0.00"
                                    )
                                ]
                            ),
                            html.Div(
                                id="Other",
                                children=[
                                    html.P("Other Costs"),
                                    dcc.Input(
                                        id="Other-Cost",
                                        type="number",
                                        placeholder="$0.00"
                                    )
                                ],
                            ),
                            html.Br(),
                            html.Div(
                                id="Cost-Block",
                                children=[
                                    html.H2("Total Travel Cost:"),
                                    html.H2(id="Travel-Total-out"),
                                    html.H2("Grand Total:"),
                                    html.H2(id="Total-Cost-out")
                                ],
                                style={
                                        "display": "grid",
                                        "grid-template-columns": "75% 20%",
                                        "grid-gap": "3%"
                                    }
                                ),
                        ]
                    ),
                    html.Div(
                            id="buttonSection",
                            children=[
                                html.Div([
                                    html.H4("Reset"),
                                    html.Button('✘', id='reset-btn')
                                ],
                                style={
                                    "padding-left": "2%",
                                }),
                                html.Div([
                                    html.H4("Submit"),
                                    html.Button('✓', id='submit-btn')
                                ],
                                style={
                                    "padding-left": "2%",
                                })
                            ],
                            style={
                                "padding": "2%",
                                "display": "grid",
                                "grid-template-columns": "75% 25%"
                            }
                        ),
                        html.Div(
                            id="dummyDiv"
                        )
                ]
            ) 
        ]
    )
])