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
    """Generate calendar events for AI Engineer events"""
    
    def __init__(self):
        # Default event for backwards compatibility
        self.default_event = {
            'title': 'AI Engineer Summit 2025',
            'start_date': datetime.datetime(2025, 11, 19, 9, 0),
            'end_date': datetime.datetime(2025, 11, 22, 17, 0),
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
    
    def _parse_date_string(self, date_str):
        """Parse various date string formats to datetime objects"""
        import re
        
        if not date_str:
            return None, None
        
        # Try to extract date ranges
        patterns = [
            (r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)\s*[-–]\s*(\d+),?\s*(20\d{2})', 'MMM d-d, YYYY'),
            (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d+)\s*[-–]\s*(\d+),?\s*(20\d{2})', 'MMMM d-d, YYYY'),
            (r'(\d{1,2})/(\d{1,2})/(20\d{2})', 'M/d/YYYY'),
        ]
        
        months = {
            'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
            'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
            'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
            'nov': 11, 'november': 11, 'dec': 12, 'december': 12
        }
        
        for pattern, format_type in patterns:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                if 'MMM' in format_type:
                    month_name = match.group(1).lower()
                    month = months.get(month_name)
                    start_day = int(match.group(2))
                    end_day = int(match.group(3))
                    year = int(match.group(4))
                    
                    start_date = datetime.datetime(year, month, start_day, 9, 0)
                    end_date = datetime.datetime(year, month, end_day, 17, 0)
                    return start_date, end_date
                elif 'M/d/YYYY' in format_type:
                    month = int(match.group(1))
                    day = int(match.group(2))
                    year = int(match.group(3))
                    
                    start_date = datetime.datetime(year, month, day, 9, 0)
                    end_date = datetime.datetime(year, month, day, 17, 0)
                    return start_date, end_date
        
        # Default fallback
        return None, None
    
    def generate_ics_content(self, event_details=None):
        """Generate the ICS file content for a single event"""
        if event_details is None:
            event_details = self.default_event
        
        uid = self._generate_uid()
        now = datetime.datetime.utcnow()
        dtstamp = self._format_datetime(now)
        
        # Parse dates if they're strings
        start_date = event_details.get('start_date')
        end_date = event_details.get('end_date')
        
        if isinstance(start_date, str) or start_date is None:
            parsed_start, parsed_end = self._parse_date_string(event_details.get('date'))
            start_date = parsed_start or datetime.datetime(2025, 11, 19, 9, 0)
            end_date = parsed_end or datetime.datetime(2025, 11, 19, 17, 0)
        
        title = event_details.get('title', 'AI Engineer Event')
        location = event_details.get('location', 'Location TBD')
        description = event_details.get('description', 'AI Engineer event')
        url = event_details.get('url', 'https://www.ai.engineer/')
        organizer = event_details.get('organizer', 'AI Engineer')
        categories = event_details.get('categories', 'CONFERENCE,TECHNOLOGY,AI')
        
        ics_lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//AI Engineer Summit//Calendar Event Generator//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
            'BEGIN:VEVENT',
            f'UID:{uid}',
            f'DTSTART:{self._format_datetime(start_date)}',
            f'DTEND:{self._format_datetime(end_date)}',
            f'DTSTAMP:{dtstamp}',
            f'SUMMARY:{self._escape_text(title)}',
            f'LOCATION:{self._escape_text(location)}',
            f'DESCRIPTION:{self._escape_text(description)}',
            f'ORGANIZER:CN={organizer}',
            f'URL:{url}',
            'STATUS:CONFIRMED',
            'TRANSP:OPAQUE',
            f'CATEGORIES:{categories}',
            # Reminder 1 day before
            'BEGIN:VALARM',
            'TRIGGER:-P1D',
            'ACTION:DISPLAY',
            f'DESCRIPTION:{title} starts tomorrow!',
            'END:VALARM',
            # Reminder 1 hour before
            'BEGIN:VALARM',
            'TRIGGER:-PT1H',
            'ACTION:DISPLAY',
            f'DESCRIPTION:{title} starts in 1 hour!',
            'END:VALARM',
            'END:VEVENT',
            'END:VCALENDAR'
        ]
        
        return '\r\n'.join(ics_lines)
    
    def save_calendar_file(self, event_details=None, filename=None, output_dir=None):
        """Save a single calendar event to an .ics file"""
        if event_details is None:
            event_details = self.default_event
            
        if filename is None:
            safe_title = "".join(c for c in event_details.get('title', 'ai-engineer-event') if c.isalnum() or c in (' ', '-')).rstrip()
            safe_title = safe_title.replace(' ', '-').lower()
            filename = f'{safe_title}.ics'
        
        if output_dir is None:
            output_dir = Path.cwd()
        else:
            output_dir = Path(output_dir)
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        try:
            ics_content = self.generate_ics_content(event_details)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(ics_content)
            
            print(f"✅ Calendar event saved successfully!")
            print(f"📁 File location: {filepath.absolute()}")
            print(f"📅 Event: {event_details.get('title', 'AI Engineer Event')}")
            print(f"📍 Location: {event_details.get('location', 'Location TBD')}")
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving calendar file: {e}")
            return None
    
    def save_multiple_calendar_files(self, events_list, output_dir=None):
        """Save multiple calendar events as separate .ics files"""
        if not events_list:
            print("❌ No events to save")
            return []
        
        if output_dir is None:
            output_dir = Path.cwd()
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        print(f"\n📅 Generating {len(events_list)} calendar files...")
        
        for i, event in enumerate(events_list, 1):
            print(f"🔄 Processing event {i}/{len(events_list)}: {event.get('title', 'Untitled')}")
            
            filepath = self.save_calendar_file(
                event_details=event,
                output_dir=output_dir
            )
            
            if filepath:
                saved_files.append(filepath)
        
        print(f"\n🎉 Successfully generated {len(saved_files)} calendar files!")
        print("\n💡 To add to your calendar:")
        print("   1. Open your calendar app (Google Calendar, Outlook, Apple Calendar, etc.)")
        print("   2. Import each .ics file")
        print("   3. All events will be added with reminders set!")
        
        return saved_files
    
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