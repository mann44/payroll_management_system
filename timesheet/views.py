from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM timesheet, project, employee_employee WHERE project_id = timesheet_project_id AND employee_id = timesheet_employee_id")
    timesheetlist = dictfetchall(cursor)

    context = {
        "timesheetlist": timesheetlist
    }

    # Message according timesheet #
    context['heading'] = "Time Sheet Report";
    return render(request, 'timesheet-view.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;


def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM timesheet WHERE timesheet_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, timesheetId):
    context = {
        "fn": "update",
        "employeetypelist": getDropDown('employee_employee', 'employee_id'),
        "projectnamelist": getDropDown('project', 'project_id'),
        "timesheetDetails": getData(timesheetId),
        "heading": 'Employee Timesheet Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE timesheet
                   SET timesheet_employee_id=%s, timesheet_project_id=%s, timesheet_work_title=%s, timesheet_description=%s, timesheet_hours=%s, timesheet_date=%s WHERE timesheet_id = %s
                """, (
            request.POST['timesheet_employee_id'],
            request.POST['timesheet_project_id'],
            request.POST['timesheet_work_title'],
            request.POST['timesheet_description'],
            request.POST['timesheet_hours'],
            request.POST['timesheet_date'],
            timesheetId
        ))
        context["timesheetDetails"] =  getData(timesheetId)
        messages.add_message(request, messages.INFO, "Employee Timesheet updated succesfully !!!")
        return redirect('listing')
    else:
        return render(request, 'timesheet.html', context)



def add(request):
    context = {
        "fn": "add",
        "employeetypelist": getDropDown('employee_employee', 'employee_id'),
        "projectnamelist": getDropDown('project', 'project_id'),
        "heading": 'Time Sheet Details'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO timesheet
		   SET timesheet_employee_id=%s, timesheet_project_id=%s, timesheet_work_title=%s, timesheet_description=%s, timesheet_hours=%s, timesheet_date=%s
		""", (
            request.POST['timesheet_employee_id'],
            request.POST['timesheet_project_id'],
            request.POST['timesheet_work_title'],
            request.POST['timesheet_description'],
            request.POST['timesheet_hours'],
            request.POST['timesheet_date']))
        return redirect('listing')
    return render(request, 'timesheet.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM timesheet WHERE timesheet_id=' + id
    cursor.execute(sql)
    return redirect('listing')
