import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "submission_evidence" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:8000"


def main():
    print("Launching Edge to capture genuine application screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        # -------------------------------------------------------------
        # 1. admin_login.png
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
        page.screenshot(path=str(SCREENSHOTS_DIR / "admin_login.png"))
        print("[OK] Saved admin_login.png")

        # -------------------------------------------------------------
        # 2. admin_logout.png
        # -------------------------------------------------------------
        print("Capturing 2. admin_logout.png...")
        # In Django 5+, logout is a POST form with button inside #user-tools
        if page.locator('#user-tools button[type="submit"]').count() > 0:
            page.locator('#user-tools button[type="submit"]').click()
        elif page.locator('form[action*="logout"] button').count() > 0:
            page.locator('form[action*="logout"] button').click()
        else:
            page.goto(f"{BASE_URL}/admin/login/")
        time.sleep(1.5)
        page.screenshot(path=str(SCREENSHOTS_DIR / "admin_logout.png"))
        print("[OK] Saved admin_logout.png")

        # -------------------------------------------------------------
        # 3. get_dealers.png (Public Landing Page before login)
        # -------------------------------------------------------------
        print("Capturing 3. get_dealers.png...")
        # Fresh context so no session cookies are present
        context_public = browser.new_context(viewport={"width": 1280, "height": 900})
        page_pub = context_public.new_page()
        page_pub.goto(f"{BASE_URL}/")
        page_pub.wait_for_selector("#dealers-grid")
        time.sleep(1.5)
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "get_dealers.png"))
        print("[OK] Saved get_dealers.png")

        # -------------------------------------------------------------
        # 4. get_dealers_loggedin.png (Landing Page after testuser login)
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
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "get_dealers_loggedin.png"))
        print("[OK] Saved get_dealers_loggedin.png")

        # -------------------------------------------------------------
        # 5. dealersbystate.png (State-filtered dealers with endpoint visible)
        # -------------------------------------------------------------
        print("Capturing 5. dealersbystate.png...")
        page_pub.select_option("#state-select", "Kansas")
        page_pub.wait_for_selector("#active-endpoint-indicator")
        time.sleep(1.5)
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "dealersbystate.png"))
        print("[OK] Saved dealersbystate.png")

        # -------------------------------------------------------------
        # 6. dealer_id_reviews.png (Dealer Detail page with reviews & endpoint)
        # -------------------------------------------------------------
        print("Capturing 6. dealer_id_reviews.png...")
        page_pub.click("#view-dealer-btn-1")
        page_pub.wait_for_selector("#dealer-endpoint-banner")
        page_pub.wait_for_selector("#reviews-list")
        time.sleep(1.5)
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "dealer_id_reviews.png"))
        print("[OK] Saved dealer_id_reviews.png")

        # -------------------------------------------------------------
        # 7. dealership_review_submission.png (Completed review form)
        # -------------------------------------------------------------
        print("Capturing 7. dealership_review_submission.png...")
        page_pub.click("#toggle-post-review-btn")
        page_pub.wait_for_selector("#review-form")
        page_pub.fill(
            "#review-text",
            "Fantastic services! The sales staff and finance manager were extraordinarily professional, transparent, and prompt. Outstanding automotive experience."
        )
        page_pub.check("#purchase-checkbox")
        page_pub.wait_for_selector("#review-car-model")
        page_pub.fill("#review-car-model", "Camry Hybrid")
        time.sleep(2)
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "dealership_review_submission.png"))
        print("[OK] Saved dealership_review_submission.png")

        # -------------------------------------------------------------
        # 8. added_review.png (Successfully posted review on dealer page)
        # -------------------------------------------------------------
        print("Capturing 8. added_review.png...")
        page_pub.click("#submit-review-btn")
        time.sleep(3)
        page_pub.screenshot(path=str(SCREENSHOTS_DIR / "added_review.png"))
        print("[OK] Saved added_review.png")

        browser.close()
        print("\nAll application screenshots successfully captured and saved!")


if __name__ == "__main__":
    main()
