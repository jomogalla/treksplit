from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from splitter.views import no_group, group, group_hash, expense_transaction, person_transaction, group_transaction, passcode

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treksplit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', no_group),
    url(r'^(?P<group_id>\d{1,3})/$', group),
    url(r'^(?P<group_hash>\w{6,6})/$', group_hash),

    # make example redirect to group 1
    url(r'^example/$', group),

    # passcode below
	# url(r'^passcode/$', passcode),
    #AJAX update functions/urls below
    url(r'^expense/(?P<expense_id>\d+)/$', expense_transaction),
    url(r'^person/(?P<person_id>\d+)/$', person_transaction),
    url(r'^group/(?P<group_id>\d+)/$', group_transaction),
)
