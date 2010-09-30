from django.db import models


class ApiClass(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
    
class ApiFunction(models.Model):
    apiclass = models.ForeignKey(ApiClass)
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s-%s" %(self.apiclass.name, self.name) 
    
    
class ApiParam(models.Model):
    apifunction = models.ForeignKey(ApiFunction)
    name = models.CharField(max_length=255)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return "%s-%s-%s" %(self.apifunction.apiclass.name, self.apifunction.name,
                         self.name)
    