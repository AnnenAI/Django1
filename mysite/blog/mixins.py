from django.shortcuts import get_object_or_404
from blog.models import Post
from django.http import HttpResponse

class RightToEditMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        post=get_object_or_404(Post,slug=slug)
        if not (post.author.id == request.user.id):
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="application/json", status=403)
        else:
            return super().dispatch(request, *args, **kwargs)
