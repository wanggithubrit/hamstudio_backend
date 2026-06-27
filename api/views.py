import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Product, Collection, FaqItem, Order, ContactMessage, SiteSetting

# Helper to serialize products
def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "originalPrice": product.original_price,
        "tag": product.tag,
        "category": product.category,
        "image": product.get_image_url(),
        "meta": product.meta,
        "description": product.description,
        "images": product.images
    }

# ----------------------------------------------------
# GET API ENDPOINTS
# ----------------------------------------------------

@require_http_methods(["GET"])
def get_products(request):
    products = Product.objects.all()
    data = [serialize_product(p) for p in products]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def get_collections(request):
    collections = Collection.objects.all()
    data = [{
        "id": c.id,
        "name": c.name,
        "tag": c.tag,
        "image": c.get_image_url()
    } for c in collections]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def get_faqs(request):
    faqs = FaqItem.objects.all()
    data = [{
        "id": f.id,
        "question": f.question,
        "answer": f.answer,
        "bullets": f.bullets
    } for f in faqs]
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def get_settings(request):
    settings = SiteSetting.objects.all()
    data = {s.key: s.get_value() for s in settings}
    return JsonResponse(data)

# ----------------------------------------------------
# POST API ENDPOINTS (CSRF exempt for standalone development)
# ----------------------------------------------------

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        body = json.loads(request.body)
        items = body.get("items")
        shipping = body.get("shipping")

        if not items or not isinstance(items, list) or len(items) == 0:
            return JsonResponse({"error": "Order must contain items"}, status=400)

        if not shipping or not shipping.get("firstName") or not shipping.get("lastName") or not shipping.get("email") or not shipping.get("phone"):
            return JsonResponse({"error": "Missing shipping details"}, status=400)

        random_num = random.randint(10000, 99999)
        order_id = f"HAM-{random_num}"

        Order.objects.create(
            orderId=order_id,
            items=items,
            shipping=shipping
        )

        print(f"[API] Order placed: {order_id}")
        return JsonResponse({"success": True, "orderId": order_id})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
def order_history(request):
    try:
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        
        # Load all orders and filter by email case-insensitively for database safety
        orders = list(Order.objects.all())
        matched_orders = []
        for o in orders:
            try:
                if o.shipping and o.shipping.get("email", "").strip().lower() == email.strip().lower():
                    matched_orders.append(o)
            except Exception:
                pass
                
        # Sort by date descending
        matched_orders.sort(key=lambda x: x.date, reverse=True)
        
        data = [{
            "orderId": o.orderId,
            "date": o.date.strftime("%Y-%m-%d %H:%M:%S") if o.date else "",
            "status": o.status,
            "items": o.items,
            "shipping": o.shipping
        } for o in matched_orders]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_contact(request):
    try:
        body = json.loads(request.body)
        name = body.get("name")
        email = body.get("email")
        subject = body.get("subject", "General Query")
        message = body.get("message")

        if not name or not email or not message:
            return JsonResponse({"error": "Name, email, and message are required"}, status=400)

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        print(f"[API] Contact message received from {email}")
        return JsonResponse({"success": True})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# ----------------------------------------------------
