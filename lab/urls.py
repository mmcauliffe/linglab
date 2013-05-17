from django.conf.urls import patterns,url
from lab.views import MemberDetailView,MemberListView, PublicationListView,PresentationListView,ExperimentListView

urlpatterns = patterns('',
    url(r'^member/(?P<pk>\d+)/$',MemberDetailView.as_view(),name='member-detail'),
    url(r'^publications/$',PublicationListView.as_view(),name='publication-list'),
    url(r'^people/$',MemberListView.as_view(),name='member-list'),
    url(r'^presentations/$',PresentationListView.as_view(),name='presentation-list'),
    url(r'^studies/$',ExperimentListView.as_view(),name='experiment-list'),
    url(r'^presentations/bibtex/(?P<pk>\d+)/$','lab.views.presentation_bibtex',name='presentation-bibtex'),
    url(r'^publications/bibtex/(?P<pk>\d+)/$','lab.views.publication_bibtex',name='publication-bibtex'),
)
