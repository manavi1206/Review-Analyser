# 📊 Groww App Review Insights Analyzer

An AI-powered review analysis system that automatically scrapes, analyzes, and delivers executive-level insights from app store reviews via beautifully designed email reports.

## ✨ Features

- **🤖 Automated Review Scraping** - Collects reviews from Google Play Store & Apple App Store
- **🧠 AI-Powered Analysis** - Uses Google Gemini 2.5 Flash for executive-level insights
- **📧 Dashboard-Style Emails** - Professional, visual reports with metrics, charts, and recommendations
- **⚡ GitHub Actions Automation** - Runs weekly on Monday mornings automatically
- **🔒 Privacy-First** - Removes all PII from outputs

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/manavi1206/Review-Analyser.git
cd Review\ Analyser
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Required: Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Required: Gmail Credentials
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# App IDs (Groww defaults)
GROWW_ANDROID_APP_ID=com.nextbillion.groww
GROWW_IOS_APP_ID=1404871703

# Analysis Settings
WEEKS_TO_ANALYZE=10
```

### 3. Get API Keys

**Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key → Copy to `.env`

**Gmail App Password:**
1. Enable [2FA on Google Account](https://myaccount.google.com/security)
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Copy 16-char password to `.env`

### 4. Run Analysis

```bash
python3 main.py
```

This will:
1. ✅ Scrape ~7,000+ reviews (Android + iOS)
2. ✅ Analyze with Gemini AI
3. ✅ Generate Markdown & PDF reports
4. ✅ Send dashboard email with insights

## 📧 Email Report Features

The automated email includes:

### **Health Snapshot**
- 4-column metric grid: Total Reviews, Avg Rating, Positive %, Themes Count
- Visual icons and clean typography

### **Platform & Sentiment Distribution**
- Side-by-side cards with progress bars
- Android vs iOS breakdown
- Positive/Neutral/Negative sentiment visualization

### **Top Themes**
- Ranked by volume with percentages
- Severity badges (High/Medium/Low)
- Business risk categories (Trust, Revenue, Experience, Onboarding)

### **User Feedback**
- 4 verbatim quotes in 2x2 grid
- Theme and user segment tags

### **Recommended Actions**
- Priority-tagged (P0/P1/P2) with color coding
- Expected impact statements
- Green arrow indicators

### **Dynamic Subject Line**
```
Groww App Review Insights: 68% Positive, KYC Verification Delays Top Concern (Oct 22 - Dec 30)
```

## 🤖 GitHub Actions Automation

### Setup (One-Time)

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

2. Add these secrets:
   - `GEMINI_API_KEY` - Your Gemini API key
   - `GMAIL_ADDRESS` - Your Gmail address
   - `GMAIL_APP_PASSWORD` - Your Gmail app password

3. The workflow runs automatically **every Monday at 9:00 AM IST**

### Manual Trigger

Go to **Actions** tab → **Weekly Review Analysis** → **Run workflow**

## 📁 Project Structure

```
Review Analyser/
├── main.py                          # Main orchestrator
├── send_test_email.py               # Test email with sample data
├── requirements.txt                 # Python dependencies
├── .env                             # Your credentials (not in git)
├── .env.example                     # Template
├── .github/workflows/
│   └── weekly-analysis.yml          # GitHub Actions automation
├── src/
│   ├── scraper.py                   # Review scraping (Android + iOS)
│   ├── analyzer_executive.py        # Executive-level AI analysis
│   ├── report_generator_executive.py # Report generation
│   └── email_mailer_visual.py       # Dashboard email design
├── data/
│   └── raw/                         # Scraped reviews (CSV)
└── reports/                         # Generated reports (MD + PDF)
```

## 🎯 Executive Analysis Features

The AI analyzer provides:

- **Executive Summary** - 5 key bullet points for leadership
- **Theme Segmentation** - Severity (High/Medium/Low) + Business Risk classification
- **High-Impact Insights** - Deep dives into critical issues with user quotes
- **Rating Correlation** - What drives positive vs negative ratings
- **Positive Signals** - What users love about the app
- **Decision-Oriented Recommendations** - P0/P1/P2 prioritized actions
- **Leadership Decisions Required** - Strategic choices needed

## 🔧 Customization

### Change Analysis Period

```env
WEEKS_TO_ANALYZE=12  # Analyze last 12 weeks
```

### Analyze Different App

```env
GROWW_ANDROID_APP_ID=com.example.app
GROWW_IOS_APP_ID=123456789
```

### Test Email Design

```bash
python3 send_test_email.py
```

Sends a test email with sample data to verify design.

## ⚠️ Important: iOS App ID

**Critical:** The iOS App ID must be correct for iOS reviews to work.

For Groww app, use:
```env
GROWW_IOS_APP_ID=1404871703
```

**Not:** `1404871631` (incorrect ID)

## 🐛 Troubleshooting

### No iOS Reviews Collected
- Verify `GROWW_IOS_APP_ID=1404871703` in `.env`
- Check internet connection

### Email Not Sending
- Use Gmail **App Password**, not regular password
- Enable 2FA first
- Verify `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` in `.env`

### Gemini API Errors
- Check API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Verify `GEMINI_API_KEY` in `.env`

### GitHub Actions Not Running
- Add all 3 secrets in repo settings
- Check workflow file is in `.github/workflows/`
- Verify workflow is enabled in Actions tab

## 📊 Sample Output

### Email Subject
```
Groww App Review Insights: 68% Positive, KYC Verification Delays Top Concern (Oct 22 - Dec 30)
```

### Key Metrics
- **Total Reviews:** 7,178
- **Average Rating:** 4.12/5
- **Positive Sentiment:** 68%
- **Themes Identified:** 5

### Top Theme Example
```
#1 KYC Verification Delays (30%)
Users experiencing long wait times for account verification, some waiting 3-5 days
[High] [Trust]
~2,153 reviews
```

### Recommendation Example
```
[P0] Implement automated KYC verification using AI/ML document verification
→ Reduce verification time from days to hours, improving onboarding conversion by estimated 25%
```

## 🔒 Privacy & Security

- **No PII** - All usernames and personal data removed
- **Local Processing** - Reviews analyzed locally
- **Secure Credentials** - API keys in `.env` (gitignored)
- **GitHub Secrets** - Encrypted storage for automation

## 📦 Dependencies

- `google-generativeai` - Gemini AI API
- `google-play-scraper` - Android review scraping
- `reportlab` - PDF generation
- `python-dotenv` - Environment management

See `requirements.txt` for full list.

## 🎓 How It Works

1. **Scraping** - Fetches reviews from both app stores for the past N weeks
2. **Analysis** - Gemini AI extracts themes, quotes, and recommendations
3. **Report Generation** - Creates Markdown and PDF reports
4. **Email Delivery** - Sends dashboard-style email with all insights
5. **Automation** - GitHub Actions runs weekly on schedule

## 📝 Files Generated

Each run creates:
- `data/raw/reviews_YYYYMMDD.csv` - Raw scraped reviews
- `reports/executive_report_YYYYMMDD.md` - Markdown report
- `reports/executive_report_YYYYMMDD.pdf` - PDF report
- Email sent to configured address

## 🚀 Production Ready

- ✅ Automated weekly execution
- ✅ Professional email design
- ✅ Executive-level insights
- ✅ Complete error handling
- ✅ Privacy compliance

---

**Built for executive stakeholders who need actionable insights from app reviews** 📊✨
