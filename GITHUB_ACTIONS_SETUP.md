# 🤖 GitHub Actions Automation Setup

This guide will help you set up automated weekly review analysis that runs every Monday.

## 📋 What This Does

- ✅ Runs **every Monday at 9:00 AM IST**
- ✅ Scrapes latest reviews from Play Store & App Store
- ✅ Analyzes with Gemini AI
- ✅ Generates reports (Markdown & PDF)
- ✅ **Sends email automatically**
- ✅ Saves reports as GitHub artifacts
- ✅ (Optional) Commits reports to repository

---

## 🚀 Setup Instructions

### Step 1: Push Code to GitHub

```bash
cd "/Users/pewpew/Review Analyser"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Groww App Review Analyzer"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/Review-Analyser.git
git branch -M main
git push -u origin main
```

### Step 2: Add GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these three secrets:

#### Secret 1: GEMINI_API_KEY
- **Name**: `GEMINI_API_KEY`
- **Value**: Your Gemini API key from https://makersuite.google.com/app/apikey

#### Secret 2: GMAIL_ADDRESS
- **Name**: `GMAIL_ADDRESS`
- **Value**: Your Gmail address (e.g., `your_email@gmail.com`)

#### Secret 3: GMAIL_APP_PASSWORD
- **Name**: `GMAIL_APP_PASSWORD`
- **Value**: Your 16-character Gmail App Password

---

## ⚙️ Configuration

### Change Schedule

Edit `.github/workflows/weekly-analysis.yml`:

```yaml
schedule:
  # Every Monday at 9:00 AM IST (3:30 AM UTC)
  - cron: '30 3 * * 1'
```

**Common schedules:**
- Every Monday at 9 AM IST: `'30 3 * * 1'`
- Every Friday at 6 PM IST: `'30 12 * * 5'`
- Every day at 8 AM IST: `'30 2 * * *'`
- First day of month at 9 AM IST: `'30 3 1 * *'`

**Cron format**: `minute hour day month weekday`
- Weekdays: 0=Sunday, 1=Monday, ..., 6=Saturday
- IST = UTC + 5:30 hours

### Change Analysis Period

Edit the workflow file:

```yaml
env:
  WEEKS_TO_ANALYZE: 10  # Change to 4, 8, 12, etc.
  MAX_THEMES: 5         # Change to 3, 7, etc.
```

---

## 🧪 Test the Workflow

### Manual Trigger

1. Go to **Actions** tab in GitHub
2. Click **Weekly Review Analysis**
3. Click **Run workflow**
4. Select branch: `main`
5. Click **Run workflow**

This will run immediately without waiting for Monday.

### Check Logs

1. Go to **Actions** tab
2. Click on the running workflow
3. Click on **analyze-reviews** job
4. Expand steps to see detailed logs

---

## 📊 View Results

### Option 1: GitHub Artifacts

1. Go to **Actions** tab
2. Click on completed workflow run
3. Scroll down to **Artifacts**
4. Download `weekly-reports-XXX.zip`

Contains:
- Markdown reports
- PDF reports
- CSV data files

### Option 2: Email

Check your Gmail inbox every Monday after 9 AM IST for the automated report!

### Option 3: Repository (if enabled)

Reports are automatically committed to the `reports/` directory.

---

## 🔧 Troubleshooting

### Workflow Not Running

**Check:**
- Repository must be **public** OR you have GitHub Actions minutes
- Workflow file is in `.github/workflows/` directory
- YAML syntax is correct (use GitHub's validator)

### Secrets Not Working

**Verify:**
- Secret names match exactly (case-sensitive)
- No extra spaces in secret values
- Secrets are set at repository level, not organization

### Email Not Sending

**Check logs for:**
- "GEMINI_API_KEY not found" → Secret not set correctly
- "GMAIL_APP_PASSWORD" error → Use App Password, not regular password
- SMTP errors → Verify Gmail settings

### Scraping Fails

**Common causes:**
- Rate limiting (reduce `WEEKS_TO_ANALYZE`)
- Network issues (workflow will retry next week)
- App ID changed (update in workflow file)

---

## 📈 Advanced Options

### Send to Multiple Recipients

Edit `src/email_mailer.py`:

```python
def send_weekly_report(self, analysis: Dict, report_paths: List[str], 
                      recipient: str = None) -> bool:
    if recipient is None:
        # Send to multiple people
        recipients = [
            "product@company.com",
            "support@company.com",
            "leadership@company.com"
        ]
        for email in recipients:
            self._send_to_single_recipient(email, analysis, report_paths)
```

### Slack/Discord Notifications

Add a step to the workflow:

```yaml
- name: Send Slack notification
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "📊 Weekly Groww review analysis complete!"
      }
```

### Store in Database

Add a step to upload results to a database:

```yaml
- name: Upload to database
  run: |
    python scripts/upload_to_db.py
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## 🎯 Best Practices

1. **Monitor First Few Runs**: Check logs to ensure everything works
2. **Set Up Notifications**: Enable GitHub Actions email notifications
3. **Review Costs**: Check GitHub Actions usage (free tier: 2000 min/month)
4. **Backup Reports**: Download artifacts periodically
5. **Update Dependencies**: Keep `requirements.txt` updated

---

## 📅 What Happens Every Monday

```
9:00 AM IST - Workflow triggers
9:01 AM     - Scrapes Play Store reviews
9:02 AM     - Scrapes App Store reviews  
9:03 AM     - Analyzes with Gemini AI
9:04 AM     - Generates reports
9:05 AM     - Sends email
9:06 AM     - Uploads artifacts
9:07 AM     - Workflow complete ✅
```

**You'll receive the email around 9:05-9:10 AM IST every Monday!**

---

## 🆘 Need Help?

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Cron Schedule Helper**: https://crontab.guru/
- **Check Workflow Status**: Repository → Actions tab

---

**Ready to automate? Follow Step 1 and Step 2 above to get started! 🚀**
