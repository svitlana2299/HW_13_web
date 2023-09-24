from django.urls import path, include
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('users/', include('users.urls')),
    path('quotes/create/', views.CreateQuoteView.as_view(), name='create_quote'),

]
