from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from splitter.views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treksplit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ('^$', index),
)
