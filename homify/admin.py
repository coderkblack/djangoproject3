from django.contrib import admin

from homify.models import Client, Houses, Onsale, Payment


# Register your models here.
admin.site.site_header = 'Homify'
admin.site.site_title = 'Manage Homify'

class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']
    list_per_page = 30

class HousesAdmin(admin.ModelAdmin):
    list_display = ['name', 'developer', 'address', 'city', 'state', 'country']
    search_fields = ['name', 'developer', 'address', 'city', 'state', 'country']
    list_per_page = 35

class OnsaleAdmin(admin.ModelAdmin):
    list_display = ['house', 'customer', 'status', 'deadline_of_payment']
    search_fields = ['house', 'customer', 'status', 'deadline_of_payment']
    list_per_page = 30

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['onsale', 'code', 'status', 'amount', 'created_at']
    search_fields = ['onsale', 'code', 'status', 'amount', 'created_at']
    list_per_page = 35

admin.site.register(Client, ClientAdmin)
admin.site.register(Houses, HousesAdmin)
admin.site.register(Onsale, OnsaleAdmin)
admin.site.register(Payment, PaymentAdmin)