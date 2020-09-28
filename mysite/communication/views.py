from django.shortcuts import render, get_object_or_404
from .custom_decorators import check_yourself_dialogue
from .models import Dialogue, Message, Users
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import SendMessageForm
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect

@method_decorator(login_required, name='dispatch')
class DialogueView(ListView):
    model = Dialogue
    template_name='communication/dialogue.html'
    paginate_by = 6

    def get_context_data(self,*args,**kwards):
        user = get_object_or_404(User, id=self.request.user.id)
        dialogue = Users.objects.select_related('member','dialogue').values(
            'member_id','member__first_name','member__last_name','dialogue__last_message_date').filter(user=user.id)
        print(dialogue)
        context=super(DialogueView,self).get_context_data(*args,**kwards)
        p = Paginator(dialogue, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='dialogue'
        return context

@method_decorator(check_yourself_dialogue, name='dispatch')
@method_decorator(login_required, name='dispatch')
class MessagesView(ListView):
    model = Message
    template_name='communication/messages.html'

    def post(self, request, *args, **kwargs):
        member = get_object_or_404(User,id=self.kwargs['pk'])
        user = get_object_or_404(User,id=self.request.user.id)
        dialogue = Dialogue.objects.filter(users__user=user.id, users__member=member.id)[0]
        #dialog_list = (Dialogue.objects.prefetch_related('users').values('id').filter(users=user))
        #dialog = Dialogue.objects.prefetch_related('users').filter(users=member,id__in = dialog_list)
        message_form = SendMessageForm(data=request.POST)
        if message_form.is_valid():
            dialogue.last_message_date=timezone.now()
            dialogue.save()
            new_message = message_form.save(commit=False)
            new_message.dialogue=dialogue
            new_message.author=user
            new_message.date_sending=timezone.now()
            new_message.save()

            message_form = SendMessageForm()
            success_url=reverse_lazy('messages', kwargs={'pk':self.kwargs['pk']})
            return HttpResponseRedirect(success_url)

    def get_context_data(self,*args,**kwards):
        member = get_object_or_404(User,id=self.kwargs['pk'])
        user = get_object_or_404(User,id=self.request.user.id)
        dialogue = Dialogue.objects.filter(users__user=user.id, users__member=member.id)
        #dialog_list = (Dialogue.objects.prefetch_related('users').values('id').filter(users=user))
        #dialog = Dialogue.objects.prefetch_related('users').filter(users=member,id__in = dialog_list)
        message_form = SendMessageForm()
        if dialogue.exists():
            messages = dialogue[0].messages.all()
        else:
            new_dialog=Dialogue()
            new_dialog.save()
            usrs=Users(user=user, member=member,dialogue=new_dialog)
            usrs.save()
            usrs = Users(user=member, member=user, dialogue=new_dialog)
            usrs.save()
            messages = []
        context=super(MessagesView,self).get_context_data(*args,**kwards)
        context['messages'] = messages
        context['member'] = member
        context['message_form']=message_form
        context['nbar']='dialogue'
        return context
