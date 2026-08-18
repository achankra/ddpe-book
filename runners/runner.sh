#!/bin/bash
# runner.sh — Run all companion code examples for Domain-Driven Platform Engineering
# Usage: ./runners/runner.sh [chapter_number]
#   No arguments: runs all chapters
#   With argument: runs only that chapter (e.g., ./runners/runner.sh 4)
#
# Run from the repository root:
#   ./runners/runner.sh

set -e

# Colors for output
GREEN=$'\033[0;32m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
YELLOW=$'\033[1;33m'
NC=$'\033[0m'

DIVIDER="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SUBDIV="──────────────────────────────────────────────────────────────────────────"

# Resolve the root directory (one level up from runners/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(dirname "$SCRIPT_DIR")"
cd "$CODE_DIR"

# Find python3 or python
PYTHON="$(command -v python3 || command -v python)"
if [ -z "$PYTHON" ]; then
    echo "Error: python3 or python not found on PATH"
    exit 1
fi

chapter_filter="${1:-all}"

print_book_header() {
    echo ""
    printf "%s%s%s\n" "$BLUE" "$DIVIDER" "$NC"
    printf "%s  DOMAIN-DRIVEN PLATFORM ENGINEERING%s\n" "$BLUE" "$NC"
    printf "%s  Companion Code — Ajay Chankramath & Eamonn Ryan (Apress, 2026)%s\n" "$BLUE" "$NC"
    printf "%s%s%s\n" "$BLUE" "$DIVIDER" "$NC"
    echo ""
    printf "  Companion site:  %shttps://ddpe.platformetrics.com%s\n" "$CYAN" "$NC"
    printf "  Also by Ajay:    %shttps://effectiveplatformengineering.com%s\n" "$CYAN" "$NC"
    printf "                   %shttps://peh-packt.platformetrics.com%s\n" "$CYAN" "$NC"
    echo ""
}

print_chapter_header() {
    local num="$1"
    local title="$2"
    echo ""
    printf "%s%s%s\n" "$GREEN" "$DIVIDER" "$NC"
    printf "%s  CHAPTER %s: %s%s\n" "$GREEN" "$num" "$title" "$NC"
    printf "%s%s%s\n" "$GREEN" "$DIVIDER" "$NC"
}

print_script_header() {
    local file="$1"
    local desc="$2"
    echo ""
    printf "%s  ▸ %s%s\n" "$YELLOW" "$file" "$NC"
    printf "    %s\n" "$desc"
    printf "  %s\n" "$SUBDIV"
}

run_script() {
    local file="$1"
    local desc="$2"
    print_script_header "$file" "$desc"
    "$PYTHON" "$file" 2>&1 | sed 's/^/    /'
    echo ""
}

should_run() {
    local ch="$1"
    [[ "$chapter_filter" == "all" || "$chapter_filter" == "$ch" ]]
}

# ─── Main ────────────────────────────────────────────────────────────────────

print_book_header

# ─── Chapter 1: The Platform Engineering Renaissance ─────────────────────────

if should_run 1; then
    print_chapter_header "1" "THE PLATFORM ENGINEERING RENAISSANCE"

    run_script "Chapter01/01-01-abstraction.py" \
        "Platform abstraction: scaffolding a new microservice with golden-path templates"

    run_script "Chapter01/01-02-ownership.py" \
        "Governance validation: checking IaC resources for mandatory ownership tags"

    printf "    %s📄 Chapter01/01-03-customer-profile-api.yaml%s\n" "$CYAN" "$NC"
    echo "       Declarative service provisioning using domain concepts."
    echo "       Open this file to see how developers express intent"
    echo "       (bounded context, data classification, compliance)"
    echo "       and the platform infers the infrastructure."
    echo ""
fi

# ─── Chapter 2: Understanding Domains in an Engineering Context ──────────────

if should_run 2; then
    print_chapter_header "2" "UNDERSTANDING DOMAINS IN AN ENGINEERING CONTEXT"

    printf "    %s📊 Chapter02/Domain Identification Scorecard.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Score each domain in your"
    echo "       organization against business criticality, engineering complexity,"
    echo "       regulatory burden, and platform readiness. The output is a"
    echo "       prioritized domain map for platform onboarding decisions."
    echo ""
    echo "       Interactive version: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 3: DDD Meets Platform Engineering ───────────────────────────────

if should_run 3; then
    print_chapter_header "3" "DDD MEETS PLATFORM ENGINEERING"

    run_script "Chapter03/check_boundaries.py" \
        "Bounded context enforcement: detecting unauthorized cross-context imports"

    run_script "Chapter03/layer_separation.py" \
        "Repository Pattern: tightly-coupled vs properly-abstracted data access"

    run_script "Chapter03/test_architecture.py" \
        "Architectural fitness function: scanning for layer violations in CI"

    printf "    %s📊 Chapter03/ddpe_strategic_tactical_assessment.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Evaluate whether your platform"
    echo "       needs strategic DDD patterns (bounded contexts, context maps),"
    echo "       tactical patterns (aggregates, repositories, domain events),"
    echo "       or both. Produces a right-sized DDD investment recommendation."
    echo ""
    echo "       Interactive version: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 4: Anatomy of a Domain-Driven Platform ─────────────────────────

