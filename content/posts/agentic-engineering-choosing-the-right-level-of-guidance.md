---
title: "Agentic Engineering — Choosing the Right Level of Guidance"
date: 2026-02-28
draft: false
tags: [agentic-engineering, ai, engineering-leadership, developer-experience]
description: "The real skill in working with AI agents isn't prompting — it's knowing when to give them full autonomy vs. tight direction."
---

Most engineers on our team are using AI agents now. The question isn't *whether* to use them — it's *how*. And most people get this wrong.

There's a spectrum from full autonomy ("build me this") to tight step-by-step direction ("use this exact pattern, handle this edge case, call this function"). Most engineers default to one mode and stay there. The ones producing the best work move fluidly along the spectrum based on context.

This is what people are calling **agentic engineering** — engineers shifting from writing code to coordinating agents that write code, with the real skill being how much oversight and direction to apply. It's not about writing better prompts. It's about making better decisions about how much control to keep.

## The Vibe Coding Zone

Sometimes you just let the agent run. You give it a high-level description, let it work, and review the output after. This is vibe coding, and it gets a bad reputation it doesn't entirely deserve.

It works well for internal tools, CLIs, prototypes, boilerplate, scaffolding, personal projects — anything where **the blast radius is low**. Wrong output is cheap to fix or throw away.

This website is a concrete example. I described a terminal-inspired theme concept to an agent and let it handle Hugo configuration, CSS, layouts, content structure — the whole thing. The risk was effectively zero: it's a personal site, redeployable in seconds, and the worst outcome is an ugly page I fix in five minutes.

Another example: writing a one-off CLI to query an internal system. The code runs locally, does one thing, and gets deleted next week. You might not even need to read every line — just run it, verify the output, and move on.

The key characteristic isn't laziness. It's a **deliberate assessment that the cost of wrong output is low enough to not warrant close supervision**.

## The Directed Zone

Then there's production services, data pipelines, auth flows, financial logic, anything customer-facing. Here, you break work into small, precise tasks and review each step carefully.

You're the architect. The agent is a skilled implementer who needs clear specs. You define the tests, specify the interfaces, and let the agent fill in implementations. You dictate the approach: "use the repository pattern here, return this error type, handle the timeout case by retrying once with exponential backoff."

This isn't about not trusting the agent. It's about the stakes. A subtle bug in payment processing costs real money. An auth bypass exposes real user data. The cost of getting it wrong is orders of magnitude higher than the cost of being thorough.

## A Risk Assessment Framework

Before starting any task with an agent, I run through five factors in my head. It takes about thirty seconds, not a ceremony:

| Factor | → More autonomy | → More direction |
|--------|----------------|-----------------|
| **Blast radius** | Only you / internal | Customer-facing / production |
| **Reversibility** | Easy to revert or redo | Hard to undo (data mutations, external APIs) |
| **Domain complexity** | Well-understood, standard patterns | Novel logic, subtle business rules |
| **Correctness bar** | "Good enough" works | Must be exactly right |
| **Your familiarity** | You know this area cold | Unfamiliar territory |

Mostly left column? Vibe code it. Mostly right? Hands-on direction. Mixed? Collaborative mode — plan together, implement in chunks, review as you go.

This isn't a formal scoring system. It's a mental model that becomes instinctive with practice. The point is to make the decision *consciously* rather than defaulting to whatever you did last time.

## The Three Workflow Modes

The engineers producing the most output across the broadest range of work are switching between these modes constantly:

**Autonomous** — "Build me X." Review the result. Ship it. Best for low-risk, well-defined tasks where you'd be rubber-stamping anyway.

**Collaborative** — Plan together, agent implements in chunks, you review each one. Good for medium-risk work where you want to stay in the loop but don't need to dictate every decision.

**Directed** — You specify exact changes, step by step. The agent is your hands on the keyboard while you make every architectural choice. For high-risk areas where precision matters.

