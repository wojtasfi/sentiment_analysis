from django.urls import path

from . import views

app_name = 'sentiments'

urlpatterns = [
    path('', views.index, name='index'),
    path('analysis/<int:analysis_id>/', views.analysis, name='analysis'),
    path('analysis/count/', views.analysis_count, name='analysis_count'),
    path('analysis/', views.analysis_all, name='analysis_all'),
    path('analysis/pending/', views.analysis_pending, name='analysis_pending'),
    path('analysis/pending/count/', views.analysis_pending_count, name='analysis_pending_count'),
    path('analysis/pending/<int:analysis_pending_id>/', views.single_analysis_pending, name='analysis_pending'),
    path('auth/twitter/', views.add_twitter_auth, name='add_twitter_auth'),
    path('auth/twitter/exists', views.twitter_auth_exists, name='twitter_auth_exists'),
    path('auth/twitter/error', views.twitter_auth_error, name='twitter_auth_error'),
]
