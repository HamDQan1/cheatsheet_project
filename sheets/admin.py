from django.contrib import admin
from .models import Topic, Entry
from django.contrib.auth.models import User


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('owner','title',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at', 'updated_at')
    list_filter = ('topic',)
    search_fields = ('title', 'content')