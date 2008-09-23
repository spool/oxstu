from django.conf.urls.defaults import *
from oxnews import urls
from story.models import Story
import os
from django.conf import settings

story_info_dict = {
        'queryset': Story.published.all(),
        'template_name': 'story.html',
        'template_object_name': 'story',
        }

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^story/id/(?P<object_id>[\d]+)/$', 'django.views.generic.list_detail.object_detail',
        story_info_dict),
    (r'^story/(?P<slug>[\w-]+)/$', 'django.views.generic.list_detail.object_detail',
        story_info_dict),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    # Static Media
    (r'^css/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.FILEROOT, "static", "css")}),
    (r'^images/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.FILEROOT, "static", "images")}),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.FILEROOT, "static", "media")}),
    (r'^js/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.FILEROOT, "static", "js")}),
    (r'^photos/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.FILEROOT, "static", "photos")}),
)
