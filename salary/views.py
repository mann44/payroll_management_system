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
    if(request.session.get('user_level_id', None) != 1):
        cursor.execute("SELECT * FROM month, salary, users_user WHERE month_id = salary_month AND user_id = salary_user_id AND salary_user_id ="+str(request.session.get('user_id'))+"  ORDER BY month_id")
    else:
        cursor.execute("SELECT * FROM month, salary, users_user WHERE month_id = salary_month AND user_id = salary_user_id ORDER BY month_id")
    salarylist = dictfetchall(cursor)

    context = {
        "salarylist": salarylist
    }

    # Message according Salary #
    context['heading'] = "Salary Details";
    return render(request, 'salary-view.html', context)


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
    cursor.execute("SELECT * FROM salary WHERE salary_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];


def slip(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM month, designation, department, salary, users_user WHERE user_department = department_id AND user_designation = designation_id AND month_id = salary_month AND user_id = salary_user_id AND salary_id ="+str(id)+"  ORDER BY month_id")
    dataList = dictfetchall(cursor)
    context = {
        "fn": "update",
        "employeetypelist": getDropDown('users_user', 'user_id'),
        "salaryDetails": dataList[0],
        "heading": 'Employee Salary Update',
    };
    return render(request, 'salary-slip.html', context)

def update(request, salaryId):
    context = {
        "fn": "update",
        "employeetypelist": getDropDown('users_user', 'user_id'),
        "salaryDetails": getData(salaryId),
        "heading": 'Employee Salary Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE salary
                   SET salary_user_id=%s, salary_month=%s, salary_working_days=%s, salary_basic=%s, salary_hra=%s, salary_mediclaim=%s, salary_ta=%s,
		   salary_da=%s, salary_reimbursement=%s, salary_ca=%s, salary_others=%s, salary_dpf=%s, salary_dtax=%s, salary_dedc=%s, salary_total=%s, salary_year=%s
		   WHERE salary_id = %s
                """, (
            request.POST['salary_user_id'],
            request.POST['salary_month'],
            request.POST['salary_working_days'],
            request.POST['salary_basic'],
            request.POST['salary_hra'],
            request.POST['salary_mediclaim'],
            request.POST['salary_ta'],
            request.POST['salary_da'],
            request.POST['salary_reimbursement'],
            request.POST['salary_ca'],
            request.POST['salary_others'],
            request.POST['salary_dpf'],
            request.POST['salary_dtax'],
            request.POST['salary_dedc'],
            request.POST['salary_total'],
            request.POST['salary_year'],
            salaryId
        ))
        context["salaryDetails"] =  getData(salaryId)
        messages.add_message(request, messages.INFO, "Employee Salary updated succesfully !!!")
        return redirect('listing')
    else:
        return render(request, 'salary.html', context)




def add(request):
    context = {
        "fn": "add",
        "employeetypelist": getDropDown('users_user', 'user_id'),
        "heading": 'Salary Details'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO salary
		   SET salary_user_id=%s, salary_month=%s, salary_working_days=%s, salary_basic=%s, salary_hra=%s, salary_mediclaim=%s, salary_ta=%s,
		   salary_da=%s, salary_reimbursement=%s, salary_ca=%s, salary_others=%s, salary_dpf=%s, salary_dtax=%s, salary_dedc=%s, salary_total=%s, salary_year=%s		   
		""", (
            request.POST['salary_user_id'],
            request.POST['salary_month'],
            request.POST['salary_working_days'],
            request.POST['salary_basic'],
            request.POST['salary_hra'],
            request.POST['salary_mediclaim'],
            request.POST['salary_ta'],
            request.POST['salary_da'],
            request.POST['salary_reimbursement'],
            request.POST['salary_ca'],
            request.POST['salary_others'],
            request.POST['salary_dpf'],
            request.POST['salary_dtax'],
            request.POST['salary_dedc'],
            request.POST['salary_total'],
            request.POST['salary_year']))
        return redirect('listing')
    return render(request, 'salary.html', context)


def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM salary WHERE salary_id=' + id
    cursor.execute(sql)
    return redirect('listing')
