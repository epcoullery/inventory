from django.conf.urls import patterns, include, url

from django.contrib import admin

from inventory import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),
    url(r'^admin/$', views.cond_redirect),
    url(r'^storage/(?P<pk>\d+)/$', views.StorageView.as_view(), name="storage"),
    url(r'^storage/(?P<pk>\d+)/edititem/$',
        views.QuantityEditView.as_view(), name="quantity_edit"),

    url(r'^admin/', include(admin.site.urls)),
)
