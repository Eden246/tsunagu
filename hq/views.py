from django.views.generic.detail import DetailView
from users.models import CustomUser
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.views import View
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import *
from .forms import *
from django.urls.base import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json

class PostSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        if query:
            posts = Post.objects.filter(
                Q(author__username__icontains=query) |
                Q(title__icontains=query) |
                Q(category__name__icontains=query) |
                Q(body__icontains=query)
            )
        else:
            posts = Post.objects.all()

        context = {
            'posts': posts
        }

        return render(request, 'hq/post.html', context)

class CategoryView(View):
    def get(self,request, category_str, *args, **kwargs):
        posts = Post.objects.filter(category=category_str)
        context = {
            'posts': posts,
            'category_str': category_str,
        }
        return render(request, 'hq/category.html',context)
    
class ProfileView(View):
    def get(self,request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        posts = Post.objects.filter(author=user).order_by('-created_at')
        books = Book.objects.filter(name=user).order_by('-date')
        context ={
            'user': user,
            'posts': posts,
            'books': books,
        }
        return render(request,'hq/profile.html', context)

class ProfileEditView(UpdateView):
    model = CustomUser
    fields = ['username', 'phone']
    template_name = 'hq/profileEdit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class PostView(View):
    def get(self,request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        context ={
            'posts': posts,
        }
        
        return render(request,'hq/post.html', context)

class PostAddView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'hq/postAdd.html'
    success_url = reverse_lazy('post')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostUpdateView(UpdateView):
        model = Post
        form_class = PostForm
        template_name = 'hq/postUpdate.html'

        def get_success_url(self):
            return reverse('postDetail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'hq/postDelete.html'
    success_url = reverse_lazy('post')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'hq/bookDelete.html'
    success_url = reverse_lazy('post')

class PostDetailView(LoginRequiredMixin, View):
    def get(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        category = Category.objects.all()
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('created_at')
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'category': category,
        }
        return render(request, 'hq/postDetail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        category = Category.objects.all()
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('created_at')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'category': category,
        }

        return render(request, 'hq/postDetail.html', context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'hq/commentDelete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('postDetail', kwargs={'pk':pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class BookView(CreateView):
    model = Book
    form_class = BookForm1
    template_name = 'hq/book.html'
    success_url = reverse_lazy('post')

class BookDetailView(View):
    def get(self,request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        books = Book.objects.filter(name=user).order_by('-date')
        context ={
            'books': books,
        }
        
        return render(request,'hq/bookDetail.html', context)

class StaffBookDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = BookSearchForm()
        books = Book.objects.all()
        context = {
            'books': books,
            "form":form,
        }
        
        return render(request, 'hq/staffBookDetail.html', context)

    def post(self, request, *args, **kwargs):
        form = BookSearchForm(request.POST)
        books = Book.objects.filter(name__username__icontains=form['name'].value(), email__icontains=form['email'].value(), date__icontains=form['date'].value(),facility__icontains=form['facility'].value())
        context = {
        "form":form,
        "books":books,
        }
        return render(request, "hq/staffBookDetail.html", context)

class SearchView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'hq/staffBookAdd.html'
    success_url = reverse_lazy('staffBookDetail')

class CustomUserAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CustomUser.objects.none()

        qs = CustomUser.objects.all()

        if self.q:
            qs = qs.filter(username__istartswith=self.q)

        return qs

class HomeView(ListView):
    model = Item
    template_name = 'hq/home-page.html'


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'hq/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "注文がございません。")
            return redirect('/')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'hq/product-page.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "カートに追加されました。")
            return redirect("order-summary")
        else:
            messages.info(request, "カートに入りました。")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
            ordered_date = ordered_date,
        )
        order.items.add(order_item)
        messages.info(request, "ご注文承りました！")
        return redirect("order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0].delete()
            messages.info(request, "カートから削除されました。")
            return redirect("product", slug=slug)
        else:
            messages.info(request, "カートに該当する商品がございません。")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "注文がございません。")
        return redirect("product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "品目が更新されました。")
            return redirect("order-summary")
        else:
            messages.info(request, "カートに該当する商品がございません。")
            return redirect("order-summary")
    else:
        messages.info(request, "注文がございません。")
        return redirect("order-summary")

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
                'form': form,
                'order': order,
            }
        return render(self.request, "hq/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            if form.is_valid():
                street_adress = form.cleaned_data('street_adress')
                apartment_address = form.cleaned_data('apartment_address')
                zip = form.cleaned_data('zip')
                # same_billing_address = form.cleaned_data('same_billing_address')
                # save_info = form.cleaned_data('save_info')
                payment_option = form.cleaned_data('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_adress=street_adress,
                    apartment_address=apartment_address,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('checkout')
            messages.warning(self.request, "決済失敗")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "注文がございません。")
            return redirect('checkout')

class PaymentComplete(View):
    def get(self, request, *args, **kwargs):
        body = json.loads(request.body)
        product = Order.objects.get(id=body['productId'])
        Compelete.objects.create(
            product=product
        )
        return render(self.request, "hq/payment.html")