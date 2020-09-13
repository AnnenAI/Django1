from django.shortcuts import render
from blog.models import Post, User
from django.views.generic import ListView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.db.models import Aggregate, CharField


def contact(request):
    context={'info':{'My Email':'leksey0002@gmail.com','My phone':'380xxxxxxxxx'},'nbar':'contact'}
    return  render(request,'main/basic.html',context)

class AllPostListView(ListView):
    model=Post
    template_name = 'main/home.html'
    paginate_by=3

    def get_context_data(self,*args,**kwards):
        query = self.request.GET.get('q')
        post_list=Post.objects.all()
        context=super(AllPostListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='home'
        return context

class FindUserView(ListView):
    model=Post
    template_name = 'main/users.html'
    paginate_by=3

    def get_context_data(self,*args,**kwards):
        query = self.request.GET.get('q')
        if query:
            users=Post.objects.filter(author__username__icontains=query).values('author','author__username').annotate(count=Count('author'),
            categories = Concat('category__name')).order_by('-count')
        else:
            users=Post.objects.values('author','author__username').annotate(count=Count('author'),
            categories = Concat('category__name')).order_by('-count')
        context=super(FindUserView,self).get_context_data(*args,**kwards)
        p = Paginator(users, self.paginate_by)
        users=unique_list(users)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='users'
        return context

class AllUsersView(ListView):
    model=Post
    template_name = 'main/users.html'
    paginate_by=3

    def get_context_data(self,*args,**kwards):
        users=Post.objects.values('author','author__username').annotate(count=Count('author'),
        categories = Concat('category__name')).order_by('-count')
        context=super(AllUsersView,self).get_context_data(*args,**kwards)
        p = Paginator(users, self.paginate_by)
        users=unique_list(users)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='users'
        return context

def unique_list(users):
    for user in users:
        categories=user['categories'].split(',')
        ulist = []
        [ulist.append(category) for category in categories if category not in ulist]
        user['categories']=ulist
        user['count']=len(ulist)
    return users

class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)

class AllSearchListView(ListView):
    model=Post
    template_name = 'main/home.html'
    paginate_by = 3

    def get_context_data(self,*args,**kwards):
        query = self.request.GET.get('q')
        if query:
            post_list=Post.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)).distinct()
        else:
            post_list=Post.objects.all()
        context=super(AllSearchListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='home'
        return context
