from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username','name', 'dob', 'phone', 'country','count')





class PostAdmin(admin.ModelAdmin):
    list_display = ('username','caption','img','Location','count' )


class friendlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')


class friendrequestAdmin(admin.ModelAdmin):
    list_display = ('From_user', 'To_user','date')


class EventsAdmin(admin.ModelAdmin):
    list_display = ('Owner', 'Name','date','Description','type','public','venue')



class GroupprofileAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'admin','DP','Dateofcreation')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(friendlist, friendlistAdmin)
admin.site.register(friendrequest, friendrequestAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Groupprofile, GroupprofileAdmin)
admin.site.register(Post, PostAdmin)