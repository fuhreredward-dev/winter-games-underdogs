# 🎯 Simple Manual Entry List Update Workflow

## How It Works

Instead of automated HTML changes (which broke things), we'll use a **simple, manual approach**:

1. **You provide** the daily entry list
2. **I parse it** and show you which nations to confirm
3. **I make targeted HTML edits** to just those nations
4. **You review** and push

## Daily Workflow

### Step 1: Create Your Entry List File

After the Olympic day, create: `data/daily updates/YYYYMMDD.txt`

```
Bobsleigh:

Men's 2-Man:
Jamaica (1)
Brazil (2)

Women's Monobob:
Australia (1)

Freestyle Skiing:

Women's Halfpipe:
Ireland (1)

Notes:
- Historic day for Jamaica
```

### Step 2: Parse It

Run this to see which nations to confirm:

```bash
python scripts/parse_entry_list_simple.py 20260206
```

Output will look like:
```
📋 Entry List Parser - 20260206
======================================================================

Bobsleigh:
  Men's 2-Man:
    ✓ Jamaica (1)
    ✓ Brazil (2)
  Women's Monobob:
    ✓ Australia (1)

Freestyle Skiing:
  Women's Halfpipe:
    ✓ Ireland (1)

======================================================================
📊 SUMMARY
======================================================================

Nations to confirm (4):
  • Australia
  • Brazil
  • Ireland
  • Jamaica
```

### Step 3: Tell Me to Confirm Them

Share the output with me, or just tell me:
> "Please confirm these 4 nations: Australia, Brazil, Ireland, Jamaica"

### Step 4: I Make the Edits

I'll find each nation in the HTML and remove the "?" prefix:

**Before:**
```html
<span>? Jamaica</span>
```

**After:**
```html
<span>Jamaica</span>
```

### Step 5: Review & Push

Check the changes look good, then:
```bash
git add -A
git commit -m "Confirm entries for Feb 6: Jamaica, Brazil, Australia, Ireland"
git push
```

## Why This Approach?

✅ **Safe** - I make targeted edits, not automated replacements  
✅ **Visible** - You see exactly what changes  
✅ **Simple** - No complex scripts or data structures  
✅ **Fast** - Parser shows you exactly what to tell me  
✅ **Reversible** - Easy to fix if something goes wrong  

## Quick Reference

| Task | Command |
|------|---------|
| Parse entry list | `python scripts/parse_entry_list_simple.py YYYYMMDD` |
| Parse today | `python scripts/parse_entry_list_simple.py` |

## Example Workflow

**1. You send me:**
```
Please update entries for Feb 6.

📋 Entry List Parser - 20260206

Bobsleigh:
  Men's 2-Man:
    ✓ Jamaica (1)
    ✓ Brazil (2)

Nations to confirm (2):
  • Brazil
  • Jamaica
```

**2. I respond:**
"Got it! I'll confirm Brazil and Jamaica in schedule.html. [Makes edits]"

**3. You review:**
- Check that Brazil and Jamaica no longer have "?"
- Check they still appear in all the right places

**4. You push:**
```bash
git add -A && git commit -m "Confirm Feb 6 entries" && git push
```

**Done!** 🎉

---

## Nation Names to Use

Make sure nation names match exactly what's in your HTML:
- ✅ "Chinese Taipei" (not "Taiwan" or "TPE")
- ✅ "Trinidad and Tobago" (not "Trinidad")
- ✅ "Bosnia and Herzegovina" (full name)
- ✅ "Marshall Islands" (if participating)

The parser will show you exactly which names appear in your file, so just use those!
