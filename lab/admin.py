from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import LabMember,Collaborator,Publication

class LabMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    
admin.site.register(LabMember,LabMemberAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    
admin.site.register(Publication,PublicationAdmin)
