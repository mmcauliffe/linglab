from django.conf.urls import patterns

urlpatterns = patterns('lab.views',
    (r'^member/(?P<member_id>\d+)/$','member'),
    (r'^publications/$','publications'),
    (r'^people/$','people'),
    (r'^presentations/$','presentations'),
)
