---
foam_template:
  name: "PKB Note"
  description: "Personal knowledge base note"
  filepath: "docs/pkb/$FOAM_SLUG.md"
title: ${1:Title}
category: ${2|Tools,Troubleshooting|}
tags:
  - ${3:product-tag}
  - ${4:topic-tag}
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
---

# ${1}

## 📝 Overview

${4:Notes and context}

## 📋 KB Articles

| KB Link | Notes |
| ------- | ----- |
| ${5:link} | ${6:note} |

## 🔧 Engineering Tickets

| Ticket # | Fixed Version | Notes |
| ----- | ------------- | ----- |
| ${7:PROJ-1234} | ${8:version} | ${9:note} |

## 📘 Confluence

| Link | Description |
| ---- | ----------- |
| ${10:link} | ${11:description} |

## 📄 Doc References

| Link | Description |
| ---- | ----------- |
| ${12:link} | ${13:description} |

$0
