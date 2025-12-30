#!/usr/bin/env python3
"""
Configuration Helper
Interactive script to help set up API keys and credentials
"""

import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(number, text):
    print(f"\n{'─'*70}")
    print(f"Step {number}: {text}")
    print('─'*70)

def main():
    print_header("🔧 Groww App Review Analyzer - Configuration Helper")
    
    print("This script will help you set up your .env file with the required API keys.")
    print("\nYou'll need:")
    print("  1. Gemini API Key (from Google AI Studio)")
    print("  2. Gmail address")
    print("  3. Gmail App Password (16 characters)")
    
    input("\nPress Enter to continue...")
    
    # Check if .env already exists
    env_path = ".env"
    if os.path.exists(env_path):
        print(f"\n⚠️  Warning: {env_path} already exists!")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("Exiting without changes.")
            sys.exit(0)
    
    # Collect information
    print_step(1, "Gemini API Key")
    print("\n📝 How to get your Gemini API Key:")
    print("   1. Visit: https://makersuite.google.com/app/apikey")
    print("   2. Click 'Create API Key'")
    print("   3. Copy the generated key")
    
    gemini_key = input("\n🔑 Enter your Gemini API Key: ").strip()
    
    print_step(2, "Gmail Configuration")
    print("\n📝 How to get your Gmail App Password:")
    print("   1. Enable 2-Step Verification at: https://myaccount.google.com/security")
    print("   2. Visit: https://myaccount.google.com/apppasswords")
    print("   3. Select 'Mail' and generate a password")
    print("   4. Copy the 16-character password (remove spaces)")
    
    gmail_address = input("\n📧 Enter your Gmail address: ").strip()
    gmail_password = input("🔐 Enter your Gmail App Password (16 chars): ").strip().replace(" ", "")
    
    print_step(3, "Optional Settings")
    weeks = input("\n📅 Weeks to analyze (default: 10): ").strip() or "10"
    max_themes = input("🏷️  Max themes to extract (default: 5): ").strip() or "5"
    
    # Create .env file
    env_content = f"""# Gemini API Configuration
GEMINI_API_KEY={gemini_key}

# Gmail Configuration
GMAIL_ADDRESS={gmail_address}
GMAIL_APP_PASSWORD={gmail_password}

# App Configuration
GROWW_ANDROID_APP_ID=com.nextbillion.groww
GROWW_IOS_APP_ID=1404871631

# Report Settings
WEEKS_TO_ANALYZE={weeks}
MAX_THEMES={max_themes}
REPORT_WORD_LIMIT=250
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print_header("✅ Configuration Complete!")
    print(f"✓ Created {env_path}")
    print(f"✓ Gemini API Key: {'*' * (len(gemini_key) - 4)}{gemini_key[-4:]}")
    print(f"✓ Gmail: {gmail_address}")
    print(f"✓ Weeks to analyze: {weeks}")
    print(f"✓ Max themes: {max_themes}")
    
    print("\n" + "="*70)
    print("🚀 Next Steps:")
    print("="*70)
    print("\n1. Run the analyzer:")
    print("   python3 main.py")
    print("\n2. Check your email for the weekly report!")
    print("\n3. Find generated reports in the 'reports/' directory")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