if should_run 4; then
    print_chapter_header "4" "ANATOMY OF A DOMAIN-DRIVEN PLATFORM"

    run_script "Chapter04/escape_hatch.py" \
        "Escape-hatch registry: classifying golden-path deviations by tier"

    run_script "Chapter04/evolution_policy.py" \
        "Evolution policies: versioning and deprecation rules per platform layer"

    run_script "Chapter04/onboarding_flow.py" \
        "Developer onboarding: the 5-stage lifecycle from init to observe"

    run_script "Chapter04/platform_telemetry.py" \
        "Platform telemetry: OpenTelemetry metrics and tracing for platform ops"

    run_script "Chapter04/run_deviation_analytics.py" \
        "Deviation analytics: reads deviation_analytics.sql and surfaces golden-path gaps"

    run_script "Chapter04/run_payments_dashboard.py" \
        "Payments dashboard: visualizes payments_dashboard.yaml with simulated domain data"

    printf "    %s📄 Chapter04/deviation_analytics.sql%s\n" "$CYAN" "$NC"
    echo "       Source SQL query for golden-path deviation analysis (used by run_deviation_analytics.py)."
    echo ""
    printf "    %s📄 Chapter04/payments_dashboard.yaml%s\n" "$CYAN" "$NC"
    echo "       Source YAML dashboard definition for Payments (used by run_payments_dashboard.py)."
    echo ""
    printf "    %s📊 Chapter04/Platform_Anatomy_Assessment.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Assess your platform's maturity"
    echo "       across layering, golden paths, deviation management, and"
    echo "       observability."
    echo ""
    echo "       Interactive version: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 5: Team Topologies and Platform as a Product ────────────────────

if should_run 5; then
    print_chapter_header "5" "TEAM TOPOLOGIES AND PLATFORM AS A PRODUCT"

    printf "    %s📄 Chapter05/service_definition.yaml%s\n" "$CYAN" "$NC"
    echo "       Platform service offering template for self-service database"
    echo "       provisioning. Defines supported engines, SLA targets, self-service"
    echo "       channels, and deprecation policies. Use as a starting point"
    echo "       for your own service catalog entries."
    echo ""
    printf "    %s📊 Chapter05/Platform_Product_Canvas.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. A structured template for"
    echo "       defining your platform's value proposition, target users,"
    echo "       key capabilities, success metrics, and roadmap priorities."
    echo "       Fill in collaboratively with platform PMs and engineering leads."
    echo ""
    echo "       Interactive version: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 6: Golden Paths and API Design per Domain ───────────────────────

if should_run 6; then
    print_chapter_header "6" "GOLDEN PATHS AND API DESIGN PER DOMAIN"

    run_script "Chapter06/override_validator.py" \
        "Override Validator: 80-15-5 pyramid for configuration override governance"

    run_script "Chapter06/flexibility_scoring.py" \
        "Flexibility Scoring: balancing standardization vs developer autonomy per config area"

    run_script "Chapter06/customization_tracker.py" \
        "Customization Tracker: lifecycle management and graduation of domain customizations"

    printf "    %s📄 Chapter06/domain-specific-api.http%s\n" "$CYAN" "$NC"
    echo "       Domain-centric database provisioning API example."
    echo "       Developer provides 3 params (name, tier, purpose); the platform"
    echo "       auto-applies encryption, compliance, and backup policies."
    echo "       Open with VS Code REST Client or any HTTP client."
    echo ""
    printf "    %s📄 Chapter06/domain_defaults.yaml%s\n" "$CYAN" "$NC"
    echo "       Opinionated domain defaults for Payments: compute, database,"
    echo "       security (OAuth 2.0, RBAC, PCI-DSS), and observability config."
    echo "       This powers the 'smart defaults' described in Chapter 6."
    echo ""
    printf "    %s📄 Chapter06/guardrails.rego%s\n" "$CYAN" "$NC"
    echo "       OPA (Open Policy Agent) rules enforcing security and compliance"
    echo "       guardrails. Run with: opa eval -d guardrails.rego 'data.guardrails'"
    echo ""
    printf "    %s📊 Chapter06/API_Design_Standards.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Documents API naming conventions,"
    echo "       versioning strategy, error formats, and domain-specific patterns."
    echo ""
    echo "       Interactive version: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 7: Measuring Platform Success ───────────────────────────────────

