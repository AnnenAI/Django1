from django.shortcuts import render
from blog.models import Post, Category, User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from .forms import EditForm, AddForm, CategoryAddForm

class CategoryView(ListView):
    model=Post
    template_name="blog/show_category.html"
    paginate_by = 3

    def get_context_data(self,*args,**kwards):
        category=Category.objects.get(slug=self.kwargs['category'])
        post_list=Post.objects.filter(category__slug=category.slug)
        context=super(CategoryView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='categories'
        context['category']=category.name.title
        return context

class CategoriesListView(ListView):
    model=Category
    template_name="blog/categories.html"

    def get_context_data(self,*args,**kwards):
        categories=Category.objects.all()
        context=super(CategoriesListView,self).get_context_data(*args,**kwards)
        context['categories']=categories
        context['nbar']='categories'
        return context

class PostListView(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 3

    def get_context_data(self,*args,**kwards):
        user = self.kwargs['pk']
        post_list=Post.objects.filter(author=user)
        context=super(PostListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['page_obj']=p.page(context['page_obj'].number)
        context['nbar']='blog'
        context['author']=User.objects.get(pk=user)
        return context

class SearchListView(ListView):
    model=Post
    template_name = 'blog/blog.html'
    paginate_by = 3

    def get_context_data(self,*args,**kwards):
        user = self.kwargs['pk']
        query = self.request.GET.get('q')
        if query:
            post_list = Post.objects.filter((Q(title__icontains=query)|Q(body__icontains=query))&Q(author=user)).distinct()
        else:
            post_list = Post.objects.filter(author=user)
        context=super(SearchListView,self).get_context_data(*args,**kwards)
        p = Paginator(post_list, self.paginate_by)
        context['post']=p.page(context['page_obj'].number)
        context['nbar']='blog'
        context['author']=User.objects.get(pk=user),
        return context

def LikeView(request,slug):
    post=get_object_or_404(Post, slug=request.POST.get('post_slug'))
    user=request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return HttpResponseRedirect(reverse('show_post',args=[str(slug)]))

class AddPostView(CreateView):
    model=Post
    form_class=AddForm
    template_name='blog/add_post.html'

    def get_queryset(self):
        return 'add_post'

class AddCategoryView(CreateView):
    model=Category
    form_class=CategoryAddForm
    template_name='blog/add_category.html'
    context_object_name='nbar'

    def get_queryset(self):
        return 'add_category'

class UpdatePostView(UpdateView):
    model=Post
    form_class=EditForm
    template_name='blog/update_post.html'

class DeletePostView(DeleteView):
    model=Post
    template_name='blog/delete_post.html'

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(Post,slug=self.kwargs['slug'])
        success_url=reverse_lazy('show_blog',kwargs={'pk': request.user.id})
        object.delete()
        return HttpResponseRedirect(success_url)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self,*args,**kwards):
        context=super(PostDetailView,self).get_context_data(*args,**kwards)
        slug_text = self.kwargs['slug']
        stuff =get_object_or_404(Post, slug=slug_text)
        liked=False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['post']=Post.objects.filter(slug=slug_text)[0]
        context['total_likes']=stuff.total_likes()
        context['liked']=liked
        return context
