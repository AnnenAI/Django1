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
            full_name = query.split(' ')
            if(len(full_name)==2):
                firstname=full_name[0]
                lastname=full_name[1]
                users = Post.objects.filter((Q(author__first_name__icontains=firstname)&
                Q(author__last_name__icontains=lastname))|(Q(author__first_name__icontains=lastname)&
                Q(author__last_name__icontains=firstname))).values('author','author__first_name','author__last_name').annotate(count=Count('author'),
                categories = Concat('category__name'),categories_slug = Concat('category__slug')).order_by('-count')
            else:
                firstname=full_name[0]
                users = Post.objects.filter(Q(author__first_name__icontains=firstname)|
                Q(author__last_name__icontains=firstname)).values('author','author__first_name','author__last_name').annotate(count=Count('author'),
                categories = Concat('category__name'),categories_slug = Concat('category__slug')).order_by('-count')
        else:
            users=Post.objects.values('author','author__first_name','author__last_name').annotate(count=Count('author'),categories = Concat('category__name'),
            categories_slug = Concat('category__slug')).order_by('-count')
        context=super(FindUserView,self).get_context_data(*args,**kwards)
        users=get_dict_category(users)
        p = Paginator(users, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='home'
        return context

class AllUsersView(ListView):
    model=Post
    template_name = 'main/users.html'
    paginate_by=3

    def get_context_data(self,*args,**kwards):
        users=Post.objects.values('author','author__first_name','author__last_name').annotate(count=Count('author'),categories = Concat('category__name'),
        categories_slug = Concat('category__slug')).order_by('-count')
        context=super(AllUsersView,self).get_context_data(*args,**kwards)
        users=get_dict_category(users)
        p = Paginator(users, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='home'
        return context

def get_dict_category(users):
    for user in users:
        categories=user['categories'].split(',')
        categories_slug=user['categories_slug'].split(',')
        name_list = []
        [name_list.append(category) for category in categories if category not in name_list]
        slug_list = []
        [slug_list.append(category) for category in categories_slug if category not in slug_list]
        dict = {name_list[i]: slug_list[i] for i in range(len(name_list))}
        user['categories']=dict
        user.pop('categories_slug', None)
        user['count']=len(dict)
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
