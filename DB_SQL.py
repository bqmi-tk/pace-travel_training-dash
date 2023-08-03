import pyodbc as pyo
from functions import email
import yaml #Module not found... But loads

selectedUser = None
selectedUserRole = None

try:
    conf = yaml.full_load(open('config/config.yml'))
    connString = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:pip-it-sharepoint-prod-eastus.database.windows.net,1433;Database=Travel Training;Uid=" + conf['AzureAccount']['username'] + ";Pwd=" + conf['AzureAccount']['password'] + ";"
    conn = pyo.connect(connString)
    cursor = conn.cursor()

    cursor.execute("Select [Employee Name], [Email] From [dbo].[Employees & Emails]")

    rows = cursor.fetchall()

    employeeList = []
    for row in rows:
        employeeList.append('' + str(row[0]) + ', ' + str(row[1]))
        employeeList.sort()
    employerList = ["Aerodyne", "BQMI", "COMSAT", "DB Consulting", "Insight Global", "Peerless", "V2 Technologies"]
    employerList.sort()

    projectCodes = []
    cursor.execute("SELECT [Number], [Title] FROM [dbo].[PACE Project Codes] Order BY [Number]")
    rows = cursor.fetchall()
    for row in rows:
        projectCodes.append('' + str(row[0]) + ' - ' + str(row[1]))

    managerList = []
    cursor.execute("Select [Employee Name], [Email] From [dbo].[Employees & Emails] WHERE [Role] = 'M' OR [Role] = 'S'")

    rows = cursor.fetchall()
    for row in rows:
        managerList.append('' + str(row[0]) + ', ' + str(row[1]))
        managerList.sort()

    customerList = []
    cursor.execute("Select [Employee Name], [Email] From [dbo].[Employees & Emails] WHERE [Role] = 'C'")

    rows = cursor.fetchall()
    for row in rows:
        customerList.append('' + str(row[0]) + ', ' + str(row[1]))
        customerList.sort()
    

    cursor.close()
    conn.close()

    manualLogIn = employeeList + customerList
except Exception as ex:
    print('Initial DB Load Failed. Dev Data Loaded. \nReason for fail:', ex)
    employeeList = ["**Working in offline mode. Database not loaded**", "**Test Email**, pkoza@bqmi.com", "Jake Parrish, jparrish@bqmi.com", "Joe Homan, jhoman@bqmi.com", "Ty Kujawa, tkujawa@bqmi.com", "Joe Banks,, jbanks@bqmi.com"]
    employerList = ["Aerodyne", "BQMI", "COMSAT", "DB Consulting", "Insight Global", "Peerless", "V2 Technologies"]
    managerList = ["**Test Email, Jake Parrish, jparrish@bqmi.com"]
    customerList = ["**Test Email, Jake Parrish, jparrish@bqmi.com"]
    employerList.sort()
    projectCodes = ["01.01.01 - Test Code", "01.02.03 - Test Code 2"]
    manualLogIn = employeeList + customerList

def submit_New_Request(dateCreated, employeeName, employeeEmail, employerName, projectCode, trainingTitle, trainingPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, workOrderLead, companySupervisor, workOrderManager, trainingCost, tripMIE, tripLodging, lodgingTF, autoMileage, carRental, groundTrans, estFuel, estAirFare, baggage, other):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        print(dateCreated)
        cursor.execute("INSERT INTO [dbo].[In Progress Requests] ([Date Created], [Approval Status], [Employee], [Employee Email], [Employer], [Project Code], [Training Title], [Training Purpose], [Certification], [Travel Start Date], [Travel End Date], [Destination], [Training Start Date], [Training End Date], [Total Cost], [Work Order Lead], [Company Supervisor], [Work Order Manager], [Training Cost], [Trip M&IE], [Trip Lodging], [Trip Lodging T&F], [Round-trip Auto Mileage], [Car Rental Price], [Ground Transportation], [Est. Fuel], [Est. Airfare], [Baggage], [Other]) VALUES (?, 'Awaiting Approval Process', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(dateCreated), str(employeeName), str(employeeEmail), str(employerName), str(projectCode), str(trainingTitle), str(trainingPurpose), str(certification), str(travelStartDate), str(travelEndDate), str(destination), str(trainingStartDate), str(trainingEndDate), str(totalCost), str(workOrderLead), str(companySupervisor), str(workOrderManager), str(trainingCost), str(tripMIE), str(tripLodging), str(lodgingTF), str(autoMileage), str(carRental), str(groundTrans), str(estFuel), str(estAirFare), str(baggage), str(other)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as ex:
        print('Submit Request Failed. \nReason for fail:', ex)

def loadUsers(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None): 
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[Employees & Emails] WHERE [Employee Name] = ?", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[Employees & Emails]")
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Request Failed. \nReason for fail:', ex)

