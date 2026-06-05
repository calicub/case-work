---
foam_template:
  name: "New Case"
  description: "Create a new support case note"
  filepath: "docs/cases/active/$FOAM_TITLE.md"
case_number: $FOAM_TITLE
customer: ${1:Customer Name}
priority: ${2|P1,P2,P3,P4|}
status: ${3|Open,In Progress,Pending Customer,Escalated,Resolved|}
note: ${4:One-line description}
tags:
  - active
created: $CURRENT_YEAR-$CURRENT_MONTH-$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE
---

# 📝 $FOAM_TITLE - ${1}

=== "📋 Notes"

    ## 🔍 Description

    !!! quote "Case Description"

        ${5:Describe the issue}

    ## 🔔 Next Action

    ## 🔄 Follow-up

    ## 🛠️ Steps Taken

=== "📎 Customer Files"

=== "📸 Screenshots"
