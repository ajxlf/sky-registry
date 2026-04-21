from django.urls import path

from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('compose/', views.compose, name='compose'),
    path('<int:pk>/', views.view_message, name='view'),
    path('<int:pk>/edit/', views.edit_draft, name='edit'),
    path('<int:pk>/delete/', views.delete_message, name='delete'),
    path('<int:pk>/reply/', views.reply, name='reply'),
    path('<int:pk>/forward/', views.forward, name='forward'),
]
