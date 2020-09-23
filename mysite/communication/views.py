from django.shortcuts import render, get_object_or_404
from .models import Dialogue,Message
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .forms import SendMessageForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect

@method_decorator(login_required, name='dispatch')
class DialogueView(ListView):
    model = Dialogue
    template_name='communication/dialogue.html'
    paginate_by = 6

    def get_context_data(self,*args,**kwards):
        user =get_object_or_404(User, id=self.request.user.id)
        dialogue = user.dialogue.all()
        context=super(DialogueView,self).get_context_data(*args,**kwards)
        p = Paginator(dialogue, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='dialogue'
        return context

@method_decorator(login_required, name='dispatch')
class MessagesView(ListView):
    model = Message
    template_name='communication/messages.html'

    def post(self, request, *args, **kwargs):
        member = get_object_or_404(User,id=self.kwargs['pk'])
        user = get_object_or_404(User,id=self.request.user.id)
        dialog_list = (Dialogue.objects.prefetch_related('users').values('id').filter(users=user))
        dialog = Dialogue.objects.prefetch_related('users').filter(users=member,id__in = dialog_list)
        message_form = SendMessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.dialogue=dialog[0]
            new_message.author=user
            new_message.save()
            new_message.date_send = timezone.localtime(timezone.now())
            message_form = SendMessageForm()
            success_url=reverse_lazy('messages', kwargs={'pk':self.kwargs['pk']})
            return HttpResponseRedirect(success_url)

    def get_context_data(self,*args,**kwards):
        member = get_object_or_404(User,id=self.kwargs['pk'])
        user = get_object_or_404(User,id=self.request.user.id)
        dialog_list = (Dialogue.objects.prefetch_related('users').values('id').filter(users=user))
        dialog = Dialogue.objects.prefetch_related('users').filter(users=member,id__in = dialog_list)
        message_form = SendMessageForm()
        if dialog.exists():
            messages = dialog[0].messages.all()
        else:
            new_dialog=Dialogue()
            new_dialog.save()
            new_dialog.users.add(user, member)
            messages = new_dialog.messages.all()
        context=super(MessagesView,self).get_context_data(*args,**kwards)
        context['messages']=messages
        context['message_form']=message_form
        context['nbar']='dialogue'
        return context
