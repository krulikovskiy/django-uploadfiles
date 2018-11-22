# django-uploadfiles

Установка
pip install https://github.com/krulikovskiy/django-autodeploy/archive/master.zip

Добавить в project/settings.py

INSTALLED_APPS = [
    ...
    uploadfiles
    ...
]

Для использованияв классе ModelInline вместо django.contrib.admin.TabularInline унаследовать uploadfiles.admin.MultipleTabularInline
А так же в главном классе ModelAdmin вместо django.contrib.admin.ModelAdmin унаследовать uploadfiles.admin.MultipleAdmin

В ModelInline переопределить 

@staticmethod
def process_uploaded_file(request, object, parent):
    object.parent = parent # связь с Model из ModelAdmin
    object.save()
    
и указать названия поля для сохранения файла
 name_field = 'file' 
