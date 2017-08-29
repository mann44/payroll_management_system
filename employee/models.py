# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_user = models.CharField(max_length=255, default = "", unique=True)
    employee_password = models.CharField(max_length=20, default = "")
    employee_level = models.CharField(max_length=255, default = '2')
    employee_sal = models.CharField(max_length=20, default = "")
    employee_first_name = models.CharField(max_length=255, default = "")    
    employee_middle_name = models.CharField(max_length=255, default = "")
    employee_last_name = models.CharField(max_length=255, default = "")	
    employee_gender = models.CharField(max_length=10, default = "")
    employee_address = models.TextField(default = "")
    employee_village = models.CharField(max_length=255, default = "")
    employee_state = models.CharField(max_length=255, default = "")
    employee_country = models.CharField(max_length=255, default = "")
    employee_landline = models.CharField(max_length=255, default = "")
    employee_mobile = models.CharField(max_length=255, default = "")
    employee_email = models.EmailField(max_length=255, default = "")
    employee_status = models.CharField(max_length=255, default = "")
    employee_deparment = models.CharField(max_length=255, default = "")
    employee_dob = models.CharField(max_length=255, default = "")
    employee_nationalty = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.employee_user

class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.state_name

class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.city_name

class country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.country_name
