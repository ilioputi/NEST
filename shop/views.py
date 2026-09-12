from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Product, CartItem


def catalog(request):
    """Каталог товаров — отдаёт hime.html с футером и модалкой описания."""
    products = Product.objects.all()
    return render(request, "hime.html", {"products": products})


def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


@require_http_methods(["POST"])
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity_str = request.POST.get('quantity', '1')

    try:
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except ValueError:
        return JsonResponse({'error': 'invalid quantity'}, status=400)

    if not product_id:
        return JsonResponse({'error': 'product_id required'}, status=400)

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, _ = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 0}
        )
        cart_item.quantity += quantity
        cart_item.save()
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        cart_item, _ = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': 0}
        )
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({
        'status': 'ok',
        'product_name': product.name,
        'quantity': cart_item.quantity,
        'total': str(cart_item.total),
    })


@require_http_methods(["POST"])
def remove_from_cart(request):
    item_id = request.POST.get('item_id')

    if not item_id:
        return JsonResponse({'error': 'item_id required'}, status=400)

    try:
        item = CartItem.objects.get(id=item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'item not found'}, status=404)

    if request.user.is_authenticated:
        if item.user != request.user:
            return JsonResponse({'error': 'not authorized'}, status=403)
    else:
        session_key = request.session.session_key or ''
        if item.session_key != session_key:
            return JsonResponse({'error': 'not authorized'}, status=403)

    item.delete()
    return JsonResponse({'status': 'ok'})


def get_cart(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key or ''
        items = CartItem.objects.filter(session_key=session_key)

    cart_data = []
    total = 0
    for item in items:
        item_total = item.product.price * item.quantity
        total += item_total
        cart_data.append({
            'id': item.id,
            'name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity,
            'total': str(item_total),
            'image_url': getattr(item.product, 'image_url', '') or '',
        })

    return JsonResponse({
        'items': cart_data,
        'total': str(total),
    })