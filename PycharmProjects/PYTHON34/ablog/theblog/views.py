from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect  , Http404

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))  # post_id - название кнопки
    liked = False
    if post.likes .filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    cats = Category.objects.all()
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk']) # получаем id поста
        total_likes = stuff.total_likes()
        liked = False
        a = Post.objects.get(id=self.kwargs['pk'])
        # a.comment_set.create(author_name=self.POST['name'], comment_text=self.kwargs['text'])
        latest_comment_list = a.comment_set.order_by('-id')
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked # context['liked'] - это для html
        context['latest_comment_list'] = latest_comment_list
        context['article'] = a
        return context

    def leave_comment(request, pk):
        if request.method == 'POST':
            try:
                a = Post.objects.get(id=pk)
            except:
                raise Http404('Статья не найдена')
    
            a.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

        return HttpResponseRedirect(reverse('article_detail', args=(a.id, )))

def PopularView(request):
    model = Post
    popular_list = Post.objects.order_by('-likes')
    a = []
    for i in popular_list[:5]:
        if i not in a:
            a.append(i)
    first = a[0]
    second = a[1]
    fird = a[2]
    return render(request, 'list_popular.html', {'popular_list': a, 'first': first, 'second': second, 'fird': fird})

class AddPostView(CreateView):
    model = Post # wow
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__'


class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')  # перемещение после удаления


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def CategoryView(request, cats):
    category_post = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_post': category_post})

def new_list(request):
    articles_new_list = Post.objects.order_by('-id')[:10]
    a = [i for i in articles_new_list]
    return render(request, 'new_list.html', {'new_list': a})

