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
        "SELECT * FROM project")
    projectlist = dictfetchall(cursor)

    context = {
        "projectlist": projectlist
    }

    # Message according Project#
    context['heading'] = "Project Details";
    return render(request, 'project-view.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM project WHERE project_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, projectId):
    context = {
        "fn": "update",
        "projectDetails": getData(projectId),
        "heading": 'Update Project',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE project
                   SET project_title=%s, project_description=%s, project_frontend=%s, project_backend=%s WHERE project_id = %s
                """, (
            request.POST['project_title'],
            request.POST['project_description'],
            request.POST['project_frontend'],
            request.POST['project_backend'],
            projectId
        ))
        context["projectDetails"] =  getData(projectId)
        messages.add_message(request, messages.INFO, "Project updated succesfully !!!")
        return redirect('listing')
    else:
        return render(request, 'project.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Project'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO project
		   SET project_title=%s, project_description=%s, project_frontend=%s, project_backend=%s
		""", (
            request.POST['project_title'],
            request.POST['project_description'],
            request.POST['project_frontend'],
            request.POST['project_backend']))
        return redirect('listing')
    return render(request, 'project.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM project WHERE project_id=' + id
    cursor.execute(sql)
    return redirect('listing')
