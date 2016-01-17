from django.conf.urls import include, url

from eventex.subscriptions.views import new, detail

urlpatterns = [
    url(r'^inscricao/$', new, name='new'),
    url(r'^inscricao/(\d+)/$', detail, name='detail'),
]
