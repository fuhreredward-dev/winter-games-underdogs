# � 2026 Winter Olympics - Underdog Nations Tracker

### Milano-Cortina 2026 🇮🇹 | February 6-22, 2026

> Interactive website tracking underdog nations and their compelling stories at the Winter Olympics

An interactive, tier-based system for discovering and following underdog nations competing in the 2026 Winter Olympics.

## 🎯 What is an Underdog Nation?

Nations are classified into **5 tiers** based on **7 criteria**:

1. **< 5 Athletes** - Minimal team size
2. **No Olympic Gold Medals** - Never won any Olympic gold
3. **No Olympic Medals** - Never won any Olympic medals
4. **Population Under 1M** - Small nation size
5. **No Winter Olympic Gold** - Never won Winter Olympic gold
6. **No Winter Olympic Medals** - Never won Winter Olympic medals
7. **Southern Hemisphere** - Located below the equator (facing unique winter sports challenges)

### Tier System

- **Tier 5** (6-7 criteria): Ultimate Underdogs 🔴
- **Tier 4** (4-5 criteria): Major Underdogs 🟠
- **Tier 3** (3 criteria): Strong Underdogs 🟡
- **Tier 2** (2 criteria): Moderate Underdogs 🟨
- **Tier 1** (1 criterion): Mild Underdogs 🔵

## 📊 Features

- **Overview Statistics** - Total nations, underdog breakdown by tier
- **Interactive Criteria Dropdowns** - Click to see which nations meet each criterion
- **Daily Schedule View** - See what events are happening each day and which underdogs compete
- **Nation Cards by Tier** - Browse all underdog nations organized by tier with competing dates
- **Sports Rankings** - See which sports have the most participating nations

## 🌍 View the Live Site

**GitHub Pages:** [View the interactive site here](#) *(Enable GitHub Pages in repository settings)*

## 🗂️ Data Sources

All data compiled from:
- Wikipedia (medal tables, participating nations, sport participation by nation)
- Official Olympic sources
- Population data

## 🛠️ Technical Details

## 🛠️ Technical Details

### Project Structure
```
├── data/
│   ├── schedule/                      # Olympic schedule (Feb 6-22, 2026)
│   ├── medals/                        # Winter & all-time medal data
│   ├── population/                    # Population by nation
│   ├── athlete_counts_2026.json       # Athlete counts per nation
│   ├── nation_sports_participation_2026.json  # Sport participation by nation
│   └── participating_nations_2026.json # All 85 participating nations
├── scripts/
│   └── generate_html_overview.py      # HTML generator
├── index.html                         # Main site (for GitHub Pages)
└── README.md
```

### Regenerate the Site

To update the HTML with new data:

```bash
python scripts/generate_html_overview.py
```

This will regenerate both `olympics_overview.html` and `index.html`.

## 🚀 Deploy to GitHub Pages

1. **Create a GitHub repository** for this project
2. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```
3. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`
   - Save

Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

## 📅 Competition Schedule

**February 6-22, 2026** | Milan-Cortina d'Ampezzo, Italy

---

*Last updated: January 21, 2026*
```bash
python main.py --date 2026-02-07
```

Generate watchlist for today:
```bash
python main.py
```

Generate for all days in Olympics:
```bash
python main.py --all
```

## Output Format
Each daily watchlist includes:
- Nation (name and IOC code)
- Sport/Discipline/Event
- Session time (if available)
- Underdog criteria met

Plus a medals-per-capita sidebar ranking.

## Notes
- Updates once per day (not real-time)
- Schedule-first approach: only nations in the schedule are included
- Late entry list changes may not be reflected until next update
