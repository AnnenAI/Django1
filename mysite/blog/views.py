from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
import json
from .models import Post, Category, User,Comment
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import EditForm, AddForm, CategoryAddForm
from django.utils import timezone
from .mixins import RightToEditMixin

class CategoryView(ListView):
    model=Post
    template_name="blog/show_category.html"
    paginate_by = 3

    def get_context_data(self,*args,**kwards):
        category=get_object_or_404(Category, slug=self.kwargs['category'])
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
"""
def LikeView(request,slug):
    post=get_object_or_404(Post, slug=request.POST.get('post_slug'))
    user=request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return HttpResponseRedirect(reverse('show_post',args=[str(slug)]))
"""

@login_required
def LikeView(request):
    slug=request.POST.get('slug')
    post=get_object_or_404(Post, slug=slug)
    user=request.user
    context={}
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        context['liked']=False
    else:
        post.likes.add(user)
        context['liked'] = True
    if request.is_ajax():
        context['total_likes']=post.total_likes()
        return JsonResponse(context,status=200)
    return HttpResponseRedirect(reverse('show_post',args=[str(slug)]))

@method_decorator(login_required, name='dispatch')
class AddPostView(CreateView):
    model=Post
    form_class=AddForm
    template_name='blog/add_post.html'

    def get_queryset(self):
        return 'add_post'

@method_decorator(login_required, name='dispatch')
class AddCategoryView(CreateView):
    model=Category
    form_class=CategoryAddForm
    template_name='blog/add_category.html'
    context_object_name='nbar'

    def get_queryset(self):
        return 'add_category'

class UpdatePostView(RightToEditMixin,UpdateView):
    model=Post
    form_class=EditForm
    template_name='blog/update_post.html'

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.update_date=timezone.localtime(timezone.now())
        self.object.save()
        return super().form_valid(form)

class DeletePostView(RightToEditMixin,DeleteView):
    model=Post
    template_name='blog/delete_post.html'

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(Post,slug=self.kwargs['slug'])
        success_url=reverse_lazy('show_blog',kwargs={'pk': request.user.id})
        object.delete()
        return HttpResponseRedirect(success_url)


def PostDetailView(request,slug):
    model = Post
    template_name = 'blog/post.html'
    post =get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        new_comment =Comment()
        new_comment.name=request.POST.get('name')
        new_comment.body=request.POST.get('body')
        new_comment.post = post
        new_comment.save()
        comments = post.comments.all()
        if request.is_ajax():
            data = render_to_string('blog/comment_section.html', {'comments': comments})
            return JsonResponse(data, safe=False)
        success_url=reverse_lazy('show_post',kwargs={'slug': slug})
        return HttpResponseRedirect(success_url)
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        liked=True
    comments = list(post.comments.all().values('name','body','date_added'))
    context={
        'comments': comments,
        'post':post,
        'total_likes':post.total_likes(),
        'liked':liked,
    }
    return render(request,template_name,context)

"""class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self,*args,**kwards):
        slug_text = self.kwargs['slug']
        post =get_object_or_404(Post, slug=slug_text)
        comments = post.comments.all()
        context=super(PostDetailView,self).get_context_data(*args,**kwards)
        liked=False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['post']=post
        context['total_likes']=post.total_likes()
        context['liked']=liked
        return context"""
