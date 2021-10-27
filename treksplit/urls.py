from django.urls import include, path, re_path

from django.contrib import admin
admin.autodiscover()

from splitter.views import no_group, group, group_hash, expense_transaction, person_transaction, group_transaction, passcode

urlpatterns = [
    # Examples:
    # url(r'^$', 'treksplit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    re_path(r'^$', no_group),
    re_path(r'^(?P<group_id>\d{1,3})/$', group),
    re_path(r'^(?P<group_hash>\w{6,6})/$', group_hash),

    # make example redirect to group 1
    re_path(r'^example/$', group),

    # passcode below
	# url(r'^passcode/$', passcode),
    #AJAX update functions/urls below
    re_path(r'^expense/(?P<expense_id>\d+)/$', expense_transaction),
    re_path(r'^person/(?P<person_id>\d+)/$', person_transaction),
    re_path(r'^group/(?P<group_id>\d+)/$', group_transaction),
]
