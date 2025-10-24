from django.http import Http404
from django.shortcuts import render, redirect
from . import services 
from .forms import EntryForm, TopicForm
from django.contrib.auth.decorators import login_required


# The @login_required decorator looks at the LOGIN_URL value in your settings to 
# figure out where to send unauthenticated users. By default, this value is /accounts/login/.



@login_required
def topic_list_view(request):
    """Handles the request for the homepage, displaying all topics."""
    topics = services.get_all_topics(user=request.user)
    context = {'topics': topics}
    return render(request, 'sheets/topic_list.html', context)


@login_required
def topic_detail_view(request, topic_id: int):
    """Handles the request for a single topic's detail page."""
    topic, entries = services.get_topic_detail(topic_id=topic_id)

    # --- Ownership Check ---
    if topic.owner != request.user:
        raise Http404
    # -----------------------    
    context = {
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'sheets/topic_detail.html', context)

@login_required
def add_topic_view(request):
    """Handles the page for adding a new topic."""
    if request.method == 'POST':
        # User is submitting data
        new_topic = services.create_topic(form_data=request.POST, owner=request.user)
        if new_topic:
            # If creation was successful, redirect to the new topic's page
            return redirect('sheets:topic_detail', topic_id=new_topic.id)
    else:
        # User is just visiting the page, show a blank form
        form = TopicForm()

    context = {'form': form}
    return render(request, 'sheets/add_topic.html', context)

@login_required
def add_entry_view(request, topic_id: int):
    """Handles adding a new entry to a specific topic."""

    topic = services.get_topic_by_id(topic_id=topic_id)

    if request.method == 'POST':
        new_entry = services.create_entry(topic=topic, form_data=request.POST)
        if new_entry:
            # Redirect back to the topic detail page to see the new entry
            return redirect('sheets:topic_detail', topic_id=topic.id)
    else:
        # Show a blank form
        form = EntryForm()

    context = {'topic': topic, 'form': form}
    return render(request, 'sheets/add_entry.html', context)

@login_required
def edit_entry_view(request, entry_id: int):
    """Handles editing an existing entry."""
    entry = services.get_entry_by_id(entry_id=entry_id)
    topic = entry.topic # We need the topic for the redirect URL

    # --- Ownership Check ---
    if entry.topic.owner != request.user:
        raise Http404
    # -----------------------

    if request.method == 'POST':
        # Pass the submitted data AND the original entry instance 
        updated_entry = services.update_entry(form_data=request.POST, instance=entry)
        if updated_entry:
            # Redirect to the topic page after a successful edit
            return redirect('sheets:topic_detail', topic_id=topic.id)
    else:
        # Show the form pre-filled with the existing entry's data
        form = EntryForm(instance=entry)

    context = {'entry': entry, 'form': form}
    return render(request, 'sheets/edit_entry.html', context)

@login_required
def edit_topic_view(request, topic_id: int):
    """Handles editing an existing entry."""
    topic = services.get_topic_by_id(topic_id=topic_id)

    # --- Ownership Check ---
    if topic.owner != request.user:
        raise Http404
    # -----------------------

    if request.method == 'POST':
        # Pass the submitted data AND the original entry instance 
        updated_topic = services.update_topic(form_data=request.POST, instance=topic)
        if updated_topic:
            # Redirect to the topic page after a successful edit
            return redirect('sheets:topic_detail', topic_id=topic.id)
    else:
        # Show the form pre-filled with the existing entry's data
        form = TopicForm(instance=topic)

    context = {'topic': topic, 'form': form}
    return render(request, 'sheets/edit_topic.html', context)


@login_required
def delete_entry_view(request, entry_id: int):
    """Handles the confirmation and deletion of an entry."""
    entry = services.get_entry_by_id(entry_id=entry_id)

    # --- Ownership Check ---
    if entry.topic.owner != request.user:
        raise Http404
    # -----------------------

    if request.method == 'POST':
        # User has confirmed the deletion
        topic_id = services.delete_entry(entry)
        return redirect('sheets:topic_detail', topic_id=topic_id)

    # If it's a GET request, show the confirmation page
    context = {'entry': entry}
    return render(request, 'sheets/delete_entry.html', context)

@login_required
def delete_topic_view(request, topic_id: int):
    """Handles the confirmation and deletion of an entry."""

    topic, entries = services.get_topic_detail(topic_id=topic_id)

    # --- Ownership Check ---
    if topic.owner != request.user:
        raise Http404
    # -----------------------

    if request.method == 'POST':
        # User has confirmed the deletion
        if services.delete_topic(topic):
            return redirect('sheets:topic_list')

    # If it's a GET request, show the confirmation page
    context = {
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'sheets/delete_topic.html', context)
