# CRM & HubSpot Tools Reference

## CRM Tools (Legacy Database)

### `ask_agent` — AI-Powered CRM Query
Ask any question in natural language. AI writes SQL, executes it, analyzes results.

**Tips:**
- Start broad, then refine — remembers context within conversation
- Specify time periods: "2024", "last 6 months", "Q3 2025"
- Ask for metrics: "revenue", "order count", "average order value"
- Can combine CRM + device analytics + HubSpot data

**Examples:**
- "Top 10 customers by revenue in 2024"
- "Which products had the highest return rate?"
- "Monthly revenue trend for B&H Photo last 3 years"

### `crm_get_customer` — Customer by ID
**Input:** `customerId` (number)
**Returns:** Company name, email, country, industry, group, registration date

### `crm_search_customers` — Find Customers
**Input:** `query` (text — company name or email)
**Returns:** Matching customers with IDs, names, emails, countries

### `crm_get_order` — Order Details
**Input:** `query` (text — PO number or description, fuzzy search)
**Returns:** Order with line items, USD totals (currency-normalized)

### `crm_get_customer_orders` — Customer Order History
**Input:** `customerId` (number), optional `year`
**Returns:** All orders with revenue aggregation

---

## HubSpot Tools

### `hubspot_search_companies` — Find Companies
**Input:** `query` (company name or domain)
**Returns:** Up to 50 matches — name, domain, city, country, legacy CRM ID

### `hubspot_get_company` — Company Details
**Input:** `companyId` (string)
**Returns:** Full company record

### `hubspot_search_contacts` — Find Contacts
**Input:** `query` (email or name)
**Returns:** Up to 50 matches — email, name, company, phone

### `hubspot_get_contact` — Contact Details
**Input:** `contactId` (string)
**Returns:** Full contact record

### `hubspot_search_deals` — Find Deals
**Input:** `query` (deal name or PO number), optional `year`
**Returns:** Matching deals with amounts and stages

### `hubspot_get_deal` — Deal Details
**Input:** `dealId` (string)
**Returns:** Deal with associated company and contacts

**Remember:** HubSpot IDs are always strings. Use search tools first to find IDs, then use get tools for details.
