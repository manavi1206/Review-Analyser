# 🚀 Setup Guide for Groww App Review Analyzer

Follow these steps to get the analyzer up and running.

## Step 1: Install Python Dependencies

```bash
cd "/Users/pewpew/Review Analyser"
pip install -r requirements.txt
```

## Step 2: Configure Your API Keys

### Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

### Get Gmail App Password

1. Go to your [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Visit [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and generate a password
5. Copy the 16-character password (remove spaces)

### Create .env File

```bash
cd "/Users/pewpew/Review Analyser"
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_password
```

## Step 3: Run the Analyzer

```bash
python main.py
```

## What Happens Next?

The tool will:
1. ✅ Scrape ~200-500 reviews from Play Store and App Store
2. ✅ Analyze them with Gemini AI
3. ✅ Generate markdown and PDF reports in `reports/`
4. ✅ Send an email to your Gmail address

## Expected Output

```
🚀 GROWW APP REVIEW INSIGHTS ANALYZER
======================================================================

📱 STEP 1: Scraping Reviews
----------------------------------------------------------------------
🤖 Scraping Play Store reviews...
✅ Collected 156 Android reviews
🍎 Scraping App Store reviews...
✅ Collected 91 iOS reviews
✅ Total reviews collected: 247

======================================================================
🧠 STEP 2: Analyzing Reviews with Gemini AI
----------------------------------------------------------------------
🔍 Step 1: Extracting themes...
💬 Step 2: Selecting representative quotes...
💡 Step 3: Generating action recommendations...
✅ Analysis complete!

======================================================================
📄 STEP 3: Generating Reports
----------------------------------------------------------------------
📄 Markdown report saved: reports/weekly_report_20241230.md
📄 PDF report saved: reports/weekly_report_20241230.pdf

======================================================================
📧 STEP 4: Sending Email Report
----------------------------------------------------------------------
📧 Preparing email to your_email@gmail.com...
🔐 Connecting to Gmail SMTP...
📎 Attached: weekly_report_20241230.md
📎 Attached: weekly_report_20241230.pdf
✅ Email sent successfully!

======================================================================
✅ WORKFLOW COMPLETE!
======================================================================
```

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists in the project root
- Check that you copied `.env.example` to `.env`
- Verify the API key is on the correct line

### "Error sending email"
- You MUST use an App Password, not your regular password
- Enable 2-factor authentication first
- Remove any spaces from the 16-character password

### "No reviews collected"
- Check your internet connection
- Verify the app IDs are correct in `.env`
- Some regions may have limited reviews

## Next Steps

Once successful, you can:
- Check the `reports/` folder for generated files
- Check your email inbox for the weekly report
- Re-run anytime with `python main.py` for updated insights

---

**Need help?** Check the main [README.md](README.md) for detailed documentation.
