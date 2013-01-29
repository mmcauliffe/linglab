from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import *

class LabAuthorshipInline(admin.TabularInline):
    model = WrittenByLab
    
class CollabAuthorshipInline(admin.TabularInline):
    model = WrittenByCollab

class LabPresentershipInline(admin.TabularInline):
    model = PresentedByLab
    
class CollabPresentershipInline(admin.TabularInline):
    model = PresentedByCollab

class LabMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    
admin.site.register(LabMember,LabMemberAdmin)

class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','link')
    
admin.site.register(Collaborator,CollaboratorAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    inlines = [LabAuthorshipInline,
                CollabAuthorshipInline]
    
admin.site.register(Publication,PublicationAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('generate_key',)
    inlines = [LabPresentershipInline,
                CollabPresentershipInline]
    
admin.site.register(Presentation,PresentationAdmin)

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title','importance')
    
admin.site.register(Position,PositionAdmin)
