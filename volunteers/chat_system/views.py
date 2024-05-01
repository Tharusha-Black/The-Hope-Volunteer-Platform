from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PrivateChat, GroupChat, Message
from volunteer_oppertunities.models import VolantDetails
from django.contrib.auth import get_user_model
from user_management.models import VolantUser


class PrivateChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_system/private_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the user ID from URL parameters
        user_id = self.kwargs['user_id']
        other_user = get_object_or_404(get_user_model(), pk=user_id)

        # Retrieve or create a private chat object between the current user and the user with the given ID
        user_chats = PrivateChat.objects.filter(participants=self.request.user)
        other_user_chats = PrivateChat.objects.filter(participants=other_user)
        
        # Find the intersection of user's chats and other user's chats to get the private chat
        chat = user_chats.filter(pk__in=other_user_chats.values_list('pk', flat=True)).first()

        # If no chat exists, create a new one
        if not chat:
            chat = PrivateChat.objects.create()
            chat.participants.add(self.request.user, other_user)

        # Get all messages associated with the private chat
        messages = Message.objects.filter(chat=chat)
        all_users = VolantUser.objects.exclude(pk=user_id)

        # Pass chat and messages to the template
        context['chat'] = chat
        context['messages'] = messages
        context['other_user'] = other_user  
        context['all_users'] = all_users 
        return context

    def post(self, request, **kwargs):
        # Get the user ID from URL parameters
        user_id = self.kwargs['user_id']
        other_user = get_object_or_404(get_user_model(), pk=user_id)
        
        # Retrieve or create a private chat object between the current user and the user with the given ID
        user_chats = PrivateChat.objects.filter(participants=self.request.user)
        other_user_chats = PrivateChat.objects.filter(participants=other_user)
        chat = user_chats.filter(pk__in=other_user_chats.values_list('pk', flat=True)).first()

        # If no chat exists, create a new one
        if not chat:
            chat = PrivateChat.objects.create()
            chat.participants.add(self.request.user, other_user)

        # Create a new message
        message_content = request.POST.get('message_content')
        if message_content:
            Message.objects.create(chat=chat, sender=request.user, content=message_content)

        # Redirect back to the private chat page
        return redirect('private_chat', user_id=user_id)


class GroupChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_system/group_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the project ID from URL parameters
        project_id = self.kwargs['project_id']
        
        # Retrieve or create a group chat object for the project with the given ID
        chat, created = GroupChat.objects.get_or_create(project_id=project_id)
        
        # Get all messages associated with the group chat
        messages = Message.objects.filter(group_chat=chat)
        
        # Get user IDs associated with the project
        project_user_ids = VolantDetails.objects.filter(project_id=project_id).values_list('user', flat=True)
        
        # Get usernames associated with the user IDs
        VolantUser = get_user_model()
        project_users = VolantUser.objects.filter(id__in=project_user_ids)
        # Pass chat, messages, and project users to the template
        context['chat'] = chat
        context['messages'] = messages
        context['members'] = project_users
        return context

    def post(self, request, **kwargs):
        project_id = self.kwargs['project_id']
        # Retrieve or create a group chat object for the project with the given ID
        chat, created = GroupChat.objects.get_or_create(project_id=project_id)
        
        # Create a new message
        message_content = request.POST.get('message_content')
        if message_content:
            Message.objects.create(group_chat=chat, sender=request.user, content=message_content)
        
        # Redirect back to the group chat page
        return redirect('group_chat', project_id=project_id)