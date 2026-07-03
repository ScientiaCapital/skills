# Marketing Tools Reference

## Semrush — SEO & Competitive Intelligence (16 tools)

### Domain Analysis
- `semrush_domain_overview` — Organic/paid traffic, keywords, cost estimate for any domain
- `semrush_competitors` — Who competes in organic search
- `semrush_domain_organic_keywords` — What keywords a domain ranks for
- `semrush_domain_paid_keywords` — What PPC keywords a domain bids on

### Keyword Research
- `semrush_keyword_overview` — Volume, difficulty, CPC across all databases
- `semrush_keyword_overview_single_db` — Detailed overview by specific database
- `semrush_keyword_difficulty` — How hard to rank in top 10
- `semrush_related_keywords` — Related keyword suggestions
- `semrush_broad_match_keywords` — Broad match alternatives
- `semrush_phrase_questions` — Question-based keywords (People Also Ask)
- `semrush_batch_keyword_overview` — Analyze up to 100 keywords at once
- `semrush_keyword_organic_results` — Top 100 domains ranking for a keyword
- `semrush_keyword_paid_results` — Domains bidding on a keyword
- `semrush_keyword_ads_history` — Who bid on this keyword (last 12 months)

### Backlinks
- `semrush_backlinks` — Get backlinks to a domain or URL
- `semrush_backlinks_domains` — Get referring domains

---

## Google Analytics 4 — Web Traffic (7 tools)

### Discovery
- `list_dimension_categories` — Browse available dimension categories
- `list_metric_categories` — Browse available metric categories
- `get_dimensions_by_category` — Dimensions in a specific category
- `get_metrics_by_category` — Metrics in a specific category
- `search_schema` — Search dimensions/metrics by keyword
- `get_property_schema` — Complete property schema

### Data Retrieval
- `get_ga4_data` — Main tool. Fetch GA4 data with:
  - Dimensions (e.g., pagePath, sessionSource, country)
  - Metrics (e.g., sessions, conversions, bounceRate)
  - Date range
  - Filters
  - Smart row estimation and auto-aggregation

**Tip:** Use `search_schema` first if unsure which dimension/metric name to use.

---

## Google Ads — Campaign Performance (10 tools)

### Account
- `list_accounts` — List accessible Google Ads accounts
- `get_account_currency` — Get account currency code

### Performance
- `get_campaign_performance` — Campaign metrics for 7, 30, or 90 day windows
- `get_ad_performance` — Ad-level performance metrics

### Creatives
- `get_ad_creatives` — Ad copy: headlines, descriptions, URLs
- `get_image_assets` — Image asset metadata
- `get_asset_usage` — Where assets are used across campaigns

### Custom Queries (Advanced)
- `list_resources` — List GAQL resource types and fields
- `execute_gaql_query` — Run custom GAQL query (table format)
- `run_gaql` — Run GAQL with custom output (table/json/csv)

**Note:** Costs are in micros (1,000,000 = 1 currency unit). Tools handle the conversion in display.
