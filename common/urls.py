from django.conf.urls import patterns, include, url

from django.contrib import admin

from inventory import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),
    url(r'^admin/$', views.cond_redirect),
    url(r'^storage/(?P<pk>\d+)/$', views.StorageView.as_view(), name="storage"),
    url(r'^storage/(?P<pk>\d+)/xlsx/$', views.StorageView.as_view(render_format='xlsx'), name="storage_export"),
    url(r'^storage/(?P<pk>\d+)/edititem/$',
        views.QuantityEditView.as_view(), name="quantity_edit"),
    url(r'^movement/(?P<year>\d{4})/$', views.MovementExport.as_view(), name="movement_export"),

    url(r'^admin/', include(admin.site.urls)),
)
