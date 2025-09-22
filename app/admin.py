from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CareersCategory)
admin.site.register(CareersLocation)
admin.site.register(CareersJobType)
admin.site.register(CareersDepartment)

admin.site.register(Privacy_Policy)
admin.site.register(Terms_of_Service)
admin.site.register(Disclaimer)

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
class Frequently_Asked_QuestionAdmin(admin.ModelAdmin):
    list_display = ('Question','Answer')
    search_fields = ('Question','Answer')
admin.site.register(Frequently_Asked_Question,Frequently_Asked_QuestionAdmin)

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('Titel', 'vacancy', 'Experience', 'Location')
    search_fields = ('Titel', 'vacancy', 'Experience', 'Location')
admin.site.register(JobPost,JobPostAdmin)\

class AppliedCandidatesAdmin(admin.ModelAdmin):
    list_display = ('Position','Full_Name','Phone','CV',)
    search_fields = ('Position','Full_Name','Phone',)
admin.site.register(AppliedCandidates,AppliedCandidatesAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('Name','Date')
    search_fields = ('Name','Date')
    readonly_fields=('slug',)
admin.site.register(Blog,BlogAdmin)