---
title: "Beyond Sprints: Initiatives, Projects, and Full Ownership"
date: 2026-05-10
draft: false
tags: [engineering-leadership, product-development, team-structure, ownership]
description: "Sprints became ceremony. The model that's actually working for us is initiatives that set the direction, projects that deliver concrete value, and 1–3 engineers who own each project end to end."
build:
  list: never
  render: always
  publishResources: true
sitemap:
  disable: true
---

I don't think sprints are needed anymore. Not as a planning tool, not as a cadence, not as a ritual. They've quietly turned into ceremony — two-week boxes we cram work into, ticket-sizing meetings nobody believes the numbers from, retros that recycle the same complaints, and a velocity chart nobody acts on.

The reason this matters *now* is speed. With AI in the loop, we're shipping multiples faster than we were even a year ago. An engineer plus a competent agent lands in a day what used to take a week. Code review went from a day to an hour. Scaffolding a service is minutes. The planning cadence we built around the old speed isn't just outdated — it's actively in the way of how fast the team can actually move.

The teams I see shipping the most meaningful work right now aren't running tighter sprints. They've stopped running them at all. What replaced sprints is simpler and, in my experience, much harder to fake: a clear **initiative** that says where we're going, **projects** inside it that say what we need to accomplish, and **a small project team with one named engineering owner** accountable for delivery end to end — supported by a **producer** whose job is making sure the work actually delivers value and moves the initiative forward.

This post is about why we made that shift and how the pieces fit together.

## Why sprints stopped working

Sprints made sense in a specific era. Work was relatively predictable, code review was the bottleneck, humans typing code was the rate limit, and a two-week box gave teams a forcing function to plan, commit, and ship. The container was useful because the contents were uniform and the throughput was roughly known.

AI broke every one of those assumptions at the same time.

Throughput per engineer has gone up several multiples and is still climbing. Work that took a sprint takes a few days. Reviews are faster. Scaffolding is instant. Drop a two-week box on a team moving at that speed and the box stops being a forcing function — it becomes a holding pattern. You spend the first day "planning" work the team could already be shipping, and you finish the sprint sitting on output that's been waiting on a review ceremony.

Estimation took the worst hit. Velocity per task is now wildly variable: an engineer plus a good agent can finish in a day what used to take a week, and then spend a week on something that looked trivial. Sprint estimates were already mostly fiction. With agents in the loop they're fiction with extra steps — story points calibrated against a workflow that doesn't exist anymore.

Real product work also doesn't fit cleanly in two-week boxes. A small fix might take three days. A first-version project might take three or four weeks. Forcing both into the same container produces two failure modes that show up everywhere: small work gets padded to fill the sprint, and bigger work gets sliced into arbitrary "sprint-sized" chunks that don't correspond to anything real. Speed makes both worse — the small stuff now finishes in an afternoon, and the bigger stuff lands much faster than the calendar suggests.

And honestly, sprints reward the wrong thing. They reward closing tickets. They don't reward shipping outcomes, owning a problem to its conclusion, or making something a customer actually uses. The metric and the goal drifted apart, and most teams kept measuring the metric. When the team was moving slowly, you barely noticed. When the team is moving 5x faster than the planning cadence assumed, the gap is embarrassing.

## The model: Initiative → Project → Owners → Producer

The replacement isn't "no process." It's a different shape of process — one organised around **direction, ownership, and delivery** instead of cadence.

**Initiative** — the direction. Where the company or the product is going over the next quarter or two. Initiatives are deliberately broad: "make onboarding self-serve," "become the default tool for X workflow," "cut latency in half across the platform." An initiative answers *why* and *toward what*. It's owned by a leader, usually a head of product or a founder, and it doesn't change every two weeks.

**Project** — the concrete deliverable inside an initiative. A project answers *what we need to accomplish*. It has a definition of done that someone could check. "Ship a redesigned signup flow that gets a new user to first value in under five minutes" is a project. "Improve onboarding" is not. Each project ladders up to exactly one initiative — if it doesn't, that's a signal the initiative isn't real or the project shouldn't exist yet.

The first version of a project should ship fast — days to a few weeks, almost never longer. Two-month first versions are how you ship the wrong thing for two months. If a project is genuinely large, scope the v1 down to the smallest version that delivers real value, ship it, then iterate. Shipping early isn't a nice-to-have, it's the thing that makes the whole model work — you find out whether the bet is right while it's still cheap to change direction.

