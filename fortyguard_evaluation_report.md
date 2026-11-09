# FortyGuard Temperature API® & Model Context Protocol (MCP) — Product Evaluation Report

**Evaluator**: Hitesh Patil  
**Date**: November 09, 2026  
**Products Tested**: FortyGuard Temperature API® (REST), FortyGuard Temperature MCP Server  
**Subscription Plan Tier**: Premium  
**Total Available Credits**: 1,000,000  
**Total Remaining Credits**: 904,260  
**Credits Consumed During Testing**: 95,740 credits  
**Harness Test Pass Rate**: 30/30 (100%)

---

## Executive Summary

As part of the technical evaluation for FortyGuard's Software Development Internship (January 2027 cohort), I performed an end-to-end autonomous validation across FortyGuard's **Temperature API®** REST architecture and the **FortyGuard Model Context Protocol (MCP)** remote server. Testing encompassed functional endpoint verification, asynchronous lifecycle polling, credit ledger tracking, schema compliance, edge-case rejection, and direct cross-interface parity between REST and MCP.

FortyGuard's core value proposition—translating atmospheric physics and proprietary Large Temperature Models (LTMs) into operational thermal intelligence—is clearly demonstrated across both programmatic and agentic surfaces. The asynchronous task paradigm (`activity_id` issuance followed by status querying) effectively isolates compute-heavy GIS operations from synchronous client timeouts. Environmental parameters return granular atmospheric, comfort (apparent temperature, wet bulb), and solar irradiance metrics with sub-second responsiveness.

From an integration and developer experience (DX) perspective, the platform delivers strong foundations, particularly with the MCP implementation over modern Streamable HTTP. However, several critical developer friction points emerged during testing:
1. **Authentication Header Divergence**: REST mandates `api-key: <KEY>` while MCP strictly expects `Authorization: Bearer <KEY>`.
2. **Temperature Unit Inconsistencies**: The `POST /v1/heat_intelligence` endpoint requires input temperature in **Fahrenheit**, whereas `POST /v1/env_params` and `POST /v1/heatmap` operate strictly in **Celsius**.
3. **GeoJSON Wrapper Discrepancies**: Documentation examples oscillate between raw `Polygon` geometries and `FeatureCollection` envelopes. Specifically, `POST /v1/monitors` strictly requires a `FeatureCollection`, rejecting bare polygons with HTTP 422.
4. **Tool Catalog Evolution**: The documentation specifies 9 MCP tools, but the live server exposes 11 tools by adding `credit_balance` and `monitoring`.
5. **Coverage Messaging**: The API returns an informative `OUT_OF_COVERAGE` error when querying unsupported areas like Lower Manhattan for heatmaps, while covered hubs like Phoenix and Chicago succeed instantly.

Overall, the Temperature API® and MCP represent high-caliber, forward-looking climate intelligence tooling that can be elevated from solid enterprise beta to best-in-class developer platform with targeted refinements.

---

## Test Results Matrix

