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
    cursor.execute("SELECT * FROM department")
    departmentlist = dictfetchall(cursor)

    context = {
        "departmentlist": departmentlist
    }

    # Message according medicines Role #
    context['heading'] = "Department Details";
    return render(request, 'department-details.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM department WHERE department_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, departmentId):
    context = {
        "fn": "update",
        "departmentDetails": getData(departmentId),
        "heading": 'Update Department',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE department
                   SET department_name=%s, department_desc=%s WHERE department_id = %s
                """, (
            request.POST['department_name'],
            request.POST['department_desc'],
            departmentId
        ))
        context["departmentDetails"] =  getData(departmentId)
        messages.add_message(request, messages.INFO, "Department updated succesfully !!!")
        return redirect('department-listing')
    else:
        return render(request, 'department.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Department'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO department
		   SET department_name=%s, department_desc=%s
		""", (
            request.POST['department_name'],
            request.POST['department_desc']))
        return redirect('department-listing')
    return render(request, 'department.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM department WHERE department_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Department Deleted succesfully !!!")
    return redirect('department-listing')
