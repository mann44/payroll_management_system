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
        "SELECT * FROM department")
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
    cursor.execute("SELECT * FROM department WHERE dept_id = " + id)
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
                   SET dept_name=%s, dept_desc=%s WHERE dept_id = %s
                """, (
            request.POST['dept_name'],
            request.POST['dept_desc'],
            departmentId
        ))
        context["departmentDetails"] =  getData(departmentId)
        messages.add_message(request, messages.INFO, "Department updated succesfully !!!")
        return redirect('listing')
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
		   SET dept_name=%s, dept_desc=%s
		""", (
            request.POST['dept_name'],
            request.POST['dept_desc']))
        return redirect('listing')
    return render(request, 'department.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM department WHERE dept_id=' + id
    cursor.execute(sql)
    return redirect('listing')
