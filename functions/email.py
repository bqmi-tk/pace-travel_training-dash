import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml #Module not found... But loads
import DB_SQL as db

def sendRequestApprovalCS(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        
        companySupervisorEmail = companySupervisor.split(', ')[1]
        csDBID = db.getUserDBID(companySupervisor.split(', ')[0])
        if csDBID is None:
            csDBID = 209

        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(csDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Company Supervisor for " + employeeName
        message['From'] = sender_email
        message['To'] = companySupervisorEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, companySupervisorEmail, message.as_string()) # CompanySupervisor Email
            server.quit()

        print('Email Sent To Company Supervisor')
        
        
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalWOM(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        
        workOrderManagerEmail = workOrderManager.split(', ')[1]
        wOMDBID = db.getUserDBID(workOrderManager.split(', ')[0])
        if wOMDBID is None:
            wOMDBID = 209

        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(wOMDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Work Order Manager for " + employeeName
        message['From'] = sender_email
        message['To'] = workOrderManagerEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, workOrderManagerEmail, message.as_string()) # Work Order Manager Email
            server.quit()   
        
        print('Email Sent To Work Order Manager')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalWOL(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']

        workOrderLeadEmail = workOrderLead.split(', ')[1]
        wOLDBID = db.getUserDBID(workOrderLead.split(', ')[0])
        if wOLDBID is None:
            wOLDBID = 209
        
        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(wOLDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Work Order Lead for " + employeeName
        message['From'] = sender_email
        message['To'] = workOrderLeadEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, workOrderLeadEmail, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Work Order Lead')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalInitial(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        reciever_email = conf['EmailAccount']['primaryApprover']
        primaryDBID = conf['EmailAccount']['primaryApproverDBID']
        
        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(primaryDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Primary Approver for " + employeeName
        message['From'] = sender_email
        message['To'] = reciever_email

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, reciever_email, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Primary Approval')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalConfirm(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        
        content = (employeeName + ' request for ' + requestPurpose + ' confirmation.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost))

        message = MIMEMultipart()
        message['Subject'] ="Approval Request for '" + requestPurpose + "' Confirmation for " + employeeName
        message['From'] = sender_email
        message['To'] = employeeEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, employeeEmail, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Employee')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalFundsPrimary(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        primary_reciever_email = conf['EmailApprovers']['primaryFundsApprover']
        primaryDBID = conf['EmailApprovers']['primaryFundsApproverDBID']
        
        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(primaryDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Primary Approver for " + employeeName
        message['From'] = sender_email
        message['To'] = primary_reciever_email

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, primary_reciever_email, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Primary Approval')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalProjectPrimary(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        primary_reciever_email = conf['EmailApprovers']['primaryProjectManager']
        primaryDBID = conf['EmailApprovers']['primaryProjectManagerDBID']
        
        
        
        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(primaryDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Primary Project Approver for " + employeeName
        message['From'] = sender_email
        message['To'] = primary_reciever_email

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, primary_reciever_email, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Primary Approval')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalProjectSecondary(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        secondary_reciever_email = conf['EmailApprovers']['secondaryProjectManager']
        secondaryDBID = conf['EmailApprovers']['secondaryProjectManagerDBID']
        
        
        content = (employeeName + ' is requesting approval for ' + requestPurpose + '.\n'
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost) + '\n'
        + 'Click the link below to view active request: \n\n'
        + 'https://pacetraveltraining.azurewebsites.net/admin/lookup=' + str(requestID) + '&redirectLog=' + str(secondaryDBID))

        message = MIMEMultipart()
        message['Subject'] ="Approval for '" + requestPurpose + "' Required By Project Approver for " + employeeName
        message['From'] = sender_email
        message['To'] = secondary_reciever_email

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, secondary_reciever_email, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Secondary PM Approval')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestApprovalFinalConfirm(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        
        content = (employeeName + ' request for ' + requestPurpose + ': ' + db.getStatus(db.getID(employeeName, projectCode, requestPurpose))
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost))

        message = MIMEMultipart()
        message['Subject'] ="Request for '" + requestPurpose + "' Confirmation for " + employeeName + ": Approved"
        message['From'] = sender_email
        message['To'] = employeeEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, employeeEmail, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Employee')
    except Exception as ex:
        print ("Something went wrong….",ex)

def sendRequestRejectFinalConfirm(employeeName, employeeEmail, employerName, trainingTitle, requestPurpose, certification, travelStartDate, travelEndDate, destination, trainingStartDate, trainingEndDate, totalCost, trainingCost, workOrderLead, companySupervisor, workOrderManager, projectCode, requestID):
    try:
        conf = yaml.full_load(open('config/config.yml'))
        port = 587  # For SSL
        password = conf['EmailAccount']['password']
        sender_email = conf['EmailAccount']['email']
        
        content = (employeeName + ' request for ' + requestPurpose + ': ' + db.getStatus(db.getID(employeeName, projectCode, requestPurpose))
        + 'Details are as follows:\n\n' 
        +'Employee: ' + employeeName + '\n' 
        + 'Employer: ' + employerName + '\n'
        + 'Work Order Lead: ' + workOrderLead.split(', ')[0] + ' (' + workOrderLead.split(', ')[1] + ')\n'
        + 'Company Supervisor: ' + companySupervisor.split(', ')[0] + ' (' + companySupervisor.split(', ')[1] + ')\n'
        + 'Work Order Manager: ' + workOrderManager.split(', ')[0] + ' (' + workOrderManager.split(', ')[1] + ')\n'
        + 'Project Code: ' + projectCode + '\n' 
        + 'Purpose: ' + requestPurpose + '\n'
        + 'Training Title: ' + trainingTitle + '\n'
        + 'Training Dates: ' + trainingStartDate + '--' + trainingEndDate + '\n'
        + 'Certification? (Y / N): ' + certification + '\n'
        + 'Destination: ' + destination + '\n'
        + 'Days of Travel: ' + travelStartDate + '--' + travelEndDate + '\n'
        + 'Total Cost of Training: $' + str(trainingCost) + '\n'
        + 'Total Cost of Trip: $' + str(totalCost))

        message = MIMEMultipart()
        message['Subject'] ="Request for '" + requestPurpose + "' Confirmation for " + employeeName + ": Rejected"
        message['From'] = sender_email
        message['To'] = employeeEmail

        message.attach(MIMEText(content))
    
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, employeeEmail, message.as_string()) # Primary Approver Email
            server.quit()   
        
        print('Email Sent To Employee')
    except Exception as ex:
        print ("Email Resend failed. Reason:",ex)
        