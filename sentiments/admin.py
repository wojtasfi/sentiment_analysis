from django.contrib import admin

from .models import Analysis, AnalysisPending, OneDayResult, TwitterAuth

admin.site.register(Analysis)
admin.site.register(AnalysisPending)
admin.site.register(OneDayResult)
admin.site.register(TwitterAuth)
