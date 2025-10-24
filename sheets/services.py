from .models import Entry, Topic
from django.shortcuts import get_object_or_404
from .forms import EntryForm, TopicForm

def get_all_topics(user):
    """Returns a queryset of all Topic objects, ordered by title."""
    return Topic.objects.filter(owner=user).order_by('title')

def get_topic_by_id(topic_id: int):
    """Safely retrieves a single topic by its ID."""
    return get_object_or_404(Topic, id=topic_id)

def get_entry_by_id(entry_id: int):
    """Safely retrieves a single entry by its ID."""
    return get_object_or_404(Entry, id=entry_id)

def get_topic_detail(topic_id: int):
    """
    Returns a specific topic and its related entries.
    - topic: The Topic object itself.
    - entries: A queryset of all entries for that topic.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entries.all() 
    return topic, entries

def create_topic(form_data,owner):
    """
    Validates and creates a new topic from the given form data.
    Returns the created topic object or None if the form is invalid.
    """
    form = TopicForm(form_data)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.owner = owner
        topic.save()
        return topic
    return None

def create_entry(topic, form_data):
    """
    Validates and creates a new entry for a specific topic.
    Returns the created entry object or None if the form is invalid.
    """
    form = EntryForm(form_data)
    if form.is_valid():
        # Don't save to the database yet.
        entry = form.save(commit=False)
        # Manually assign the topic before the final save.
        entry.topic = topic
        entry.save()
        return entry
    return None

def update_entry(form_data, instance):
    """
    Validates and saves the updated entry data from a form.
    Returns the updated entry object or None if the form is invalid.
    """
    form = EntryForm(form_data, instance=instance)
    if form.is_valid():
        entry = form.save()
        return entry
    return None

def update_topic(form_data, instance):
    """
    Validates and saves the updated entry data from a form.
    Returns the updated entry object or None if the form is invalid.
    """
    form = TopicForm(form_data, instance=instance)
    if form.is_valid():
        entry = form.save()
        return entry
    return None

def delete_entry(entry):
    """Deletes a given entry object."""
    topic_id = entry.topic.id
    entry.delete()
    # Return the topic_id for a successful redirect
    return topic_id

def delete_topic(topic):
    """Deletes a given entry object."""
    topic.delete()
    # Return the topic_id for a successful redirect
    return True