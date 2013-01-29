from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import LabMember,Collaborator,Publication,Presentation,Position

class LabMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    
admin.site.register(LabMember,LabMemberAdmin)

class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    
admin.site.register(Collaborator,CollaboratorAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    
admin.site.register(Publication,PublicationAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    
admin.site.register(Presentation,PresentationAdmin)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    
admin.site.register(Position,PositionAdmin)
