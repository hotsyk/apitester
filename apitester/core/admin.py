from django.contrib import admin
from apitester.core.models import *

class ApiFunctionInline(admin.TabularInline):
    model = ApiFunction
 
 
class ApiClassAdmin(admin.ModelAdmin):
    inlines = [
        ApiFunctionInline,
    ]


class ApiParamInline(admin.TabularInline):
    model = ApiParam

   
class ApiFunctionAdmin(admin.ModelAdmin):
    inlines = [
        ApiParamInline,
    ]


class ApiParamAdmin(admin.ModelAdmin):
    pass



    
admin.site.register(ApiClass, ApiClassAdmin)
admin.site.register(ApiFunction, ApiFunctionAdmin)
admin.site.register(ApiParam, ApiParamAdmin)