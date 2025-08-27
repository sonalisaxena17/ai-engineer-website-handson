#!/usr/bin/env python3
"""
AI Engineer Summit 2025 Calendar Event Generator

This script generates an .ics calendar file for the AI Engineer Summit 2025
that can be imported into any calendar application.

Usage:
    python calendar_generator.py

Requirements:
    - Python 3.6+
    - No external dependencies (uses only standard library)
"""

import os
import datetime
from pathlib import Path


class AIEngineerCalendarGenerator:
    """Generate calendar events for AI Engineer Summit 2025"""
    
    def __init__(self):
        self.event_details = {
            'title': 'AI Engineer Summit 2025',
            'start_date': datetime.datetime(2025, 11, 19, 9, 0),  # Nov 19, 2025 9:00 AM
            'end_date': datetime.datetime(2025, 11, 22, 17, 0),   # Nov 22, 2025 5:00 PM
            'location': 'New York, New York',
            'description': (
                'The premier technical AI summit for AI Engineers & AI Leaders who ship. '
                'Invite-only, curated for top AI Engineers.\n\n'
                'Website: https://apply.ai.engineer/\n'
                'Application Deadline: September 15, 2025'
            ),
            'url': 'https://apply.ai.engineer/',
            'organizer': 'AI Engineer Summit',
            'categories': 'CONFERENCE,TECHNOLOGY,AI'
        }
    
    def _format_datetime(self, dt):
        """Format datetime for ICS format (UTC)"""
        return dt.strftime('%Y%m%dT%H%M%SZ')
    
    def _generate_uid(self):
        """Generate unique event ID"""
        timestamp = int(datetime.datetime.now().timestamp())
        return f'ai-engineer-summit-2025-{timestamp}@ai.engineer'
    
    def _escape_text(self, text):
        """Escape special characters in ICS text fields"""
        # Replace newlines with \n and escape special characters
        return text.replace('\n', '\\n').replace(',', '\\,').replace(';', '\\;')
    
    def generate_ics_content(self):
        """Generate the ICS file content"""
        uid = self._generate_uid()
        now = datetime.datetime.utcnow()
        dtstamp = self._format_datetime(now)
        
        ics_lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//AI Engineer Summit//Calendar Event Generator//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
            'BEGIN:VEVENT',
            f'UID:{uid}',
            f'DTSTART:{self._format_datetime(self.event_details["start_date"])}',
            f'DTEND:{self._format_datetime(self.event_details["end_date"])}',
            f'DTSTAMP:{dtstamp}',
            f'SUMMARY:{self._escape_text(self.event_details["title"])}',
            f'LOCATION:{self._escape_text(self.event_details["location"])}',
            f'DESCRIPTION:{self._escape_text(self.event_details["description"])}',
            f'ORGANIZER:CN={self.event_details["organizer"]}',
            f'URL:{self.event_details["url"]}',
            'STATUS:CONFIRMED',
            'TRANSP:OPAQUE',
            f'CATEGORIES:{self.event_details["categories"]}',
            # Reminder 1 day before
            'BEGIN:VALARM',
            'TRIGGER:-P1D',
            'ACTION:DISPLAY',
            'DESCRIPTION:AI Engineer Summit 2025 starts tomorrow!',
            'END:VALARM',
            # Reminder 1 hour before
            'BEGIN:VALARM',
            'TRIGGER:-PT1H',
            'ACTION:DISPLAY',
            'DESCRIPTION:AI Engineer Summit 2025 starts in 1 hour!',
            'END:VALARM',
            'END:VEVENT',
            'END:VCALENDAR'
        ]
        
        return '\r\n'.join(ics_lines)
    
    def save_calendar_file(self, filename=None, output_dir=None):
        """Save the calendar event to an .ics file"""
        if filename is None:
            filename = 'ai-engineer-summit-2025.ics'
        
        if output_dir is None:
            output_dir = Path.cwd()
        else:
            output_dir = Path(output_dir)
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        try:
            ics_content = self.generate_ics_content()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(ics_content)
            
            print(f"✅ Calendar event saved successfully!")
            print(f"📁 File location: {filepath.absolute()}")
            print(f"📅 Event: {self.event_details['title']}")
            print(f"📍 Location: {self.event_details['location']}")
            print(f"🗓️  Date: {self.event_details['start_date'].strftime('%B %d-%d, %Y')}")
            print(f"\n💡 To add to your calendar:")
            print(f"   1. Open your calendar app (Google Calendar, Outlook, Apple Calendar, etc.)")
            print(f"   2. Import the .ics file: {filename}")
            print(f"   3. The event will be added with reminders set!")
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving calendar file: {e}")
            return None
    
    def show_event_details(self):
        """Display event details to the user"""
        print("🎯 AI Engineer Summit 2025 - Event Details")
        print("=" * 50)
        print(f"📅 Event: {self.event_details['title']}")
        print(f"📍 Location: {self.event_details['location']}")
        print(f"🗓️  Dates: {self.event_details['start_date'].strftime('%B %d')} - {self.event_details['end_date'].strftime('%B %d, %Y')}")
        print(f"🌐 Website: {self.event_details['url']}")
        print(f"📝 Description: {self.event_details['description'][:100]}...")
        print("=" * 50)


def main():
    """Main function to run the calendar generator"""
    print("🤖 AI Engineer Summit 2025 Calendar Generator")
    print("=" * 50)
    
    generator = AIEngineerCalendarGenerator()
    
    # Show event details
    generator.show_event_details()
    
    # Ask user for confirmation
    while True:
        choice = input("\nGenerate calendar file? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            break
        elif choice in ['n', 'no']:
            print("Calendar generation cancelled.")
            return
        else:
            print("Please enter 'y' for yes or 'n' for no.")
    
    # Generate and save the calendar file
    output_path = generator.save_calendar_file()
    
    if output_path:
        print(f"\n🎉 Success! Your calendar file is ready.")
        
        # Ask if user wants to open the file location
        if os.name == 'nt':  # Windows
            choice = input("\nOpen file location in Explorer? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                os.system(f'explorer /select,"{output_path}"')
        elif os.name == 'posix':  # macOS/Linux
            choice = input("\nOpen file location? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                if 'darwin' in os.sys.platform:  # macOS
                    os.system(f'open -R "{output_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{output_path.parent}"')


if __name__ == "__main__":
    main()