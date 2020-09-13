from django.shortcuts import render
from blog.models import Post, Category, User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import EditForm, AddForm
from django import http

class CategoryView(ListView):
    model=Category
    template_name="blog/show_category.html"

    def get_context_data(self,*args,**kwards):
        category=self.kwargs['category'].replace('-',' ')
        context=super(CategoryView,self).get_context_data(*args,**kwards)
        context = {
            'category':category.title,
            'post_list':Post.objects.filter(category__name__iexact=category),
        }
        return context

class CategoriesListView(ListView):
    model=Category
    template_name="blog/categories.html"
    #context_object_name = 'categories'

    def get_context_data(self,*args,**kwards):
        categories=Category.objects.all()
        context=super(CategoriesListView,self).get_context_data(*args,**kwards)
        context = {
            'categories':categories,
            'nbar':'categories',
        }
        return context
    #def get_queryset(self):
    #    categories=Category.objects.all()
    #    return categories

class PostListView(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 3
    #context_object_name = 'post_list'

    def get_context_data(self,*args,**kwards):
        user = self.kwargs['user_id']
        post_list=Post.objects.filter(author=user)
        context=super(PostListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='blog'
        context['author']=User.objects.get(pk=user)
        return context

#   #def get_queryset(self):
#        user = self.kwargs['user_id']
#        return list(Post.objects.filter(author=user))

class AddPostView(CreateView):
    model=Post
    form_class=AddForm
    template_name='blog/add_post.html'

    def get_context_data(self,*args,**kwards):
        context=super(AddPostView,self).get_context_data(*args,**kwards)
        context['nbar']='add_post'
        return context


class AddCategoryView(CreateView):
    model=Category
    fields='__all__'
    template_name='blog/add_category.html'

    def get_context_data(self,*args,**kwards):
        context=super(AddCategoryView,self).get_context_data(*args,**kwards)
        context['nbar']='add_category'
        return context

class UpdatePostView(UpdateView):
    model=Post
    form_class=EditForm
    template_name='blog/update_post.html'

class DeletePostView(DeleteView):
    model=Post
    template_name='blog/delete_post.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url=reverse_lazy('show_blog',kwargs={'user_id': request.user.id})
        self.object.delete()
        return http.HttpResponseRedirect(success_url)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    success_url=reverse_lazy('home')

    def get_queryset(self):
        slug_text = self.kwargs['slug']
        return Post.objects.filter(slug=slug_text)

class SearchListView(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 3
    #context_object_name = 'post_list'

    def get_context_data(self,*args,**kwards):
        user = self.kwargs['user_id']
        query = self.request.GET.get('q')
        if query:
            post_list = Post.objects.filter((Q(title__icontains=query)|Q(body__icontains=query))&Q(author=user)).distinct()
        else:
            post_list = Post.objects.filter(author=user)
        context=super(SearchListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='blog'
        context['author']=User.objects.get(pk=user)
        return context

#    def get_queryset(self):
#        query = self.request.GET.get('q')
#        if query:
#            return Post.objects.filter((Q(title__icontains=query)|Q(body__icontains=query))&Q(author=self.request.user)).distinct()
#        else:
#            return Post.objects.filter(author=self.request.user)

"""
def show_blog(request):
    template='blog/blog.html'
    posts=Post.objects.all()[:25]
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'post_list': post_list
    }
    return render(request,template,context)


def show_post(request,slug_text):
    template='blog/post.html'
    query=Post.objects.filter(slug=slug_text)
    if query.exists():
        query=query.first()
    else:
        return HttpResponse("<h1 align='center'>Page Not Found</h1>")
    context={
        'post':query
    }
    return render(request,template,context)

def search_post(request):
    template='blog/blog.html'
    query=request.GET.get('q')
    posts=[]
    posts.extend(Post.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)).distinct())
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'post_list': post_list
    }
    return render(request,template,context)
"""
