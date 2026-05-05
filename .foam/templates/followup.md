---
foam_template:
  name: "Follow-up"
  description: "Create a follow-up note for an existing case"
  filepath: "docs/followup/$FOAM_TITLE.md"
case_number: $FOAM_TITLE
customer: ${1:Customer Name}
priority: ${2|P1,P2,P3,P4|}
status: ${3|Pending Customer,Awaiting Escalation,Scheduled,Monitoring|}
follow_up_date: ${4:YYYY-MM-DD}
note: ${5:Follow-up reason}
tags:
  - followup
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE
---

# 🔄 $FOAM_TITLE - ${1} (Follow-up)

## 📅 Follow-up Date

${4}

## 📋 Context

${6:Background on the case}

## ✅ Action Items

- [ ] ${7:Action}

$0