# ADMIN DASHBOARD API ENDPOINTS
# ----------------------------------------------------
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")
        
        user = authenticate(username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            return JsonResponse({
                "success": True, 
                "username": user.username,
                "is_staff": user.is_staff
            })
        else:
            # Convenience auto-bootstrap for development environment
            if not User.objects.filter(is_superuser=True).exists():
                admin_user = User.objects.create_superuser(username=username, password=password, email="admin@hamstudio.com")
                login(request, admin_user)
                return JsonResponse({
                    "success": True, 
                    "username": admin_user.username,
                    "is_staff": True
                })
            return JsonResponse({"success": False, "error": "Invalid admin credentials"}, status=401)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def admin_logout(request):
    logout(request)
    return JsonResponse({"success": True})

@require_http_methods(["GET"])
def admin_stats(request):
    try:
        orders = Order.objects.all()
        total_sales = 0
        for o in orders:
            items = o.items
            if isinstance(items, list):
                for item in items:
                    try:
                        price = float(item.get('price', 0))
                        qty = float(item.get('quantity', 1))
                        total_sales += price * qty
                    except Exception:
                        pass
        
        # Calculate last 7 days chart data
        sales_history = []
        today = timezone.now().date()
        for i in range(6, -1, -1):
            day = today - datetime.timedelta(days=i)
            day_orders = Order.objects.filter(date__date=day)
            day_sales = 0
            for o in day_orders:
                items = o.items
                if isinstance(items, list):
                    for item in items:
                        try:
                            price = float(item.get('price', 0))
                            qty = float(item.get('quantity', 1))
                            day_sales += price * qty
                        except Exception:
                            pass
            sales_history.append({
                "date": day.strftime("%b %d"),
                "sales": int(day_sales),
                "orders": day_orders.count()
            })

        return JsonResponse({
            "total_sales": int(total_sales),
            "total_orders": orders.count(),
            "total_products": Product.objects.count(),
            "total_messages": ContactMessage.objects.count(),
            "sales_history": sales_history
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_products(request):
    if request.method == "GET":
        products = Product.objects.all()
        data = [serialize_product(p) for p in products]
        return JsonResponse(data, safe=False)
        
    elif request.method == "POST":
        try:
            name = request.POST.get("name")
            price = request.POST.get("price")
            category = request.POST.get("category", "")
            
            if not name or not price:
                return JsonResponse({"error": "Name and Price are required"}, status=400)
                
            prod_id = request.POST.get("id")
            if not prod_id:
                prod_id = name.lower().strip().replace(" ", "-")
                # Ensure unique ID
                count = 1
                base_id = prod_id
                while Product.objects.filter(id=prod_id).exists():
                    prod_id = f"{base_id}-{count}"
                    count += 1
            
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            import uuid

            # Save additional gallery images
            gallery_urls = []
            gallery_files = request.FILES.getlist("images_files")
            for gf in gallery_files:
                ext = os.path.splitext(gf.name)[1]
                unique_name = f"products/{uuid.uuid4()}{ext}"
                path = default_storage.save(unique_name, ContentFile(gf.read()))
                url = default_storage.url(path)
                gallery_urls.append(url)

            orig_price = request.POST.get("originalPrice")
            product = Product.objects.create(
                id=prod_id,
                name=name,
                price=int(price),
                original_price=int(orig_price) if orig_price else None,
                category=category,
                tag=request.POST.get("tag", ""),
                description=request.POST.get("description", ""),
                meta=request.POST.get("meta", ""),
                image=request.FILES.get("image"),
                images=gallery_urls
            )
            return JsonResponse({"success": True, "product": serialize_product(product)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def admin_product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
        
    if request.method == "DELETE":
        product.delete()
        return JsonResponse({"success": True})
        
    elif request.method == "POST":
        try:
            product.name = request.POST.get("name", product.name)
            product.price = int(request.POST.get("price", product.price))
            orig_price = request.POST.get("originalPrice")
            product.original_price = int(orig_price) if orig_price else None
            product.category = request.POST.get("category", product.category)
            product.tag = request.POST.get("tag", product.tag)
            product.description = request.POST.get("description", product.description)
            product.meta = request.POST.get("meta", product.meta)
            
            if request.FILES.get("image"):
                product.image = request.FILES.get("image")
                
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            import uuid

            # Parse remaining existing images
            existing_images_raw = request.POST.get("existing_images")
            if existing_images_raw is not None:
                try:
                    product.images = json.loads(existing_images_raw)
                except Exception:
                    product.images = []

            # Upload and append new gallery images
            gallery_files = request.FILES.getlist("images_files")
            if not isinstance(product.images, list):
                product.images = []
                
            for gf in gallery_files:
                ext = os.path.splitext(gf.name)[1]
                unique_name = f"products/{uuid.uuid4()}{ext}"
                path = default_storage.save(unique_name, ContentFile(gf.read()))
                url = default_storage.url(path)
                product.images.append(url)
                
            product.save()
            return JsonResponse({"success": True, "product": serialize_product(product)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_collections(request):
    if request.method == "GET":
        collections = Collection.objects.all()
        data = [{
            "id": c.id,
            "name": c.name,
            "tag": c.tag,
            "image": c.get_image_url()
        } for c in collections]
        return JsonResponse(data, safe=False)
        
    elif request.method == "POST":
        try:
            name = request.POST.get("name")
            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)
                
            coll_id = request.POST.get("id")
            if not coll_id:
                coll_id = name.lower().strip().replace(" ", "-")
                count = 1
                base_id = coll_id
                while Collection.objects.filter(id=coll_id).exists():
                    coll_id = f"{base_id}-{count}"
                    count += 1
                    
            collection = Collection.objects.create(
                id=coll_id,
                name=name,
                tag=request.POST.get("tag", ""),
                image=request.FILES.get("image")
            )
            return JsonResponse({"success": True, "collection": {
                "id": collection.id,
                "name": collection.name,
                "tag": collection.tag,
                "image": collection.get_image_url()
            }})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def admin_collection_detail(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        return JsonResponse({"error": "Collection not found"}, status=404)
        
    if request.method == "DELETE":
        collection.delete()
        return JsonResponse({"success": True})
        
    elif request.method == "POST":
        try:
            collection.name = request.POST.get("name", collection.name)
            collection.tag = request.POST.get("tag", collection.tag)
            
            if request.FILES.get("image"):
                collection.image = request.FILES.get("image")
                
            collection.save()
            return JsonResponse({"success": True, "collection": {
                "id": collection.id,
                "name": collection.name,
                "tag": collection.tag,
                "image": collection.get_image_url()
            }})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_orders(request):
    if request.method == "GET":
        orders = Order.objects.all().order_by("-date")
        data = [{
            "id": o.id,
            "orderId": o.orderId,
            "items": o.items,
            "shipping": o.shipping,
            "date": o.date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": o.status
        } for o in orders]
        return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def admin_order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
        
    if request.method == "DELETE":
        order.delete()
        return JsonResponse({"success": True})
        
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            order.status = body.get("status", order.status)
            order.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def admin_messages(request):
    messages = ContactMessage.objects.all().order_by("-timestamp")
    data = [{
        "id": m.id,
        "name": m.name,
        "email": m.email,
        "subject": m.subject,
        "message": m.message,
        "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for m in messages]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["DELETE"])
def admin_message_detail(request, msg_id):
    try:
        msg = ContactMessage.objects.get(id=msg_id)
        msg.delete()
        return JsonResponse({"success": True})
    except ContactMessage.DoesNotExist:
        return JsonResponse({"error": "Message not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_settings(request):
    if request.method == "GET":
        settings = SiteSetting.objects.all()
        data = [{
            "key": s.key,
            "value": s.value,
            "image": s.image.url if s.image else None,
            "description": s.description
        } for s in settings]
        return JsonResponse(data, safe=False)
        
    elif request.method == "POST":
        try:
            key = request.POST.get("key")
            value = request.POST.get("value", "")
            
            setting, created = SiteSetting.objects.get_or_create(key=key)
            setting.value = value
            setting.description = request.POST.get("description", setting.description)
            
            if request.FILES.get("image"):
                setting.image = request.FILES.get("image")
                
            setting.save()
            return JsonResponse({"success": True, "setting": {
                "key": setting.key,
                "value": setting.value,
                "image": setting.image.url if setting.image else None,
                "description": setting.description
            }})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_faqs(request):
    if request.method == "GET":
        faqs = FaqItem.objects.all()
        data = [{
            "id": f.id,
            "question": f.question,
            "answer": f.answer,
            "bullets": f.bullets
        } for f in faqs]
        return JsonResponse(data, safe=False)
        
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            question = body.get("question")
            answer = body.get("answer")
            bullets = body.get("bullets", [])
            
            if not question or not answer:
                return JsonResponse({"error": "Question and Answer are required"}, status=400)
                
            faq_id = body.get("id")
            if not faq_id:
                faq_id = question.lower().strip().replace(" ", "-")[:50]
                count = 1
                base_id = faq_id
                while FaqItem.objects.filter(id=faq_id).exists():
                    faq_id = f"{base_id}-{count}"
                    count += 1
                    
            faq = FaqItem.objects.create(
                id=faq_id,
                question=question,
                answer=answer,
                bullets=bullets if isinstance(bullets, list) else []
            )
            return JsonResponse({"success": True, "faq": {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer,
                "bullets": faq.bullets
            }})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def admin_faq_detail(request, faq_id):
    try:
        faq = FaqItem.objects.get(id=faq_id)
    except FaqItem.DoesNotExist:
        return JsonResponse({"error": "FAQ not found"}, status=404)
        
    if request.method == "DELETE":
        faq.delete()
        return JsonResponse({"success": True})
        
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            faq.question = body.get("question", faq.question)
            faq.answer = body.get("answer", faq.answer)
            faq.bullets = body.get("bullets", faq.bullets)
            faq.save()
            return JsonResponse({"success": True, "faq": {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer,
                "bullets": faq.bullets
            }})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
