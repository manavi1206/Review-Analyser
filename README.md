# 📊 Groww App Review Insights Analyzer

A comprehensive Python-based tool that analyzes app reviews from Google Play Store and Apple App Store, extracts key insights using Gemini AI, and generates weekly reports sent via email.

## 🎯 Features

- **Automated Review Scraping**: Collects reviews from both Android and iOS platforms
- **AI-Powered Analysis**: Uses Google Gemini to extract themes, quotes, and recommendations
- **Professional Reports**: Generates both Markdown and PDF reports
- **Email Automation**: Sends weekly insights directly to your inbox
- **Privacy-First**: Automatically removes PII from all outputs

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Gmail account with App Password enabled

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail Configuration
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# App Configuration (default values for Groww)
GROWW_ANDROID_APP_ID=com.nextbillion.groww
GROWW_IOS_APP_ID=1404871631

# Report Settings
WEEKS_TO_ANALYZE=10
MAX_THEMES=5
REPORT_WORD_LIMIT=250
```

### 3. Get Your API Keys

#### Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into `.env`

#### Gmail App Password:
1. Enable 2-factor authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Copy the 16-character password into `.env`

### 4. Run the Analyzer

```bash
python main.py
```

This will:
1. ✅ Scrape reviews from Play Store and App Store
2. ✅ Analyze reviews with Gemini AI
3. ✅ Generate markdown and PDF reports
4. ✅ Send email with insights

## 📁 Project Structure

```
Review Analyser/
├── main.py                 # Main orchestrator script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── src/
│   ├── scraper.py         # Review scraping logic
│   ├── analyzer.py        # Gemini AI analysis
│   ├── report_generator.py # Report creation
│   └── email_mailer.py    # Email sending
├── data/
│   ├── raw/               # Scraped reviews (CSV)
│   └── processed/         # Processed data
└── reports/               # Generated reports (MD & PDF)
```

## 🔄 How to Re-run for a New Week

Simply run the main script again:

```bash
python main.py
```

The tool automatically:
- Fetches the latest reviews from the past N weeks (configured in `.env`)
- Generates a new timestamped report
- Sends a fresh email with updated insights

## 🏷️ Theme Legend

The analyzer identifies up to 5 themes from reviews. Common themes for Groww include:

| Theme | Description |
|-------|-------------|
| **KYC & Verification** | Account setup, document verification, approval delays |
| **Payment Issues** | Deposits, withdrawals, transaction failures |
| **App Performance** | Crashes, bugs, slow loading, UI glitches |
| **Customer Support** | Response time, helpfulness, issue resolution |
| **Feature Requests** | New features, improvements, missing functionality |
| **User Experience** | Navigation, design, ease of use |

## 📊 Sample Output

### Weekly Report Includes:
- **Top 3 Themes**: Most discussed topics with percentages
- **3 User Quotes**: Real feedback from users (anonymized)
- **3 Action Items**: Specific, actionable recommendations

### Example:

```
📊 Groww App Weekly Review Insights

Report Period: 2024-10-21 to 2024-12-30
Total Reviews Analyzed: 247
Average Rating: 3.9/5 ⭐

🔍 Top 3 Themes
1. KYC Issues (35%) - Users facing delays in verification
2. Payment Problems (28%) - Withdrawal and deposit issues
3. App Performance (22%) - Crashes and slow loading

💬 User Voices
1. 😞 "KYC verification taking too long, been waiting for 3 days"
2. 😊 "Great app for beginners, easy to understand"
3. 😞 "Withdrawal stuck, customer support not responding"

💡 Recommended Actions
1. Implement automated KYC verification to reduce processing time
2. Add real-time withdrawal tracking dashboard
3. Optimize app performance with caching and lazy loading
```

## 🛠️ Customization

### Change Analysis Period

Edit `.env`:
```env
WEEKS_TO_ANALYZE=12  # Analyze last 12 weeks instead of 10
```

### Adjust Number of Themes

Edit `.env`:
```env
MAX_THEMES=3  # Extract only top 3 themes
```

### Analyze Different App

Edit `.env` with new app IDs:
```env
GROWW_ANDROID_APP_ID=com.example.app
GROWW_IOS_APP_ID=123456789
```

## 🐛 Troubleshooting

### "No reviews collected"
- Check if the app IDs are correct
- Verify internet connection
- Some apps may have limited public reviews

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Check that the API key is correctly formatted
- Verify the API key is active in Google AI Studio

### "Error sending email"
- Use an App Password, not your regular Gmail password
- Enable 2-factor authentication first
- Check that the email address is correct

## 📦 Deliverables Checklist

- ✅ Working prototype (this repository)
- ✅ Latest one-page weekly note (generated in `reports/`)
- ✅ Email draft (sent to configured Gmail address)
- ✅ Reviews CSV (saved in `data/raw/`)
- ✅ README with re-run instructions

## 🔒 Privacy & Security

- **No PII**: All usernames, emails, and personal identifiers are removed
- **Local Processing**: Reviews are processed locally
- **Secure Credentials**: API keys stored in `.env` (not committed to git)

## 📝 License

This project is for educational and internal use as part of Milestone 2 requirements.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed

---

**Built with ❤️ for Milestone 2 — App Review Insights Analyzer**