**Owner** — every project has one named engineering owner who is accountable for it landing end to end. Often there's a second or third engineer working alongside them, depending on the size of the project, but the buck stops with one person. They scope the work, design the approach, write the code, ship it, watch it in production, and follow up on the metrics. The owner isn't "assigned tasks within the project." They own the outcome — not just their tickets.

**Producer** — the person whose job is making sure the project actually delivers the value it promised, and that the value still maps to the initiative. The producer keeps the team unblocked, validates the shape of what's being built against the real customer problem, kills work that's drifted off-target, and protects scope when the team is being pulled sideways. This isn't a project manager pushing tickets. It's closer to a film producer: the buck stops with them on whether the thing ships and whether it was worth shipping.

**Supporting functions — Design and QA.** Most projects need design input and quality assurance, but neither is the owner. A designer embeds in the project to shape the user-facing surface — flows, components, interaction details — and stays close while engineers build. QA partners with the team on test strategy, exploratory testing, and the edge cases engineers won't catch on their own. They're not handed a queue of tickets. They're attached to the project for its duration, accountable for their slice of the outcome, and they ship with the team. Same principle as the rest of the model: small, named, accountable, attached to one project at a time wherever possible.

## How it actually works

A small team — let's say 1 to 3 engineers — gets a project. They're told what needs to be true when it's done, why it matters, and which initiative it serves. Then they go.

There's no sprint planning. There's no ticket sizing. There's no commitment ceremony. The team breaks the work down themselves, in the way that makes sense for *this* project, and starts shipping. They write the design doc if the design is non-trivial. They skip it if it isn't. They review each other's code. They deploy. They watch it.

The producer checks in on cadence — not on a sprint cadence, on a *project* cadence. Early on, that might be daily because the shape of the problem is still fuzzy. Mid-project, weekly is usually enough. Near the finish line, it tightens up again because the questions get sharper: is this actually solving the problem we said it would? Do we need to cut scope? Is something we shipped not getting used?

Projects end. That's the thing that almost never happens cleanly inside a sprint model. A project has a finish line, the team crosses it, and then they pick up the next project — possibly under a different initiative, possibly with a different combination of engineers. The unit of work is the project, not the calendar window.

## Sprints vs. initiatives

The two models pull in different directions on most of the things that actually matter day to day.

| Concern | Sprint model | Initiative model |
|---------|--------------|------------------|
| **Unit of work** | Tickets sized to fit a 2-week box | Projects sized to the actual problem |
| **Planning cadence** | Every two weeks, for everyone | Per project, when the project starts |
| **Ownership** | Tickets assigned individually | One named engineering owner, small team around them |
| **Done means** | Ticket closed | Outcome shipped and validated |
| **Direction** | Set in roadmap docs, often stale | Set by the active initiative |
| **Status reporting** | Burndown, velocity, story points | Project state, customer impact, blockers |
| **Scope changes** | Re-prioritise next sprint | Producer renegotiates against the initiative |
| **Failure mode** | Closing tickets that don't ship value | Picking the wrong project (caught earlier) |

The interesting thing about that last row: the initiative model exposes wrong-project decisions much faster than the sprint model exposes wrong-ticket decisions. When a project is the unit of work and a producer is checking it against the initiative, "we're building the wrong thing" is a question that gets asked weekly, not quarterly.

## Why these teams have to stay small

The "small team, single owner" part of this model is the most important and the part that gets watered down first.

Two-pizza teams, squad-of-eight, "the whole platform team owns this" — these all sound like ownership and they aren't. Ownership requires that *someone, by name, can make every decision the project needs*. Once you have five engineers on a project, decisions route through meetings. Once you have eight, the project slows to the speed of consensus. Once you have ten, nobody is actually accountable and the project becomes everybody's-and-nobody's.

The shape that works for us looks like this: one named engineering owner per project, often with one or two more engineers alongside, plus a designer if the project has a meaningful UI surface, a QA partner if the risk justifies it, and a producer keeping the whole thing honest. The exact numbers flex with the project — what doesn't flex is *small*. If the team starts looking like a sub-org chart, the project is too big and should be split into smaller projects, each with its own owner, all laddering to the same initiative.

