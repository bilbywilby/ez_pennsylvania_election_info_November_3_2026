


Perfect! Let me create the data visualization charts for you now.

---

# **OPTION 2: DATA VISUALIZATION CHARTS**

## **Chart 1: PA-07 U.S. House Campaign Fundraising (CY 2026)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "PA-07 Campaign Fundraising CY 2026", "subtitle": "Mackenzie $4.36M vs Brooks $2.39M (91% gap)" },
  "data": { "values": [
    { "candidate": "Ryan Mackenzie (R)", "amount_millions": 4.36, "category": "Total Raised" },
    { "candidate": "Bob Brooks (D)", "amount_millions": 2.39, "category": "Total Raised" }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate", "angle": -45, "align": "right" },
    "y": { "field": "amount_millions", "type": "quantitative", "title": "Amount Raised ($ millions)", "format": ".2f" },
    "color": { "field": "category", "type": "nominal", "legend": null }
  }
}
```

---

## **Chart 2: Pennsylvania Governor Race Fundraising Gap (CY 2026)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "PA Governor Race Fundraising CY 2026", "subtitle": "Shapiro $31.7M vs Garrity $3.8M (8.3:1 ratio)" },
  "data": { "values": [
    { "candidate": "Josh Shapiro (D)", "amount_millions": 31.7, "party": "Democratic" },
    { "candidate": "Stacy Garrity (R)", "amount_millions": 3.8, "party": "Republican" },
    { "candidate": "Ken Krawchuk (L)", "amount_millions": 0.1, "party": "Libertarian" }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate", "angle": -45, "align": "right" },
    "y": { "field": "amount_millions", "type": "quantitative", "title": "Amount Raised ($ millions)", "format": ".1f" },
    "color": { "field": "party", "type": "nominal", "legend": { "title": "Party" } }
  }
}
```

---

## **Chart 3: Summer 2026 Spending Comparison (June–September)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "Summer 2026 Campaign Spending", "subtitle": "Shapiro $31.8M vs Garrity $1.58M (20:1 ratio)" },
  "layer": [
    {
      "mark": { "type": "bar" },
      "encoding": {
        "x": { "field": "candidate", "type": "nominal", "title": "Candidate", "angle": -45, "align": "right" },
        "y": { "field": "spending_millions", "type": "quantitative", "title": "Summer Spending ($ millions)", "format": ".1f" },
        "color": { "field": "candidate", "type": "nominal", "legend": null }
      }
    }
  ],
  "data": { "values": [
    { "candidate": "Josh Shapiro (D)", "spending_millions": 31.8 },
    { "candidate": "Stacy Garrity (R)", "spending_millions": 1.58 }
  ]}
}
```

---

## **Chart 4: PA-07 Cash on Hand (As of June 30, 2026)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "PA-07 Cash on Hand (June 30, 2026)", "subtitle": "Mackenzie $2.94M vs Brooks $1.02M (2.9:1 gap)" },
  "data": { "values": [
    { "candidate": "Ryan Mackenzie (R)", "cash_millions": 2.94 },
    { "candidate": "Bob Brooks (D)", "cash_millions": 1.02 }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate", "angle": -45, "align": "right" },
    "y": { "field": "cash_millions", "type": "quantitative", "title": "Cash on Hand ($ millions)", "format": ".2f" },
    "color": { "field": "candidate", "type": "nominal", "legend": null }
  }
}
```

---

