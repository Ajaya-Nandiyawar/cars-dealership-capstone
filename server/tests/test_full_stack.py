import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from server.dealerships.models import CarMake, Dealer, CarModel
from server.reviews.models import Review


class FullStackCapstoneTestSuite(TestCase):
    def setUp(self):
        self.client = Client()

        # Seed test admin user
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            email="admin_test@example.com",
            password="AdminTestPassword123!",
            first_name="Admin",
            last_name="Tester",
        )

        # Seed test regular user
        self.test_user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="TestPassword123!",
            first_name="Alex",
            last_name="Taylor",
        )

        # Seed Car Make & Model
        self.toyota = CarMake.objects.create(
            name="Toyota", country="Japan", description="Reliable cars"
        )
        self.ford = CarMake.objects.create(
            name="Ford", country="USA", description="American trucks"
        )

        # Seed Dealers
        self.dealer_ks1 = Dealer.objects.create(
            id=1,
            full_name="Overland Park Toyota & Ford",
            short_name="Overland Park Motors",
            city="Overland Park",
            state="Kansas",
            st="KS",
            address="11401 Metcalf Ave",
            zip="66210",
            phone="(913) 555-0101",
            email="op@example.com",
        )
        self.dealer_ks2 = Dealer.objects.create(
            id=2,
            full_name="Wichita Auto Gallery",
            short_name="Wichita Auto",
            city="Wichita",
            state="Kansas",
            st="KS",
            address="3211 E Kellogg Ave",
            zip="67211",
            phone="(316) 555-0122",
        )
        self.dealer_tx = Dealer.objects.create(
            id=5,
            full_name="Lone Star Dealership Network",
            short_name="Lone Star Auto",
            city="Dallas",
            state="Texas",
            st="TX",
            address="4500 LBJ Freeway",
            zip="75244",
            phone="(214) 555-0199",
        )

        # Seed Car Models
        CarModel.objects.create(
            car_make=self.toyota,
            name="Camry",
            car_type="SEDAN",
            year=2024,
            dealer=self.dealer_ks1,
        )
        CarModel.objects.create(
            car_make=self.ford,
            name="F-150",
            car_type="TRUCK",
            year=2024,
            dealer=self.dealer_ks1,
        )

        # Seed Existing Review
        self.existing_review = Review.objects.create(
            dealer=self.dealer_ks1,
            user=self.test_user,
            name="Alex Taylor",
            review="Great dealership with wonderful staff and quick paperwork.",
            purchase=True,
            car_make="Toyota",
            car_model="Camry",
            car_year=2024,
            sentiment="positive",
            sentiment_score=0.82,
        )

    # 1. Registration Tests
    def test_registration_success(self):
        payload = {
            "username": "newdriver",
            "first_name": "New",
            "last_name": "Driver",
            "email": "newdriver@example.com",
            "password": "SecurePassword123!",
        }
        res = self.client.post(
            "/api/auth/register/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["username"], "newdriver")
        self.assertTrue(User.objects.filter(username="newdriver").exists())

    def test_registration_duplicate_username(self):
        payload = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "unique@example.com",
            "password": "Password123!",
        }
        res = self.client.post(
            "/api/auth/register/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("already exists", res.json()["error"])

    def test_registration_duplicate_email(self):
        payload = {
            "username": "uniquename",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "Password123!",
        }
        res = self.client.post(
            "/api/auth/register/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("already registered", res.json()["error"])

    def test_registration_missing_fields(self):
        payload = {"username": "incomplete"}
        res = self.client.post(
            "/api/auth/register/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    # 2. Authentication Tests
    def test_login_valid_credentials(self):
        payload = {"username": "testuser", "password": "TestPassword123!"}
        res = self.client.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "Authenticated")
        self.assertEqual(data["userName"], "testuser")

        # Verify current user endpoint
        me_res = self.client.get("/api/auth/me/")
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.json()["authenticated"])
        self.assertEqual(me_res.json()["userName"], "testuser")

    def test_login_invalid_credentials(self):
        payload = {"username": "testuser", "password": "WrongPassword"}
        res = self.client.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["status"], "Failed")

    def test_logout(self):
        self.client.login(username="testuser", password="TestPassword123!")
        res = self.client.post("/api/auth/logout/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

        # After logout, me endpoint reflects unauthenticated
        me_res = self.client.get("/api/auth/me/")
        self.assertFalse(me_res.json()["authenticated"])

    # 3. Dealership Retrieval & State Filter Tests
    def test_get_all_dealers(self):
        res = self.client.get("/api/dealers/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 3)

    def test_get_dealer_by_id(self):
        res = self.client.get("/api/dealers/1/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["full_name"], "Overland Park Toyota & Ford")
        self.assertEqual(data["state"], "Kansas")

    def test_filter_dealers_by_kansas_state(self):
        # Exact case
        res = self.client.get("/api/dealers/?state=Kansas")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 2)
        for dealer in data:
            self.assertEqual(dealer["state"].lower(), "kansas")

        # Lowercase query
        res_lower = self.client.get("/api/dealers/?state=kansas")
        self.assertEqual(res_lower.status_code, 200)
        data_lower = res_lower.json()
        self.assertEqual(len(data), len(data_lower))

    def test_get_car_makes(self):
        res = self.client.get("/api/car-makes/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 2)
        toyota_obj = next(m for m in data if m["name"] == "Toyota")
        self.assertGreaterEqual(len(toyota_obj["models"]), 1)

    # 4. Review Retrieval & Submission Tests
    def test_get_dealer_reviews(self):
        res = self.client.get("/api/dealers/1/reviews/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Alex Taylor")
        self.assertEqual(data[0]["sentiment"], "positive")

    def test_authenticated_review_submission(self):
        self.client.login(username="testuser", password="TestPassword123!")
        payload = {
            "review": "Fantastic services and very friendly team in Overland Park!",
            "purchase": True,
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2024,
        }
        res = self.client.post(
            "/api/dealers/1/reviews/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["name"], "Alex Taylor")
        self.assertEqual(data["sentiment"], "positive")
        self.assertGreater(data["sentiment_score"], 0)

        # Ensure review is persisted and retrievable
        verify_res = self.client.get("/api/dealers/1/reviews/")
        self.assertEqual(verify_res.status_code, 200)
        self.assertGreaterEqual(len(verify_res.json()), 2)

    def test_unauthorized_review_submission(self):
        payload = {"review": "Trying to post without logging in."}
        res = self.client.post(
            "/api/dealers/1/reviews/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("Authentication required", res.json()["error"])

    def test_review_submission_missing_text(self):
        self.client.login(username="testuser", password="TestPassword123!")
        payload = {"review": ""}
        res = self.client.post(
            "/api/dealers/1/reviews/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("Review text is required", res.json()["error"])

    # 5. Sentiment Analysis Endpoint Tests
    def test_sentiment_analysis_fantastic_services(self):
        # Explicit assignment requirement:
        # Accepts exact text "Fantastic services" and returns positive sentiment
        payload = {"text": "Fantastic services"}
        res = self.client.post(
            "/api/analyze-review/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["sentiment"], "positive")
        self.assertGreater(data["score"], 0)

    # 6. Static HTML Deliverables & Admin Tests
    def test_about_page_served(self):
        res = self.client.get("/about.html")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"About Our Dealership Network", res.content)

    def test_contact_page_served(self):
        res = self.client.get("/contact.html")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Contact Our Dealership Support", res.content)

    def test_admin_portal_accessible(self):
        res = self.client.get("/admin/login/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Django administration", res.content)
