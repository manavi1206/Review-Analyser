# ⚠️ IMPORTANT: Update Your .env File

## Issue: Wrong iOS App ID

Your `.env` file currently has the **wrong App ID** for the Groww iOS app.

### Current (WRONG):
```
GROWW_IOS_APP_ID=1404871631
```

### Should be (CORRECT):
```
GROWW_IOS_APP_ID=1404871703
```

## How to Fix

1. Open your `.env` file:
   ```bash
   nano .env
   ```
   or use any text editor

2. Find the line with `GROWW_IOS_APP_ID`

3. Change `1404871631` to `1404871703`

4. Save the file

5. Run the analyzer again:
   ```bash
   python3 main.py
   ```

## Why This Matters

- The correct App ID is from: https://apps.apple.com/in/app/groww-stocks-mutual-fund-ipo/id**1404871703**
- With the wrong ID, you get 0 iOS reviews
- With the correct ID, you'll get ~500 iOS reviews

## What Was Fixed

✅ **Gemini API**: Updated to use `gemini-2.5-flash` (latest model)  
✅ **iOS Scraper**: Replaced broken library with working RSS-based scraper  
⚠️ **App ID**: You need to update this in your `.env` file manually

---

**After updating .env, run `python3 main.py` again to collect iOS reviews!**
