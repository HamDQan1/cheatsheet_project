"""
Context processors for the cheatsheet project.
Context processors make data available to ALL templates automatically.
"""

from sheets.models import Topic


def topics_list(request):
    """
    Makes all topics available in every template as 'all_topics'.
    
    This allows the sidebar to display topics on every page without
    explicitly passing them from each view.
    
    Usage in templates: {{ all_topics }}
    """
    if request.user.is_authenticated:
        # Only show topics for logged-in users, ordered alphabetically
        topics = Topic.objects.filter(owner=request.user).order_by('title')
    else:
        topics = []
    
    return {
        'all_topics': topics
    }
