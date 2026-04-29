from django.urls import path
# import path function for defining URLs

from . import views
# import views from current app


app_name = 'messaging'
# namespace for messaging URLs (used in templates like messaging:inbox)


urlpatterns = [
    path('', views.inbox, name='inbox'),
    # /messages/ → inbox page

    path('sent/', views.sent, name='sent'),
    # /messages/sent/ → sent messages

    path('drafts/', views.drafts, name='drafts'),
    # /messages/drafts/ → drafts page

    path('compose/', views.compose, name='compose'),
    # /messages/compose/ → compose new message

    path('<int:pk>/', views.view_message, name='view'),
    # /messages/1/ → view a specific message

    path('<int:pk>/edit/', views.edit_draft, name='edit'),
    # /messages/1/edit/ → edit a draft message

    path('<int:pk>/delete/', views.delete_message, name='delete'),
    # /messages/1/delete/ → delete a message

    path('<int:pk>/reply/', views.reply, name='reply'),
    # /messages/1/reply/ → reply to a message

    path('<int:pk>/forward/', views.forward, name='forward'),
    # /messages/1/forward/ → forward a message
]