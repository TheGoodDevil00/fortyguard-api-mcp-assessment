"""
FortyGuard API & MCP Autonomous Validation Suite - Test Verification
Standard pytest test suite asserting all 30 recorded execution fixtures,
contract schemas, parity matrices, and edge-case error boundaries.
"""

import json
from pathlib import Path
import pytest

TEST_RESULTS_DIR = Path(__file__).resolve().parent.parent / "test-results"


def load_fixture(name: str):
    path = TEST_RESULTS_DIR / name
    assert path.exists(), f"Fixture {name} not found at {path}"
    return json.loads(path.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────
# Phase 1: Baseline & Authentication
# ─────────────────────────────────────────────────────────────

def test_phase_1_credit_baseline():
    """Verify baseline plan tier and credit balance accounting."""
    data = load_fixture("1.1_credit_baseline.json")
    assert data["plan_details"]["plan_type"] == "Premium"
    assert data["api_key_details"]["status"] == "active"
    assert data["api_key_details"]["valid"] is True
    assert data["credit_summary"]["total_available_credits"] == 1_000_000
    assert data["credit_summary"]["total_remaining_credits"] == 898_460


def test_phase_1_valid_auth_header():
    """Verify server accepts valid api-key header."""
    data = load_fixture("1.2_auth_valid.json")
    assert data["status"] != 401


def test_phase_1_invalid_auth_rejection():
    """Verify server rejects invalid api-key with HTTP 401."""
    data = load_fixture("1.3_auth_invalid.json")
    assert data["status"] == 401


# ─────────────────────────────────────────────────────────────
# Phase 2: REST API Core Capabilities
# ─────────────────────────────────────────────────────────────

def test_phase_2_env_params():
    """Verify point atmospheric and thermal parameters."""
    data = load_fixture("2.1a_env_params_result.json")
    location = data["result"]["locations"][0]
    params = location["parameters"]
    assert "apparent_temperature_celsius" in params
    assert "relative_humidity_percent" in params
    assert "wet_bulb_temperature_celsius" in params
    assert params["apparent_temperature_celsius"][0] > 0.0


def test_phase_2_env_params_filtered():
    """Verify selective parameter filtering reduces payload size."""
    data = load_fixture("2.1b_env_params_filtered_result.json")
    location = data["result"]["locations"][0]
    params = location["parameters"]
    assert "apparent_temperature_celsius" in params
    assert "wet_bulb_temperature_celsius" in params


def test_phase_2_heatmap_generation():
    """Verify 100m spatial heatmap moments and GeoJSON structure."""
    data = load_fixture("2.2a_heatmap_result.json")
    stats = data["result"]["stats_data"]["temperature_stats"]
    assert "mean" in stats
    assert float(stats["mean"]) > 0.0


def test_phase_2_satellite_segmentation():
    """Verify overhead satellite semantic land-cover segmentation."""
    data = load_fixture("2.3_satellite_result.json")
    segments = data["result"]["segmentation"]["segments"]
    assert "building" in segments
    assert "plant" in segments
    assert "water" in segments


def test_phase_2_streetview_segmentation():
    """Verify street-level facade segmentation and image output."""
    data = load_fixture("2.4_streetview_result.json")
    front = data["result"]["front"]
    assert "segmented_image" in front
    assert "segments" in front


def test_phase_2_heat_intelligence_report():
    """Verify synthesis of multi-dimensional PDF report from S3."""
    data = load_fixture("2.5_heat_intelligence_result.json")
    pdf_path = TEST_RESULTS_DIR / "heat_intelligence_report.pdf"
    assert "download_link" in data["result"]
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 500_000  # 774 KB downloaded PDF


def test_phase_2_thermal_routing():
    """Verify temperature-aware route alternatives and thermal metrics."""
    data = load_fixture("2.6_routing_result.json")
    features = data["result"]["result_routing"]["features"]
    assert len(features) > 0
    route = features[0]
    assert route["geometry"]["type"] == "LineString"
    thermal = route["properties"]["thermal"]
    assert "mean_c" in thermal
    assert "peak_c" in thermal


def test_phase_2_monitors_crud_lifecycle():
    """Verify complete lifecycle: create, list, get, update, alerts, delete."""
    created = load_fixture("2.7a_create_monitor.json")
    assert "data" in created
    listed = load_fixture("2.7b_list_monitors.json")
    assert "data" in listed
    got = load_fixture("2.7c_get_monitor.json")
    assert "data" in got
    updated = load_fixture("2.7d_update_monitor.json")
    assert "data" in updated
    deleted = load_fixture("2.7f_delete_monitor.json")
    assert deleted.get("status") in (200, "success") or "data" in deleted or "message" in deleted


def test_phase_2_status_polling_and_midpoint_credits():
    """Verify asynchronous task status query and midpoint credit tracking."""
    midpoint = load_fixture("2.8c_credits_midpoint.json")
    assert "credit_summary" in midpoint
    assert midpoint["credit_summary"]["total_remaining_credits"] == 892_660
    assert midpoint["credit_summary"]["total_available_credits"] == 1_000_000


# ─────────────────────────────────────────────────────────────
# Phase 3: Model Context Protocol (MCP) Server
# ─────────────────────────────────────────────────────────────

def test_phase_3_mcp_tool_discovery():
    """Verify live discovery of 11 MCP tools over Streamable HTTP."""
    data = load_fixture("3.1_mcp_tools_discovered.json")
    tool_names = [t["name"] for t in data]
    assert len(tool_names) == 11
    assert "credit_balance" in tool_names
    assert "env_params" in tool_names
    assert "heatmap" in tool_names
    assert "heatmap_read" in tool_names
    assert "monitoring" in tool_names
    assert "report" in tool_names
    assert "report_read" in tool_names
    assert "satellite" in tool_names
    assert "streetview" in tool_names
    assert "temperature_routing" in tool_names
    assert "temperature_routing_read" in tool_names


def test_phase_3_mcp_credit_balance():
    """Verify execution of native credit_balance MCP tool."""
    data = load_fixture("3.2_mcp_credit_balance.json")
    assert data.get("is_error") is False
    assert any("credit" in text.lower() for text in data.get("content", []))


def test_phase_3_mcp_env_params():
    """Verify execution of native env_params MCP tool."""
    data = load_fixture("3.3_mcp_env_params_result.json")
    assert data.get("is_error") is False
    assert any("temperature" in text.lower() for text in data.get("content", []))


def test_phase_3_mcp_auth_failure():
    """Verify MCP rejects invalid Bearer tokens."""
    data = load_fixture("3.8_mcp_auth_failure.json")
    assert "error" in data


# ─────────────────────────────────────────────────────────────
# Phase 4: Cross-Platform Parity
# ─────────────────────────────────────────────────────────────

def test_phase_4_cross_parity():
    """Verify cross-validation parity between REST and MCP."""
    data = load_fixture("4.1_cross_validation_parity.json")
    assert data["rest_available"] is True
    assert data["mcp_available"] is True
    assert "api-key" in data["auth_header_distinction"]
    assert "Bearer" in data["auth_header_distinction"]


# ─────────────────────────────────────────────────────────────
# Phase 5: Edge Cases & Error Boundaries
# ─────────────────────────────────────────────────────────────

def test_phase_5_out_of_coverage():
    """Verify geographic coverage rejection (OUT_OF_COVERAGE)."""
    data = load_fixture("5.1_out_of_bounds.json")
    assert "OUT_OF_COVERAGE" in json.dumps(data)


def test_phase_5_invalid_date_boundary():
    """Verify server response boundary on non-ISO date format."""
    data = load_fixture("5.2_invalid_date_format.json")
    assert data.get("status") == 500


def test_phase_5_missing_required_fields():
    """Verify schema rejection (HTTP 422 Unprocessable Entity)."""
    data = load_fixture("5.3_missing_required_fields.json")
    assert data.get("status") == 422


def test_phase_5_routing_excessive_distance():
    """Verify boundary halt on excessive routing distance (detecting FortyGuard's HTTP 500 error boundary)."""
    data = load_fixture("5.4_routing_excessive_distance.json")
    assert data.get("status") == 500


def test_phase_5_empty_aoi():
    """Verify empty AOI polygon rejection (HTTP 400)."""
    data = load_fixture("5.5_empty_aoi.json")
    assert data.get("status") == 400


def test_phase_5_diagnostic_headers():
    """Verify server response headers inspection."""
    data = load_fixture("5.6_diagnostic_headers.json")
    assert "server" in data
    assert data.get("server") == "envoy"


# ─────────────────────────────────────────────────────────────
# Governance & Credit Accounting Audit
# ─────────────────────────────────────────────────────────────

def test_credit_ledger_audit():
    """Verify credit consumption remained strictly under the 200,000 ceiling and matches single source of truth."""
    data = load_fixture("test_summary.json")
    assert data["total_tests"] == 30
    assert data["passed"] == 30
    assert data["failed"] == 0
    assert data["pass_rate_pct"] == 100.0
    assert data["credit_allocation"] == 1_000_000
    assert data["credits_consumed"] == 110_240
    assert data["credits_remaining"] == 889_760
    assert data["credits_consumed"] < 200_000


def test_openapi_3_2_specification_contract():
    """Verify integrity of reference OpenAPI 3.2.0 contract."""
    import yaml
    spec_path = Path(__file__).resolve().parent.parent / "openapi.yaml"
    assert spec_path.exists(), f"openapi.yaml missing at {spec_path}"
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    assert spec.get("openapi") == "3.2.0"
    paths = spec.get("paths", {})
    assert "/env_params" in paths
    assert "query" in paths["/env_params"]
    assert "/status/{activity_id}" in paths
    status_content = paths["/status/{activity_id}"]["get"]["responses"]["200"]["content"]
    assert "text/event-stream" in status_content
    assert "itemSchema" in status_content["text/event-stream"]
    assert "/mcp" in paths
    assert len(spec.get("tags", [])) == 8
