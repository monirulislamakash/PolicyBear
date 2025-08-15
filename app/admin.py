from django.contrib import admin
from .models import *
# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('state',)
    search_fields = ('state',)
admin.site.register(State,StateAdmin)

class CarrierAdmin(admin.ModelAdmin):
    list_display = ('carrier',)
    search_fields = ('carrier',)
admin.site.register(Carrier,CarrierAdmin)

class Our_Partner_And_LocationAdmin(admin.ModelAdmin):
    list_display = ('Carrier', 'State','Payout')
    search_fields = ('Carrier', 'State','Payout')
admin.site.register(Our_Partner_And_Location,Our_Partner_And_LocationAdmin)

class SecondaryOfferAdmin(admin.ModelAdmin):
    list_display = ('State', 'Carrier','PolicyPlan','AgeFrom','AgeTo','IncomeFrom',"IncomeTO")
    search_fields = ('State', 'Carrier','PolicyPlan','AgeFrom','AgeTo','IncomeFrom',"IncomeTO")
admin.site.register(SecondaryOffer,SecondaryOfferAdmin)