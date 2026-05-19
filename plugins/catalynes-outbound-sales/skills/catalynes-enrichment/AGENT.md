# Catalyne Enrichment — Sub-Agent Brief

You are one of 10 parallel sub-agents enriching a batch of qualified sales leads with LinkedIn data via the Apify harvestapi scrapers. Be efficient: 2 actor calls total for the whole batch.

## YOUR INPUT

Read the file: `<WORKING_DIR>/enrich_batch_<N>.json` (substitute N — the orchestrator tells you which batch).

Each lead has: `row_number`, `full_name`, `linkedin_url`, `current_company_csv`, `current_job_csv`.

Typical batch size: 5-6 leads.

## TOOLS

- `mcp__Apify__call-actor` with `async: false` (waits for completion, returns dataset preview)
- `mcp__Apify__get-actor-output` to fetch full results via `datasetId` if the preview is incomplete

## JOB — 2 ACTOR CALLS TOTAL FOR THE WHOLE BATCH

### Call 1 — LinkedIn posts (last 2 per profile)

Actor: `harvestapi/linkedin-profile-posts`

Input:

```json
{
  "targetUrls": ["<all linkedin_url values from the batch>"],
  "maxPosts": 2,
  "includeQuotePosts": true,
  "includeReposts": true,
  "scrapeReactions": false,
  "scrapeComments": false
}
```

Returns up to 2 posts per profile (originals, quote-shares, reposts). Each item carries author info linking back to the profile URL.

### Call 2 — LinkedIn profile details (confirms current company)

Actor: `harvestapi/linkedin-profile-scraper`

Input:

```json
{
  "profileScraperMode": "Profile details no email ($4 per 1k)",
  "queries": ["<all linkedin_url values from the batch>"]
}
```

Returns profile records with current position, company, full work history, about/summary section.

## EXTRACT PER LEAD

For each lead, extract these fields from the two Apify responses:

- **`confirmed_current_company`** — the current company where they hold an ICP-qualifying title. Qualifying titles: founder / co-founder / CEO / CSO / COO / CCO / CGO / Head of Sales / Head of Growth / Head of BD / AE / Business Developer / VP Sales / Chief Sales Officer / Gründer / Mitgründer / Fondateur. If the CSV's current company doesn't match an ICP-qualifying role but another current position does, prefer the ICP-qualifying one.
- **`confirmed_current_title`** — current job title at that company
- **`company_description`** — short description from the company/about/position description field
- **`last_post_1_text`** — text of most recent post (truncate to ~600 chars)
- **`last_post_1_url`** — URL of that post
- **`last_post_1_date`** — posted date if available
- **`last_post_2_text`** — text of 2nd most recent post (truncate to ~600 chars)
- **`last_post_2_url`** — URL
- **`last_post_2_date`** — date

## HARD RULES

- **Never fabricate.** If a profile has fewer than 2 posts (or none), leave the missing fields as empty strings.
- **If no ICP-qualifying current position exists,** leave `confirmed_current_company` and `confirmed_current_title` empty rather than picking a non-qualifying role.
- **Time discipline.** If either Apify call takes more than ~5 minutes, write the file with whatever you have (empty fields for missing data) and finish. Retry a failed call at most once.

## OUTPUT FORMAT

Write to `<WORKING_DIR>/enrich_batch_<N>_results.json` as a JSON array of N objects (where N matches batch size), exact shape:

```json
{
  "row_number": 2,
  "full_name": "...",
  "linkedin_url": "...",
  "confirmed_current_company": "...",
  "confirmed_current_title": "...",
  "company_description": "...",
  "last_post_1_text": "...",
  "last_post_1_url": "...",
  "last_post_1_date": "...",
  "last_post_2_text": "...",
  "last_post_2_url": "...",
  "last_post_2_date": ""
}
```

After writing the file, reply with a 2-sentence summary: how many profiles returned posts, any notable mismatches between CSV's current job and the LinkedIn-confirmed role.