def loadRequestsDESC(employeeName): ##LOADS RESULTS FROM NEWEST TO OLDEST
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None): 
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [Employee] = ? ORDER BY ID DESC", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] ORDER BY ID DESC")
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('LoadRequestsDESC Request Failed. \nReason for fail:', ex)

def loadRequests(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None): 
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [Employee] = ?", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests]")
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Request Failed. \nReason for fail:', ex)

def loadRequestsForMyApprovals(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None): 
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [Employee] = ? AND ([Work Order Lead] = ? OR [Company Supervisor] = ? OR [Work Order Manager] = ?)", employeeName, selectedUser, selectedUser, selectedUser)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Work Order Lead] = ? OR [Company Supervisor] = ? OR [Work Order Manager] = ?)", selectedUser, selectedUser, selectedUser)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Requests for My Approval Failed. \nReason for fail:', ex)

def loadRejectedRequests(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None):
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Approval Status] LIKE '%Rejected%') AND ([Employee] = ?)", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [Approval Status] LIKE '%Rejected%'")
        rows = cursor.fetchall()
        for row in rows:
            searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Rejected Requests Failed. \nReason for fail:', ex)

def loadActiveRequests(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None):
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Approval Status] = 'Awaiting Approval Process') OR ([Approval Status] = 'Approved By Work Order Lead') OR ([Approval Status] = 'In Progress') OR ([Approval Status] = 'Approved By Company Supervisor') OR ([Approval Status] = 'Approved By Work Order Manager') AND ([Employee] = ?)", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Approval Status] = 'Awaiting Approval Process') OR ([Approval Status] = 'Approved By Work Order Lead') OR ([Approval Status] = 'In Progress') OR ([Approval Status] = 'Approved By Company Supervisor') OR ([Approval Status] = 'Approved By Work Order Manager')")
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Active Requests Failed. \nReason for fail:', ex)

def loadApprovedRequests(employeeName):
    try:
        searchResults = []
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        if(employeeName is not None):
            employeeName = employeeName.split(', ')[0]
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Approval Status] = 'Request Approved') AND ([Employee] = ?)", employeeName)
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        else:
            cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [Approval Status] = 'Request Approved'")
            rows = cursor.fetchall()
            for row in rows:
                searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('Load Approved Requests Requests Failed. \nReason for fail:', ex)

def getStatus(num):
    try:
        
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        status = rows[2]
        cursor.close()
        conn.close()
        return status
    except Exception as ex:
        print('getStatus Failed. \nReason for fail:', ex)

def getRole(user):
    try:
        if user is not None:
            if ", " in user:
                userEmail = user.split(', ')[1]
                conn = pyo.connect(connString)
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM [dbo].[Employees & Emails] WHERE [Email] = ?", userEmail)
                rows = cursor.fetchall()

                for row in rows:
                    userRole = row[2]
            else:
                username = user.split(', ')[0]
                conn = pyo.connect(connString)
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM [dbo].[Employees & Emails] WHERE [Employee Name] = ?", username)
                rows = cursor.fetchall()

                for row in rows:
                    userRole = row[2]

            cursor.close()
            conn.close()
            return userRole
    except Exception as ex:
        print('getRole Failed. \nReason for fail:', ex)

def getUserDBID(name):
    try:
        if name is not None:
            conn = pyo.connect(connString)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [dbo].[Employees & Emails] WHERE [Employee Name] = ?", name)
            rows = cursor.fetchall()
            dBID = rows[0][3]
            cursor.close()
            conn.close()
            dBID = int(dBID)
            return dBID
    except Exception as ex:
        print('getUserDBID Failed. \nReason for fail:', ex)

