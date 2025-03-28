from django.apps import apps
from django import template

register = template.Library()

@register.simple_tag
def installed_apps():
    modules = []
        
    if apps.is_installed('scuffle'):
        modules.append('scuffle')
    if apps.is_installed('squeak'):
        modules.append('squeak')        

    return modules
