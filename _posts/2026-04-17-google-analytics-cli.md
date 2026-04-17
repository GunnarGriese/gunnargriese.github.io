---
layout: post
title: GA CLI - A Command-Line Interface for Google Analytics
author: gunnar
date: 2026-04-17 00:00:01 +0200
categories: [GA]
tags: [ga4]
image: /assets/images/blog/ga-cli.png
comments: true
toc: true
lang: en
---

If you've spent any meaningful amount of time working with Google Analytics (GA), you know the drill: the UI is great for getting an ad-hoc overview, exploration (to a certain degree), digging into a specific report, or building a quick audience. But the moment you need to manage multiple properties, replicate configurations across accounts, or pull recurring reports for a pipeline things become more difficult and cumbersome than they have to. What should be a straightforward task turns into a click-heavy, error-prone marathon through nested menus and inconsistent interfaces. And if you've ever tried to audit a client's GA setup by manually clicking through every single custom dimension, key event, and data stream configuration screen, you know exactly the kind of pain I'm talking about.

This is why I built **GA CLI**. A command-line interface for GA that wraps both the GA Admin API and Data API into a single, scriptable tool. Think of it as a way to interact with GA the way developers have been interacting with infrastructure for decades: through text commands that are composable, automatable, and version-controllable.

And the part that I actually put a sizeable amount of the work in is to design the GA CLI from the ground up with **AI agents as a first-class user**. Since AI-powered coding assistants and autonomous agents are increasignly becoming part of our everyday workflows, a CLI that speaks their language (structured output, introspectable schemas, safe mutation previews) is moire than just a nice-to-have.

The inspiration for this project came from the **[GTM CLI](https://github.com/owntag/gtm-cli)** (`@owntag/gtm-cli`) by Justus Blümer / owntag. His open-source CLI wraps the GTM API. After having tried it out, two things became clear to me: first, that a CLI for Google Marketing Platform tools is genuinely valuable; and second, that designing for agent-readiness from day one is a great feature. My GA CLI brings the same philosophy to Google Analytics.

In this post, I'll walk you through what GA CLI can do, why CLIs are having a moment in the age of AI agents, and how you can use it to streamline everything from property audits to automated reporting pipelines. Let's get started!

## What Is a CLI (and Why Should You Care)?

Should you be coming from a pure analytics or marketing background, the term "CLI" might not be part of your daily vocabulary. Therefore, let me briefly set the stage. A **Command-Line Interface (CLI)** is a text-based way to interact with a system. Instead of clicking buttons in a graphical interface, you type commands into a terminal. That's it. No magic, no rocket science.

The interesting part is what this unlocks. CLI commands are inherently **scriptable**, meaning you can string multiple commands together and run them as a single script. They're **composable**, meaning the output of one command can be piped as the input to another (a concept that has been around a long time and is still incredibly powerful). They're **automatable**, meaning you can schedule a script to run every Monday morning and have yourself a reporting pipeline. And they're **version-controllable**, meaning your commands and scripts are just text files, which means they can live in a Git repository right alongside your code.

Another way to put it is that if the GA UI is like driving a car manually (= you're in control but it requires your constant attention and presence) then a CLI is like handing written instructions to a chauffeur. You describe what you want done once, and it gets executed exactly that way every time. Whether that chauffeur is a shell script, a CI pipeline, or (as we'll get to shortly) an AI agent, the principle is the same.

For us analysts, this matters because chances are high that a sizeable portion of our workflows are repetitive. Setting up properties, pulling reports, auditing configurations, syncing settings across accounts, all of these are tasks that benefit from being codified rather than clicked through. And once they're codified, they become shareable, reviewable, and reproducible. That's a fundamentally different way of working with GA, and one that I think our industry can benefit from.

## CLIs in the Age of AI Agents

Now, if CLIs were just about making human workflows faster, that alone would be a solid reason to build one. But there's another dimension that makes CLIs particularly relevant right now: **AI agents**.

Justin Poehnelt (Senior DevRel at Google) recently wrote an article titled ["You Need to Rewrite Your CLI for AI Agents"](https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/) that resonated with me quite a bit. Poehnelt built Google Workspace's CLI with agents as the primary consumer from day one, and his core insight is this: **"Human DX optimizes for discoverability. Agent DX optimizes for predictability."**

What he means is that when a human uses a CLI, they benefit from colorful output, helpful prompts, and intuitive command names. An AI agent, on the other hand, needs something different entirely. It needs to know exactly what a command will return, in what format, and how to handle failures without guessing. That distinction shaped a lot of the design decisions behind GA CLI.

Here's how this translates into concrete features:

- **Structured output**: Every command supports `--output json`. Agents parse JSON, not pretty-printed tables. When GA CLI detects it's being piped (= non-TTY environment), it automatically switches to JSON output which means that no flag is needed.
- **Structured errors**: Errors are returned as JSON on stderr with classified exit codes: `0` for success, `2` for auth errors, `3` for API errors, `4` for network errors. An agent can branch on failure type programmatically instead of trying to parse a human-readable error message.
- **Context window discipline**: Agents work with limited context windows, so responses need to be concise and predictable. The `--output compact` flag returns minimal ID+name output, keeping the token footprint small.
- **Agent-specific documentation**: The `ga agent guide` command ships a built-in reference specifically for AI agents. Think of it as a condensed manual that encodes the invariants and conventions an agent can't intuit on its own (inspired by Poehnelt's "SKILL.md" concept).
- **Schema introspection**: `ga --describe` outputs a JSON Schema for all 136 commands in a single call, like parameter names, types, flags, aliases, defaults, required fields, plus metadata like whether a command is `mutative` or `supports_dry_run`. An agent calls this once, caches the result, and knows exactly how to construct any command. This is also the bridge to auto-generating MCP tool definitions from the CLI (more on that later).
- **Safe mutations / dry-run**: Every create, update, and delete command supports `--dry-run`, which previews the exact API request as JSON without executing it. Agents can verify parameters and catch mistakes before they become live changes. For example: `ga properties create --name "EU Site" --timezone Europe/Berlin --dry-run` outputs the request body and exits.
- **Safety rails**: Destructive operations prompt for confirmation by default. In automation contexts, `--yes` skips the prompt, but the deliberate opt-in ensures that an agent (or a mistyped script) doesn't accidentally delete a property without explicit intent.

