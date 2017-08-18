from __future__ import unicode_literals
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.conf import settings

class ImageSelect(Select):

    # class Media:
    #     css = {
    #         'all': ('/static/image-picker/image-picker/image-picker.css')
    #     }
    #     js = ('/static/image-picker/image-picker/image-picker.js')

    def __init__(self, attrs=None, choices=(), field_img=None):
        super(ImageSelect, self).__init__(attrs)
        self.choices = list(choices)
        self.field_img = field_img

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        i = img = None
        if option_value != '':
            i = int(option_value) - 1
            img = self.field_img[i]
        else:
            # img = '/static/img/nenhum.png'
            img = '/static/img/X.svg'

        return format_html('<option data-img-src="{}" value="{}"{}>{}</option>',
            img,
            option_value,
            selected_html,
            force_text(option_label)
            )