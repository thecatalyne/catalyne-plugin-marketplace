# Catalyne Plugin Marketplace

A small, curated marketplace of Claude Code plugins and skills that we use ourselves and ship publicly.

Everything here is MIT-licensed, independently installable, and held to a "ready-to-share" bar — meaning it does what its README says, on a fresh install, without any Catalyne-internal dependencies.

## Available plugins

| Plugin | Version | Description |
|---|---|---|
| [`expert-design-n-brand`](./plugins/expert-design-n-brand) | `0.9.3` | A guided pipeline that takes a team from brand discovery → multi-stakeholder synthesis → full design-system build → exported artifacts (HTML guidelines, PDF, W3C DTCG tokens, Tailwind config, Figma Tokens Studio JSON, cross-surface design map, LLM-readable brand definition). |

## How to add this marketplace to Claude Code

```
/plugin marketplace add thecatalyne/catalyne-plugin-marketplace
```

You only need to do that once. Then install any plugin from the list above:

```
/plugin install expert-design-n-brand@catalyne-plugin-marketplace
```

After installation, each plugin's own README explains how to invoke its skills.

## Want to try a plugin without installing?

Each plugin under `plugins/` ships with an `examples/` folder containing:

- A sample input (e.g. `sample-brand-identity.yaml`) you can drop into a working directory and run the plugin against
- Pre-rendered sample outputs (e.g. `sample-output/brand-guidelines.html`, `tokens.css`, `brand-guidelines.pdf`) you can preview directly in your browser without ever running the plugin

That gives you three friction levels: read the README → preview the rendered samples → install and run yourself.

## Curation policy

This marketplace is *curated*, not open-PR. We don't accept third-party plugin submissions here. The tradeoff is small (you can always fork) and the benefit is that everything published here has been used in production by us and meets a portability + safety bar.

If you have feedback, ideas, or bug reports for an existing plugin, open an issue on this repo and we'll triage it.

## License

MIT — see [`LICENSE`](./LICENSE) at the repo root and inside each plugin folder. Plugins may carry additional license notices for embedded reference materials; check each plugin's `LICENSE` file for specifics.

## About

Maintained by [Brennan Wilkerson](https://github.com/brennanw) under the [Catalyne](https://thecatalyne.com) organization.
