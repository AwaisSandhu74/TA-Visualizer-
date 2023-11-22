from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.render_news_and_sentiment, name="home"),
    path('company_graph_lch/<str:ticker>/<int:period>', views.company_graph_lch, name='company_graph_lch'),
    path('company_graph_3type/<str:ticker>/<str:indicator_type>/<int:window>', views.company_graph_3type, name='company_graph_3type'),
    path('company_graph_4type/<str:ticker>/<str:indicator_type>/<int:window>', views.company_graph_4type, name='company_graph_4type'),
    path('company_graph_bbands/<str:ticker>/<int:window>', views.company_graph_bbands, name='company_graph_bbands'),
    path('company_graph_aroon/<str:ticker>/<int:window>', views.company_graph_aroon, name='company_graph_aroon'),
    path('topic_graph/<int:number>', views.render_topic_graph, name='topic_relevance_graph'),
    path('sentiment_graph/<int:number>', views.render_sentiment_graph, name='ticker_sentiment_graph'),



]
    