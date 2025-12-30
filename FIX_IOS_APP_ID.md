# ⚠️ URGENT: Fix iOS App ID in .env

## Problem
Your `.env` file has the **WRONG iOS App ID**, which is why you're getting 0 iOS reviews.

## Current (WRONG)
```
GROWW_IOS_APP_ID=1404871631
```

## Should Be (CORRECT)
```
GROWW_IOS_APP_ID=1404871703
```

## How to Fix

### Option 1: Edit .env Directly
```bash
nano .env
```

Find the line with `GROWW_IOS_APP_ID` and change it to `1404871703`, then save.

### Option 2: Use sed Command
```bash
sed -i '' 's/GROWW_IOS_APP_ID=1404871631/GROWW_IOS_APP_ID=1404871703/' .env
```

### Option 3: Recreate .env
```bash
rm .env
python3 configure.py
```

When prompted for iOS App ID, enter: `1404871703`

## Verify the Fix
```bash
grep GROWW_IOS_APP_ID .env
```

Should show: `GROWW_IOS_APP_ID=1404871703`

## Then Run Again
```bash
python3 main.py
```

You should now see ~500 iOS reviews collected! 🎉

---

**Why This Matters:**
- Wrong ID: 0 iOS reviews
- Correct ID: ~500 iOS reviews
- Total: 7,178 Android + 500 iOS = **7,678 reviews**!