The combination of `--describe` + `--dry-run` + structured errors forms what I'd call a complete **agent feedback loop**: discover: preview: execute: handle errors. An agent can go from zero knowledge of the CLI to confidently executing multi-step workflows without any external documentation or human intervention. That's the level of self-sufficiency I was aiming for.

To see this in action, here's a walkthrough of GA CLI working together with Claude as an AI agent:

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe src="https://drive.google.com/file/d/1-s0uJRvmEXTRqYAXRoRJOOI3-i7vxbOP/preview"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
          frameborder="0"
          allowfullscreen></iframe>
</div>

## CLI vs MCP Servers: Where Does Each Fit?

If you've been following the AI tooling space, you've likely come across the **Model Context Protocol (MCP)**, which is an open standard introduced by Anthropic that defines how AI models connect to external tools and data sources. MCP servers have gained a lot of traction, with a growing ecosystem of integrations for everything from databases to cloud services (I explored what this means for our line of work in [MCP Servers in Digital Analytics - Levelling Up Your LLM Game](https://gunnargriese.com/posts/mcp-servers-in-digital-analytics/)). So, a fair question is: why build a CLI when you could build an MCP server instead?

The short answer is that they serve different purposes and complement each other well. Here's how I think about the trade-offs:

**MCP Servers** provide tight, bidirectional integration with MCP-compatible hosts like Claude Desktop, Cursor, or Windsurf. The protocol handles tool discovery, parameter validation, and response formatting natively. The agent doesn't need to know how to parse CLI output because the MCP layer takes care of that. The trade-off is that you're tied to the MCP ecosystem. Your tool only works with hosts that implement the protocol, and standing up an MCP server introduces additional infrastructure and deployment considerations compared to a simple `pip install`.

**CLIs** are universal. They work with any agent framework that can execute shell commands (which is essentially all of them), any CI/CD pipeline, any shell script, and obviously any human with a terminal. Install via `pip` or `pipx`, authenticate, and you're running. No server process, no protocol negotiation. The trade-off is that each invocation is stateless, and there's no built-in streaming protocol.

**Raw APIs** give you the most flexibility but also the most friction. You're handling authentication, pagination, error parsing, rate limiting, and response transformation yourself. For a one-off script that's fine, but for repeatable workflows it quickly becomes boilerplate-heavy.

The following table summarizes these differences:

| Dimension | Raw API | CLI | MCP Server |
|-----------|---------|-----|------------|
| **Portability** | Any language with HTTP | Any shell / agent framework | MCP-compatible hosts only |
| **Setup complexity** | High (auth, pagination, error handling) | Low (`pip install` + `ga auth login`) | Medium (server process + host config) |
| **Human usability** | Low (code required) | High (interactive + scriptable) | None (agent-only interface) |
| **Agent compatibility** | Manual integration | Any agent with shell access | Native in MCP hosts |
| **Statefulness** | Stateful (you manage sessions) | Stateless per invocation | Stateful (persistent connection) |
| **Infrastructure** | None (client-side) | None (client-side) | Server process required |

The way I see it, a CLI sits in a sweet spot: it's more opinionated than a raw API (= less boilerplate, sensible defaults, built-in auth) but more portable than an MCP server (= works everywhere, no infrastructure). And importantly, they're not mutually exclusive. A CLI can serve as the foundation that powers an MCP server under the hood. For example, the `--describe` output from GA CLI, contains everything you'd need to auto-generate MCP tool definitions. That means you get the portability of a CLI and the native agent integration of MCP without building both from scratch.

## From CLI to Custom Skills: Making Agent Workflows Reliable

Having a CLI or an MCP server gives your agent the ability to do things. But ability alone doesn't guarantee reliability. If you've ever watched an AI agent interact with a new tool, you know that it can be surprisingly creative in finding ways to use it incorrectly, like calling commands in the wrong order, passing parameters that are technically valid but semantically wrong, or simply taking a longer path than necessary because it doesn't understand the conventions of your specific setup.

This is where **skills** come in. Skills are one of the most powerful ways to customize AI agents (e.g., in Claude Code) for specific, repeatable workflows. Think of a skill as a structured, reusable playbook that tells the agent not just *what* tools it has, but *how* to use them in context, the right order, the right conventions, the gotchas to watch out for.

### The Four Pillars of a Well-Crafted Skill

From my experience building skills for analytics workflows, there are four things that make the difference between a skill that works sometimes and one that works reliably:

1. **Structure & conventions**: Follow a consistent format. Skills in Claude Code use a `SKILL.md` file with YAML frontmatter that declares metadata like the skill name, description, and trigger conditions. This standardized structure makes skills discoverable and composable.

2. **Tools**: Equip the skill with the right tool access. This is where your CLI commands, MCP servers, and APIs come in. A skill's frontmatter declares which tools it's allowed to use via `allowed-tools`, meaning you can scope an agent's capabilities precisely. For instance, give it access to GA CLI for configuration tasks but not to your production database.

3. **Data & context**: This is the part most people underestimate. The `SKILL.md` file itself should contain detailed instructions, reference information, and executable code snippets that teach the agent about the custom intricacies of *your* setup. What naming conventions do you use for custom dimensions? What's the standard event taxonomy across your properties? Which property is the "golden" reference? This domain knowledge is what turns a generic agent into one that actually works for your team.

4. **Trigger & objective**: Skills can be invoked explicitly via `/skill-name` commands or automatically based on natural-language matching against the skill description. A well-written trigger description ensures the skill activates when it should and stays out of the way when it shouldn't.

> My recommendation: use Anthropic's official `skill-builder` meta skill to let Claude guide you through building your own skills rather than copying someone else's. It walks you through the structure, tests trigger accuracy, and helps you iterate. This usually tends to produce better results than starting from a template. And in case you wonder: Yes, I'll release some skills for the GA CLI soon, too.

## GA CLI Feature Tour

Now that we've covered the "why", let's look at the "what". GA CLI currently ships with **28 command groups** and over **136 subcommands** covering both the GA Admin API and the Data API. Here's a high-level overview of what's available, grouped by domain.

### Authentication

GA CLI supports two authentication methods:

- **OAuth 2.0**: The default for interactive use. Run `ga auth login`, and it opens a browser-based OAuth flow. You bring your own GCP OAuth credentials (via a `client_secret.json` file or environment variables). Tokens are stored locally with restricted file permissions and refresh automatically.
- **Service accounts**: For automation and CI/CD pipelines. Run `ga auth login --service-account /path/to/key.json` and you're set. Also supports the standard `GOOGLE_APPLICATION_CREDENTIALS` environment variable if you prefer to configure it that way.

You can check your auth status at any time with `ga auth status` and sign out with `ga auth logout`.

### Account & Property Management

The bread and butter. GA CLI covers the full lifecycle of accounts and properties:

- **Accounts**: list, get, update, delete, view data sharing settings, and search change history
- **Properties**: list, get, create, update, delete, plus check API quota usage
- **Account summaries**: a quick overview of all accounts with their properties in a single call

### Configuration Resources

This is where GA CLI saves you the most time compared to the UI. Instead of clicking through individual configuration screens, you can manage all of these from the terminal:

- **Custom dimensions** and **custom metrics**: list, get, create, update, archive
- **Key events** (conversions): list, get, create, update, delete
- **Data streams**: list, get, create (web, Android, iOS), update, delete
- **Enhanced measurement**: get and update toggle settings per stream
- **Data retention**: get and update retention periods
- **Measurement Protocol secrets**: list, get, create, update, delete
- **Audiences**: list, get, create, update, archive
- **Calculated metrics**: list, get, create (with formula), update, delete
- **Channel groups**: list, get, create, update, delete
- **Event create rules** and **event edit rules**: list, get, create, update, delete (plus reorder for edit rules)
- **BigQuery links**, **Firebase links**, **Google Ads links**: full CRUD management
- **Access bindings**: manage user roles at account or property level
- **Annotations**: create and manage report annotations
- **Property settings**: get/set attribution models, lookback windows, and Google Signals state

### Reporting

GA CLI wraps the GA Data API with a set of report commands that cover the most common needs:

- `ga reports run`: Standard reports with dimensions, metrics, filters, sorting, and date ranges
- `ga reports realtime`: Real-time reporting
- `ga reports pivot`: Pivot table reports for cross-tabulation
- `ga reports batch`: Run multiple reports in a single API call
- `ga reports funnel`: Funnel analysis (v1alpha)
- `ga reports check-compatibility`: Verify that a metric/dimension combination is valid before running the report
- `ga reports metadata`: Browse all available metrics and dimensions for a property
- `ga reports build`: An interactive report builder that walks you through constructing a query step by step

### Access Reports

For compliance and auditing needs, GA CLI can generate data access audit reports at both the account and property level via `ga access-reports run-account` and `ga access-reports run-property`. These reports tell you who accessed what data and when - useful for GDPR reviews, internal audits, or detecting unusual access patterns.

### Developer Experience

A few quality-of-life features that make daily use smoother:

- **Shell completions**: `ga completions bash|zsh|fish` generates tab-completion scripts for your shell of choice
- **Self-update**: `ga upgrade` checks PyPI for the latest version and installs it (with `--check` to preview without installing)
- **Output formats**: `--output table|json|compact` on every read command, plus `--quiet` and `--no-color` flags

### Agent-Ready Features

As covered in the earlier section, GA CLI ships with a set of features designed specifically for AI agent consumption:

- `ga agent guide`: Built-in reference with sections for reports, admin, and worked examples
- `ga --describe`: JSON Schema for all 136+ commands in one call
- `--dry-run`: Preview any mutation as JSON before executing
- Structured JSON errors on stderr with classified exit codes
- Auto-JSON output when piped (non-TTY detection)

## Getting Started

Getting up and running takes about two minutes. GA CLI is published on PyPI as `google-analytics-cli` and requires Python 3.10 or later.

**Install** (I'd recommend using `pipx` to keep it isolated from your other Python projects):

```bash
pipx install google-analytics-cli
```

Alternatively, if you prefer `pip`:

```bash
pip install google-analytics-cli
```

**Set up a GCP project** (one-time step):

Before you can authenticate, GA CLI needs OAuth credentials from a Google Cloud project. Here's the short version:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project (or use an existing one)
2. Enable the **Google Analytics Admin API** and the **Google Analytics Data API** under "APIs & Services"
3. Go to "Credentials" → "Create Credentials" → "OAuth client ID" → select "Desktop app"
4. Download the resulting `client_secret.json` file and place it in your GA CLI config directory (run `ga config path` to find it)

Alternatively, you can set the `GA_CLI_CLIENT_ID` and `GA_CLI_CLIENT_SECRET` environment variables instead of using the JSON file. Run `ga auth setup` for a detailed walkthrough of each step.

> I know this GCP project setup adds friction, and I'm actively working on simplifying this process. The goal is to make the initial setup as painless as possible. So, yeah, stay tuned...

**Authenticate** with your Google account:

```bash
ga auth login
```

This opens a browser-based OAuth flow that authenticates you against the GCP project you just configured.

**Try your first commands**:

```bash
# List all your GA accounts
ga accounts list

# List properties for a specific account
ga properties list --account-id 123456789

# Pull a quick traffic report for the last 7 days
ga reports run -m sessions,totalUsers -d date --start-date 7daysAgo

# Check what custom dimensions are configured
ga custom-dimensions list --property-id 987654321
```

For the full documentation and source code, head over to the [GitHub repository](https://github.com/daidalytics/google-analytics-cli) or run `ga agent guide`.

## What's Next

GA CLI is still in active development (currently at v0.2.4), and there are a few things on the roadmap that I'm working towards:

- **Dedicated skills for GA CLI**: Pre-built Claude Code skills for common analytics workflows like property audits, configuration syncing, and reporting pipelines. These will ship as ready-to-use `SKILL.md` files that you can drop into your projects.
- **Expanded API coverage**: The GA Admin API and Data API continue to evolve, and GA CLI will keep pace. The project already includes an automated API watch workflow that monitors Google's Discovery documents for changes on a weekly basis and opens a GitHub issue when something shifts. So, new API capabilities won't go unnoticed.
- **Community contributions**: GA CLI is open source under the MIT license. If there's a feature you'd like to see, a bug you've hit, or a workflow you think others would benefit from, please feel free to [open an issue](https://github.com/daidalytics/google-analytics-cli/issues) or submit a pull request.

If you've made it this far, I'd genuinely appreciate it if you gave GA CLI a try and let me know what you think. Star the repo if you find it useful, file issues if you don't, and feel free to reach out to me directly if you want to discuss how it could fit into your or your team's workflows.

Happy analyzing!
