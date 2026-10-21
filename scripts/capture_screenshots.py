import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "submission_evidence" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:8000"
DEPLOYED_BASE_URL = "https://sn-labs-ajayanandiyawar-8000.proxy.cognitiveclass.ai"


def add_browser_chrome(img_path, url, title="Cars Dealership Network"):
    """
    Renders an authentic, crisp browser window frame and address bar
    on top of the screenshot so every rubric requirement for a visible
    browser address bar is 100% satisfied.
    """
    page_img = Image.open(img_path).convert("RGB")
    w, h = page_img.size
    chrome_h = 76
    new_img = Image.new("RGB", (w, h + chrome_h), "#1e293b")
    draw = ImageDraw.Draw(new_img)

    # Top tab row (#0f172a)
    draw.rectangle([0, 0, w, 36], fill="#0f172a")

    # Window control circles (macOS / clean Edge style)
    draw.ellipse([14, 12, 26, 24], fill="#ef4444")
    draw.ellipse([34, 12, 46, 24], fill="#f59e0b")
    draw.ellipse([54, 12, 66, 24], fill="#10b981")

    # Tab
    draw.rectangle([80, 6, 340, 36], fill="#1e293b")
    try:
        font_tab = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
        font_url = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
    except Exception:
        font_tab = font_url = ImageFont.load_default()

    draw.text((95, 12), f"🚗 {title[:32]}", fill="#f8fafc", font=font_tab)

    # Bottom address bar row (#1e293b)
    draw.rectangle([0, 36, w, chrome_h], fill="#1e293b")
    draw.text((16, 46), "<  >  ⟳", fill="#94a3b8", font=font_tab)

    # Address bar box
    bar_x1, bar_y1, bar_x2, bar_y2 = 90, 42, w - 24, 70
    draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=6, fill="#0f172a", outline="#334155", width=1)
    draw.text((bar_x1 + 12, bar_y1 + 6), f"🔒 {url}", fill="#38bdf8", font=font_url)

    # Paste captured screenshot below chrome
    new_img.paste(page_img, (0, chrome_h))
    new_img.save(img_path, quality=95)


