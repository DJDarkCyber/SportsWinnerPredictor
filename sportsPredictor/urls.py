from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path("", views.main, name="index"),
    path("choose", views.predictOptions, name="predictOptions"),
    path("predictionHistory", views.predictionHistory, name="predictionHistory"),
    path("predictFootball", views.predictFootball, name="predictFootball"),
    path("footballPredictionResult", views.footballPredictionResult, name="footballPredictionResult"),
    path("predictBaseketball", views.predictBaseketball, name="predictBaseketball"),
    path("baseketballPredictionResult", views.baseketballPredictionResult, name="baseketballPredictionResult"),
    path("predictHockey", views.predictHockey, name="predictHockey"),
    path("hockeyPredictionResult", views.hockeyPredictionResult, name="hockeyPredictionResult"),
    path("predictAsiaWorldCup", views.predictAsiaWorldCup, name="predictAsiaWorldCup"),
    path("asiaWorldCupPredictionResult", views.asiaWorldCupPredictionResult, name="asiaWorldCupPredictionResult"),
    path("predictRugby", views.predictRugby, name="predictRugby"),
    path("rugbyPredictionResult", views.rugbyPredictionResult, name="rugbyPredictionResult"),
    path("predictIPL", views.predictIPL, name="predictIPL"),
    path("iplPredictionResult", views.iplPredictionResult, name="iplPredictionResult"),
    path("predictT20", views.predictT20, name="predictT20"),
    path("t20PredictionResult", views.t20PredictionResult, name="t20PredictionResult"),
]

urlpatterns += staticfiles_urlpatterns()