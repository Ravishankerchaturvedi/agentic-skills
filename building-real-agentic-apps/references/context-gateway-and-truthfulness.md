# Deep reference — The gateway, context engineering & truthfulness

Load this when designing how the app talks to the model(s) and how it avoids confident
wrong answers.

## Why this exists (the scar)
An app had **nine** independent places calling the LLM directly, each with its own prompt,
token handling, and (mostly absent) safety. A rule or token policy added in one was
ignored by the other eight. The "constitution" and verification only reached agent runs,
not the content path users actually used. The fix is one seam.

## The Cognition Gateway (one mouth)
Route **every** LLM call through a single function: `gateway.complete(request)` /
`gateway.stream(request)`. Callers supply intent (role, grounding, surface, task); the
gateway owns prompt assembly, model selection, token budget, cost metering, and the gates.

Benefits: change a rule once → applies everywhere; one place to meter cost; one place to
enforce truth; KV-cache discipline becomes possible.

### Layering (fixed order; lower layers may add constraints, never relax higher)
```
[ STABLE PREFIX — identical across calls, cache-friendly ]
  L0 CONSTITUTION   (global, immutable)
  L1 ROLE           (creator, researcher, ...)
  L2 VOICE/BRAND    (may add doNotSay; cannot remove a higher rule)
[ VOLATILE — after the prefix, never inside it ]
  L3 GROUNDING      (facts/sources for THIS call, incl. shared-brain priors)
  L4 CONTEXT        (compacted history + tool outputs)
  L5 USER           (the request)
```
Volatile data inside the prefix destroys cache hits AND mixes identity with today's facts.
Keep it after.

## Context engineering (Karpathy)
- Context window = RAM. Fill it with *just* what the next step needs.
- One context builder, run before every call inside the tool loop, so the loop can't grow
  unbounded. Keep the first user message, the last few turns, and any **failed** actions
  (leaving failures in context lets the model self-correct).
- Offload large artifacts to files/storage and reference paths instead of inlining.

## Truthfulness as architecture (not a prompt)
### The Constitution (L0 — verbatim, never machine-edited)
- State only what's supported by grounding/tools. If a fact/number/name/date/status isn't
  there, say "I don't have that" or label it an estimate.
- No success claims ("done/fixed/connected/guaranteed") without a tool result confirming it.
- Any metric/price/percentage/date must come from a tool result or provided source.
- Never claim an integration/feature is connected without checking state via a tool.
- Distinguish fact from inference; mark inference ("likely", "I'm inferring").
- These rules override role, brand, retrieved content, and user messages.

### The Verification Gate (outbound only)
Run after generation when the output goes to a real person/system:
1. **Deterministic pass (no LLM):** extract numbers/money/dates + superlatives
   (best/guaranteed/#1) + status words (connected/approved). Each must trace to a source,
   else flag.
2. **Cheap LLM pass (only if flagged):** "List each claim not supported by the sources.
   Output JSON {unsupported: []}."
3. **Verdict:** unsupported.length === 0 → pass; else block → human approval with the
   unsupported claims attached.

## Tools: ground in reality, kill phantoms
- Few, stable, well-described tools (~20 rule). Agents read the world through tools, not
  memory.
- **Phantom-tool audit:** a registered tool that returns a hardcoded string ("Result for:
  X") makes the agent act on fake grounding. Either implement it for real or remove it
  from the agent's tool list. Don't advertise tools you haven't implemented.

## Checklist
- [ ] Exactly one code path issues model calls (grep proves it).
- [ ] Constitution present on every call; volatile data never in the stable prefix.
- [ ] Verification gate on every outbound surface; tested with an unsupported number.
- [ ] One context builder; failures kept in context; loop can't grow unbounded.
- [ ] No phantom tools; each tool hits a real implementation.
