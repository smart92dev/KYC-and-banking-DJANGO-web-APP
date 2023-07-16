from django.contrib import admin
from django.urls import path, include
from core import views, transfer

app_name='core'

urlpatterns = [
    path ("", views.index,name='index'),

#Transfers
    path("search-account/", transfer.search_users_account_number, name="search-account")

]