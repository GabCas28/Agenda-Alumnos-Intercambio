from typing import Text
from django import forms
from django.forms import ModelForm, Form, ModelMultipleChoiceField
from django.forms.fields import BooleanField, CharField, EmailField, ChoiceField, MultipleChoiceField
from django.forms.widgets import PasswordInput
from .models import  MassMail
from django_summernote.widgets import SummernoteWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from agendas.models import Agenda
from contacts.models import Contact
from mailtemplates.models import MailTemplate

class MassMailForm(ModelForm):
    user= CharField(required=True, label="Email del remitente")
    password = CharField(widget=PasswordInput(), label="Contraseña del email")
    agenda = ChoiceField()
    template = ChoiceField()
    maintain = BooleanField(required=False, label="Conservar contactos existentes")
    headers = ChoiceField()

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category') if 'category' in kwargs else None
        headers = kwargs.pop('headers') if 'headers' in kwargs else []
        headers = [("{{ "+header+" }}","{{ "+header+" }}") for header in headers]
        agendas=[(agenda.slug, agenda.__str__) for agenda in Agenda.objects.all()]
        templates=[(template.slug, template.__str__) for template in MailTemplate.objects.all()]
        headers.insert(0,(None,"---"))
        agendas.insert(0,(None,"---"))
        templates.insert(0,(None,"---"))
        queryset=Contact.objects.filter(agenda__category__slug=category.slug) if category else Contact.objects.all()
        super(MassMailForm, self).__init__(*args, **kwargs)
        self.fields['agenda'] = ChoiceField(choices=agendas, required = False, label="Agenda",)
        self.fields['template'] = ChoiceField(choices=templates, required = False, label="Plantilla")
        self.fields['headers'] = ChoiceField(choices=headers, required = False, label="Variables de la agenda")
        self.fields['recipients'] = ModelMultipleChoiceField(
                label="Destinatarios del mensaje",
                required=False,
                queryset=queryset,
                widget=FilteredSelectMultiple("contacts", is_stacked=True),
                )

    class Meta:
        model = MassMail
        fields = ['subject', 'recipients', 'headers','content','user', 'password', 'agenda', 'maintain', 'template']
        widgets = {
            'content': SummernoteWidget(),
            # 'recipients': FilteredSelectMultiple("contacts", is_stacked=False),
        }
    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css', '/static/css/styles.css', ),
        }
        js = ('/admin/jsi18n','/static/js/custom-menu.js',)

# class RecipientsForm(ModelForm):
#     agenda=ChoiceField(choices=[(agenda.id, agenda.__str__) for agenda in Agenda.objects.all()], required = False)

# class TemplateForm(ModelForm):
#     template=ChoiceField(choices=[(template.id, template.__str__) for template in MailTemplate.objects.all()], required = False)