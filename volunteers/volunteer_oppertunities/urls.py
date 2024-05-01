from django.urls import path
from . import views

app_name = 'volunteer_opportunities'

urlpatterns = [
    path('opportunity_list/', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('create_opportunity/', views.CreateOpportunityView.as_view(), name='create_opportunity'),
    path('<int:pk>/update/', views.UpdateOpportunityView.as_view(), name='opportunity_update'),
    path('<int:pk>/delete/', views.DeleteOpportunityView.as_view(), name='opportunity_delete'),
    path('opportunity/<int:pk>/join/', views.JoinOpportunityConfirmView.as_view(), name='opportunity_join'),
]
