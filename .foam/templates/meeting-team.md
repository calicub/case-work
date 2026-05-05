---
foam_template:
  name: "Team Meeting"
  description: "Meeting notes for team meetings"
  filepath: "docs/meetings/team/$FOAM_DATE_MONTH-$FOAM_DATE_DATE-$FOAM_DATE_YEAR_SHORT.md"
date: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
tags:
  - meetings
  - team
---

# 👥 Team Meeting — $CURRENT_MONTH/$CURRENT_DATE/$CURRENT_YEAR_SHORT

## 🙋 Attendees

- ${1:Name}

## 🗣️ Discussion Topics

- ${2:Topic}

## ✅ Action Items

- [ ] ${3:Action item}

$0
