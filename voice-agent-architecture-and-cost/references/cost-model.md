# Deep reference — Voice agent cost & pricing model

All figures are 2026 list prices; assume a 3-minute average call and Claude Haiku-class
brain. Volume discounts exist. Numbers move — re-check before committing.

## Per-minute component costs
| Component | Rate /min |
|---|---|
| Telephony — Twilio US (local/mobile) | ~$0.013 |
| Telephony — India (Exotel/Plivo, + DLT registration) | ~$0.010 |
| STT — Deepgram Nova (streaming) | ~$0.008 |
| LLM brain — Claude Haiku (w/ prompt caching) | ~$0.012 |
| Orchestration — LiveKit agent session | ~$0.010 |
| TTS — ElevenLabs (Business low-latency) | ~$0.050 |
| TTS — Cartesia Sonic (alternative) | ~$0.006 |
| Observability / misc | ~$0.005 |

## The three stacks
| Stack | ~$/min | ~$/3-min call |
|---|---|---|
| Managed (ElevenLabs Agents) + telephony | ~$0.09 | ~$0.28 |
| Controlled + ElevenLabs voice | ~$0.10 | ~$0.30 |
| Controlled + Cartesia voice | ~$0.05 | ~$0.16 |

Key insight: control costs ~the same per minute as managed when using ElevenLabs voice —
so control is "free" on cost; you pay for it in glue effort. The cost *win* comes from
swapping the voice to Cartesia (~half). Managed locks you to one voice's pricing.

## Monthly (illustrative)
- Pilot (1,000 calls × 3 min = 3,000 min): managed ~$300 · controlled+ElevenLabs ~$360 ·
  controlled+Cartesia ~$210 (+ hosting ~$25–100, + plan base fees).
- Scale (10,000 calls = 30,000 min): managed ~$2,900 · controlled+ElevenLabs ~$3,100 ·
  controlled+Cartesia ~$1,750.
Caveat: cheap ElevenLabs voice (~$0.05/min) assumes its Business plan (~$990/mo), so at low
volume Cartesia is the honest cheap path.

## Pricing & margin (the part that matters)
- Your cost: ~$0.05–0.10/min.
- Sell at: $0.30–0.50/min, OR a monthly retainer ($500–2,000/client), OR per booked
  outcome ($10–50 each).
- Result: ~70–85% gross margin at almost any volume.

## Productization note (separate setup from running cost)
- One-time **setup fee** (your labour) ≠ ongoing **running cost** (telephony+voice+LLM,
  client pays). State this explicitly or you go underwater when the client scales: a
  modest 1,000–2,000 calls/mo = $75–$240/mo (₹6k–20k) in raw usage alone.
- Capture **recurring revenue** (monthly platform/maintenance fee), not just a one-time
  build + tiny AMC. A voice agent delivers value every month; price it monthly.

## Calculator inputs (to model a real client)
`calls/month × avg minutes × per-min cost(stack, region) + fixed/month` = monthly cost;
`price/min × minutes − cost` = gross profit. Swing levers: voice choice, region, volume.
