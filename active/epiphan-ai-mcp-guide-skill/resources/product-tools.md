# Product Knowledge Tools Reference

## `search_product_catalog` — Product Pricing, Specs, Features

Fast fuzzy search over structured product catalog + live CRM prices + RAG fallback for technical questions.

**Input:**
- `query` — product name, feature, use case, competitor, SKU (e.g. "Pearl Mini", "NDI encoder", "Extron alternative")
- `category` — optional filter: encoder, camera, bundle, capture_card, cloud_service, software
- `includeRag` — force RAG search (default: auto-detect by keywords)
- `includeCrmPrices` — fetch live prices from CRM (default: auto for pricing queries)

**Returns:**
- `catalog` — markdown with product families, SKUs, ESP codes, prices
- `crmPrices` — live prices from CRM database (if pricing query)
- `ragAnswer` — deep technical answer from vector store (if technical query)
- `source` — "catalog", "catalog+crm_prices", "catalog+rag", etc.

**How it works:**
1. Fuzzy search over `product-catalog.json` (instant, free)
2. If pricing query → fetches live prices from `crm_products` table
3. If technical query (keywords: "how", "setup", "troubleshoot", "configure") → RAG from OpenAI vector store

**Supported products:**
- Pearl-2 (Desktop/Rackmount), Pearl Mini, Pearl Nano, Pearl Nexus
- EC20 PTZ Camera
- AV.io 4K, AV.io HD+, AV.io SDI+
- DVI2PCIe Duo
- Epiphan Cloud & Edge, LiveScrypt
- Production Bundles (Pearl + EC20 combos)

---

## `search_product_knowledge` — Deep Technical RAG

Searches Epiphan product documentation and tech support knowledge base via OpenAI vector store (215+ files).

**Input:** `query` — technical question about Epiphan products

**Returns:** AI-generated answer grounded in Epiphan documentation.

**Best for:**
- Troubleshooting (error messages, device behavior)
- Setup guides (Panopto, Kaltura, Crestron integration)
- Technical specifications (detailed I/O, protocols, codecs)
- Firmware questions
- Product comparisons (Pearl models)

**Note:** `search_product_catalog` calls this automatically for technical questions. Use directly only when you specifically want RAG without catalog results.

---

## Key Product Facts

| Model | Physical Video In | Streaming | NDI | SRT | Max Res |
|-------|------------------|-----------|-----|-----|---------|
| Pearl-2 | 4 HDMI + 2 SDI + 2 USB | RTMP, SRT, HLS, RTSP | ✅ | ✅ | 4K |
| Pearl Mini | 2 HDMI + 1 SDI + 2 USB | RTMP, SRT, HLS, RTSP | ✅ | ✅ | 1080p |
| Pearl Nano | 1 HDMI + 1 SDI | RTMP, SRT, HLS, RTSP | ❌ | ✅ | 4K (add-on) |
| Pearl Nexus | 1 SDI + 2 HDMI + 2 USB | SRT, RTMP, HLS, RTSP | ✅ | ✅ | 1080p |
| EC20 | PTZ camera (outputs) | NDI|HX2, SRT, RTMP | ✅ | ✅ | 4K |

**Common confusions to avoid:**
- Epiphan Connect ≠ fleet management (Connect = Teams/Zoom video extraction via SRT)
- Epiphan Edge = fleet management (remote monitoring, scheduling, firmware)
- Epiphan Unify = live video mixing/switching
- Pearl devices are encoders/recorders — they do NOT run Teams/Zoom
- Pearl-2: 4K add-on now included free (activate via web UI)
- Pearl Nano: NO NDI support (only SRT/RTMP/HLS/RTSP)
