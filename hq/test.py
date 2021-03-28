# from hq.views import Order
# class OrderView(View):
#     def get(self, request, *args, **kwargs):
#         menus = MenuItem.objects.all()
#         context = {
#                 'menus' : menus,
#             }
#         return render(request, 'hq/order.html', context)

# class OrderMakeView(CreateView):
#     model = Order
#     form_class = OrderForm
#     template_name = 'hq/order.html'

#     order_items = {
#             'items' : []
#         }
        
#     items = request.POST.getlist('items[]')

#     price = 0
#     item_ids =[]

#     for item in items:
#         menu_item = MenuItem.objects.get(pk__contains=int(item))
#         item_data = {
#             'id': menu_item.pk,
#             'name': menu_item.name,
#             'price': menu_item.price,
#         }
#         order_items['items'].append(item_data)

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     def get_success_url(self):
#         return reverse_lazy('orderConfirmation', kwargs={'pk': self.get_object(Order.objects.all().pk})

# class Order(View):
#     def get(self, request, *args, **kwargs):
#          view = OrderView.as_view()
#          return view(request, *args, **kwargs) 

#     def post(self, request, *args, **kwargs) :
#          view = OrderMakeView.as_view()
#          return view(request, *args, **kwargs)