A single engineering owner sounds risky to people used to bigger teams. In practice it's the opposite: it forces the project to be sized to a human, forces clear scope, and removes the ambiguity about who decides. When two or three engineers work on the same project, it still works — because there's one name on the project, not a committee.

This also changes hiring and promotion. You're not optimising for engineers who can take tickets and execute. You're optimising for engineers who can take a *project* — fuzzy edges, real customer in mind, no one to escalate ambiguity to — and land it. That's a different and much higher bar, and it's the bar that matters now.

## What the producer is actually doing

The producer role is the part of this model people most often misunderstand. It is not a project manager. It is not a scrum master. It is not a TPM tracking dependencies across teams. It can include those activities, but if that's *all* the producer is doing, the role isn't earning its keep.

The producer's actual job is to keep the project pointed at value. Concretely:

- **Validating the shape against the real problem.** The team is heads-down building. The producer is the one talking to customers, looking at usage data, and asking "are we still solving the right thing?" When the answer is no, they bring that back early.
- **Killing scope that drifted.** Engineers naturally accrete scope — edge cases they noticed, refactors that "would be cleaner," tangential features that "while we're in here." A good producer cuts the ones that don't ladder to the initiative and protects the ones that do.
- **Connecting the project back up to the initiative.** Every project is one bet inside a larger thesis. The producer's job is making sure the bet still makes sense as the thesis evolves, and that the team understands which way it's evolving.
- **Removing real blockers, not paper ones.** Not "I'll write a Jira ticket for legal." More like "I'll get the answer from legal by Thursday." Producers do the unglamorous coordination work so engineers don't have to context-switch out of building.

The best producers are people who could have been engineers or PMs and have a foot in both worlds. They earn their seat at the table by making projects ship better than they would have otherwise — not by running ceremonies.

## Common mistakes

**Renaming sprints to "cycles" and calling it a day.** If you've kept the two-week box, the planning ceremony, and the velocity chart, and you've just changed the word, nothing has changed. The container is the problem.

**Initiatives that aren't real directions.** "Improve quality." "Be more customer-centric." "Modernise the stack." These are values, not initiatives. An initiative tells you which projects belong inside it and which don't. If everything qualifies, it isn't doing the work.

**Projects without a clear definition of done.** If the team can't tell you, in one sentence, what will be true when this project is finished and who will benefit, the project is too vague to start. Ship the definition first.

**Letting the first version stretch into months.** A two-month v1 is almost always a sign that scope wasn't cut hard enough. If the team can't get something real in front of users in a few weeks, the project is too big and needs to be split. The longer the first version takes, the more expensive it is to discover you built the wrong thing.

**Big teams masquerading as one "project."** A project that needs five or six engineers isn't a project, it's a programme. Split it into smaller projects, each with its own named owner, and accept that they'll need to talk to each other. Coordination across small projects is healthier than consensus inside a big one.

**Producers who turn into ticket pushers.** If your producer's calendar is full of standups and their main artefact is a Jira board, they've drifted into project management. Pull them back to the part of the job that only they can do: keeping the project honest against the initiative.

**No project end.** A project that runs forever isn't a project, it's a team's standing remit. Either declare it done and move on, or admit it's a standing remit and stop pretending it's project work.

## Closing thoughts

I'm not anti-process. I'm anti-ceremony-pretending-to-be-process. Sprints used to be process. For most modern product teams, they've decayed into ceremony — and the underlying problem they were solving (how do we plan, ship, and stay aligned?) has new and better solutions.

Initiatives, projects, and small accountable owner teams are not novel ideas. What's new is that they're starting to feel sufficient on their own — without a sprint cadence wrapped around them — because AI changed the rate at which we ship. Individual engineers are several multiples more productive than they were two years ago. Code review is fast. CI is fast. The bottleneck has moved from "can the team coordinate enough to ship every two weeks" to "is the team pointed at the right thing, and does someone own it landing." When the constraint moves, the process has to move with it.

That's the shift. The work isn't measured in tickets closed per sprint anymore. It's measured in projects landed, value delivered, and initiatives moved. Set the direction, scope the project, hand it to one to three people who can own it, and put a producer on top who makes sure the value actually shows up.

That's the model. Sprints can rest.