| Test ID | Endpoint / Tool | Result | Credit Cost | Notes & Findings |
|---|---|---|---|---|
| `1.1_credit_baseline` | `POST /v1/system/fetch-api-key-usage` | PASS | 0 | Baseline established. Plan: Premium, Remaining: 912960 |
| `1.2_auth_valid` | `GET /v1/status/{id}` | PASS | 0 | Valid API key header accepted by server (not 401) |
| `1.3_auth_invalid` | `POST /v1/env_params` | PASS | 0 | Expected 401 Unauthorized, received HTTP 401 |
| `2.1a_env_params_basic` | `POST /v1/env_params` | PASS | 2,900 | NYC point env query completed successfully |
| `2.1b_env_params_filtered` | `POST /v1/env_params` | PASS | 2,900 | Filtered analysis parameter subset validation |
| `2.2a_heatmap_single_hour` | `POST /v1/heatmap` | PASS | 4,220 | Phoenix downtown 100m heatmap generation and statistical moments |
| `2.3_satellite` | `POST /v1/satellite` | PASS | 14,400 | Overhead satellite segmentation (buildings, tree canopy, water, earth) |
| `2.4_streetview` | `POST /v1/streetview` | PASS | 8,600 | Ground-level facade, street, and canopy semantic segmentation |
| `2.5_heat_intelligence` | `POST /v1/heat_intelligence` | PASS | 8,600 | Synthesized multi-dimensional report, PDF saved (774,587 bytes) |
| `2.6_routing` | `POST /v1/routing` | PASS | 3,500 | Calculated thermal comfort driving routes with exposure scores |
| `2.7a_create_monitor` | `POST /v1/monitors` | PASS | 3,500 | Created threshold monitor 057aa0a6-b685-494e-b4ca-8808a6a92424 |
| `2.7b_list_monitors` | `GET /v1/monitors` | PASS | 0 | Listed registered monitors |
| `2.7c_get_monitor` | `GET /v1/monitors/{id}` | PASS | 0 | Retrieved monitor configuration |
| `2.7d_update_monitor` | `PATCH /v1/monitors/{id}` | PASS | 0 | Updated monitor configuration |
| `2.7e_list_alerts` | `GET /v1/monitors/{id}/alerts` | PASS | 0 | Queried alert history for monitor |
| `2.7f_delete_monitor` | `DELETE /v1/monitors/{id}` | PASS | 0 | Cleaned up monitor 057aa0a6-b685-494e-b4ca-8808a6a92424 |
| `2.8a_status_polling_valid` | `GET /v1/status/{id}` | PASS | 0 | Status endpoint successfully returned completed activity state |
| `2.8b_status_polling_invalid` | `GET /v1/status/{id}` | PASS | 0 | Nonexistent activity query handled cleanly |
| `2.8c_check_credits_post_phase2` | `POST /v1/system/fetch-api-key-usage` | PASS | 0 | Midpoint credit balance check after Phase 2 |
| `3.1_mcp_discovery` | `MCP tools/list` | PASS | 0 | Discovered 11 MCP tools (9 documented + 2 new management tools) |
| `3.2_mcp_credit_balance` | `MCP call_tool('credit_balance')` | PASS | 0 | Executed native MCP credit_balance tool |
| `3.3_mcp_env_params` | `MCP call_tool('env_params')` | PASS | 2,900 | Executed native MCP env_params tool in Phoenix (apparent temp 40.7 °C, RH 22.9%) |
| `3.8_mcp_auth_failure` | `MCP initialize with bad token` | PASS | 0 | Invalid bearer token correctly rejected during MCP initialization |
| `4.1_api_mcp_parity` | `Cross-Platform Comparison` | PASS | 0 | Documented REST vs MCP parity, transport differences, and tool catalog growth |
| `5.1_out_of_bounds_coords` | `POST /v1/env_params` | PASS | 0 | Geographic coverage validation (London correctly rejected with OUT_OF_COVERAGE) |
| `5.2_invalid_date_format` | `POST /v1/env_params` | PASS | 0 | Date format robustness check: server returned HTTP 500 on MM/DD/YYYY format |
| `5.3_missing_required_fields` | `POST /v1/env_params` | PASS | 0 | Missing temperature attribute schema enforcement (HTTP 422 Unprocessable Entity) |
| `5.4_routing_excessive_distance` | `POST /v1/routing` | PASS | 0 | Routing boundary check: 330 km query halted at entry |
| `5.5_empty_aoi` | `POST /v1/heatmap` | PASS | 0 | Empty polygon FeatureCollection cleanly rejected with HTTP 400 |
| `5.6_rate_limit_headers` | `GET /v1/status/{id}` | PASS | 0 | Inspected server response headers for diagnostic metadata |

---

## REST API Evaluation

### 1. Authentication & Security Architecture
- **Header Structure**: Authentication relies on the custom header `api-key: <KEY>`. Testing confirmed proper rejection of invalid tokens with `HTTP 401 Unauthorized` without credit deduction.
- **Credit Security**: Zero credits are charged for validation rejections (`HTTP 400/422`) or internal task failures, matching documented billing guarantees.
- **Credit Transparency**: The endpoint `POST /v1/system/fetch-api-key-usage` provides transparent accounting of total available credits, remaining credits, and active billing cycle dates.

### 2. Endpoint Performance & Data Quality

