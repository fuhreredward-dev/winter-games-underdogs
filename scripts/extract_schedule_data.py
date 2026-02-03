"""
Extract schedule data from schedule.html and create schedule-data.json

This script parses the HTML to extract:
- All days with dates
- All events with sports and times
- All nations with athlete counts and tier levels
- Confirmed status (indicated by ✓ vs ?)

Output: data/schedule-data.json
"""

import json
import re
from pathlib import Path
from datetime import datetime


def extract_schedule_data(html_file: str) -> dict:
    """Extract schedule data from HTML file."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    schedule = {}
    
    # Find all day sections - be more flexible with closing tag
    day_pattern = r'<div class="day-section" data-date="([^"]+)">(.+?)(?=<div class="day-section"|$)'
    day_matches = re.finditer(day_pattern, html, re.DOTALL)
    
    for day_match in day_matches:
        date = day_match.group(1)
        day_content = day_match.group(2)
        
        schedule[date] = {
            'date': date,
            'events': []
        }
        
        # Extract day title
        title_match = re.search(r'<div class="day-title">([^<]+)</div>', day_content)
        if title_match:
            schedule[date]['title'] = title_match.group(1)
        
        # Find all events in this day - match from event-card to next event-card or end
        event_pattern = r'<div class="event-card" data-sport="([^"]+)">(.+?)(?=<div class="event-card"|$)'
        event_matches = re.finditer(event_pattern, day_content, re.DOTALL)
        
        for event_match in event_matches:
            sport = event_match.group(1)
            event_content = event_match.group(2)
            
            # Extract event title
            title_match = re.search(r'<div class="event-title">([^<]+)</div>', event_content)
            event_title = title_match.group(1) if title_match else 'Unknown Event'
            
            # Extract time
            time_match = re.search(r'<div class="event-time">([^<]+)</div>', event_content)
            time = time_match.group(1) if time_match else ''
            
            # Extract nations
            nations = []
            nation_pattern = r'<div class="nation-pill\s+([^"]*)" data-nation="([^"]+)">(.+?)</div>'
            nation_matches = re.finditer(nation_pattern, event_content, re.DOTALL)
            
            for nation_match in nation_matches:
                classes = nation_match.group(1).strip()
                nation_name = nation_match.group(2)
                nation_html = nation_match.group(3)
                
                # Extract athlete count
                count_match = re.search(r'<span class="athlete-count">(\d+)</span>', nation_html)
                athlete_count = int(count_match.group(1)) if count_match else 1
                
                # Extract tier
                tier_match = re.search(r'tier-(\d)', classes)
                tier = int(tier_match.group(1)) if tier_match else 3
                
                # Check if confirmed (has ✓ instead of ?)
                confirmed = '✓' in nation_html
                
                nations.append({
                    'name': nation_name,
                    'count': athlete_count,
                    'tier': tier,
                    'confirmed': confirmed
                })
            
            schedule[date]['events'].append({
                'sport': sport,
                'title': event_title,
                'time': time,
                'nations': nations
            })
    
    return schedule


def save_schedule_data(data: dict, output_file: str = 'data/schedule-data.json'):
    """Save extracted schedule data to JSON."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved schedule data to {output_file}")


def main():
    html_file = 'schedule.html'
    
    if not Path(html_file).exists():
        print(f"❌ File not found: {html_file}")
        return 1
    
    print("📊 Extracting schedule data from HTML...")
    
    schedule = extract_schedule_data(html_file)
    
    # Count stats
    total_events = sum(len(day['events']) for day in schedule.values())
    total_nations = sum(
        len(event['nations'])
        for day in schedule.values()
        for event in day['events']
    )
    confirmed_nations = set()
    for day in schedule.values():
        for event in day['events']:
            for nation in event['nations']:
                if nation['confirmed']:
                    confirmed_nations.add(nation['name'])
    
    print(f"✓ Extracted:")
    print(f"  - {len(schedule)} days")
    print(f"  - {total_events} events")
    print(f"  - {total_nations} nation participations")
    print(f"  - {len(confirmed_nations)} confirmed nations")
    
    # Save the data
    Path('data').mkdir(exist_ok=True)
    save_schedule_data(schedule)
    
    print("\n✅ Schedule data extraction complete!")
    return 0


if __name__ == '__main__':
    exit(main())
