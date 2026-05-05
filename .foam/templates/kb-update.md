---
foam_template:
  name: "KB Update"
  description: "Create a knowledge base article note"
  filepath: "docs/kb-updates/$FOAM_TITLE.md"
kb_number: ${1:KB-XXXX}
title: ${2:Article Title}
category: ${3:Category}
status: ${4|Draft,Review,Published,Not-Started|}
note: ${5:Brief overview}
tags:
  - kb-updates
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
---

# 📚 ${1} — ${2}

## 📖 Problem Statement

${5}

## 📝 Details

${6:Detailed description}

## 🔗 Related Cases

$0

## Solution

${7:Detailed description}