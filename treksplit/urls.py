from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from splitter.views import no_group, group, expense_transaction, person_transaction, group_transaction

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treksplit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', no_group),
    url(r'^(?P<group_id>\d+)/$', group),
    #AJAX update functions/urls below
    url(r'^expense/(?P<expense_id>\d+)/$', expense_transaction),
    url(r'^person/(?P<person_id>\d+)/$', person_transaction),
    url(r'^group/(?P<group_id>\d+)/$', group_transaction),
)
