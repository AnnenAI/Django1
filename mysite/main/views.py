from django.shortcuts import render
from blog.models import Post
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator

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
