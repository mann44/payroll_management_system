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
        "SELECT * FROM appraisal, employee_employee WHERE employee_id = appr_emp_id")
    appraisallist = dictfetchall(cursor)

    context = {
        "appraisallist": appraisallist
    }

    # Message according timesheet #
    context['heading'] = "Appraisal Report";
    return render(request, 'appraisal-view.html', context)


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
    cursor.execute("SELECT * FROM appraisal WHERE appr_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, apprId):
    context = {
        "fn": "update",
        "employeetypelist": getDropDown('employee_employee', 'employee_id'),
        "apprDetails": getData(apprId),
        "heading": 'Employee Appraisal Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE appraisal
                   SET appr_emp_id=%s, appr_manager_name=%s, appr_comm_point=%s, appr_team_point=%s, appr_prog_point=%s, appr_write_point=%s, appr_client_point=%s, appr_database_point=%s WHERE appr_id = %s
                """, (
            request.POST['appr_emp_id'],
            request.POST['appr_manager_name'],
            request.POST['appr_comm_point'],
            request.POST['appr_team_point'],
            request.POST['appr_prog_point'],
            request.POST['appr_write_point'],
            request.POST['appr_client_point'],
            request.POST['appr_database_point'],
            apprId
        ))
        context["apprDetails"] =  getData(apprId)
        messages.add_message(request, messages.INFO, "Employee Appraisal updated succesfully !!!")
        return redirect('listing')
    else:
        return render(request, 'appraisal.html', context)


def add(request):
    context = {
        "fn": "add",
        "employeetypelist": getDropDown('employee_employee', 'employee_id'),
        "heading": 'Appraisal Details'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO `appraisal`
		   SET appr_emp_id=%s, appr_manager_name=%s, appr_comm_point=%s, appr_team_point=%s, appr_prog_point=%s, appr_write_point=%s, appr_client_point=%s, appr_database_point=%s
		""", (
            request.POST['appr_emp_id'],
            request.POST['appr_manager_name'],
            request.POST['appr_comm_point'],
            request.POST['appr_team_point'],
            request.POST['appr_prog_point'],
            request.POST['appr_write_point'],
            request.POST['appr_client_point'],
            request.POST['appr_database_point']))
        return redirect('listing')
    return render(request, 'appraisal.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM appraisal WHERE appr_id=' + id
    cursor.execute(sql)
    return redirect('listing')
