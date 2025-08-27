#!/usr/bin/env python3
"""
AI Engineer Website Automation Script

This script automates interactions with the AI Engineer Summit website
including email signup, calendar event generation, and navigation to forms.

Requirements:
    pip install playwright beautifulsoup4 requests
    playwright install

Usage:
    python web_automation.py
"""

import asyncio
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
import json
import time

try:
    from playwright.async_api import async_playwright
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("Please install with: pip install playwright beautifulsoup4 requests")
    print("Then run: playwright install")
    sys.exit(1)

from calendar_generator import AIEngineerCalendarGenerator


class AIEngineerWebAutomation:
    """Automate interactions with AI Engineer Summit website"""
    
    def __init__(self):
        self.base_url = "https://apply.ai.engineer/"
        self.calendar_generator = AIEngineerCalendarGenerator()
        self.browser = None
        self.page = None
    
    async def start_browser(self, headless=True):
        """Start the browser and create a new page"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()
        
        # Set user agent to appear more human-like
        await self.page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
    
    async def close_browser(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def navigate_to_site(self):
        """Navigate to the AI Engineer Summit website"""
        try:
            print(f"🌐 Navigating to {self.base_url}")
            await self.page.goto(self.base_url, wait_until="networkidle")
            
            # Take a screenshot for debugging
            await self.page.screenshot(path="ai_engineer_site.png")
            print("📸 Screenshot saved as ai_engineer_site.png")
            
            return True
        except Exception as e:
            print(f"❌ Error navigating to website: {e}")
            return False
    
    async def auto_signup_email(self, email):
        """Automatically fill and submit email signup form"""
        try:
            print(f"📧 Attempting to sign up with email: {email}")
            
            # Find email input field
            email_input = await self.page.query_selector('input[type="email"]')
            if not email_input:
                # Try alternative selectors
                email_input = await self.page.query_selector('input[placeholder*="email" i]')
            
            if email_input:
                await email_input.fill(email)
                print("✅ Email filled in form")
                
                # Find and click submit button
                submit_button = await self.page.query_selector('button[type="submit"]')
                if not submit_button:
                    # Try to find any button near the email input
                    submit_button = await self.page.query_selector('button')
                
                if submit_button:
                    await submit_button.click()
                    print("✅ Submit button clicked")
                    
                    # Wait for response
                    await self.page.wait_for_timeout(2000)
                    return True
                else:
                    print("❌ Could not find submit button")
                    return False
            else:
                print("❌ Could not find email input field")
                return False
                
        except Exception as e:
            print(f"❌ Error during email signup: {e}")
            return False
    
    async def extract_event_info(self):
        """Extract event information from the website"""
        try:
            print("🔍 Extracting event information from website...")
            
            # Get page content
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract event details
            event_info = {
                'title': None,
                'date': None,
                'location': None,
                'description': None
            }
            
            # Look for event title
            title_selectors = ['h1', '.title', '[class*="title"]', '[class*="heading"]']
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element and 'AI Engineer' in element.get_text():
                    event_info['title'] = element.get_text().strip()
                    break
            
            # Look for date information
            text_content = soup.get_text()
            if 'Nov' in text_content and '2025' in text_content:
                # Extract date pattern
                import re
                date_pattern = r'Nov\s+\d+\s*[-–]\s*\d+,\s*2025'
                date_match = re.search(date_pattern, text_content)
                if date_match:
                    event_info['date'] = date_match.group().strip()
            
            # Look for location
            if 'New York' in text_content:
                event_info['location'] = 'New York, New York'
            
            # Extract description
            desc_selectors = ['p', '.description', '[class*="desc"]']
            for selector in desc_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip()
                    if len(text) > 50 and ('AI Engineer' in text or 'summit' in text.lower()):
                        event_info['description'] = text[:200] + '...'
                        break
                if event_info['description']:
                    break
            
            print(f"📊 Extracted event info: {event_info}")
            return event_info
            
        except Exception as e:
            print(f"❌ Error extracting event info: {e}")
            return {}
    
    async def open_external_forms(self):
        """Open external forms in new tabs"""
        try:
            print("🔗 Looking for external form links...")
            
            # Get all links
            links = await self.page.query_selector_all('a')
            
            external_links = {}
            for link in links:
                href = await link.get_attribute('href')
                text = await link.text_content()
                
                if href:
                    if 'forms.gle' in href:
                        external_links['speaker_form'] = href
                        print(f"🎤 Found speaker application: {href}")
                    elif 'docs.google.com/forms' in href:
                        external_links['volunteer_form'] = href
                        print(f"🙋 Found volunteer form: {href}")
                    elif 'mailto:' in href:
                        external_links['sponsor_email'] = href
                        print(f"📧 Found sponsor email: {href}")
            
            return external_links
            
        except Exception as e:
            print(f"❌ Error finding external forms: {e}")
            return {}
    
    async def automated_workflow(self, email=None, generate_calendar=True):
        """Run the complete automated workflow"""
        print("🤖 Starting AI Engineer Website Automation")
        print("=" * 50)
        
        # Navigate to website
        if not await self.navigate_to_site():
            return False
        
        # Extract event information
        event_info = await self.extract_event_info()
        
        # Auto signup email if provided
        if email:
            await self.auto_signup_email(email)
        
        # Find external forms
        external_links = await self.open_external_forms()
        
        # Generate calendar event if requested
        if generate_calendar:
            print("\n📅 Generating calendar event...")
            calendar_file = self.calendar_generator.save_calendar_file()
            if calendar_file:
                print(f"✅ Calendar file generated: {calendar_file}")
        
        # Save automation results
        results = {
            'timestamp': time.time(),
            'website_url': self.base_url,
            'event_info': event_info,
            'external_links': external_links,
            'email_signup': email is not None,
            'calendar_generated': generate_calendar
        }
        
        # Save results to JSON file
        results_file = Path('automation_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Automation results saved to: {results_file}")
        return True


async def interactive_mode():
    """Run the automation in interactive mode"""
    automation = AIEngineerWebAutomation()
    
    try:
        print("🚀 AI Engineer Website Automation Tool")
        print("=" * 50)
        
        # Ask user for preferences
        email = input("Enter your email for signup (or press Enter to skip): ").strip()
        if not email:
            email = None
        
        headless_choice = input("Run browser in headless mode? (y/n): ").lower().strip()
        headless = headless_choice not in ['n', 'no']
        
        calendar_choice = input("Generate calendar event? (y/n): ").lower().strip()
        generate_calendar = calendar_choice not in ['n', 'no']
        
        # Start automation
        await automation.start_browser(headless=headless)
        success = await automation.automated_workflow(
            email=email,
            generate_calendar=generate_calendar
        )
        
        if success:
            print("\n🎉 Automation completed successfully!")
            
            # Ask if user wants to keep browser open for manual interaction
            if not headless:
                keep_open = input("\nKeep browser open for manual interaction? (y/n): ").lower().strip()
                if keep_open in ['y', 'yes']:
                    input("Press Enter when you're done with manual interaction...")
        
    except KeyboardInterrupt:
        print("\n⏹️  Automation interrupted by user")
    except Exception as e:
        print(f"❌ Automation error: {e}")
    finally:
        await automation.close_browser()


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print(__doc__)
        return
    
    # Run the interactive automation
    asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()