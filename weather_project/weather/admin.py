from django.contrib import admin
from .models import ContactTicket

@admin.register(ContactTicket)
class ContactTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات تماس', {
            'fields': ('name', 'email')
        }),
        ('پیام', {
            'fields': ('message',)
        }),
        ('وضعیت', {
            'fields': ('is_read', 'created_at')
        }),
    )