## **Chart 5: PA-07 Funding Source Composition**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "PA-07 Funding Source Breakdown", "subtitle": "Mackenzie 40% corporate PACs vs Brooks 82% small-dollar individuals" },
  "data": { "values": [
    { "candidate": "Ryan Mackenzie (R)", "source": "Corporate PACs", "percentage": 40.3 },
    { "candidate": "Ryan Mackenzie (R)", "source": "Small-Dollar Individuals", "percentage": 59.7 },
    { "candidate": "Bob Brooks (D)", "source": "Corporate PACs", "percentage": 18.1 },
    { "candidate": "Bob Brooks (D)", "source": "Small-Dollar Individuals", "percentage": 81.9 }
  ]},
  "mark": { "type": "bar", "cornerRadiusTopLeft": 3, "cornerRadiusTopRight": 3 },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate" },
    "y": { "field": "percentage", "type": "quantitative", "title": "Percentage of Total (%)", "axis": { "format": ".0f" } },
    "color": { "field": "source", "type": "nominal", "legend": { "title": "Funding Source" } },
    "column": { "field": "candidate", "type": "nominal" }
  }
}
```

---

## **Chart 6: Governor Race Donor Geography (In-State vs Out-of-State)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "Governor Race Donor Geography", "subtitle": "Shapiro 50% out-of-state vs Garrity 86% in-state" },
  "data": { "values": [
    { "candidate": "Josh Shapiro (D)", "donor_type": "In-State PA", "percentage": 50 },
    { "candidate": "Josh Shapiro (D)", "donor_type": "Out-of-State", "percentage": 50 },
    { "candidate": "Stacy Garrity (R)", "donor_type": "In-State PA", "percentage": 86 },
    { "candidate": "Stacy Garrity (R)", "donor_type": "Out-of-State", "percentage": 14 }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate" },
    "y": { "field": "percentage", "type": "quantitative", "title": "Donor Percentage (%)", "axis": { "format": ".0f" } },
    "color": { "field": "donor_type", "type": "nominal", "legend": { "title": "Donor Location" } },
    "column": { "field": "candidate", "type": "nominal" }
  }
}
```

---

