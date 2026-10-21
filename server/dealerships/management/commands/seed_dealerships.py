import os
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from server.dealerships.models import CarMake, Dealer, CarModel
from server.reviews.models import Review
from server.sentiment.services import analyze_text_sentiment


class Command(BaseCommand):
    help = "Seed database with realistic dealerships, car makes, models, reviews, and test users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding..."))

        # 1. Create or update Admin User
        admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@dealerships.example.com")
        admin_pass = os.getenv("DJANGO_SUPERUSER_PASSWORD", "AdminSecurePassword123!")

        admin_user, created = User.objects.get_or_create(username=admin_username)
        admin_user.email = admin_email
        admin_user.first_name = "Super"
        admin_user.last_name = "Admin"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password(admin_pass)
        admin_user.save()
        status_str = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Administrator account '{admin_username}' {status_str}."))

        # 2. Create or update regular test user
        test_user, created = User.objects.get_or_create(username="testuser")
        test_user.email = "testuser@dealerships.example.com"
        test_user.first_name = "Alex"
        test_user.last_name = "Taylor"
        test_user.is_staff = False
        test_user.is_superuser = False
        test_user.set_password("TestUserPassword123!")
        test_user.save()
        self.stdout.write(self.style.SUCCESS("Demo test user 'testuser' configured."))

        # 3. Seed Car Makes
        makes_data = [
            {"name": "Toyota", "country": "Japan", "description": "Global leader in reliable, high-efficiency vehicles and hybrids."},
            {"name": "Ford", "country": "USA", "description": "Iconic American automaker renowned for trucks, SUVs, and performance cars."},
            {"name": "Honda", "country": "Japan", "description": "Engineered for durability, modern safety, and exceptional fuel economy."},
            {"name": "Chevrolet", "country": "USA", "description": "Dependable American trucks, versatile crossovers, and electric models."},
            {"name": "Tesla", "country": "USA", "description": "Pioneering premium electric vehicles with cutting-edge autonomous technology."},
            {"name": "BMW", "country": "Germany", "description": "The ultimate driving machine delivering luxury, style, and sport performance."},
            {"name": "Audi", "country": "Germany", "description": "Progressive luxury vehicles known for Quattro all-wheel drive and sleek digital cockpits."},
            {"name": "Hyundai", "country": "South Korea", "description": "Award-winning design, long warranties, and innovative electric platforms."},
        ]

        makes_map = {}
        for item in makes_data:
            make_obj, _ = CarMake.objects.update_or_create(
                name=item["name"],
                defaults={
                    "country": item["country"],
                    "description": item["description"],
                },
            )
            makes_map[item["name"]] = make_obj
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(makes_map)} car makes."))

        # 4. Seed Dealerships (including multiple in Kansas)
        dealers_data = [
            {
                "id": 1,
                "full_name": "Overland Park Toyota & Ford",
                "short_name": "Overland Park Motors",
                "city": "Overland Park",
                "state": "Kansas",
                "st": "KS",
                "address": "11401 Metcalf Ave",
                "zip": "66210",
                "lat": 38.9213,
                "long": -94.6672,
                "phone": "(913) 555-0101",
                "email": "contact@opmotors-kansas.com",
                "website": "https://opmotors-kansas.com",
                "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 2,
                "full_name": "Wichita Auto Gallery",
                "short_name": "Wichita Auto",
                "city": "Wichita",
                "state": "Kansas",
                "st": "KS",
                "address": "3211 E Kellogg Ave",
                "zip": "67211",
                "lat": 37.6833,
                "long": -97.3001,
                "phone": "(316) 555-0122",
                "email": "sales@wichita-autogallery.com",
                "website": "https://wichita-autogallery.com",
                "image": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 3,
                "full_name": "Topeka Premier Motors",
                "short_name": "Topeka Premier",
                "city": "Topeka",
                "state": "Kansas",
                "st": "KS",
                "address": "2901 SW Wanamaker Rd",
                "zip": "66614",
                "lat": 39.0234,
                "long": -95.7482,
                "phone": "(785) 555-0144",
                "email": "info@topekapremier.com",
                "website": "https://topekapremier.com",
                "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 4,
                "full_name": "Kansas City Metro Auto",
                "short_name": "KC Metro Auto",
                "city": "Kansas City",
                "state": "Kansas",
                "st": "KS",
                "address": "7800 State Ave",
                "zip": "66112",
                "lat": 39.1172,
                "long": -94.7554,
                "phone": "(913) 555-0188",
                "email": "care@kcmetroauto.com",
                "website": "https://kcmetroauto.com",
                "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 5,
                "full_name": "Lone Star Dealership Network",
                "short_name": "Lone Star Auto",
                "city": "Dallas",
                "state": "Texas",
                "st": "TX",
                "address": "4500 LBJ Freeway",
                "zip": "75244",
                "lat": 32.9234,
                "long": -96.8341,
                "phone": "(214) 555-0199",
                "email": "contact@lonestarauto-tx.com",
                "website": "https://lonestarauto-tx.com",
                "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 6,
                "full_name": "Austin Precision Automotive",
                "short_name": "Austin Precision",
                "city": "Austin",
                "state": "Texas",
                "st": "TX",
                "address": "8101 N MoPac Expy",
                "zip": "78759",
                "lat": 30.3644,
                "long": -97.7428,
                "phone": "(512) 555-0133",
                "email": "sales@austinprecision.com",
                "website": "https://austinprecision.com",
                "image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 7,
                "full_name": "Golden Gate Auto Mall",
                "short_name": "Golden Gate Auto",
                "city": "San Francisco",
                "state": "California",
                "st": "CA",
                "address": "1550 Van Ness Ave",
                "zip": "94109",
                "lat": 37.7915,
                "long": -122.4223,
                "phone": "(415) 555-0155",
                "email": "info@goldengatecars.com",
                "website": "https://goldengatecars.com",
                "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 8,
                "full_name": "SoCal Luxury Cars",
                "short_name": "SoCal Luxury",
                "city": "Los Angeles",
                "state": "California",
                "st": "CA",
                "address": "9000 Wilshire Blvd",
                "zip": "90211",
                "lat": 34.0667,
                "long": -118.3888,
                "phone": "(310) 555-0177",
                "email": "concierge@socalluxury.com",
                "website": "https://socalluxury.com",
                "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 9,
                "full_name": "Manhattan City Dealership",
                "short_name": "Manhattan City",
                "city": "New York",
                "state": "New York",
                "st": "NY",
                "address": "787 11th Ave",
                "zip": "10019",
                "lat": 40.7689,
                "long": -73.9933,
                "phone": "(212) 555-0166",
                "email": "sales@manhattancitydealers.com",
                "website": "https://manhattancitydealers.com",
                "image": "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 10,
                "full_name": "Sunshine State Automotive",
                "short_name": "Sunshine State Auto",
                "city": "Miami",
                "state": "Florida",
                "st": "FL",
                "address": "3401 Biscayne Blvd",
                "zip": "33137",
                "lat": 25.8089,
                "long": -80.1895,
                "phone": "(305) 555-0111",
                "email": "drive@sunshinestateauto.com",
                "website": "https://sunshinestateauto.com",
                "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 11,
                "full_name": "Windy City Car Hub",
                "short_name": "Windy City Hub",
                "city": "Chicago",
                "state": "Illinois",
                "st": "IL",
                "address": "2500 N Western Ave",
                "zip": "60647",
                "lat": 41.9272,
                "long": -87.6873,
                "phone": "(312) 555-0149",
                "email": "help@windycitycarhub.com",
                "website": "https://windycitycarhub.com",
                "image": "https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 12,
                "full_name": "Emerald City Motors",
                "short_name": "Emerald City",
                "city": "Seattle",
                "state": "Washington",
                "st": "WA",
                "address": "1133 4th Ave S",
                "zip": "98134",
                "lat": 47.5925,
                "long": -122.3291,
                "phone": "(206) 555-0125",
                "email": "sales@emeraldcitymotors.com",
                "website": "https://emeraldcitymotors.com",
                "image": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 13,
                "full_name": "Mile High Automotive Group",
                "short_name": "Mile High Auto",
                "city": "Denver",
                "state": "Colorado",
                "st": "CO",
                "address": "1200 S Colorado Blvd",
                "zip": "80246",
                "lat": 39.6943,
                "long": -104.9405,
                "phone": "(303) 555-0182",
                "email": "contact@milehighautogroup.com",
                "website": "https://milehighautogroup.com",
                "image": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": 14,
                "full_name": "Great Plains Auto Center",
                "short_name": "Great Plains Auto",
                "city": "Lawrence",
                "state": "Kansas",
                "st": "KS",
                "address": "2233 W 23rd St",
                "zip": "66046",
                "lat": 38.9392,
                "long": -95.2612,
                "phone": "(785) 555-0191",
                "email": "service@greatplainsautocenter.com",
                "website": "https://greatplainsautocenter.com",
                "image": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80",
            },
        ]

        dealers_map = {}
        for d in dealers_data:
            dealer_obj, _ = Dealer.objects.update_or_create(
                id=d["id"],
                defaults={
                    "full_name": d["full_name"],
                    "short_name": d["short_name"],
                    "city": d["city"],
                    "state": d["state"],
                    "st": d["st"],
                    "address": d["address"],
                    "zip": d["zip"],
                    "lat": d["lat"],
                    "long": d["long"],
                    "phone": d["phone"],
                    "email": d["email"],
                    "website": d["website"],
                    "image": d["image"],
                },
            )
            dealers_map[d["id"]] = dealer_obj
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(dealers_map)} dealerships across multiple US states."))

        # 5. Seed Car Models associated with Car Makes and Dealers
        models_data = [
            # Toyota
            {"make": "Toyota", "name": "Camry", "type": "SEDAN", "year": 2024, "dealer_id": 1},
            {"make": "Toyota", "name": "RAV4", "type": "SUV", "year": 2024, "dealer_id": 1},
            {"make": "Toyota", "name": "Corolla", "type": "SEDAN", "year": 2023, "dealer_id": 2},
            {"make": "Toyota", "name": "Highlander", "type": "SUV", "year": 2024, "dealer_id": 3},
            {"make": "Toyota", "name": "Tacoma", "type": "TRUCK", "year": 2024, "dealer_id": 4},
            # Ford
            {"make": "Ford", "name": "F-150", "type": "TRUCK", "year": 2024, "dealer_id": 1},
            {"make": "Ford", "name": "Mustang", "type": "COUPE", "year": 2024, "dealer_id": 5},
            {"make": "Ford", "name": "Explorer", "type": "SUV", "year": 2023, "dealer_id": 6},
            {"make": "Ford", "name": "Escape", "type": "SUV", "year": 2024, "dealer_id": 14},
            # Honda
            {"make": "Honda", "name": "Civic", "type": "SEDAN", "year": 2024, "dealer_id": 2},
            {"make": "Honda", "name": "CR-V", "type": "SUV", "year": 2024, "dealer_id": 2},
            {"make": "Honda", "name": "Accord", "type": "SEDAN", "year": 2023, "dealer_id": 7},
            # Chevrolet
            {"make": "Chevrolet", "name": "Silverado", "type": "TRUCK", "year": 2024, "dealer_id": 5},
            {"make": "Chevrolet", "name": "Equinox", "type": "SUV", "year": 2024, "dealer_id": 6},
            {"make": "Chevrolet", "name": "Tahoe", "type": "SUV", "year": 2023, "dealer_id": 11},
            # Tesla
            {"make": "Tesla", "name": "Model 3", "type": "SEDAN", "year": 2024, "dealer_id": 7},
            {"make": "Tesla", "name": "Model Y", "type": "SUV", "year": 2024, "dealer_id": 8},
            {"make": "Tesla", "name": "Cybertruck", "type": "TRUCK", "year": 2024, "dealer_id": 8},
            # BMW
            {"make": "BMW", "name": "3 Series", "type": "SEDAN", "year": 2024, "dealer_id": 8},
            {"make": "BMW", "name": "X5", "type": "SUV", "year": 2024, "dealer_id": 9},
            {"make": "BMW", "name": "M4", "type": "COUPE", "year": 2024, "dealer_id": 9},
            # Audi
            {"make": "Audi", "name": "A4", "type": "SEDAN", "year": 2024, "dealer_id": 9},
            {"make": "Audi", "name": "Q5", "type": "SUV", "year": 2023, "dealer_id": 10},
            {"make": "Audi", "name": "e-tron GT", "type": "ELECTRIC", "year": 2024, "dealer_id": 10},
            # Hyundai
            {"make": "Hyundai", "name": "Ioniq 5", "type": "ELECTRIC", "year": 2024, "dealer_id": 12},
            {"make": "Hyundai", "name": "Tucson", "type": "SUV", "year": 2024, "dealer_id": 13},
        ]

        created_models = 0
        for m in models_data:
            make_obj = makes_map.get(m["make"])
            if make_obj:
                dealer_obj = dealers_map.get(m["dealer_id"])
                CarModel.objects.update_or_create(
                    car_make=make_obj,
                    name=m["name"],
                    year=m["year"],
                    defaults={
                        "car_type": m["type"],
                        "dealer": dealer_obj,
                    },
                )
                created_models += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created_models} car models."))

        # 6. Seed Reviews (with sentiment scores)
        reviews_data = [
            {
                "dealer_id": 1,
                "name": "Jordan Smith",
                "review": "Fantastic services! The sales team was knowledgeable and helped me pick the perfect Camry.",
                "purchase": True,
                "purchase_date": date(2024, 2, 14),
                "car_make": "Toyota",
                "car_model": "Camry",
                "car_year": 2024,
            },
            {
                "dealer_id": 1,
                "name": "Sarah Jenkins",
                "review": "Great experience purchasing my F-150. Transparent financing and very friendly staff.",
                "purchase": True,
                "purchase_date": date(2024, 1, 20),
                "car_make": "Ford",
                "car_model": "F-150",
                "car_year": 2024,
            },
            {
                "dealer_id": 1,
                "name": "Michael Chang",
                "review": "Average customer experience. The paperwork took longer than expected but the car is good.",
                "purchase": True,
                "purchase_date": date(2023, 11, 10),
                "car_make": "Toyota",
                "car_model": "RAV4",
                "car_year": 2024,
            },
            {
                "dealer_id": 2,
                "name": "Emily Watson",
                "review": "Exceptional customer support! The trade-in value on my old sedan was very generous.",
                "purchase": True,
                "purchase_date": date(2024, 3, 5),
                "car_make": "Honda",
                "car_model": "Civic",
                "car_year": 2024,
            },
            {
                "dealer_id": 2,
                "name": "David Miller",
                "review": "Test drive was smooth and the facility was very clean. Highly recommended Wichita dealer.",
                "purchase": False,
                "purchase_date": None,
                "car_make": "Honda",
                "car_model": "CR-V",
                "car_year": 2024,
            },
            {
                "dealer_id": 3,
                "name": "Amanda Lopez",
                "review": "Wonderful buying process from start to finish. The team answered all my questions patiently.",
                "purchase": True,
                "purchase_date": date(2024, 2, 28),
                "car_make": "Toyota",
                "car_model": "Highlander",
                "car_year": 2024,
            },
            {
                "dealer_id": 5,
                "name": "Robert Gonzalez",
                "review": "Huge inventory and top-notch customer service in Dallas. Love my new Silverado!",
                "purchase": True,
                "purchase_date": date(2024, 3, 12),
                "car_make": "Chevrolet",
                "car_model": "Silverado",
                "car_year": 2024,
            },
            {
                "dealer_id": 7,
                "name": "Elena Rostova",
                "review": "Seamless electric vehicle purchase. They set up the charging app and explained everything clearly.",
                "purchase": True,
                "purchase_date": date(2024, 1, 18),
                "car_make": "Tesla",
                "car_model": "Model 3",
                "car_year": 2024,
            },
        ]

        seeded_reviews = 0
        for r in reviews_data:
            dealer_obj = dealers_map.get(r["dealer_id"])
            if dealer_obj:
                sentiment_info = analyze_text_sentiment(r["review"])
                Review.objects.update_or_create(
                    dealer=dealer_obj,
                    name=r["name"],
                    defaults={
                        "user": test_user,
                        "review": r["review"],
                        "purchase": r["purchase"],
                        "purchase_date": r["purchase_date"],
                        "car_make": r["car_make"],
                        "car_model": r["car_model"],
                        "car_year": r["car_year"],
                        "sentiment": sentiment_info["sentiment"],
                        "sentiment_score": sentiment_info["score"],
                    },
                )
                seeded_reviews += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {seeded_reviews} customer reviews with sentiment analysis."))

        self.stdout.write(self.style.SUCCESS("All seed data successfully applied and verified!"))
