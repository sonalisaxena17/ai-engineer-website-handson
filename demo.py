#!/usr/bin/env python3
"""
Demo script to automatically generate the AI Engineer Summit calendar event
without user interaction.
"""

from calendar_generator import AIEngineerCalendarGenerator

def main():
    """Generate calendar event automatically for demo purposes"""
    print("🎯 AI Engineer Summit 2025 - Auto Demo")
    print("=" * 50)
    
    generator = AIEngineerCalendarGenerator()
    generator.show_event_details()
    
    print("\n📅 Generating calendar file automatically...")
    calendar_file = generator.save_calendar_file()
    
    if calendar_file:
        print(f"\n🎉 Demo complete! Calendar file created successfully.")
        
        # Show the ICS content preview
        print(f"\n📄 Preview of generated .ics content:")
        print("-" * 40)
        ics_content = generator.generate_ics_content()
        lines = ics_content.split('\r\n')
        for i, line in enumerate(lines[:15]):  # Show first 15 lines
            print(f"{i+1:2d}: {line}")
        print(f"... ({len(lines)-15} more lines)")
        print("-" * 40)

if __name__ == "__main__":
    main()