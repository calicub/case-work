---
foam_template:
  name: "KB Article"
  description: "General knowledge base article — how-to, reference, or troubleshooting"
  filepath: "docs/pkb/$FOAM_SLUG.md"
title: ${1:Title}
category: ${2|Tools,Troubleshooting,Kubernetes,General|}
type: ${3|how-to,reference,troubleshooting,concept|}
tags:
  - ${4:product-tag}
  - ${5:topic-tag}
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
---

# ${1}

???+ abstract "Summary"

    ${6:One or two sentence description of what this article covers and who it is for.}

---

## Overview

${7:Background context — what is this feature/component, and why does this matter?}

---

## ${8:Section Title}

${9:Content for this section. Add more H2 sections as needed.}

---

## :material-alert: Common Issues

!!! warning "${10:Issue Title}"
    ${11:Describe the issue, symptom, or error message.}

    **Cause:** ${12:Root cause explanation.}

    **Resolution:**

    ${13:Step-by-step fix or workaround.}

---

## :fontawesome-solid-book-atlas: References

| Source | Link | Notes |
| ------ | ---- | ----- |
| ${14:Source} | ${15:URL} | ${16:Notes} |

---

## :lucide-file-text: Related Articles

- [[${17:related-article-slug}]]

$0
