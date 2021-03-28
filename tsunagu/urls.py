from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hq.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path(
        r'customuser-autocomplete/',
        CustomUserAutoComplete.as_view(create_field='username'),
        name='customuser-autocomplete'
    ),
    path('', PostView.as_view(), name='post'),
    path('add/', PostAddView.as_view(), name='postAdd'),
    path('book/', BookView.as_view(), name='book'),
    path('bookdetail/<int:pk>/', BookDetailView.as_view(), name='bookDetail'),
    path('staffbookdetail/', StaffBookDetailView.as_view(), name='staffBookDetail'),
    path('usersearch/', SearchView.as_view(), name='usersearch'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='postUpdate'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='postDelete'),
    path('bookdelete/<int:pk>/', BookDeleteView.as_view(), name='bookDelete'),
    path('map/', TemplateView.as_view(template_name="hq/map.html"), name='map'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='postDetail'),
    path('search/', PostSearch.as_view(), name='PostSearch'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profileEdit'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='commentDelete'),
# order
    path('menu/', HomeView.as_view(), name='menu'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-form-cart'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout-page/', CheckoutView.as_view(), name='checkout-page'),
    path('complete/', PaymentComplete.as_view(), name='complete')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
