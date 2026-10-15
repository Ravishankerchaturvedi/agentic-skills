---
name: voice-agent-architecture-and-cost
description: How to architect an AI voice calling agent (rent vs own decision) and model its true per-minute cost and margin. Use when designing, pricing, or evaluating a voice/telephony AI product.
---

# Voice Agent Architecture & Cost

For building an AI phone agent that calls people, holds a real conversation, takes actions,
and logs outcomes — and knowing what it actually costs.

## The architecture decision: rent the loop, own the brain
A voice agent is a streaming pipeline: `telephony → STT → LLM brain → TTS → caller`,
with interruption handling and sub-second latency. Do NOT build that pipeline.

Three ways to get it:
1. **Fully managed** (e.g. ElevenLabs Agents, Retell, Vapi) — easiest, least control; the
   brain + logic live in their platform; weak learning loop; lock-in.
2. **Own the stack** (LiveKit Agents or Pipecat) + a TTS voice + your own LLM brain — full
   control, better margin at scale, more glue to write.
3. **Hybrid (recommended):** open-source real-time engine (LiveKit) + **best voice as a
   swappable plugin** (ElevenLabs for quality / Cartesia for cost) + **your Claude brain +
   your learning loop + your data**. Easy (you rent the hard real-time parts) AND
   controlled (you own the brain, can swap every rented piece behind a port).

**Why hybrid:** the learning loop is your moat; if the brain lives in a managed platform,
your loop is bolted on the outside and can't shape the conversation. Own the brain.

## Standard production targets (don't reinvent)
- Streaming cascaded pipeline; each stage streams into the next.
- Latency: p50 < 400ms, p95 < 800ms. >1.5s degrades the call.
- Interruption: stop TTS + cancel LLM + restart — handled by LiveKit/Pipecat automatically.
- Co-locate STT/LLM/TTS near the telephony edge (region matters — e.g. India vs US).

## What you build vs rent
| Own (control + moat) | Rent (easy, swappable) |
|---|---|
| The brain (LLM logic, constitution, tools) | Real-time pipeline (LiveKit) |
| The learning loop + all data | Voice/TTS (ElevenLabs / Cartesia) |
| Transcripts, outcomes, patterns | STT (Deepgram) |
| The CRM connector | Phone numbers (Twilio US / Exotel-Plivo India) |

## Truthfulness on a call (non-negotiable)
A wrong price/promise on a call = lost money + trust. Apply the gateway pattern:
constitution ("never quote a price/availability not in the catalog tool"), grounding in
the lead + offer data, a verification gate on anything spoken, and human transfer on a
buying signal or anything sensitive. Disclose it's an AI; honor opt-out.

## Cost & margin
The per-minute economics and a pricing/margin model are in `references/cost-model.md`.
Headline: built right, cost ≈ $0.05–0.10/min; sold at $0.30/min or a retainer → ~70–85%
gross margin. The voice (TTS) is the swing cost — owning the swap (ElevenLabs↔Cartesia) is
the biggest lever.

## Compliance is a config, not a blocker
Lean **warm** (a business calling its own/opted-in contacts) over cold lists. AI
self-disclosure + instant opt-out + per-region rules (US TCPA, India TRAI/DND/DLT). Design
the consent/disclosure/opt-out into the core; then it's handled, move on.

## The one line
Rent the real-time pipeline and the voice; own the brain, the data, and the loop; keep
every rented piece swappable; price on outcomes, not minutes.
