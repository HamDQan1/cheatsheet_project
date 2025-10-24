from django.urls import path
from . import views

app_name = 'sheets'
urlpatterns = [
    # Homepage that lists all topics
    path('', views.topic_list_view, name='topic_list'),

    # Page for a single topic and its entries
    # The <int:topic_id> part captures the number from the URL
    path('topics/<int:topic_id>/', views.topic_detail_view, name='topic_detail'),
    # Page for adding a new topic
    path('add-topic/', views.add_topic_view, name='add_topic'),

    # Page for adding a new entry to a specific topic
    path('topics/<int:topic_id>/add-entry/', views.add_entry_view, name='add_entry'),

    # Page for editing an existing entry
    path('edit-entry/<int:entry_id>/', views.edit_entry_view, name='edit_entry'),
    
    # Page for editing an existing entry
    path('edit-topic/<int:topic_id>/', views.edit_topic_view, name='edit_topic'),

    # Page for deleting an entry
    path('delete-entry/<int:entry_id>/', views.delete_entry_view, name='delete_entry'),

    # Page for deleting an entry
    path('delete-topic/<int:topic_id>/', views.delete_topic_view, name='delete_topic'),
]