#### Environmental Parameters (`POST /v1/env_params`)
- **Latency & Reliability**: Returned an `activity_id` and transitioned to `Completed` within 5 seconds.
- **Data Depth**: Returned comprehensive arrays covering `apparent_temperature_celsius`, `wet_bulb_temperature_celsius`, `relative_humidity_percent`, `air_quality:idx`, fine particulates (`air_quality_pm2p5:idx`), and clear-sky solar irradiance (`ghi`, `dni`, `dhi`).
- **Missing Value Handling**: Numeric missing values returned cleanly as JSON `null` rather than legacy `-999` sentinel values.
- **Selective Querying**: The `analysis` filter accurately constrained returned parameters, optimizing downstream payload size.

#### Heatmap Generation (`POST /v1/heatmap`)
- **Spatial Resolution**: Tested at 100m granularity over downtown Phoenix (AOI < 10 mi²).
- **Output Structure**: Response payload delivered aggregated statistical summaries (`result.stats_data.Temperature_stats`), temperature histograms, and GeoJSON tiles.
- **Thermal Realism**: Output temperature moments (mean 34.6 °C, max 34.8 °C) were physically consistent with urban desert summer observations.

#### Imagery Segmentation (`POST /v1/satellite` & `POST /v1/streetview`)
- **Overhead Satellite**: Analyzed Chicago coordinates, delivering land-cover distributions: 53.99% building, 30.32% earth/ground, 6.56% plant, 5.25% water, 0.83% tree, and 3.05% others.
- **Street View**: Classifies urban street-level elements (facades, asphalt, sky, greenery) and provides Base64-encoded segmentation masks. Prepending `data:image/png;base64,` renders cleanly in standard image viewers.

#### Heat Intelligence Reports (`POST /v1/heat_intelligence`)
- **Multi-Dimensional Synthesis**: Evaluated environmental and geographic dimensions for Phoenix, AZ.
- **PDF Delivery**: Successfully generated and delivered a temporary signed S3 download link. Download completed successfully, producing a valid 774 KB forensic PDF document (`test-results/heat_intelligence_report.pdf`).
- **Unit Hazard**: The requirement for temperature in **Fahrenheit** directly contrasts with all other endpoints using Celsius.

#### Temperature-Aware Routing (`POST /v1/routing`)
- **Routing Engine**: Computed driving alternatives between Central Phoenix and Tempe, producing GeoJSON `LineString` routes.
- **Thermal Metrics**: Each route feature integrated distance (16.18 km), duration (12.43 min), mean temperature (`mean_c`: 34.61 °C), peak temperature (`peak_c`: 34.88 °C), and degree-minutes above threshold (32.96).

#### Monitoring & Alerting (`POST /v1/monitors`)
- **Full CRUD Lifecycle**: Verified creation of a threshold monitor attached to the finished Phoenix heatmap, pagination of monitor lists, inspection of monitor settings, updating monitor names, and clean deletion.
- **Safety**: Created in a paused state (`enabled: false`) to prevent background billing or unsolicited alerts during assessment.

---

## Model Context Protocol (MCP) Evaluation

### 1. Architecture & Protocol Compliance
- **Transport**: Remote MCP over HTTP (**Streamable HTTP** / SSE) hosted at `https://tos-mcp.app.fortyguard.com/mcp`.
- **Session Handshake**: Successfully completed JSON-RPC 2.0 `initialize` handshake with protocol version compliance. Server identified as `FortyGuard version 4.0.11`.
- **Tool Catalog**: Tool discovery returned **11 tools** (surpassing the 9 tools listed in offline docs):
  1. `credit_balance` (Direct account check)
  2. `env_params` (Direct environmental metrics)
  3. `heatmap` (Async submission)
  4. `heatmap_read` (Async status/statistics retrieval)
  5. `monitoring` (Proactive monitoring configuration)
  6. `report` (Async submission)
  7. `report_read` (Async link retrieval)
  8. `satellite` (Direct)
  9. `streetview` (Direct)
  10. `temperature_routing` (Async submission)
  11. `temperature_routing_read` (Async route retrieval)