def getUserWithDBID(dBID):
    try:
        if dBID is not None:
            if '&' in dBID:
                dBID = dBID.split('&')[0]
            dBID = int(dBID)
            conn = pyo.connect(connString)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [dbo].[Employees & Emails] WHERE [DBID] = ?", dBID)
            rows = cursor.fetchall()
            userName = rows[0][0]
            email = rows[0][1]
            fullUser = userName + ', ' + email
            cursor.close()
            conn.close()
            return fullUser
    except Exception as ex:
        print('getUserWithDBID Failed. \nReason for fail:', ex)

def approveRow(num):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        for row in rows:
            status = row[2]

        if(status == 'Awaiting Approval Process'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Work Order Lead Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalWOL(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Lead Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Company Supervisor Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalCS(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Company Supervisor Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Financial Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalFundsPrimary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Financial Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Work Order Manager Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalWOM(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Manager Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Primary Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalInitial(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Primary Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Awaiting Project Manager Approval' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalProjectPrimary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
            email.sendRequestApprovalProjectSecondary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Project Manager Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Request Approved' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestApprovalFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        cursor.close()
        conn.close()
    except Exception as ex:
        print('approveRow Failed. \nReason for fail:', ex)

def rejectRow(num):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        for row in rows:
            status = row[2]
        if(status == 'Awaiting Approval Process'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Initial Approver' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Lead Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Work Order Lead' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Company Supervisor Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Company Supervisor' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Financial Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Financial Approver' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Manager Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Work Order Manager' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Primary Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Primary Approver' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Project Manager Approval'):
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = 'Rejected By Project Manager' WHERE [ID] = ?", num)
            cursor.commit()
            email.sendRequestRejectFinalConfirm(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        cursor.close()
        conn.close()
    except Exception as ex:
        print('rejectRow Failed. \nReason for fail:', ex)

def lookupRow(num):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        searchResults = []
        cursor.execute(f"SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        for row in rows:
            searchResults.append(row)
        cursor.close()
        conn.close()
        return searchResults
    except Exception as ex:
        print('lookupRow Failed. \nReason for fail:', ex)

def expandRow(num):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        expandedRow = []
        for row in rows:
            for value in row:
                expandedRow.append(value)
        cursor.commit()
        cursor.close()
        conn.close()
        return expandedRow
    except Exception as ex:
        print('expandRow Failed. \nReason for fail:', ex)

def getID(employeeName, projectCode, trainingPurpose):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[In Progress Requests] WHERE ([Employee] = ?) AND ([Training Purpose] = ?) AND ([Project Code] = ?)", employeeName, trainingPurpose, projectCode)
        rows = cursor.fetchall()
        rowID = rows[0]
        rowID = rowID[0]
        cursor.close()
        conn.close()
        return rowID
    except Exception as ex:
        print('getID Failed. \nReason for fail:', ex)

def getNewRequestID(employeeName):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (1) * FROM [dbo].[In Progress Requests] WHERE ([Employee] = ?) ORDER BY ID DESC", employeeName)
        rows = cursor.fetchall()
        rowID = rows[0]
        rowID = rowID[0]
        cursor.close()
        conn.close()
        return rowID
    except Exception as ex:
        print('getNewRequestID Failed. \nReason for fail:', ex)

def updateRow(num, status, employee, employer, projectCode, trainingTitle, trainingPurpose, certification, travelStart, travelEnd, destination, trainingStart, trainingEnd, totalCost, workOrderLead, companySupervisor, workOrderManager, trainingCost, tripMIE, lodging, lodgingTaxFee, autoMileage, rentalCar, groundTransportation, fuelCost, airfare, baggage, other):
    try:
        if('Rejected' not in status):
            if(employee == None):
                employee == 'N/A, N/A'
            if(employer == None):
                employee == 'N/A'
            if(projectCode == None):
                projectCode == 'N/A'
            if(trainingTitle == None):
                trainingTitle == 'N/A'
            if(trainingPurpose == None):
                trainingPurpose == 'N/A'
            if(certification == None):
                certification == 'N/A'
            if(travelStart == None):
                travelStart == 'N/A'
            if(travelEnd == None):
                travelEnd == 'N/A'
            if(destination == None):
                destination == 'N/A'
            if(trainingStart == None):
                trainingStart == 'N/A'
            if(trainingEnd == None):
                trainingEnd == 'N/A'
            if(totalCost == None):
                totalCost == 0.00
            if(workOrderLead == None):
                workOrderLead == 'N/A, N/A'
            if(companySupervisor == None):
                companySupervisor == 'N/A, N/A'
            if(workOrderManager == None):
                workOrderManager == 'N/A, N/A'
            if(trainingCost == None):
                trainingCost == 0.00
            if(tripMIE == None):
                tripMIE == 0.00
            if(lodging == None):
                lodging == 0.00
            if(lodgingTaxFee == None):
                lodgingTaxFee == 0.00
            if(autoMileage == None):
                autoMileage == 0.00
            if(rentalCar == None):
                rentalCar == 0.00
            if(groundTransportation == None):
                groundTransportation == 0.00
            if(fuelCost == None):
                fuelCost == 0.00
            if(airfare == None):
                airfare == 0.00
            if(baggage == None):
                baggage == 0.00
            if(other == None):
                other == 0.00

            travelCosts = float(float(tripMIE.strip('$')) + float(lodging.strip('$')) + float(lodgingTaxFee.strip('$')) + float(autoMileage.strip('$')) + float(groundTransportation.strip('$')) + float(airfare.strip('$')) + float(baggage.strip('$')) + float(rentalCar.strip('$')) + float(fuelCost.strip('$')) + float(other.strip('$'))) 

            
            totalCost = round(travelCosts + float(trainingCost.strip('$')), 2)
        
            conn = pyo.connect(connString)
            cursor = conn.cursor()
            cursor.execute("UPDATE [dbo].[In Progress Requests] SET [Approval Status] = ?, [Employee] = ?, [Employee Email] = ?, [Employer] = ?, [Project Code] = ?, [Training Title] = ?, [Training Purpose] = ?, [Certification] = ?, [Travel Start Date] = ?, [Travel End Date] = ?, [Destination] = ?, [Training Start Date] = ?, [Training End Date] = ?, [Total Cost] = ?, [Work Order Lead] = ?, [Company Supervisor] = ?, [Work Order Manager] = ?, [Training Cost] = ?,  [Trip M&IE] = ?, [Trip Lodging] = ?, [Trip Lodging T&F] = ?, [Round-trip Auto Mileage] = ?,  [Car Rental Price] = ?, [Ground Transportation] = ?, [Est. Fuel] = ?, [Est. Airfare] = ?, [Baggage] = ?, [Other] = ? WHERE [ID] = ?", status, employee.split(', ')[0], employee.split(', ')[1], employer, projectCode, trainingTitle, trainingPurpose, certification, travelStart, travelEnd, destination, trainingStart, trainingEnd, totalCost, workOrderLead, companySupervisor, workOrderManager, trainingCost, tripMIE, lodging, lodgingTaxFee, autoMileage, rentalCar, groundTransportation, fuelCost, airfare, baggage, other, num)
            

            cursor.commit()
            cursor.close()
            conn.close()
    except Exception as ex:
        print('updateRow Failed. \nReason for fail:', ex)

def resendEmail(num):
    try:
        conn = pyo.connect(connString)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM [dbo].[In Progress Requests] WHERE [ID] = ?", num)
        rows = cursor.fetchall()
        for row in rows:
            status = row[2]

        if(status == 'Awaiting Approval Process'):
            email.sendRequestApprovalInitial(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Lead Approval'):
            email.sendRequestApprovalWOL(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Company Supervisor Approval'):
            email.sendRequestApprovalCS(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Financial Approval'):
            email.sendRequestApprovalFundsPrimary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Work Order Manager Approval'):
            email.sendRequestApprovalWOM(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Primary Approval'):
            email.sendRequestApprovalInitial(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        elif(status == 'Awaiting Project Manager Approval'):
            email.sendRequestApprovalProjectPrimary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
            email.sendRequestApprovalProjectSecondary(row[3], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[19], row[16], row[17], row[18], row[6], row[0])
        cursor.close()
        conn.close()
    except Exception as ex:
        print('approveRow Failed. \nReason for fail:', ex)