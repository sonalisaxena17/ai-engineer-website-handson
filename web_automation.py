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
        self.base_url = "https://www.ai.engineer/"
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
    
    async def extract_multiple_events(self):
        """Extract multiple event information from the website"""
        import re
        
        try:
            print("🔍 Extracting multiple events from website...")
            
            # Get page content
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            events = []
            
            # Look for event containers - common patterns
            event_containers = []
            
            # Try various selectors for event containers
            container_selectors = [
                '[class*="event"]',
                '[class*="events"]',
                '[class*="upcoming"]',
                '[class*="conference"]', 
                '[class*="summit"]',
                '[class*="card"]',
                'article',
                'section',
                'li',
                'div',
                '.event-item',
                '.conference-item'
            ]
            
            # Look for event cards/containers with specific patterns
            # Target event-specific containers first
            event_specific_containers = []
            
            # Look for containers that likely contain individual events
            potential_events = soup.find_all(['div', 'article', 'section'])
            
            for container in potential_events:
                container_text = container.get_text()
                if not container_text:
                    continue
                    
                # Check if this container has event indicators
                container_lower = container_text.lower()
                has_event_title = any(keyword in container_lower for keyword in 
                    ['aie paris', 'fall summit', 'world\'s fair', 'ai engineer summit', 'ai engineer world', 'paris 2025'])
                
                # Look for specific event patterns including dates
                has_date_location = bool(re.search(r'(paris.*2025|september.*paris|november.*new york|june.*san francisco)', container_lower))
                
                # Size filter - should be substantial but not the whole page
                text_length = len(container_text.strip())
                is_reasonable_size = 30 < text_length < 800
                
                # Must contain year indicator for events
                has_year = bool(re.search(r'20\d{2}', container_text))
                
                if (has_event_title or has_date_location) and is_reasonable_size and has_year:
                    event_specific_containers.append(container)
                    # print(f"🎯 Found potential event container: {container_text[:80].replace(chr(10), ' ')}...")
            
            # Add these specific containers first
            event_containers.extend(event_specific_containers)
            
            # Also scan with regular selectors for comprehensive coverage
            for selector in container_selectors:
                containers = soup.select(selector)
                for container in containers:
                    container_text = container.get_text().lower()
                    # Check if this container likely contains event info
                    if any(keyword in container_text for keyword in ['2025', '2026', 'summit', 'conference', 'event', 'workshop', 'meetup', 'hackathon']):
                        event_containers.append(container)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_containers = []
            for container in event_containers:
                container_id = id(container)
                if container_id not in seen:
                    seen.add(container_id)
                    unique_containers.append(container)
            event_containers = unique_containers
            
            print(f"🔍 Found {len(event_containers)} potential event containers")
            
            # If no specific containers found, scan the entire page for event patterns
            if not event_containers:
                event_containers = [soup.body] if soup.body else [soup]
            
            for i, container in enumerate(event_containers):
                event_info = self._extract_single_event(container)
                # print(f"🔍 Container {i+1}: {container.name if hasattr(container, 'name') else 'unknown'} - {event_info.get('title') if event_info else 'No title found'}")
                
                if event_info and event_info.get('title'):
                    # Avoid duplicates
                    if not any(e.get('title') == event_info.get('title') for e in events):
                        events.append(event_info)
                        # print(f"✅ Added event: {event_info.get('title')}")
            
            print(f"📊 Found {len(events)} unique events: {[e.get('title', 'Untitled') for e in events]}")
            return events
            
        except Exception as e:
            print(f"❌ Error extracting events: {e}")
            return []
    
    def _extract_single_event(self, container):
        """Extract event information from a container element"""
        import re
        
        text = container.get_text()
        event_info = {
            'title': None,
            'date': None,
            'location': None,
            'description': None,
            'url': None
        }
        
        # Skip containers that are too large (likely page containers)
        if len(text) > 2000:
            return None
            
        # Skip containers with very little text
        if len(text.strip()) < 10:
            return None
        
        # Skip non-event content by checking for exclusion patterns
        text_lower = text.lower()
        exclude_patterns = [
            'newsletter', 'email', 'spam', 'subscribe', 'join our', 'terms of service', 
            'code of conduct', 'sponsor inquiry', 'scholarships', 'contact us', 
            'copyright', '©', 'software 3.0', 'valuable insights', 'exclusive content',
            'special offers', 'event updates', 'find more talks', 'watch our',
            'what is an ai engineer', 'workshops'
        ]
        
        if any(exclude in text_lower for exclude in exclude_patterns):
            return None
        
        # Skip if the text looks like just a date string
        date_only_patterns = [
            r'^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+[-–]\d+\s+20\d{2},?\s*[A-Za-z\s,]+$',
            r'^(June|November|September)\s+\d+[-–](July\s+)?\d+\s+20\d{2},?\s*[A-Za-z\s,]+$'
        ]
        
        for pattern in date_only_patterns:
            if re.match(pattern, text.strip()):
                print(f"🚫 Skipping date-only string: {text.strip()[:50]}")
                return None
        
        # Must contain either a date pattern OR event-related keywords to be considered
        has_date = False
        if text and isinstance(text, str):
            has_date = bool(re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+[\s\-–]*(\d+)?,?\s*20\d{2}', text, re.IGNORECASE))
        
        has_event_keywords = any(keyword in text_lower for keyword in ['summit', 'conference', 'fair', 'workshop', 'meetup', 'hackathon'])
        
        if not (has_date or has_event_keywords):
            return None
        
        # Extract title - look for headings first, then strong text, then meaningful text
        title_candidates = []
        
        # Check headings
        headings = container.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            heading_text = heading.get_text().strip()
            if len(heading_text) > 3:
                title_candidates.append(heading_text)
        
        # Check strong/bold text
        strong_elements = container.find_all(['strong', 'b'])
        for strong in strong_elements:
            strong_text = strong.get_text().strip()
            if len(strong_text) > 3 and len(strong_text) < 100:
                title_candidates.append(strong_text)
        
        # Check links that might be event titles
        links = container.find_all('a', href=True)
        for link in links:
            link_text = link.get_text().strip()
            if len(link_text) > 3 and len(link_text) < 100:
                title_candidates.append(link_text)
        
        # Use the most relevant title with broader keyword matching
        for title in title_candidates:
            title_lower = title.lower()
            # Accept specific AI Engineer event patterns
            if any(keyword in title_lower for keyword in ['summit', 'conference', 'fair', 'workshop', 'meetup', 'hackathon', 'aie paris']):
                event_info['title'] = title
                break
        
        # If no good title found and we have dates, try to find a meaningful title
        if not event_info['title'] and has_date:
            lines = text.strip().split('\n') if text else []
            for line in lines:
                line = line.strip()
                # Skip lines that look like pure date strings
                if re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+', line):
                    continue
                if len(line) > 10 and len(line) < 100 and re.search(r'20\d{2}', line):
                    event_info['title'] = line
                    break
        
        # Extract dates - look for various date formats including those in titles
        date_patterns = [
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s*[-–]\s*\d+,?\s*20\d{2}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+\s*[-–]\s*\d+,?\s*20\d{2}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+,?\s*20\d{2}',
            r'(September|November|June)\s+\d+[-–]\d+,?\s*20\d{2}',
            r'\d{1,2}/\d{1,2}/20\d{2}',
            r'20\d{2}-\d{2}-\d{2}'
        ]
        
        # First, look for date info in the entire container text
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                event_info['date'] = match.group().strip()
                print(f"🗓️ Found date in text: {event_info['date']}")
                break
        
        # Also check the title if we have one
        title_text = event_info.get('title') or ''
        if title_text and not event_info['date']:
            for pattern in date_patterns:
                match = re.search(pattern, title_text, re.IGNORECASE)
                if match:
                    event_info['date'] = match.group().strip()
                    print(f"🗓️ Found date in title: {event_info['date']}")
                    break
        
        # Look for specific event date patterns
        if not event_info['date']:
            # Check for specific patterns in the text
            event_date_patterns = [
                (r'september\s+23[-–]24.*2025', 'September 23-24, 2025'),
                (r'november\s+20[-–]22.*2025', 'November 20-22, 2025'),
                (r'june\s+30.*july\s+2.*2026', 'June 30-July 2, 2026'),
                (r'march.*2025', 'March 2025')
            ]
            
            for pattern, standard_date in event_date_patterns:
                if re.search(pattern, text.lower()):
                    event_info['date'] = standard_date
                    print(f"🗓️ Found specific event date: {standard_date}")
                    break
        
        # Extract location
        location_patterns = [
            r'(New York|San Francisco|Los Angeles|Chicago|Boston|Seattle|Austin|Denver|Miami|Las Vegas|Washington DC|Atlanta|Portland|Phoenix|Dallas|Houston|Toronto|Vancouver|London|Berlin|Paris|Tokyo|Sydney)',
            r'[A-Z][a-z]+,\s*[A-Z]{2}',
            r'[A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2}'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                event_info['location'] = match.group().strip()
                break
        
        # Extract description - find meaningful paragraphs
        paragraphs = container.find_all('p')
        for p in paragraphs:
            p_text = p.get_text().strip()
            if len(p_text) > 30:
                event_info['description'] = p_text[:300] + ('...' if len(p_text) > 300 else '')
                break
        
        # If no paragraph description, use container text but limit it
        if not event_info['description'] and len(text.strip()) > 30:
            clean_text = ' '.join(text.split())  # Remove extra whitespace
            event_info['description'] = clean_text[:200] + ('...' if len(clean_text) > 200 else '')
        
        # Extract URL
        for link in links:
            href = link.get('href')
            if href and ('apply' in href or 'register' in href or 'event' in href or 'ticket' in href):
                if href.startswith('http'):
                    event_info['url'] = href
                else:
                    event_info['url'] = urljoin(self.base_url, href)
                break
        
        # Only return event if it has at least a title
        if event_info['title']:
            return event_info
        
        return None
    
    def select_events_interactive(self, events):
        """Interactive selection of events to generate calendar invites for"""
        if not events:
            print("❌ No events found to select from")
            return []
        
        print("\n📅 Available Events:")
        print("=" * 50)
        
        for i, event in enumerate(events, 1):
            title = event.get('title', 'Untitled Event')
            date = event.get('date', 'Date TBD')
            location = event.get('location', 'Location TBD')
            print(f"{i}. {title}")
            print(f"   📅 {date}")
            print(f"   📍 {location}")
            print()
        
        # Get user selection
        while True:
            try:
                choice = input("Select events to download (comma-separated numbers, or 'all'): ").strip().lower()
                
                if choice == 'all':
                    return events
                
                if choice == '':
                    print("❌ Please make a selection or type 'all'")
                    continue
                
                # Parse comma-separated numbers
                selections = []
                for num_str in choice.split(','):
                    num = int(num_str.strip())
                    if 1 <= num <= len(events):
                        selections.append(events[num - 1])
                    else:
                        print(f"❌ Invalid selection: {num}. Please choose between 1-{len(events)}")
                        break
                else:
                    return selections
                    
            except ValueError:
                print("❌ Please enter numbers separated by commas, or 'all'")
            except KeyboardInterrupt:
                print("\n⏹️ Selection cancelled")
                return []
    
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
        
        # Extract multiple events from the website
        events = await self.extract_multiple_events()
        
        # Auto signup email if provided
        if email:
            await self.auto_signup_email(email)
        
        # Find external forms
        external_links = await self.open_external_forms()
        
        # Generate calendar events if requested
        calendar_files = []
        if generate_calendar and events:
            # Let user select which events to download
            selected_events = self.select_events_interactive(events)
            
            if selected_events:
                print("\n📅 Generating calendar files...")
                calendar_files = self.calendar_generator.save_multiple_calendar_files(selected_events)
        
        # Save automation results
        results = {
            'timestamp': time.time(),
            'website_url': self.base_url,
            'events_found': len(events),
            'events_info': events,
            'external_links': external_links,
            'email_signup': email is not None,
            'calendar_files_generated': len(calendar_files),
            'calendar_files': [str(f) for f in calendar_files]
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
