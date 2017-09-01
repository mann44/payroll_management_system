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
        "SELECT * FROM leave, status, employee_employee WHERE status_id = leave_status AND employee_id = leave_employee_id")
    leavelist = dictfetchall(cursor)

    context = {
        "leavelist": leavelist
    }
   
    # Message according leavelist Role #
    context['heading'] = "Employee Leave Report";
    return render(request,'leave-view.html',context)


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


def add(request):
    context = {
        "fn": "add",
        "employeetypelist": getDropDown('employee_employee', 'employee_id'),
        "statusList": getDropDown('status','status_id'),
        "heading": 'Leave Details'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        print cursor.execute("""
		   INSERT INTO leave
		   SET leave_employee_id=%s, leave_reason=%s, leave_description=%s, leave_from_date=%s, leave_to_date=%s, leave_status=%s
		""", (
            request.POST['leave_employee_id'],
            request.POST['leave_reason'],
            request.POST['leave_description'],
            request.POST['leave_from_date'],
            request.POST['leave_to_date'],
            request.POST['leave_status']))
        return redirect('listing')
    return render(request, 'leave-add.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM leave WHERE leave_id=' + id
    cursor.execute(sql)
    return redirect('listing')
