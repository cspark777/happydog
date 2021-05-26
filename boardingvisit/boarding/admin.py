from django.contrib import admin
from .models import Dateinyear, Dog, Visit
from django.core.exceptions import ValidationError
# Register your models here.
from django.contrib import messages

class DogAdmin(admin.ModelAdmin):
    list_display =['id', 'first_name', 'last_name']

    def save_model(self, request, obj, form, change):
        
        instance = form.save(commit=False)
        
        sql = "SELECT * FROM boarding_dog WHERE first_name='{}' AND last_name='{}'".format(instance.first_name, instance.last_name)

        
        a = Dog.objects.raw(sql)
        
        if len(a) > 0:   
            messages.error(request, 'The name is already existed')            
            return

        instance.save()
        form.save_m2m()

admin.site.register(Dog, DogAdmin)

class VisitAdmin(admin.ModelAdmin):
    list_display = ('dog', 'start_at', 'end_at')

    def save_model(self, request, obj, form, change):
        
        instance = form.save(commit=False)
        
        sql = "SELECT * FROM boarding_visit WHERE dog_id={} AND \
        start_at<'{}' AND end_at>'{}'".format(instance.dog.id, instance.end_at, instance.start_at)

        print(sql)
        a = Visit.objects.raw(sql)
        print(len(a))
        if len(a) > 0:   
            messages.error(request, 'Date range is conflict with previous range')         
            
            return

        instance.save()
        form.save_m2m()

admin.site.register(Visit, VisitAdmin)