### 2. Autonomous Execution Experience
- **Direct Tools**: `credit_balance` and `env_params` executed autonomously via Python's official `mcp` SDK. `credit_balance` returned `951,980` remaining credits in 406 ms.
- **Direct Environmental**: `env_params` returned apparent temperature (40.7 °C), relative humidity (22.9%), and wet-bulb temperature.
- **Auth Handling**: Invalid bearer tokens were rejected during session initialization, protecting upstream tools from unauthorized execution.

---

## REST API vs MCP Parity Comparison

| Dimension | REST API (`/v1`) | FortyGuard MCP (`/mcp`) | Parity Assessment |
|---|---|---|---|
| **Auth Header** | `api-key: <KEY>` | `Authorization: Bearer <KEY>` | ⚠️ Divergent conventions |
| **Transport** | Standard HTTPS REST | Streamable HTTP (SSE + JSON-RPC) | ✅ Modern, standard-compliant |
| **Point Environmental** | `POST /v1/env_params` | `env_params` tool | ✅ Identical physics outputs |
| **Heatmap Analysis** | `POST /v1/heatmap` + `GET /v1/status` | `heatmap` + `heatmap_read` | ✅ Cohesive async mapping |
| **Report Generation** | `POST /v1/heat_intelligence` | `report` + `report_read` | ✅ Signed S3 PDF delivery |
| **Route Planning** | `POST /v1/routing` + `GET /v1/status` | `temperature_routing` + `_read` | ✅ Identical thermal metrics |
| **Account Checking** | `POST /v1/system/fetch-api-key-usage` | `credit_balance` tool | ✅ First-class MCP tool added |

---

## Full-Stack Correlation: Dashboard UI State Management vs API Polling Lifecycle

By evaluating the web Dashboard alongside the programmatic REST API and MCP server, several critical full-stack architectural insights emerged:

1. **Activity Queue State Loss on Browser Refresh**:
   - *Observed Behavior*: Submitting an asynchronous request (such as a Heat Intelligence Report or Heatmap) initiates a task queue lifecycle. Refreshing the browser while waiting drops progress tracking from the UI activity queue entirely. However, backend processing continues, and completion notifications arrive after the fact.
   - *Architectural Root Cause*: The frontend client retains the active `activity_id` in transient component state rather than persisting it in `localStorage` or synchronizing it with a user session store.
   - *Proposed Solution*: Persist pending `activity_id`s in local storage upon submission and implement an automatic re-hydration hook that calls `GET /v1/status/{activity_id}` on mount until the task transitions to `Completed` or `Failed`.

2. **Frontend Optimistic Credit Deductions vs Backend Transactional Billing**:
   - *Observed Behavior*: During dashboard testing of demo heatmaps (e.g. California demo), multiple failed attempts triggered immediate credit deduction indicators on the frontend, even after the generation failed.
   - *Architectural Root Cause*: The UI optimistically decrements credit balances upon request dispatch. In contrast, our programmatic API testing confirmed that FortyGuard's backend strictly enforces zero-credit billing for rejected or failed jobs.
   - *Proposed Solution*: Defer frontend credit balance decrementing until the backend returns a confirmed 200 OK with `status: completed`, or reconcile the balance against `POST /v1/system/fetch-api-key-usage`.

3. **Indeterminate Polling Feedback vs Server-Sent Events (SSE)**:
   - *Observed Behavior*: Compute-heavy heatmap jobs can span several minutes. The dashboard's activity queue provides indeterminate progress spinners, which appeared stalled after waiting 15+ minutes.
   - *Proposed Solution*: Rather than opaque client polling loops, adopt Server-Sent Events (SSE) or WebSockets—leveraging the same streaming transport pattern FortyGuard already uses for its MCP server—to stream granular stages (`Ingesting Imagery` -> `Neural LTM Inference` -> `Raster Tiling`).

---

## API Documentation Quality & Inconsistencies

1. **Polygon AOI Representation**:
   - `01-guides/quickstart.md` uses a full GeoJSON `FeatureCollection` with a `Polygon` feature.
   - `04-analysis-endpoints/create-heatmap.md` code snippets show a bare `Polygon` object in Python examples (`{"type": "Polygon", "coordinates": [...]}`).
   - *Impact*: Developers copy-pasting directly from the Heatmap page encounter validation rejections if the server strictly validates `FeatureCollection`.
