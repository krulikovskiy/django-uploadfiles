from django.contrib import admin
from django.contrib.admin import options
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import File
from string import ascii_letters
import random
from django.core.exceptions import FieldDoesNotExist
from django.urls import path
from PIL import Image


class MultipleTabularInline(options.InlineModelAdmin):
    # todo-nick Сделать template по виду менеджера файла и вынести в новую админ модель MultipleManageInline
    template = 'admin/uploadfiles/tabular.html'
    name_field = False  # Название поля в модели с model.FileField
    random_filename = False  # Рандомное название или оригинальное

    @staticmethod
    def process_uploaded_file(request, object, parent):
        # ... можно сохранить свои поля
        # object.parent = parent # Нужно указать поле
        raise NotImplementedError


class MultipleAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/uploadfiles/js/uploadfiles.js',)
        css = {
            'all': ('admin/uploadfiles/css/uploadfiles.css',)
        }

    multiupload_inline = []

    def get_multiupload_inline(self):
        for inline in self.inlines:
            try:
                if inline.name_field != False:
                    self.multiupload_inline.append(inline)
            except AttributeError:
                pass

    def get_urls(self, *args, **kwargs):
        self.get_multiupload_inline()
        multi_urls = []
        for inline in self.multiupload_inline:
            app_name = inline.model._meta.app_label
            model_name = inline.model.__name__
            print(model_name)
            multi_urls.append(
                path('<path:object_id>/uploadfiles/<inline_name>', self.admin_site.admin_view(self.inline_upload_view),
                     name='uploadfiles'))

        return multi_urls + super(MultipleAdmin, self).get_urls(*args, **kwargs)

    @csrf_exempt
    def inline_upload_view(self, request, object_id, inline_name):
        if object_id:
            parent = self.get_object(request, object_id)

        inline = None
        self.get_multiupload_inline()
        for inline_model in self.multiupload_inline:
            if inline_model.model.__name__ == inline_name:
                inline = inline_model

        if request.method == 'POST' and inline:
            for f in request.FILES.getlist('uploadfiles[]'):
                object = inline.model()

                try:
                    file_field = object._meta.get_field(inline.name_field)
                except FieldDoesNotExist:
                    break

                if inline.random_filename:
                    filename = ''.join(random.choice(ascii_letters) for i in range(24))
                else:
                    filename = f.name

                try:
                    if file_field.__class__.__name__ == 'ImageField':
                        image = Image.open(f)
                        image.verify()
                        file_field = image
                    else:
                        file_field = file

                    file = File(f)
                    file.name = filename

                    setattr(object, inline.name_field, file)
                    inline.process_uploaded_file(request, object, parent)
                except Exception as exc:
                    pass

                # todo-nick Сделать возращения формы formsets inline с ошибками
                # inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
                # for inline_formset in inline_formsets:
                #     media = media + inline_formset.media

        return JsonResponse({'status': True})
