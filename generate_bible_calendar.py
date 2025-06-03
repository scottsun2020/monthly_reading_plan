
import re
from datetime import datetime, timedelta

# Bible reading plan for 30 days of June
reading_plan = [
    "可一1-11/詩41/撒下9-10", "可一12-20/詩42/撒下11-12", "可一21-34/詩43/撒下13-14",
    "可一35-45/詩44/撒下15-16", "可二1-12/詩45/撒下17-18", "可二13-20/詩46/撒下19-20",
    "可二21-28/詩47/撒下21-22", "可三1-12/詩48/撒下23-24", "可三13-27/詩49/王上1-2",
    "可三28-35/詩50/王上3-4", "可四1-12/詩51/王上5-6", "可四13-20/詩52/王上7-8",
    "可四21-34/詩53/王上9-10", "可四35-41/詩54/王上11-12", "可五1-20/詩55/王上13-14",
    "可五21-34/詩56/王上15-16", "可五35-43/詩57/王上17-18", "可六1-13/詩58/王上19-20",
    "可六14-29/詩59/王上21-22", "可六30-44/詩60/王下1-2", "可六45-56/詩61/王下3-4",
    "可七1-13/詩62/王下5-6", "可七14-23/詩63/王下7-8", "可七24-37/詩64/王下9-10",
    "可八1-10/詩65/王下11-12", "可八11-21/詩66/王下13-14", "可八22-30/詩67/王下15-16",
    "可八31-38/詩68/王下17-18", "可九1-13/詩69/王下19-20", "可九14-22/詩70/王下21-22"
]

# Mapping book names to bible.com codes
book_url_map = {
    "可": "MRK", "詩": "PSA", "撒下": "2SA", "王上": "1KI", "王下": "2KI"
}

# Chinese to Arabic number conversion
chinese_to_arabic = {
    "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7",
    "八": "8", "九": "9", "十": "10"
}

def convert_chinese_number(ch):
    for c, d in chinese_to_arabic.items():
        ch = ch.replace(c, d)
    return ch

def extract_chapter_fixed(book_chapter):
    match = re.match(r'([^\d]+)([\d]+)([\d\-]*)', book_chapter)
    if match:
        book = match.group(1)
        chapter_chinese = match.group(2)
        chapter = convert_chinese_number(chapter_chinese)
        return book, chapter
    return None, None

def make_bible_link(part):
    book, chapter = extract_chapter_fixed(part)
    if book in book_url_map and chapter:
        return f"https://www.bible.com/zh-CN/bible/46/{book_url_map[book]}.{chapter}.CUNP"
    return ""

def format_datetime(dt):
    return dt.strftime("%Y%m%dT070000")

# Start generating ICS
calendar_header = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\n"
calendar_footer = "END:VCALENDAR"
start_date = datetime(2025, 6, 1)
events = []

for i, entry in enumerate(reading_plan):
    event_date = start_date + timedelta(days=i)
    formatted_date = format_datetime(event_date)
    parts = entry.split('/')
    links = [make_bible_link(p.strip()) for p in parts]
    description_lines = [f"{p.strip()}: {link}" for p, link in zip(parts, links) if link]
    full_description = "\\n".join(description_lines)

    event = f"""BEGIN:VEVENT
DTSTAMP:{formatted_date}
DTSTART:{formatted_date}
SUMMARY:Day {i+1}: {entry}
DESCRIPTION:每日读经：{entry}\\n{full_description}
END:VEVENT
"""
    events.append(event)

ics_content = calendar_header + "".join(events) + calendar_footer

with open("june-bible-plan.ics", "w", encoding="utf-8") as f:
    f.write(ics_content)

print("✅ Calendar file generated: june-bible-plan.ics")
