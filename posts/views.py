from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

def get_posts(request):
    """
    Create a view that will return a list of
    Posts that were published prior to 'now'
    and render them to the 'blogposts.html' template
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", {'posts': posts})
    
def post_detail(request, pk):
    """
    Create a view that returns a single Post
    object based on the Post id (pk) and render
    it to the 'postdetail.html' template. Or, 
    return a 404 error if the Post is not found
    """
    post = get_object_or_404(Post, pk=pk)  # Get post item based on post id
    post.views += 1  # Increment views of post by +1 
    post.save()
    return render(request, "postdetail.html", {'post': post})
    
def create_or_edit_post(request, pk=None):
    """
    Create a view that allows us to create or
    edit a Post depending if the Post id is null
    or not
    """
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":  # User to post a blog
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()  # Full and valid blog is saved
            return redirect(post_detail, post.pk) 
        else:
            form = BlogPostForm(instance=post)
            # If blog not valid then user returns back to original list 
            # of blog posts
        return render(request, "blogposts.html", {'form': form})
        
    