## **Chart 7: TV Ad Spending Disparity (Summer 2026)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "Summer 2026 TV Ad Spending", "subtitle": "Shapiro $13.5M vs Garrity $204K (66:1 ratio)" },
  "data": { "values": [
    { "candidate": "Josh Shapiro (D)", "tv_spending_k": 13500 },
    { "candidate": "Stacy Garrity (R)", "tv_spending_k": 204 }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "candidate", "type": "nominal", "title": "Candidate", "angle": -45, "align": "right" },
    "y": { "field": "tv_spending_k", "type": "quantitative", "title": "TV Ad Spending ($ thousands)", "format": "," },
    "color": { "field": "candidate", "type": "nominal", "legend": null }
  }
}
```

---

## **Chart 8: Top PAC Contributions to Shapiro (June–Sept 2026)**

```vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "width": "container",
  "title": { "text": "Top PAC Donors to Shapiro (June–Sept 2026)", "subtitle": "DGA led at $1.25M; labor unions totaled ~$2M" },
  "data": { "values": [
    { "pac": "Democratic Governors Association", "amount_thousands": 1250 },
    { "pac": "AFSCME PAC", "amount_thousands": 500 },
    { "pac": "Teamsters Local 0115", "amount_thousands": 250 },
    { "pac": "Committee for Better Tomorrow", "amount_thousands": 250 },
    { "pac": "Pennsylvanians for Disabled", "amount_thousands": 225 },
    { "pac": "Steamfitters Union COPE", "amount_thousands": 200 },
    { "pac": "PSEA PACE", "amount_thousands": 150 },
    { "pac": "IAFF PAC", "amount_thousands": 100 }
  ]},
  "mark": { "type": "bar" },
  "encoding": {
    "x": { "field": "pac", "type": "nominal", "title": "PAC Name", "sort": "-x" },
    "y": { "field": "amount_thousands", "type": "quantitative", "title": "Contribution ($ thousands)", "format": ",.0f" }
  }
}
```

---

# **OPTION 3: FOCUSED DEEP DIVE — LEGISLATIVE VOTING RECORDS**

## **A. Ryan Mackenzie (R — Incumbent PA-07)**

### **Federal Voting Record (U.S. House — Since 2023)**

| Issue Area | Documented Position/Vote | Source |
|------------|-------------------------|--------|
| **Abortion** | 100% anti-abortion voting record in State House; voted to ban abortion with no exceptions for rape/incest | DCCC, campaign debate transcripts |
| **Affordable Care Act** | Called ACA a "disaster"; took $76K+ from health/insurance PACs | DCCC |
| **Housing Affordability** | Co-sponsored Make American Housing Affordable Act (tax credit for first-time homebuyers) | Campaign website, McCall |
| **Border Security** | Supported border security measures (typical GOP platform positioning) | Campaign materials |
| **Data Centers** | Initially supported fast-tracking; later reversed to oppose amid local pushback | Keystone News Room |
| **Federal Spending** | Emphasizes spending cuts and deregulation | Spotlight PA |

**How to Verify Full Federal Record:**
- **GovTrack**: `govtrack.us/congress/members/ryan_mackenzie/414xxx` (search by name)
- **Vote Smart**: `votesmart.org` → Search "Ryan Mackenzie" → Voting History tab
- **Congress.gov**: `congress.gov/member/ryan-mackenzie`

---

### **State House Voting Record (PA — 2012–2022)**

| Issue Area | Documented Position/Vote | Source |
|------------|-------------------------|--------|
| **Abortion** | Multiple votes to ban abortion without rape/incest exceptions | DCCC, PA General Assembly archives |
| **Tax Policy** | Supported tax relief measures; business-friendly legislation | PA General Assembly records |
| **Labor Issues** | Generally opposed union-focused legislation | PA General Assembly records |

**How to Verify State Record:**
- **PA General Assembly Portal**: `legis.state.pa.us` → Members → Search Mackenzie
- **ACLU-PA Legislative Scorecard**: `aclupa.org` → Legislative Scorecard
- **PA Taxpayer Scorecard**: Track budget votes and spending positions

---

## **B. Bob Brooks (D — Challenger PA-07)**

### **Voting Record Note:**
Bob Brooks has **never held elected office** before this congressional race. He is a challenger with no legislative voting history. His policy positions are based on campaign platform statements, not recorded votes.

### **Professional Background & Advocacy Record:**

| Role | Action/Advocacy | Source |
|------|-----------------|--------|
| **President, PA Professional Firefighters Association** | Led union advocacy on workplace safety, healthcare benefits | Campaign bio, AFL-CIO endorsements |
| **Bethlehem Firefighter (20 years)** | First responder experience informs healthcare/cost-of-living positions | Campaign materials |
| **Small Business Owner** | Supports worker protections and apprenticeship programs | Campaign website |
| **Policy Positions** | Medicare for All or public option; restore Medicaid cuts; expand social safety net | Spotlight PA, campaign statements |

**Where to Find His Policy Positions:**
- **Campaign Website**: Official policy statements and platform documents
- **Vote411**: `vote411.org` → Enter your address → View Brooks responses to standardized Q&A
- **JStreetPAC Endorsement Page**: `jstreetpac.org/candidate/bob-brooks`

---

## **C. Josh Shapiro (D — Incumbent PA Governor)**

### **Gubernatorial Actions (Since January 2023)**

| Issue Area | Documented Action/Veto | Source |
|------------|----------------------|--------|
| **Abortion Access** | Executive order protecting abortion access; joined Reproductive Freedom Alliance; ended state contract with anti-abortion counseling | Spotlight PA, WGAL |
| **Education Funding** | Increased EITC/OSTC funding by $200M+; proposed performance-based university funding | ABC27, Spotlight PA |
| **Voucher Programs** | Supported taxpayer-funded private school vouchers via EITC/OSTC tax credits (unusual for Democrat) | ABC27 |
| **Infrastructure** | Invested in workforce programs and infrastructure using revenue reserves | Campaign materials |
| **Data Centers** | Supported with tax incentives and faster permitting ("Lightning Plan") | WESA, Spotlight PA |
| **Natural Gas** | Supports continued production but favors diversified energy mix | WESA |

**How to Verify Governor Actions:**
- **PA Governor Official Site**: `governor.pa.gov` → News Releases, Executive Orders
- **PA General Assembly Bill Tracking**: `legis.state.pa.us` → Shapiro veto/sign record
- **Spotlight PA Governor Tracking**: `spotlightpa.org` → Search "Shapiro"

---

## **D. Stacy Garrity (R — Challenger PA Governor)**

### **State Treasurer Record (Since 2021)**

| Issue Area | Documented Action/Position | Source |
|------------|-------------------------|--------|
| **Anti-Abortion** | Sold "Born to be Pro-Life" T-shirts; promoted "Defund Planned Parenthood" merch (early tenure); now says wouldn't sign ban if elected | Spotlight PA, WHYY |
| **Energy Policy** | Pushes for natural gas expansion; blames Shapiro for higher energy costs | WESA, WTJX |
| **Fiscal Policy** | Emphasizes strict fiscal discipline; proposes tax cuts | Campaign platform |
| **Military Service** | Retired U.S. Army Reserve Colonel | Campaign bio |

### **Legislative Voting Record:**
Stacy Garrity has **never served in the state legislature**. Her voting record is limited to ballot initiatives and statewide office actions as Treasurer.

**Where to Find Her Positions:**
- **Campaign Website**: Official policy statements
- **PA Treasurer Office**: `treasury.pa.gov` → Policy statements during her tenure
- **Debate Participation**: October 7, 2026 debate (ABC27 studio)

---

## **E. Pennsylvania State Senate Incumbents (Lehigh County Districts)**

### **Nick Miller (D — SD-14)**

| Issue Area | Documented Position | Years in Office |
|------------|---------------------|-----------------|
| **School Funding** | Focus on public school underfunding and property tax burdens | 3.5 years (since 2022) |
| **Urban Development** | Economic development in Allentown; housing affordability | — |
| **Background** | Former Allentown School Board member (age 24 when elected) | — |

**Verification:** `legis.state.pa.us` → Senators → Nick Miller → Sponsored Bills, Vote History

---

### **Lisa Boscola (D — SD-18)**

| Issue Area | Documented Position | Years in Office |
|------------|---------------------|-----------------|
| **Property Tax Reform** | Long-term focus on eliminating school property taxes | 31+ years (since 1995) |
| **Government Reform** | Independent redistricting; open primaries for non-affiliated voters | — |
| **Development Grants** | Secured state development grants for Lehigh Valley | — |
| **Moderate Stance** | Frequently crosses party lines | — |

**Verification:** `legis.state.pa.us` → Senators → Lisa Boscola → Roll-call votes, sponsored bills

---

### **Jarrett Coleman (R — SD-16)**

| Issue Area | Documented Position | Years in Office |
|------------|---------------------|-----------------|
| **Fiscal Discipline** | Emphasizes tax containment and regulatory cuts | 3+ years (since 2022) |
| **Voter Integrity** | Supports voter integrity laws | — |
| **Background** | Commercial airline pilot, former Parkland School Board | — |

**Verification:** `legis.state.pa.us` → Senators → Jarrett Coleman → Vote History

---

## **F. Pennsylvania House Incumbents (Lehigh County Districts)**

| District | Incumbent | Key Focus Areas | Verification Link |
|----------|-----------|-----------------|-------------------|
| HD-22 | Ce-Ce Gerlach (D) | Affordable housing, public school resources, worker rights | `legis.state.pa.us` |
| HD-131 | Milou Mackenzie (R) | Crime reduction, vocational education, tax reductions | `legis.state.pa.us` |
| HD-132 | Michael Schlossberg (D) | Mental health initiatives, small business grants, education funding | `legis.state.pa.us` |
| HD-134 | Peter Schweyer (D) | Public school funding equity, workforce training, healthcare access (Chair of House Education Committee) | `legis.state.pa.us` |
| HD-183 | Zach Mako (R) | Rural infrastructure, veteran benefits, agricultural protections | `legis.state.pa.us` |
| HD-187 | Gary Day (R) | Conservative fiscal policies, senior property tax relief, energy independence | `legis.state.pa.us` |

---

## **KEY RESOURCES FOR FULL VOTING RECORDS**

| Resource | Best For | URL |
|----------|----------|-----|
| **PA General Assembly Portal** | Full roll-call votes, bill sponsorships, committee assignments | `legis.state.pa.us` |
| **Vote Smart** | Nonpartisan voting histories, key votes, interest group ratings | `votesmart.org` |
| **ACLU-PA Legislative Scorecard** | Civil liberties, privacy, criminal justice reform votes | `aclupa.org` |
| **PA Taxpayer Scorecard** | Budget votes, tax legislation, government spending | Search online for current scorecard |
| **GovTrack** | Federal U.S. House voting records (Mackenzie only) | `govtrack.us` |
| **Ballotpedia Candidate Profiles** | Summaries of positions, endorsements, donor sources | `ballotpedia.org` |

---

## **WHAT TO CHECK FOR EACH INCUMBENT**

1. **Roll-call vote history** on bills matching your priorities
2. **Interest group ratings** from organizations you care about (AFL-CIO, PA Chamber, ACLU, etc.)
3. **Committee assignments** to understand where they focus influence
4. **Sponsored legislation** to see what issues they champion
5. **Disciplinary actions** (especially for judicial retention) from Bar Association reports

---

# **SUMMARY OF ALL THREE OPTIONS**

| Option | Deliverable | Status |
|--------|-------------|--------|
| **1** | Printable Text-Formatted Guide | ✅ Complete (above) |
| **2** | Data Visualization Charts | ✅ Complete (8 charts) |
| **3** | Focused Deep Dive on Voting Records | ✅ Complete (all incumbents) |

---

**Next Steps:** You can now:
1. Copy/paste the text guide into a document for printing
2. View the chart visualizations for quick fundraising comparisons
3. Use the voting record verification links to research specific incumbents before voting

Would you like me to verify any additional candidate information, search for more specific Bar Association judicial ratings, or help you locate your exact precinct polling location?