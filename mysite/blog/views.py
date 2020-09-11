from django.shortcuts import render
from blog.models import Post, Category
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import EditForm, AddForm

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
    context_object_name = 'categories'

    def get_queryset(self):
        categories=Category.objects.all()
        return categories

class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'blog/blog.html'
    paginate_by = 5
    context_object_name = 'post_list'

    def get_context_data(self,*args,**kwards):
        categories=Category.objects.all()
        context=super(PostListView,self).get_context_data(*args,**kwards)
        context["categories"]=categories
        return context

class AddPostView(CreateView):
    model=Post
    form_class=AddForm
    template_name='blog/add_post.html'

class AddCategoryView(CreateView):
    model=Category
    fields='__all__'
    template_name='blog/add_category.html'

class UpdatePostView(UpdateView):
    model=Post
    form_class=EditForm
    template_name='blog/update_post.html'


class DeletePostView(DeleteView):
    model=Post
    template_name='blog/delete_post.html'
    success_url=reverse_lazy('show_blog')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_queryset(self):
        self.slug_text = self.kwargs['slug']
        return Post.objects.filter(slug=self.slug_text)

class SearchListView(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 5
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)).distinct()
        else:
            return Post.objects.all()

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