Here's the key insight: **a single feature often uses all three modes**. Scaffold the project structure autonomously. Direct the agent through the critical business logic. Collaborate on the API design. The transitions happen naturally once you develop a feel for it.

## Common Mistakes

**Vibe-coding critical paths because high output feels productive.** Shipping fast feels great until you're debugging a subtle data corruption issue at 2 AM because nobody actually reviewed the agent's implementation of the sync logic.

**Over-directing trivial tasks.** Spending twenty minutes carefully reviewing generated boilerplate for a CRUD endpoint that follows the exact same pattern as the twenty other endpoints in the service. Your time has a cost too.

**Not adjusting when context changes.** You started this as a prototype. Now it's heading to production. The level of guidance that was appropriate last week isn't appropriate today. Recalibrate.

**Assuming one workflow fits all tasks.** "I always review everything line by line" is as much of a failure mode as "I always let the agent handle it." Both waste either your time or your users' trust.

**Confusing "the agent wrote it" with "I reviewed it."** Review debt is real. If you let three features land with minimal review because you were moving fast, you now have three features' worth of code you don't fully understand in production. That compounds.

## Building the Muscle

This is a skill, and like any skill, it improves with deliberate practice:

**Classify tasks before starting.** Thirty seconds of risk assessment before you begin. Not a ceremony, not a form to fill out — just a conscious decision about which mode you're in.

**Get comfortable with all three modes.** Most people default to one. If you always vibe code, practice directing. If you always direct, practice letting go on low-risk tasks. The discomfort means you're learning.

**Develop taste.** The best engineers I work with have an almost instinctive sense of when to intervene and when to let the agent run. This only comes from experience and paying attention to what works and what doesn't.

**Run retrospectives on your own process.** When something goes wrong, ask: was I in the right mode for this task? Would more direction have caught this? Would less direction have saved time without adding risk?

## Addressing the "Just Vibe Coding" Misconception

There's a growing perception that engineers using agents are "just vibe coding" — implying less skill, less rigor, less real engineering. I think this gets it exactly backwards.

Effective agent-assisted engineering requires **more** judgment, not less. You're doing architecture, risk assessment, code review, quality control, and system design — simultaneously, at a higher level of abstraction. You need to know what to build, how to break it down, when to trust the output, and when to intervene. That's not less engineering. It's engineering at a different altitude.

Writing code line-by-line is one skill. Orchestrating systems of work, making continuous judgment calls about quality and risk, and maintaining a mental model of a system while an agent implements it — that's a complementary skill, and it's becoming just as important.

The engineers who dismiss this as "not real coding" are making the same mistake people made about high-level languages replacing assembly, frameworks replacing hand-rolled HTTP servers, and cloud services replacing self-managed infrastructure. The abstraction layer moves up. The engineering judgment doesn't go away — it shifts to where it creates more leverage.

## Closing Thoughts

The most productive engineers I know aren't writing the code anymore. They're orchestrating — defining architecture, assessing risk, reviewing output, and intervening at exactly the right moments. But they absolutely know when to take the wheel.

This isn't about prompt engineering. It's about **engineering judgment**: the ability to make good decisions about how to build systems, applied to a new set of tools.

The bar for what makes a great engineer is shifting. Not from "can you write this code" to "can you use AI" — that's trivially learnable. It's shifting from "can you write this code" to "can you make the right decisions about how to build this system." That's always been the harder skill. Now it's the one that matters most.

One thing worth acknowledging: we're still in the early days of this. The framework I've described here reflects where I am today — working with our team, figuring out what works through trial and error. Models will get faster and more capable. Agents will get better at self-correction and reasoning about risk. The modes and boundaries I've outlined will shift as the tools mature. What won't change is the need for engineering judgment about when to trust and when to intervene. The specifics of how we apply that judgment? Ask me again in six months — I expect a different answer.

This post was written with an agent, but the ideas are mine — shaped by months of working this way with our team at Fast Track. The risk of writing it this way was low and the output was reviewable. That's the framework in action.
