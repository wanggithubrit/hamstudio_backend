from django.apps import AppConfig
import sys

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Prevent seeding running during database migration commands
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            return

        try:
            from .models import Product, Collection, FaqItem, SiteSetting
            
            # 1. Seed Collections
            if Collection.objects.count() == 0:
                print("[SEEDER] Populating database Collections...")
                collections_data = [
                    {
                        "id": "necklaces",
                        "name": "Necklaces & Chokers",
                        "tag": "Architectural Pendants",
                        "image": "/media__1781974764102.jpg"
                    },
                    {
                        "id": "rings",
                        "name": "Heirloom Rings",
                        "tag": "Sterling Silver Bands",
                        "image": "/media__1781974705838.jpg"
                    },
                    {
                        "id": "bracelets",
                        "name": "Bracelets",
                        "tag": "Gothic Chains",
                        "image": "/media__1781974764104.jpg"
                    }
                ]
                for item in collections_data:
                    Collection.objects.create(
                        id=item["id"],
                        name=item["name"],
                        tag=item["tag"],
                        image_url=item["image"]
                    )

            # 2. Seed Products
            if Product.objects.count() == 0:
                print("[SEEDER] Populating database Products...")
                products_data = [
                    {
                        "id": "obsidian-cross",
                        "name": "Obsidian Cross Pendant",
                        "price": 3850,
                        "originalPrice": 4500,
                        "tag": "Best Seller",
                        "category": "Necklaces",
                        "gemstone": "Onyx",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764102.jpg",
                        "meta": "Silver / 18 inches",
                        "description": "A testament to timeless devotion and modern artistry. This curated pendant features high-clarity cubic zirconia and onyx accents set in an architectural cross design, suspended from a delicate snake chain.",
                        "images": [
                            "/media__1781974764102.jpg",
                            "/media__1781974705841.jpg",
                            "/media__1781974764103.jpg"
                        ]
                    },
                    {
                        "id": "iced-cuban-bracelet",
                        "name": "Iced Cuban Link Bracelet",
                        "price": 2450,
                        "tag": "New Drop",
                        "category": "Bracelets",
                        "gemstone": "Diamond",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764104.jpg",
                        "meta": "Silver / One Size",
                        "description": "A heavy-weight sterling silver Cuban chain, iced out with micropavé lab diamonds. Bold, gothic, and crafted to command the light in dark rooms.",
                        "images": [
                            "/media__1781974764104.jpg",
                            "/media__1781974705838.jpg"
                        ]
                    },
                    {
                        "id": "sapphire-crucifix",
                        "name": "Sapphire Heart Crucifix",
                        "price": 3200,
                        "tag": "Limited",
                        "category": "Necklaces",
                        "gemstone": "Sapphire",
                        "material": "Sterling Silver",
                        "image": "/media__1781974705839.jpg",
                        "meta": "Silver / 20 inches",
                        "description": "A deep navy sapphire glass heart centerpiece set in a gothic crucifix frame. Hand-polished to a mirror finish and details that reflect the night.",
                        "images": [
                            "/media__1781974705839.jpg",
                            "/media__1781974764108.jpg"
                        ]
                    },
                    {
                        "id": "emerald-crown-ring",
                        "name": "Emerald Crown Ring",
                        "price": 4150,
                        "tag": "",
                        "category": "Rings",
                        "gemstone": "Emerald",
                        "material": "18K Gold Plate",
                        "image": "/media__1781974705838.jpg",
                        "meta": "Gold / Size 7",
                        "description": "An intricate crown band set with lab-grown emerald baguettes. Reminiscent of medieval sovereignty and classic architectural vault arches.",
                        "images": [
                            "/media__1781974705838.jpg"
                        ]
                    },
                    {
                        "id": "ruby-gothic-cross",
                        "name": "Ruby Gothic Cross",
                        "price": 2150,
                        "tag": "Rare",
                        "category": "Necklaces",
                        "gemstone": "Ruby",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764103.jpg",
                        "meta": "Silver / 18 inches",
                        "description": "A sharp, geometric gothic cross pendant with a blood-red ruby center. Suspended on a blackened sterling steel chain.",
                        "images": [
                            "/media__1781974764103.jpg",
                            "/media__1781974705841.jpg"
                        ]
                    },
                    {
                        "id": "minimalist-silver-choker",
                        "name": "Minimalist Silver Choker",
                        "price": 950,
                        "tag": "",
                        "category": "Necklaces",
                        "gemstone": "None",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764108.jpg",
                        "meta": "Silver / One Size",
                        "description": "A simple, polished solid 925 sterling silver band that sits flush against the neck. Perfect for standalone elegance or layering.",
                        "images": [
                            "/media__1781974764108.jpg"
                        ]
                    },
                    {
                        "id": "diamond-eternity-band",
                        "name": "Diamond Eternity Band",
                        "price": 5500,
                        "tag": "",
                        "category": "Rings",
                        "gemstone": "Diamond",
                        "material": "Sterling Silver",
                        "image": "/media__1781974705838.jpg",
                        "meta": "Silver / Size 6",
                        "description": "A continuous loop of brilliant-cut cubic zirconia, tension-set in sterling silver. A symbol of unending strength and gothic architecture details.",
                        "images": [
                            "/media__1781974705838.jpg"
                        ]
                    },
                    {
                        "id": "rose-thorn-bracelet",
                        "name": "Rose Thorn Bracelet",
                        "price": 2200,
                        "tag": "",
                        "category": "Bracelets",
                        "gemstone": "None",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764104.jpg",
                        "meta": "Silver / One Size",
                        "description": "An organic wire-wrap bracelet designed to resemble wild rose branches, complete with hand-finished thorn spikes.",
                        "images": [
                            "/media__1781974764104.jpg"
                        ]
                    },
                    {
                        "id": "dice-8ball-keyring",
                        "name": "Dice & 8-Ball Keyring",
                        "price": 2600,
                        "tag": "",
                        "category": "Earrings",
                        "gemstone": "Onyx",
                        "material": "Sterling Silver",
                        "image": "/media__1781974764105.jpg",
                        "meta": "Silver / One Pair",
                        "description": "A bold, subculture-inspired keyring featuring a resin 8-ball, chrome metal dice, and an architectural star charm.",
                        "images": [
                            "/media__1781974764105.jpg"
                        ]
                    }
                ]
                for item in products_data:
                    Product.objects.create(
                        id=item["id"],
                        name=item["name"],
                        price=item["price"],
                        original_price=item.get("originalPrice"),
                        tag=item["tag"],
                        category=item["category"],
                        image_url=item["image"],
                        meta=item["meta"],
                        description=item["description"],
                        images=item["images"]
                    )

            # 3. Seed FAQs
            if FaqItem.objects.count() == 0:
                print("[SEEDER] Populating database FAQs...")
                faq_data = [
                    {
                        "id": "when-will-my-order-be-dispatched",
                        "question": "When will my order be dispatched?",
                        "answer": "In-stock items are shipped within 6-7 business days from the date of placing an order. For items that are out of stock and available only on preorder, estimated time to be taken for restock will be mentioned in the individual descriptions.",
                        "bullets": []
                    },
                    {
                        "id": "how-long-would-it-take-for-my-parcel-to-reach-me",
                        "question": "How long would it take for my parcel to reach me?",
                        "answer": "After orders are shipped, estimated time taken for parcels to get delivered is usually between 6-10 days depending on your location. This can be subjected to other factors that affect working days (i.e. national holidays, road blockades, etc.), in such cases your parcel would take longer to reach you.",
                        "bullets": []
                    },
                    {
                        "id": "tracking-status-says-it-is-delivered-to-addressee",
                        "question": "Tracking status says it's 'Delivered to addressee' but I haven't received it?",
                        "answer": "When this happens, please double check if you have any missed calls from the post office or if your parcel was left with a security guard, hostel warden or anyone else who could have accepted it in your stead. Otherwise, the post office will attempt delivery in the next 2-3 days from the time the status was updated on the website.",
                        "bullets": []
                    },
                    {
                        "id": "are-all-your-pieces-made-from-anti-tarnish-materials",
                        "question": "Are all your pieces made from anti tarnish materials ?",
                        "answer": "Anti-tarnish/stainless steel findings are rare and expensive in India hence we cannot transition entirely to anti tarnish accessories quickly since the prices of items would also increase in that case.\n\nBut we are gradually switching to anti tarnish findings.\n\nPlease refer to -Accessories care- to get more tips on making your accessories last longer.",
                        "bullets": []
                    },
                    {
                        "id": "will-you-ever-restock-sold-out-items",
                        "question": "Will you ever restock sold out items?",
                        "answer": "With the exception of a few limited edition pieces, we will try our best to restock on-demand sold out items. Preorder option will be provided in the website for items to be restocked.",
                        "bullets": []
                    },
                    {
                        "id": "my-parcel-arrived-damaged-or-lost",
                        "question": "My parcel arrived damaged/is lost in transit. Can I get a refund?",
                        "answer": "Unboxing videos are mandatory for all claims. Refunding is against our store policy, we cannot offer refunds but we will compensate for your loss with discount coupons in cases where parcels have been lost in transit or items reach you severely damaged.",
                        "bullets": []
                    },
                    {
                        "id": "can-i-cancel-or-return-my-order",
                        "question": "Can I cancel/return my order?",
                        "answer": "All orders placed are final and cannot be cancelled once placed.\n\nWe operate as an exclusive online catalog, hence order cancellations or returns are generally not supported unless items reach you damaged. We suggest you to always make your purchases carefully to avoid such situations.",
                        "bullets": []
                    },
                    {
                        "id": "incomplete-or-wrong-address",
                        "question": "I accidentally typed in an incomplete/wrong address while placing my order. What to do now?",
                        "answer": "Please immediately contact us on our Instagram page if this happens. Once your order is shipped to the wrong/incomplete address, there is nothing we can do about it.",
                        "bullets": []
                    }
                ]
                for item in faq_data:
                    FaqItem.objects.create(
                        id=item["id"],
                        question=item["question"],
                        answer=item["answer"],
                        bullets=item["bullets"]
                    )

            # 4. Seed SiteSettings
            if SiteSetting.objects.filter(key="home_hero_bg").count() == 0:
                print("[SEEDER] Populating database SiteSettings...")
                settings_data = [
                    {
                        "key": "home_hero_bg",
                        "value": "/media__1781974764102.jpg",
                        "description": "Background image for the Home page hero section"
                    },
                    {
                        "key": "about_hero_bg",
                        "value": "/media__1781974764103.jpg",
                        "description": "Background image for the About page hero section"
                    },
                    {
                        "key": "about_story_img",
                        "value": "/media__1781974764108.jpg",
                        "description": "Image shown in the About page story section"
                    },
                    {
                        "key": "social_img_1",
                        "value": "/media__1781974764103.jpg",
                        "description": "As Seen on You - Social feed image 1"
                    },
                    {
                        "key": "social_img_2",
                        "value": "/media__1781974705838.jpg",
                        "description": "As Seen on You - Social feed image 2"
                    },
                    {
                        "key": "social_img_3",
                        "value": "/media__1781974705839.jpg",
                        "description": "As Seen on You - Social feed image 3"
                    },
                    {
                        "key": "policy_terms",
                        "value": "Welcome to HAM STUDIO. By using our website and purchasing our curated sterling silver jewelry, you agree to comply with and be bound by the following terms and conditions. Please read them carefully before making a purchase.\n\n1. Product Accuracy\nEach piece in our catalog is individually finished. Minor variations in texture, color, and size are characteristics of the finishing process and should not be considered defects.\n\n2. Order Acceptance\nAll orders placed through our website are subject to acceptance and availability. We reserve the right to refuse or cancel any order for any reason, including inaccuracies in product details or pricing.\n\n3. Pricing & Payments\nAll prices are displayed in Indian Rupees (₹). Payments must be made using our accepted online payment methods at checkout.",
                        "description": "Terms & Conditions policy text"
                    },
                    {
                        "key": "policy_privacy",
                        "value": "HAM STUDIO is committed to protecting your privacy. This Privacy Policy details how we collect, use, and secure your personal information when you interact with our online storefront.\n\n1. Personal Information Collection\nWe collect information you provide directly to us, such as your name, delivery address, email, phone number, and transaction details during checkout.\n\n2. Information Usage\nWe use the collected information to process and fulfill your orders, communicate transaction updates, and handle support requests.\n\n3. Third-Party Sharing\nYour personal data is shared with shipping and delivery partners to ensure secure transit of your package. We do not sell or lease your personal information.",
                        "description": "Privacy Policy policy text"
                    },
                    {
                        "key": "policy_shipping",
                        "value": "At HAM STUDIO, we ensure that your delicate jewelry pieces reach you securely and in perfect condition.\n\n1. Shipping Locations\nWe operate exclusively within Indian domestic borders. We do not ship internationally.\n\n2. Delivery Timelines\nIn-stock items are dispatched within 6-7 business days. Delivery typically takes 6-10 business days after dispatch depending on your city and pincode.\n\n3. Shipping Charges\nStandard domestic shipping is complimentary for all catalog purchases across India.",
                        "description": "Shipping Policy policy text"
                    },
                    {
                        "key": "policy_refund",
                        "value": "Please read our refund and exchange policy carefully prior to placing your order.\n\n1. No Refunds\nDue to the exclusive nature of our sterling silver jewelry pieces, all sales are final. Refunding is against store policy and we cannot offer direct cash refunds.\n\n2. Damaged or Lost Parcels\nIn the rare event that your parcel is lost in transit or items arrive damaged, we will compensate for your loss with discount coupons or shop credits. Unboxing videos are mandatory for all damage claims.",
                        "description": "Refund Policy policy text"
                    },
                    {
                        "key": "policy_cookie",
                        "value": "This Cookie Policy explains how HAM STUDIO uses cookies and similar tracking technologies to enhance your browsing experience.\n\n1. What are Cookies?\nCookies are small text files stored on your browser or device to remember information about your visit, such as your preferred page tab or cart state.\n\n2. How We Use Cookies\nWe use essential cookies to persist your active shopping cart items, preserve your logged-in administrator session, and verify page view animation states.",
                        "description": "Cookie Policy policy text"
                    }
                ]
                for item in settings_data:
                    SiteSetting.objects.create(
                        key=item["key"],
                        value=item["value"],
                        description=item["description"]
                    )
        except Exception as e:
            # Table doesn't exist yet or migrations have not run
            pass
