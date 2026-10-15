# Deep reference — State, durability & the compounding loop

Load this when designing persistence, memory, multi-tenancy, or the learning loop.

## Why this exists (the scar)
An app's entire "moat" — the learning, the voice profiles, the entity knowledge, the
reinforcement signals — lived in in-memory `Map`s. "Persistence" snapshotted 6 of ~20
stores to a JSON file. So every restart wiped the thing the whole product was supposed to
compound. The services even *had* `getSnapshot()` methods — they just were never wired
into the persistence layer. **Capable ≠ wired.**

## Law: state is the substrate
If your learning/state lives in RAM, you have a demo. Durable state is not a chore you do
"later" — it is the foundation the moat stands on. Data that dies on restart is not a moat.

## Rules
1. **Persist as you build.** Every stateful service gets durable storage *in the same
   change* that creates it — not a later "durability pass."
2. **Audit the half-wire.** List every service with `getSnapshot`/serialization; confirm
   the persistence layer actually reads/writes each. A method nobody calls is a trap.
3. **DB as source of truth, memory as cache** (once past the prototype). In-memory
   singletons also block horizontal scale — you can't run two instances if state is
   in-process.
4. **Restart-survival is a release gate.** Create → restart → still there. Run it before
   claiming any stateful feature done.

## Single source of truth (SSOT) + events — so changes propagate
- Each fact lives in exactly **one** service. The UI reads/writes that service; it never
  keeps its own copy of truth.
- A change **emits an event**; subscribers react (calendar updates, notifications fire,
  the learning loop records).
- Agents **read at decision time** through the one gateway, so a user's edit is honored on
  the very next action. (Scar: a user could "edit their voice" but the change never
  propagated because the generator read a cached/string copy, not the live profile.)
- The bug to hunt: any path that caches truth outside its owning service.

## The compounding loop (the real moat)
```
input → distill → SSOT → event → learn (per-tenant) →
  aggregate + anonymize → shared brain → redistribute as priors →
  injected at decision time → better action → outcome → (learn again)
```
- The defensible asset is the **loop compounding**, not the model or the data source.
- **Inputs behind ports** (scrapers, providers, voices) so one dying ≠ moat dying.
  Distilled, shared knowledge outlives any single feeder.
- **Privacy is part of the loop:** cross-tenant learning must be aggregated + anonymized;
  raw data must never leak between tenants. Route the read-back through the anonymized
  path, not the raw one.
- **Read-back must actually be triggered.** A correct aggregation that no scheduler ever
  calls produces empty priors — the loop looks wired but is inert. Verify with a live
  gate: seed signals across ≥N tenants → a real action's context contains a shared prior.

## Checklist
- [ ] Every stateful service persists, and the persistence layer actually calls it.
- [ ] Restart-survival gate passes for each stateful feature.
- [ ] One fact = one service; UI/agents read it live; edits emit events.
- [ ] The learning loop's aggregation is scheduled (not just defined).
- [ ] Cross-tenant sharing is anonymized; tested with a PII-laden input.
- [ ] External inputs are behind swappable ports.
