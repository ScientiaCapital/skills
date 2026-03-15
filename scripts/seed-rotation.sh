#!/usr/bin/env bash
# Seeds ~/.claude/rotation-state.json with Tim's prioritized project order
# Revenue-first: Tier 1 → Tier 2 → Tier 3 → Tier 4

STATE_FILE="$HOME/.claude/rotation-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

cat > "$STATE_FILE" <<'EOF'
{
  "projects": [
    "chamba",
    "solarappraisal-ai",
    "epiphan-sales-agent",
    "conductor-ai",
    "fieldvault-ai",
    "scientia-capital",
    "sunedge-power",
    "netzero-expert",
    "netzero-calculator",
    "netzero-bot",
    "langgraph-voice-agents",
    "model-finops",
    "signal-siphon",
    "thetaroom",
    "epiphan-lead-harvester",
    "epiphan-lead-tracker",
    "epiphan-linkedin-engine",
    "epiphan-cost-calculator",
    "epiphan-storyboard",
    "lang-core",
    "deep-research",
    "research-hub",
    "unsloth-mcp-server",
    "swaggy-stacks",
    "chef-vito",
    "skills",
    "conductor-ai-dashboard",
    "silkroute",
    "stripe-stack",
    "solarvoice-ai",
    "vozlux",
    "theta-room",
    "epiphan-mcp-server",
    "epiphan-bdr-playbook",
    "epiphan-ai-souffleur",
    "epiphan-openav-bridge",
    "openav-epiphan-ec20",
    "testing-setup",
    "animation-ip-factory",
    "clockin-bot"
  ],
  "pointer": 0,
  "last_run": null,
  "last_block": null,
  "history": []
}
EOF

echo "✅ Seeded rotation with 40 projects (revenue-first order)"
echo "   Pointer: 0 → starts with chamba"
echo "   State file: $STATE_FILE"
