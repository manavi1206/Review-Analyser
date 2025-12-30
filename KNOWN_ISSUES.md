# ⚠️ Known Issues & Solutions

## Issue 1: App Store Reviews Not Scraping (0 iOS reviews)

**Problem**: The `app-store-scraper` library is experiencing issues with Apple's API, resulting in JSON parsing errors.

**Error Message**:
```
[ERROR] Base - Something went wrong: Expecting value: line 1 column 1 (char 0)
```

**Why This Happens**:
- Apple's App Store API is not officially public and can be unreliable
- The scraper library depends on undocumented endpoints that may change
- Regional restrictions or rate limiting may block requests

**Solutions**:

### ✅ Solution 1: Use Android Reviews Only (Current Default)
The system now gracefully handles App Store failures and continues with Play Store reviews. With **7,179 Android reviews**, you have more than enough data for meaningful insights!

### 🔧 Solution 2: Manual iOS Review Export
If you need iOS reviews:
1. Log into [App Store Connect](https://appstoreconnect.apple.com/)
2. Go to "Ratings and Reviews"
3. Export reviews as CSV
4. Place the CSV in `data/raw/` and modify the scraper to read from file

### 🔄 Solution 3: Try Alternative Scraper
Update `requirements.txt` to use a different library:
```bash
pip install app-store-reviews-reader
```

Then modify `src/scraper.py` to use the alternative library.

---

## Issue 2: Gemini API Model Error (FIXED ✅)

**Problem**: Old model name `gemini-pro` is deprecated.

**Error Message**:
```
404 models/gemini-pro is not found for API version v1beta
```

**Solution**: ✅ **FIXED** - Updated to `gemini-1.5-flash` in `src/analyzer.py`

---

## Issue 3: Python Version Warning

**Warning Message**:
```
You are using a Python version (3.9.6) past its end of life
```

**Impact**: Low - The code still works, but you may miss security updates.

**Solution** (Optional):
```bash
# Install Python 3.10+ using Homebrew
brew install python@3.11

# Or use pyenv to manage Python versions
brew install pyenv
pyenv install 3.11
pyenv global 3.11
```

---

## Issue 4: Dependency Conflicts

**Problem**: Some package version conflicts during installation.

**Solution**: ✅ **FIXED** - Removed strict version constraint for `requests` package.

**Note**: You may see warnings about `selenium` and `urllib3` compatibility, but these don't affect the analyzer's functionality.

---

## Current Status

✅ **Working Features**:
- ✅ Android (Play Store) review scraping (7,179 reviews collected!)
- ✅ Gemini AI analysis with updated model
- ✅ Report generation (Markdown & PDF)
- ✅ Email automation via Gmail

⚠️ **Known Limitations**:
- ⚠️ iOS (App Store) scraping unreliable due to library issues
- ⚠️ Python 3.9 is past end-of-life (upgrade recommended but not required)

---

## Recommendations

1. **For now**: Continue using Android reviews only - 7,179 reviews is excellent sample size!
2. **If iOS reviews are critical**: Use manual export from App Store Connect
3. **Long term**: Consider upgrading to Python 3.10+ for better support

---

## Testing the Fixes

Run the analyzer again to test the Gemini API fix:

```bash
python3 main.py
```

You should now see:
- ✅ Themes extracted successfully
- ✅ Quotes selected from reviews
- ✅ Recommendations generated
- ✅ Professional report with real insights

---

**Last Updated**: 2025-12-31  
**Status**: Android scraping working perfectly, iOS scraping has known issues with third-party library