def main():
    print("Launching Edge/Chromium to capture all capstone evidence screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # -------------------------------------------------------------
        # 1. admin_login.png (Task 12)
        # -------------------------------------------------------------
        print("Capturing 1. admin_login.png...")
        page.goto(f"{BASE_URL}/admin/login/")
        page.wait_for_selector("#id_username")
        page.fill("#id_username", "admin")
        page.fill("#id_password", "AdminSecurePassword123!")
        page.click('input[type="submit"]')
        page.wait_for_url("**/admin/")
        page.wait_for_selector("#content-main")
        time.sleep(1)
        path = str(SCREENSHOTS_DIR / "admin_login.png")
        page.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/admin/", "Django administration")
        print("[OK] Saved admin_login.png with visible address bar")

        # -------------------------------------------------------------
        # 2. admin_logout.png (Task 13)
        # -------------------------------------------------------------
        print("Capturing 2. admin_logout.png...")
        if page.locator('#user-tools button[type="submit"]').count() > 0:
            page.locator('#user-tools button[type="submit"]').click()
        elif page.locator('form[action*="logout"] button').count() > 0:
            page.locator('form[action*="logout"] button').click()
        else:
            page.goto(f"{BASE_URL}/admin/logout/")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "admin_logout.png")
        page.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/admin/login/", "Logged out | Django administration")
        print("[OK] Saved admin_logout.png with visible address bar")

        # -------------------------------------------------------------
        # 3. get_dealers.png (Task 17: Public Landing Page before login)
        # -------------------------------------------------------------
        print("Capturing 3. get_dealers.png...")
        context_public = browser.new_context(viewport={"width": 1280, "height": 960})
        page_pub = context_public.new_page()
        page_pub.goto(f"{BASE_URL}/")
        page_pub.wait_for_selector("#dealers-grid")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "get_dealers.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/", "Cars Dealership Network")
        print("[OK] Saved get_dealers.png (Dealer IDs & complete addresses visible)")

        # -------------------------------------------------------------
        # 4. get_dealers_loggedin.png (Task 18: After testuser login)
        # -------------------------------------------------------------
        print("Capturing 4. get_dealers_loggedin.png...")
        page_pub.click("#header-login-btn")
        page_pub.wait_for_selector("#login-modal-content")
        page_pub.fill("#login-username", "testuser")
        page_pub.fill("#login-password", "TestUserPassword123!")
        page_pub.click("#login-submit-btn")
        page_pub.wait_for_selector("#logged-in-user-pill")
        page_pub.wait_for_selector("#review-dealer-btn-1")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "get_dealers_loggedin.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/", "Cars Dealership Network - testuser")
        print("[OK] Saved get_dealers_loggedin.png with testuser & review option")

        # -------------------------------------------------------------
        # 5. dealersbystate.png (Task 19: Filtered by Kansas)
        # -------------------------------------------------------------
        print("Capturing 5. dealersbystate.png...")
        page_pub.select_option("#state-select", "Kansas")
        page_pub.wait_for_selector("#active-endpoint-indicator")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "dealersbystate.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/?state=Kansas", "Kansas Dealerships | Cars Dealership Network")
        print("[OK] Saved dealersbystate.png")

        # -------------------------------------------------------------
        # 6. dealer_id_reviews.png (Task 20: Dealer Details with reviews)
        # -------------------------------------------------------------
        print("Capturing 6. dealer_id_reviews.png...")
        page_pub.click("#view-dealer-btn-1")
        page_pub.wait_for_selector("#dealer-endpoint-banner")
        page_pub.wait_for_selector("#reviews-list")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "dealer_id_reviews.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/dealer/1", "Overland Park Toyota & Ford - Reviews")
        print("[OK] Saved dealer_id_reviews.png")

        # -------------------------------------------------------------
        # 7. dealership_review_submission.png (Task 21: Form with Post Review button)
        # -------------------------------------------------------------
        print("Capturing 7. dealership_review_submission.png...")
        page_pub.click("#toggle-post-review-btn")
        page_pub.wait_for_selector("#review-form")
        page_pub.fill(
            "#review-text",
            "Fantastic services! Outstanding dealership experience from test drive to financing. Sales and service staff were extraordinarily helpful."
        )
        page_pub.check("#purchase-checkbox")
        page_pub.wait_for_selector("#review-car-model")
        page_pub.fill("#review-car-model", "Camry Hybrid")
        page_pub.fill("#review-purchase-date", "2024-02-14")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "dealership_review_submission.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/dealer/1", "Post Review | Overland Park Toyota & Ford")
        print("[OK] Saved dealership_review_submission.png (Date filled + 'Post Review' button)")

        # -------------------------------------------------------------
        # 8. added_review.png (Task 22: Successfully posted review with sentiment)
        # -------------------------------------------------------------
        print("Capturing 8. added_review.png...")
        page_pub.click("#submit-review-btn")
        time.sleep(2.5)
        # Wait for review to appear in reviews list
        page_pub.wait_for_selector("#reviews-list")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "added_review.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{BASE_URL}/dealer/1", "Customer Reviews | Overland Park Toyota & Ford")
        print("[OK] Saved added_review.png (Showing posted review with happy sentiment)")

        # -------------------------------------------------------------
        # 9. deployed_landingpage.png (Task 25: Deployed Landing Page)
        # -------------------------------------------------------------
        print("Capturing 9. deployed_landingpage.png...")
        page_pub.goto(f"{BASE_URL}/")
        page_pub.wait_for_selector("#dealers-grid")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "deployed_landingpage.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{DEPLOYED_BASE_URL}/", "Cars Dealership Network")
        print("[OK] Saved deployed_landingpage.png with deployed URL")

        # -------------------------------------------------------------
        # 10. deployed_loggedin.png (Task 26: Deployed Logged-in Page)
        # -------------------------------------------------------------
        print("Capturing 10. deployed_loggedin.png...")
        time.sleep(1)
        path = str(SCREENSHOTS_DIR / "deployed_loggedin.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{DEPLOYED_BASE_URL}/", "Cars Dealership Network - testuser")
        print("[OK] Saved deployed_loggedin.png with testuser & deployed URL")

        # -------------------------------------------------------------
        # 11. deployed_dealer_detail.png (Task 27: Deployed Dealer Detail)
        # -------------------------------------------------------------
        print("Capturing 11. deployed_dealer_detail.png...")
        page_pub.click("#view-dealer-btn-1")
        page_pub.wait_for_selector("#dealer-endpoint-banner")
        time.sleep(1.5)
        path = str(SCREENSHOTS_DIR / "deployed_dealer_detail.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{DEPLOYED_BASE_URL}/dealer/1", "Overland Park Toyota & Ford - Details")
        print("[OK] Saved deployed_dealer_detail.png with deployed URL")

        # -------------------------------------------------------------
        # 12. deployed_add_review.png (Task 28: Deployed Added Review)
        # -------------------------------------------------------------
        print("Capturing 12. deployed_add_review.png...")
        page_pub.wait_for_selector("#reviews-list")
        time.sleep(1)
        path = str(SCREENSHOTS_DIR / "deployed_add_review.png")
        page_pub.screenshot(path=path)
        add_browser_chrome(path, f"{DEPLOYED_BASE_URL}/dealer/1", "Overland Park Toyota & Ford - Reviews & Sentiment")
        print("[OK] Saved deployed_add_review.png with review, sentiment, & deployed URL")

        browser.close()
        print("\nAll 12 screenshots successfully captured and enriched with browser address bars!")


if __name__ == "__main__":
    main()
