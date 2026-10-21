---
foam_template:
  name: "PKB Note"
  description: "Topic overview — collects the helpful KBs, engineering tickets, Confluence pages and doc links for one area"
  filepath: "docs/pkb/$FOAM_SLUG.md"
title: ${1:Title}
category: ${2|Tools,Troubleshooting,Kubernetes,Other|}
tags:
  - ${3:product-tag}
  - ${4:topic-tag}
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
---

# ${1}

## 📝 Overview

${5:Notes and context}

## 📋 KB Articles

| KB Link | Notes |
| ------- | ----- |
| ${6:link} | ${7:note} |

## 🔧 Engineering Tickets

| Ticket # | Fixed Version | Notes |
| ----- | ------------- | ----- |
| ${8:PROJ-1234} | ${9:version} | ${10:note} |

## 📘 Confluence

| Link | Description |
| ---- | ----------- |
| ${11:link} | ${12:description} |

## 📄 Doc References

| Link | Description |
| ---- | ----------- |
| ${13:link} | ${14:description} |

$0