if should_run 7; then
    print_chapter_header "7" "MEASURING PLATFORM SUCCESS"

    run_script "Chapter07/dora_metrics.py" \
        "Domain-aware DORA metrics: deployment freq, lead time, CFR, MTTR by domain"

    run_script "Chapter07/friction_score.py" \
        "Developer friction scoring: weighted composite with trend prediction"

    run_script "Chapter07/platform_roi.py" \
        "Platform ROI modeling: multi-year cost/benefit with breakeven analysis"

    run_script "Chapter07/platform_entropy_score.py" \
        "Platform Entropy Score: tracking domain drift across model, path, and boundary dimensions"

    run_script "Chapter07/compliance_depth_index.py" \
        "Compliance Depth Index: 4-layer adoption depth scoring with theater detection"

    printf "    %s📊 Chapter07/Platform Return on Investment.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Interactive ROI model with"
    echo "       pre-built formulas for multi-scenario, multi-year analysis."
    echo ""
    printf "    %s📊 Chapter07/Team Level Metrics tied to business outcomes.xlsx%s\n" "$CYAN" "$NC"
    echo "       Maps team-level engineering metrics to business outcomes."
    echo "       Use to demonstrate the platform-to-revenue connection."
    echo ""
    echo "       Interactive versions: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 8: Patterns for Scaling Platform Adoption ───────────────────────

if should_run 8; then
    print_chapter_header "8" "PATTERNS FOR SCALING PLATFORM ADOPTION"

    run_script "Chapter08/adoption_health.py" \
        "Adoption health check: detecting anti-patterns and scoring platform health"

    run_script "Chapter08/rollout_planner.py" \
        "Phased rollout planner: 4-phase strategy from pilot to org-wide standard"

    printf "    %s📊 Chapter08/Adoption_Scoring.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Measure adoption depth across"
    echo "       teams and domains — beyond simple usage counts to real benefit."
    echo ""
    printf "    %s📊 Chapter08/MaturityModel.xlsx%s\n" "$CYAN" "$NC"
    echo "       Platform adoption maturity model: Ad Hoc, Emerging, Established,"
    echo "       Optimized. Benchmark your organization and plan the next level."
    echo ""
    echo "       Interactive versions: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Chapter 9: Real-World Case Studies ──────────────────────────────────────

if should_run 9; then
    print_chapter_header "9" "REAL-WORLD CASE STUDIES"

    run_script "Chapter09/transaction_domain.py" \
        "BFSI: automatic AML screening and PCI-DSS compliance in transactions"

    run_script "Chapter09/patient_data_domain.py" \
        "Healthcare: care-team access control with HIPAA-aligned audit logging"

    run_script "Chapter09/schema_governance.py" \
        "Semiconductor: schema-based governance for service deployment readiness"

    printf "    %s📊 Chapter09/Before-After-Case-Study.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Before/after metrics showing"
    echo "       measurable improvements after DDPE adoption across industries."
    echo ""
    printf "    %s📊 Chapter09/DDD Pattern Matrix.xlsx%s\n" "$CYAN" "$NC"
    echo "       Maps DDD patterns to their value across BFSI, Healthcare,"
    echo "       and Semiconductor domains."
    echo ""
fi

# ─── Chapter 10: GenAI and Autonomous Platforms ──────────────────────────────

if should_run 10; then
    print_chapter_header "10" "GENAI AND AUTONOMOUS PLATFORMS"

    run_script "Chapter10/genai_platform_interface.py" \
        "GenAI prompt-driven interface: natural language to domain-aware provisioning"

    printf "    %s📊 Chapter10/GenAI - 6 Level Maturity Model.xlsx%s\n" "$CYAN" "$NC"
    echo "       Open in Excel or Google Sheets. Six-level maturity model for"
    echo "       GenAI adoption in platform engineering — from basic code assist"
    echo "       through fully autonomous operations."
    echo ""
    printf "    %s📊 Chapter10/GenAI Readiness Assessment.xlsx%s\n" "$CYAN" "$NC"
    echo "       Evaluate your platform's readiness for GenAI-augmented workflows:"
    echo "       data readiness, governance, domain context, and team capability."
    echo ""
    echo "       Interactive versions: https://ddpe.platformetrics.com"
    echo ""
fi

# ─── Footer ──────────────────────────────────────────────────────────────────

printf "%s%s%s\n" "$BLUE" "$DIVIDER" "$NC"
echo ""
echo "  All scripts completed successfully."
echo ""
echo "  For interactive assessment models and updated examples, visit:"
printf "  %shttps://ddpe.platformetrics.com%s\n" "$CYAN" "$NC"
echo ""
echo "  Also by Ajay Chankramath:"
printf "  %shttps://effectiveplatformengineering.com%s  — Effective Platform Engineering\n" "$CYAN" "$NC"
printf "  %shttps://peh-packt.platformetrics.com%s     — The Platform Engineer's Handbook\n" "$CYAN" "$NC"
echo ""
printf "%s%s%s\n" "$BLUE" "$DIVIDER" "$NC"
echo ""
