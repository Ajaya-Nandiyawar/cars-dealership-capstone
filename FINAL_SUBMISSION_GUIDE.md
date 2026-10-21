# Cars Dealership Full-Stack Capstone: Final Submission Guide

Follow this step-by-step submission guide to submit your graded Full-Stack Capstone assignment.

---

## Part 1: Push Your Code to GitHub

Your local git repository is initialized, configured, and contains all production code. To push to GitHub:

### Step 1. Create a New Public GitHub Repository
1. Go to [https://github.com/new](https://github.com/new).
2. Set Repository name: e.g. `cars-dealership-capstone`.
3. Set Visibility: **Public** (required by Coursera / peer graders).
4. Do NOT initialize with a README, .gitignore, or license (these already exist locally).
5. Click **Create repository**.

### Step 2. Commit and Push from Your Terminal
Run the following PowerShell commands in your project directory:

```powershell
# Stage all project files
git add .

# Create initial commit
git commit -m "feat: complete cars dealership full-stack capstone application"

# Rename branch to main
git branch -M main

# Add your remote URL (replace <YOUR_USERNAME> and <YOUR_REPO>)
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git

# Push code to GitHub
git push -u origin main
```

---

## Part 2: Exact URLs for Peer Review Questions

Once pushed to GitHub, replace `<YOUR_USERNAME>` and `<YOUR_REPO>` with your actual repository values:

### Question 1 (Task 1): README URL
```text
https://github.com/Ajaya-Nandiyawar/cars-dealership-capstone/blob/main/README.md
```

### Question 2 (Task 3): About Us Page URL
```text
https://github.com/Ajaya-Nandiyawar/cars-dealership-capstone/blob/main/server/frontend/static/About.html
```

### Question 3 (Task 4): Contact Us Page URL
```text
https://github.com/Ajaya-Nandiyawar/cars-dealership-capstone/blob/main/server/frontend/static/Contact.html
```

### Question 4 (Task 7): Registration Component URL
```text
https://github.com/Ajaya-Nandiyawar/cars-dealership-capstone/blob/main/server/frontend/src/components/Register/Register.jsx
```

---

## Part 3: Text Evidence Files to Copy & Paste

Open each file in `submission_evidence/commands/` and copy the contents into the assessment form:

| Form Field | File Path | Description |
|---|---|---|
| **Django Server Running** | `submission_evidence/commands/django_server.txt` | Shows server active on port 8000 |
| **Login User** | `submission_evidence/commands/loginuser.txt` | Shows authenticated login response |
| **Logout User** | `submission_evidence/commands/logoutuser.txt` | Shows session termination response |
| **Get All Dealers** | `submission_evidence/commands/getalldealers.txt` | Shows all 14 dealership records |
| **Get Dealer by ID** | `submission_evidence/commands/getdealerbyid.txt` | Shows Dealer 1 details |
| **Get Dealers by State (Kansas)** | `submission_evidence/commands/getdealersbyState.txt` | Shows Kansas dealerships query |
| **Get Dealer Reviews** | `submission_evidence/commands/getdealerreviews.txt` | Shows Dealer 1 reviews |
| **Get Car Makes & Models** | `submission_evidence/commands/getallcarmakes.txt` | Shows makes and models list |
| **Sentiment Analysis** | `submission_evidence/commands/analyzereview.txt` | Shows positive score on "Fantastic services" |
| **CI/CD Evidence** | `submission_evidence/commands/CICD.txt` | Shows workflow execution & 19/19 test passes |
| **Deployment URL** | `submission_evidence/commands/deploymentURL.txt` | Shows deployment status and URLs |

---

## Part 4: Screenshot Evidence Files to Upload

Upload the corresponding PNG files located in `submission_evidence/screenshots/`:

| Question # | Required File | What It Demonstrates |
|---|---|---|
| **Admin Login** | `submission_evidence/screenshots/admin_login.png` | Authenticated Django administration portal |
| **Admin Logout** | `submission_evidence/screenshots/admin_logout.png` | Admin login page after logging out |
| **Public Landing Page** | `submission_evidence/screenshots/get_dealers.png` | Dealers list, search, filter before login |
| **Logged-in Landing Page** | `submission_evidence/screenshots/get_dealers_loggedin.png` | Username in header & "Review Dealer" button |
| **State Filtered Dealers** | `submission_evidence/screenshots/dealersbystate.png` | Kansas filter active with endpoint banner visible |
| **Dealer Details & Reviews** | `submission_evidence/screenshots/dealer_id_reviews.png` | Dealer 1 detail, review endpoint banner, reviews |
| **Review Submission Form** | `submission_evidence/screenshots/dealership_review_submission.png` | Completed review form before clicking publish |
| **Posted Review** | `submission_evidence/screenshots/added_review.png` | Newly submitted review appearing on dealer page |

---

## Part 5: Deployed Questions (Tasks 25–28)

If your grading rubric requires public deployment screenshots (Tasks 25–28):
1. Install IBM Cloud CLI or use Render/Railway.
2. Follow `scripts/deploy_ibm_cloud.sh`.
3. Once deployed, capture screenshots of the public URL matching filenames:
   - `deployed_landingpage.png`
   - `deployed_loggedin.png`
   - `deployed_dealer_detail.png`
   - `deployed_add_review.png`
