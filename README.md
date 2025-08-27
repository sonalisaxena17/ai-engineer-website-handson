# AI Engineer Summit 2025 - Website Automation Tools

Automated tools for interacting with the AI Engineer Summit website (https://apply.ai.engineer/) including calendar event generation and form automation.

## 🚀 Quick Start

### Option 1: Simple Calendar Generator (Recommended)
Generate a calendar event without any dependencies:

```bash
python3 calendar_generator.py
```

### Option 2: JavaScript Bookmarklet (Browser-based)
1. Copy the bookmarklet code from `bookmarklet.js`
2. Create a new bookmark in your browser
3. Paste the code as the bookmark URL
4. Click the bookmark on any website to download the calendar event

### Option 3: Full Web Automation (Advanced)
Automate email signup and website interactions:

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run automation
python3 web_automation.py
```

## 📁 Project Structure

```
ai-engineer-website-handson/
├── calendar_generator.py    # Standalone calendar event generator
├── web_automation.py       # Full website automation with Playwright
├── bookmarklet.js          # JavaScript bookmarklet for browsers
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Tools Overview

### 1. Calendar Generator (`calendar_generator.py`)
- **Purpose**: Generate .ics calendar files for AI Engineer Summit 2025
- **Dependencies**: None (Python standard library only)
- **Output**: `.ics` file compatible with all calendar apps

**Features:**
- ✅ Event details: Nov 19-22, 2025 in New York
- ✅ Automatic reminders (1 day & 1 hour before)
- ✅ Compatible with Google Calendar, Outlook, Apple Calendar
- ✅ Cross-platform file location opening

### 2. Web Automation (`web_automation.py`)
- **Purpose**: Automate interactions with the AI Engineer website
- **Dependencies**: Playwright, BeautifulSoup4, Requests
- **Capabilities**: Email signup, event extraction, form navigation

**Features:**
- 🌐 Automatic website navigation
- 📧 Email signup automation  
- 🔍 Event information extraction
- 🔗 External form discovery (speaker/volunteer applications)
- 📸 Screenshot capture for debugging
- 📊 Results saved to JSON file

### 3. JavaScript Bookmarklet (`bookmarklet.js`)
- **Purpose**: Browser-based calendar event generation
- **Dependencies**: None (runs in any modern browser)
- **Usage**: Click bookmark to download calendar event

**Features:**
- 🖱️ One-click calendar download
- 📅 Works on any website
- ✨ Visual success notification
- 🚀 No installation required

## 📋 Installation & Setup

### Prerequisites
- Python 3.6+ 
- Modern web browser (for bookmarklet)

### Setup Instructions

1. **Clone or download this project:**
   ```bash
   cd ai-engineer-website-handson
   ```

2. **For Python scripts (Optional):**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **For bookmarklet setup:**
   - Open `bookmarklet.js`
   - Copy the minified JavaScript code
   - Create new bookmark in your browser
   - Paste code as the bookmark URL

## 🎯 Usage Examples

### Simple Calendar Generation
```bash
$ python calendar_generator.py

🤖 AI Engineer Summit 2025 Calendar Generator
==================================================
🎯 AI Engineer Summit 2025 - Event Details
==================================================
📅 Event: AI Engineer Summit 2025
📍 Location: New York, New York
🗓️  Dates: November 19 - November 22, 2025
🌐 Website: https://apply.ai.engineer/
📝 Description: The premier technical AI summit...
==================================================

Generate calendar file? (y/n): y
✅ Calendar event saved successfully!
📁 File location: /path/to/ai-engineer-summit-2025.ics
```

### Web Automation with Email Signup
```bash
$ python web_automation.py

🚀 AI Engineer Website Automation Tool
==================================================
Enter your email for signup (or press Enter to skip): your.email@example.com
Run browser in headless mode? (y/n): n
Generate calendar event? (y/n): y

🌐 Navigating to https://apply.ai.engineer/
📧 Attempting to sign up with email: your.email@example.com
✅ Email filled in form
✅ Submit button clicked
📅 Generating calendar event...
✅ Calendar file generated: ai-engineer-summit-2025.ics
🎉 Automation completed successfully!
```

### Bookmarklet Usage
1. Install the bookmarklet in your browser
2. Visit any website (works great on apply.ai.engineer)
3. Click the "AI Engineer Calendar" bookmark
4. Calendar event downloads automatically
5. Open the .ics file in your preferred calendar app

## 📅 Generated Calendar Event Details

The generated calendar event includes:

- **Event Name**: AI Engineer Summit 2025
- **Dates**: November 19-22, 2025 (4 days)
- **Time**: 9:00 AM - 5:00 PM (estimated)
- **Location**: New York, New York
- **Description**: Complete event details and website link
- **Reminders**: 1 day before and 1 hour before
- **Website**: https://apply.ai.engineer/
- **Categories**: CONFERENCE, TECHNOLOGY, AI

## 🔧 Automation Features

### Email Signup Automation
- Automatically detects email input fields
- Fills in provided email address
- Submits the signup form
- Handles various form structures

### Event Information Extraction
- Parses website content for event details
- Extracts dates, location, and descriptions
- Saves information for future use
- Creates structured data output

### External Form Discovery
- Finds speaker application links
- Locates volunteer signup forms  
- Identifies sponsor contact information
- Provides direct navigation options

## 🛡️ Privacy & Security

- **No data collection**: All scripts run locally
- **No external API calls**: Except to the AI Engineer website
- **Open source**: All code is visible and auditable
- **Minimal permissions**: Only accesses the target website

## 🚨 Important Notes

- **Event Status**: AI Engineer Summit 2025 is invite-only
- **Application Deadline**: September 15, 2025
- **Website**: https://apply.ai.engineer/
- **Automation Ethics**: Use responsibly and respect website terms of service

## 🐛 Troubleshooting

### Calendar Generator Issues
```bash
# If the script doesn't run
python3 calendar_generator.py

# Check file permissions
ls -la ai-engineer-summit-2025.ics
```

### Web Automation Issues
```bash
# Install browser drivers
playwright install

# Run with debug output
python web_automation.py --help

# Check screenshot output
ls ai_engineer_site.png
```

### Bookmarklet Issues
- Ensure you copied the complete JavaScript code
- Try refreshing the page before clicking bookmark
- Check browser console for errors (F12 → Console)

## 📖 Advanced Usage

### Customizing Event Details
Edit the `event_details` dictionary in `calendar_generator.py`:

```python
self.event_details = {
    'title': 'Your Custom Event',
    'start_date': datetime.datetime(2025, 11, 19, 9, 0),
    'location': 'Your Location',
    # ... other details
}
```

### Automation Scripting
Use the web automation as a module:

```python
from web_automation import AIEngineerWebAutomation
import asyncio

async def custom_automation():
    automation = AIEngineerWebAutomation()
    await automation.start_browser()
    await automation.navigate_to_site()
    # Your custom automation logic
    await automation.close_browser()

asyncio.run(custom_automation())
```

## 🤝 Contributing

Feel free to improve these automation tools:

1. Fork the project
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

These tools are for educational and personal use. Always respect website terms of service and use automation responsibly. The AI Engineer Summit is an invite-only event - please apply through official channels.
