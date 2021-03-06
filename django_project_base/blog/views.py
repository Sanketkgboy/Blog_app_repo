from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from . models import Post


# written alternative view for home function i.e class based PostListView 
# def home(request):
# 	context = {
# 		'posts': Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)


""" Note: Class based views do not replace the function based views, some times its better 
to use class based views if it satisfies our requirements"""  
class PostListView(ListView):
	# Model I wil be dealing with
	model = Post
	"""By default django will look for <app>/<model>_<viewtype>.html so we need to provide
	existing template name"""
	template_name = 'blog/home.html'
	# to loop over posts we need to do below step
	context_object_name = 'posts'
	#  To show the latest post on the top '-date_posted'
	ordering = ['-date_posted']
	# Number of posts per page
	paginate_by = 4


# imported get_object_or_404 and User model is used  in this class in get_query_set function
class UserPostListView(ListView):
	# Model I wil be dealing with
	model = Post
	template_name = 'blog/user_posts.html'
	# to loop over posts we need to do below step
	context_object_name = 'posts'
	# Number of posts per page
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post


""" We cannot use decorators on classes so we need Login Mixin thats just a class that we 
inherit from and that will add that login functionality to the view """
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content'] # Fields that I want to create
	
	""" This will be sharing a template with the PostUpdate view so the template name will no-
	t be 'post_create.html' rather it will be 'post_form.html' i.e 'model_form.html' Also 
	you need to overwrite the form_valid method to set the current user as the author of 
	the post """
	
	def form_valid(self, form):
		# before saving the form take the instance and set the author as current login user
		form.instance.author = self.request.user
		return super().form_valid(form)
		""" After this I am supposed to add an redirect or get absolute url method so th-
		at I can see the detail view after creating the Post, hence adding get absolute 
		url method in 'blog/models.py' and if I want to redirect to home page, I can set 
		success_url in this class only """ 


# UserPassesTestMixin will run test_func inorder to see if user passes certain condition
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content'] # Fields that I want to update

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	# If the user is author of the post then only he will be able to update the post
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	# success_url will reirect you after the post is deleted
	success_url = '/blog/home/'
	
	# If the user is author of the post then only he will be able to delete the post
	def test_func(self):
		post = self.get_object()

		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'blog/about.html', {'title':'About'})