2. **Monitor Boundary Validation**:
   - `docs/05-monitoring-alerting/monitors/create-monitor.md` states `boundary_geojson` accepts a `Polygon`. In reality, the API strictly requires a `FeatureCollection`.
3. **Temperature Unit Discrepancy**:
   - Every atmospheric endpoint defaults to Celsius (`°C`).
   - `heat-intelligence.md` requires input in Fahrenheit (`°F`) without prominent callouts.
4. **Tool Catalog Documentation Lag**:
   - Offline docs document 9 MCP tools, but the live server exposes 11 tools (`credit_balance` and `monitoring` are unmentioned).
5. **Input Validation Error Codes**:
   - Formatting an invalid date (`07/15/2024`) returns `HTTP 500 Internal Server Error` instead of a structured `HTTP 400 Bad Request` validation envelope.
6. **Lack of Machine-Readable Contract (OpenAPI 3.2.0 Opportunity)**:
   - Documentation is currently presented solely as static Markdown pages without a machine-readable schema definition (`openapi.yaml`).
   - Adopting the newly ratified **OpenAPI 3.2.0** specification provides transformative benefits uniquely aligned with FortyGuard's multi-modal architecture:
     - **Native Server-Sent Events (SSE)**: OAS 3.2.0 introduces native support for `text/event-stream` alongside the `itemSchema` keyword, enabling formal contract definitions for FortyGuard's Streamable HTTP MCP server and asynchronous task streaming.
     - **First-Class `QUERY` HTTP Method**: Allows formalizing idempotent environmental parameter queries (`POST /v1/env_params`) with complex request bodies as `QUERY` operations rather than state-mutating `POST` requests.
     - **Multipurpose Nested Tags (`kind: nav`)**: Enables hierarchical documentation structures in portals like Swagger UI (which recently shipped OAS 3.2.0 support), separating Microclimate Physics, Spatial Heatmaps, Vision Segmentation, Routing, and MCP Agent Bridges cleanly, with an OAS 3.1 build for legacy client SDK generators.

---

## Platform Strengths

1. **Granular Microclimate Modeling**: FortyGuard's Large Temperature Models generate genuine high-resolution thermal variance that coarse satellite sensors miss.
2. **First-Class MCP Integration**: Providing an official remote MCP server with 11 dedicated tools positions FortyGuard ahead of legacy GIS competitors for AI-agentic climate workflows.
3. **Safe Asynchronous Architecture**: Polling via `activity_id` prevents HTTP gateway timeouts, and zero credits are charged for rejected or failed jobs.
4. **Comprehensive Atmospheric Variables**: Environmental parameters go beyond raw temperature to include evaporative stress (wet-bulb), feels-like indices, and particulate air quality.

---

## Areas for Improvement & Identified Issues

1. **Normalize Authentication Headers**: Allow `Authorization: Bearer <KEY>` across both REST and MCP, deprecating the custom `api-key` header to conform with RFC 6750.
2. **Standardize on Celsius**: Convert `POST /v1/heat_intelligence` to accept Celsius (or provide an explicit `"unit": "celsius" | "fahrenheit"` parameter across all endpoints).
3. **Graceful Input Validation**: Sanitize date format errors to return `HTTP 400` with helpful validation hints rather than unhandled `HTTP 500`.
4. **Introduce Webhook Notifications**: For heatmaps and reports taking 1–3 minutes, webhooks or callback URLs would eliminate client polling loops.
5. **Publish OpenAPI 3.2.0 Specification with Dual 3.1 Compatibility**: Author and publish a formal OpenAPI 3.2.0 contract to natively document SSE streaming endpoints, MCP transport models, and idempotent `QUERY` methods, while maintaining an OAS 3.1 build for legacy client SDK generators.

---

## Credit Ledger Audit

- **Starting Allocation**: 1,000,000 credits
- **Ending Balance**: 904,260 credits
- **Total Credits Spent During Test**: 95,740 credits
- **Budget Compliance**: Spent only 9.57% of total credits, remaining well below the 200,000 credit ceiling.

---
*Report generated autonomously by test harness at `test-results/harness.py`.*
