
from django.contrib import admin
from .models import DreamEntry, DreamSymbol, DreamEntrySymbol


@admin.register(DreamSymbol)
class DreamSymbolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(DreamEntry)
class DreamEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'dream_date', 'created_at')
    search_fields = ('title', 'dream_text', 'user__username')
    list_filter = ('dream_date',)


admin.site.register(DreamEntrySymbol)
