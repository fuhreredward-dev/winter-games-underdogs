"""
Simple entry list parser - identifies nations to confirm.

This script parses your daily entry list file and tells you which nations
should be marked as confirmed in the HTML.

Usage:
    python scripts/parse_entry_list_simple.py 20260206
    
Output:
    Lists all nations from your entry file so you can tell me which ones to confirm.
"""

import re
from pathlib import Path
from datetime import datetime


def parse_entry_list(filepath: str) -> dict:
    """Parse entry list and return structured data."""
    entries = {}
    current_sport = None
    current_event = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if not line or line.lower().startswith('note'):
            continue
        
        # Sport header (no apostrophe, typically short)
        if line.endswith(':') and current_sport is None:
            current_sport = line[:-1]
            if current_sport not in entries:
                entries[current_sport] = {}
            continue
        
        # Event header (has apostrophe or longer)
        if line.endswith(':') and current_sport and current_event is None:
            current_event = line[:-1]
            if current_event not in entries[current_sport]:
                entries[current_sport][current_event] = []
            continue
        
        # Check if we found a new sport
        if line.endswith(':') and current_sport and current_event:
            if "'" not in line and len(line) < 20:
                current_sport = line[:-1]
                if current_sport not in entries:
                    entries[current_sport] = {}
                current_event = None
                continue
            else:
                current_event = line[:-1]
                if current_event not in entries[current_sport]:
                    entries[current_sport][current_event] = []
                continue
        
        # Parse nation entry
        match = re.match(r'^(.+?)\s*\((\d+)\)\s*$', line)
        if match and current_sport and current_event:
            nation = match.group(1).strip()
            count = int(match.group(2))
            entries[current_sport][current_event].append({
                'nation': nation,
                'count': count
            })
    
    return entries


def main():
    import sys
    
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime('%Y%m%d')
    
    entry_file = Path(f'data/daily updates/{date_str}.txt')
    
    if not entry_file.exists():
        print(f"❌ File not found: {entry_file}")
        return 1
    
    print(f"\n📋 Entry List Parser - {date_str}")
    print("=" * 70)
    
    entries = parse_entry_list(entry_file)
    
    # Collect all unique nations
    all_nations = set()
    
    for sport, events in entries.items():
        print(f"\n{sport}:")
        for event, nations_list in events.items():
            print(f"  {event}:")
            for item in nations_list:
                nation = item['nation']
                count = item['count']
                all_nations.add(nation)
                print(f"    ✓ {nation} ({count})")
    
    print("\n" + "=" * 70)
    print(f"📊 SUMMARY")
    print("=" * 70)
    print(f"\nNations to confirm ({len(all_nations)}):")
    for nation in sorted(all_nations):
        print(f"  • {nation}")
    
    print("\n" + "=" * 70)
    print("👉 Copy the list above and tell me which nations to confirm!")
    print("=" * 70 + "\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
