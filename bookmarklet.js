/**
 * AI Engineer Summit 2025 Calendar Event Generator Bookmarklet
 * 
 * Copy the minified version below and save it as a bookmark in your browser.
 * When clicked, it will generate and download a calendar event (.ics file)
 * for the AI Engineer Summit 2025.
 */

// Full readable version (for development and understanding)
function aiEngineerCalendarBookmarklet() {
    // Event details
    const event = {
        title: "AI Engineer Summit 2025",
        start: "20251119T090000Z",
        end: "20251122T170000Z", 
        location: "New York, New York",
        description: "The premier technical AI summit for AI Engineers & AI Leaders who ship. Invite-only, curated for top AI Engineers.\\n\\nWebsite: https://apply.ai.engineer/",
        url: "https://apply.ai.engineer/"
    };
    
    // Generate ICS content
    const ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0", 
        "PRODID:-//AI Engineer Summit//Bookmarklet//EN",
        "BEGIN:VEVENT",
        `UID:aie-summit-2025-${Date.now()}@ai.engineer`,
        `DTSTART:${event.start}`,
        `DTEND:${event.end}`,
        `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z`,
        `SUMMARY:${event.title}`,
        `LOCATION:${event.location}`,
        `DESCRIPTION:${event.description}`,
        `URL:${event.url}`,
        "STATUS:CONFIRMED",
        "BEGIN:VALARM",
        "TRIGGER:-P1D",
        "ACTION:DISPLAY", 
        "DESCRIPTION:AI Engineer Summit 2025 tomorrow!",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR"
    ].join('\r\n');
    
    // Create and download file
    const blob = new Blob([ics], {type: 'text/calendar'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-engineer-summit-2025.ics';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Show notification
    const notify = document.createElement('div');
    notify.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;background:#10b981;color:white;padding:15px;border-radius:8px;font-family:Arial,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.15);';
    notify.textContent = '✅ AI Engineer Summit 2025 calendar event downloaded!';
    document.body.appendChild(notify);
    setTimeout(() => notify.remove(), 4000);
}

// Minified bookmarklet (copy this entire line and save as bookmark)
// javascript:(function(){const e={title:"AI Engineer Summit 2025",start:"20251119T090000Z",end:"20251122T170000Z",location:"New York, New York",description:"The premier technical AI summit for AI Engineers & AI Leaders who ship. Invite-only, curated for top AI Engineers.\\n\\nWebsite: https://apply.ai.engineer/",url:"https://apply.ai.engineer/"};const t=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//AI Engineer Summit//Bookmarklet//EN","BEGIN:VEVENT",`UID:aie-summit-2025-${Date.now()}@ai.engineer`,`DTSTART:${e.start}`,`DTEND:${e.end}`,`DTSTAMP:${new Date().toISOString().replace(/[-:]/g,'').split('.')[0]}Z`,`SUMMARY:${e.title}`,`LOCATION:${e.location}`,`DESCRIPTION:${e.description}`,`URL:${e.url}`,"STATUS:CONFIRMED","BEGIN:VALARM","TRIGGER:-P1D","ACTION:DISPLAY","DESCRIPTION:AI Engineer Summit 2025 tomorrow!","END:VALARM","END:VEVENT","END:VCALENDAR"].join('\r\n');const n=new Blob([t],{type:'text/calendar'});const o=URL.createObjectURL(n);const a=document.createElement('a');a.href=o;a.download='ai-engineer-summit-2025.ics';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(o);const r=document.createElement('div');r.style.cssText='position:fixed;top:20px;right:20px;z-index:9999;background:#10b981;color:white;padding:15px;border-radius:8px;font-family:Arial,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.15);';r.textContent='✅ AI Engineer Summit 2025 calendar event downloaded!';document.body.appendChild(r);setTimeout(()=>r.remove(),4000);})();

/*
BOOKMARKLET INSTALLATION INSTRUCTIONS:

1. Copy the minified javascript code above (the line starting with javascript:)
2. In your browser, create a new bookmark:
   - Chrome: Ctrl+Shift+O > Add new bookmark
   - Firefox: Ctrl+Shift+B > Add bookmark
   - Safari: Cmd+Option+B > Add bookmark
3. Name it: "AI Engineer Calendar"
4. Paste the javascript code as the URL
5. Save the bookmark

USAGE:
- Visit any website (works best on apply.ai.engineer)
- Click the "AI Engineer Calendar" bookmark
- The .ics file will download automatically
- Open the file with any calendar app to add the event

The generated calendar event includes:
- Event: AI Engineer Summit 2025
- Dates: November 19-22, 2025
- Location: New York, New York
- Reminder: 1 day before the event
- Website link and description
*/