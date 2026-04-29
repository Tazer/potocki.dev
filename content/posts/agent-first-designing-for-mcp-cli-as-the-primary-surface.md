---
title: "Agent-First: Designing for MCP and CLI as the Primary Surface"
date: 2026-04-29
draft: false
tags: [agent-first, ax, agentic-engineering, mcp, developer-experience]
description: "If agents are the long-term primary user of your software, MCP and CLI aren't a side-channel — they're the main UI. Here's what changes when you take that seriously."
---

Most teams still design software like a human is going to click through it. They build the frontend first, treat the API as plumbing behind it, and bolt a CLI on at the end if anyone asks. That order made sense when the user was always a person.

It doesn't anymore. The fastest-growing user of any non-trivial software product right now is an agent — driving it through an API, an MCP server, or a CLI. If you accept that, the priority order has to flip.

This is what I mean by **agent-first**: build for MCP and CLI as the primary surface, and treat the frontend as the secondary, human-facing view onto the same capabilities. Not a side-channel. Not a "we'll add MCP later" item on the roadmap. The main UI.

## What agent-first actually means

Agent-first isn't "no frontend." Frontends still matter — humans still log in, configure, audit, and intervene. The shift is which surface gets designed first, tested first, and held to the highest bar.

In an agent-first product, the canonical way to do anything — create the resource, query the data, run the action — is through a tool the agent can call. Underneath, the API is the shared foundation; the CLI, the MCP server, and the web UI are all clients on top of it. The shift is which client you design *for first*. **The agent-facing clients — CLI and MCP — set the bar. The web UI is one client among several, not the canonical one.**

That sounds like a small reordering. It isn't. It changes who you optimize for, what you test, what "done" means, and where you spend design effort.

## Why the surface order matters

Long-term, this is just where the world is going. The interactions a customer used to do by clicking — pulling a report, configuring a workflow, kicking off a job — are increasingly going to happen by asking an agent to do it. If your product can't be driven cleanly by an agent, you become the friction in someone else's workflow.

Short-term, even before that future fully arrives, an agent-first surface compounds. Every internal tool, automation, eval, and integration becomes cheaper to build because the primitives already exist. Engineers stop writing one-off scripts against private APIs and start composing the same tools an external agent would use. The investment pays off the day after you make it, not in two years.

## The testing habit that has to change

This is the part most engineers skip, and it's the part where the discipline actually shows up.

The default testing loop for the last twenty years has been: build the feature, click through the frontend, ship it. That habit doesn't survive an agent-first product. By the time you're clicking, you've already missed the failure modes that matter.

The new default looks like this:

1. Build the feature.
2. Drive it yourself via the CLI or MCP. Does the surface make sense without a UI to lean on?
3. Drive it via the CLI or MCP **with an agent in the loop**. Hand the agent a realistic task and watch what it actually does.
4. Then check the frontend.

Step 3 is the one almost everyone underweights. Driving the tool yourself proves the surface works. Driving it through an agent proves the surface is *legible* — that the names, descriptions, errors, and output shapes are good enough that something without your context can find its way through. Humans are extremely forgiving testers. We pattern-match around bad naming, ignore confusing errors, and remember which fields matter. Agents don't. They surface every soft spot in the design immediately.

## E2E tests aren't enough — you need evals

E2E tests over the CLI and MCP are easy and you should have them. They prove the surface works: inputs go in, outputs come out, the right side effects happen.

What they don't prove is that **an agent can figure out how to use it**. That's a different question, and it needs a different test.

That test is an eval. You write a realistic task — "the user wants to do X" — and you measure whether an agent, given your tools and skills, actually completes it. Whether it picks the right tool. Whether it interprets the error correctly when something goes wrong. Whether it discovers a capability you expected it to discover.

Once you start running these, you find out fast that tool names, parameter descriptions, error messages, and skill prompts are part of the public contract of your product. They're not documentation around the API. They *are* the API, from the agent's point of view. Change a tool description and your eval scores move. That's the loop.

## Designing for humans vs designing for agents

The instincts that produce a good human UI often produce a bad agent UI. The two columns below aren't opposites in every row, but they pull in different directions often enough that you have to pick which one you're optimizing for.

| Concern | Human-first instinct | Agent-first instinct |
|---------|---------------------|----------------------|
| **Discoverability** | Visual hierarchy, menus, tooltips | Tool names, descriptions, well-scoped skills |
| **Errors** | Friendly message, suggest next click | Structured, actionable, explains *why* and what to try next |
| **Output format** | Pretty-printed, paginated, progressive disclosure | Stable, parseable, complete; chunked only when it has to be |
| **State** | Implicit, held in the session | Explicit, queryable, idempotent where possible |
| **Docs** | Onboarding flows, walkthroughs | In-tool descriptions; the agent reads these at call time |
| **Auth** | Login screen, remembered session | Scoped tokens, predictable failure modes, machine-friendly refresh |

None of these mean the human surface gets worse. It means the canonical answer lives in a form an agent can consume, and the human UI is built on top of that.

## AX: Agent Experience

We have UX for humans clicking through interfaces. We have DX for developers building against APIs. There's a third discipline forming, and it doesn't have a settled name yet, so I'll plant a flag: **AX, Agent Experience**.

AX is the quality of the interaction surface from an agent's point of view. It covers:

- **Discoverability** — can the agent find the right capability from the names and descriptions alone?
- **Predictability** — does calling the same tool twice produce the same shape of result?
- **Recoverable errors** — when something fails, does the error tell the agent enough to try a different approach?
- **Composable primitives** — can small tools be chained into bigger workflows without custom glue?
- **Eval-backed skills** — are the higher-level skills you ship to the agent measured, not just written?

AX is to agents what UX was to web users fifteen years ago: under-invested, mostly intuited, occasionally great by accident. The teams that take it seriously now will look obvious in hindsight, the same way "we hired a designer" looked obvious by 2015.

## Common mistakes

**Treating the CLI or MCP as a thin wrapper over the API.** A wrapper exposes endpoints. A surface designed for agents exposes *capabilities* — named, scoped, and described in a way that maps to how the agent thinks about the task. These are not the same thing.

**Shipping a tool with no eval and assuming the agent will "figure it out."** It might. It might not. You won't know which until a customer's agent fails on a task you never tested. The eval is how you find out before they do.

**Testing only without an agent.** Driving your own tool by hand always feels fine. You wrote it. You know which field is which. You're the worst possible tester for whether the surface is legible to anything that isn't you.

**Letting the frontend dictate the data model the agent has to consume.** UI-shaped responses — fields named for components, pagination tuned to a scroll viewport, state implicit in the session — are awkward for agents. If the same model serves both, it has to be designed for the stricter consumer first. That's the agent.

**Inconsistent naming, auth, and error shape across tools.** Humans tolerate inconsistency. Agents pay for it on every call. A product where each tool authenticates differently, names parameters differently, and returns errors in five different shapes is a product that scores badly on every eval you'll ever run against it.

## Closing thoughts

Frontends aren't going anywhere. Humans will still log in, look at dashboards, approve things, audit things, override things. That work stays.

What changes is which surface is primary. The default interaction with most software, over a long enough horizon, is going to be an agent acting on someone's behalf. If you build for that surface first, the human one composes naturally on top of it. If you build for the human one first and treat the agent surface as an afterthought, you end up retrofitting forever.
