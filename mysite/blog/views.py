from django.shortcuts import render
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import EditForm, AddForm

class PostList(ListView):
    queryset = Post.objects.all()
    template_name = 'blog/blog.html'
    paginate_by = 6
    context_object_name = 'post_list'

class AddPostView(CreateView):
    model=Post
    form_class=AddForm
    template_name='blog/add_post.html'

class UpdatePostView(UpdateView):
    model=Post
    form_class=EditForm
    template_name='blog/update_post.html'
    #fields=['title','slug','body','date','picture']

class DeletePostView(DeleteView):
    model=Post
    template_name='blog/delete_post.html'
    success_url=reverse_lazy('show_blog')

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

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_queryset(self):
        self.slug_text = self.kwargs['slug']
        return self.model.objects.filter(slug=self.slug_text)

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

class SearchList(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 6
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(Q(title__icontains=query)|Q(body__icontains=query)).distinct()
        else:
            return self.model.objects.all()

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
