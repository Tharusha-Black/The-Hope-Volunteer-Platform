from django.urls import path
from .views import PrivateChatView, GroupChatView

urlpatterns = [
    path('private_chat/<int:user_id>/', PrivateChatView.as_view(), name='private_chat'),
    path('group_chat/<int:project_id>/', GroupChatView.as_view(), name='group_chat'),

]
