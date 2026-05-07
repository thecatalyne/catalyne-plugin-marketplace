---
name: "{{ brand_name }}"
tagline: "{{ tagline }}"
version: {{ version_integer }}
language: "{{ language | 'en' }}"
type: "{{ brand_type | 'master' }}"
architecture: "{{ architecture | 'branded-house' }}"
extensions: "./brand.extensions.yaml"
owner: "{{ owner_name }}"
generated: "{{ generated_date }}"
source: "brand-identity.yaml {{ source_version }}"
---

# {{ brand_name }}

> {{ elevator_pitch }}

## Strategy

### Overview

{{ overview_paragraph }}

### Positioning

- **Category**: {{ category }}
- **Is not**: {{ positioning_isnt_list }}
- **Does**: {{ positioning_does_list }}
- **Does not**: {{ positioning_doesnt_list }}
- **Differentiators**:
{{ differentiators_list }}
- **Territory**: {{ territory_statement }}

### Personality

- **Archetype**: {{ archetype_primary }}{{ " / " + archetype_blend if archetype_blend }}
- **Triad** (if present): product = {{ product_archetype }}, brand = {{ brand_archetype }}, client = {{ client_archetype }}
- **Keywords**: {{ keywords_list }}
- **Is**: {{ is_list }}
- **Is not**: {{ isnt_list }}

**Character**: {{ personality_character }}

### Promise

- **Core promise**: {{ core_promise }}
- **Base message**: {{ base_message }}
- **Synthesizing phrase**: {{ synthesizing_phrase }}

### Guardrails

- **Tone summary**: {{ tone_summary_attributes }}
- **The brand cannot be**: {{ cannot_be_list }}
- **Litmus test**: "{{ litmus_test }}"

## Voice

### Identity

{{ voice_identity_paragraph_1 }}

{{ voice_identity_paragraph_2 }}

**Essence**: {{ voice_essence_sentence }}

### Tagline & Slogans

- **Primary tagline**: "{{ tagline }}"
- **Alternatives**:
{{ tagline_alternatives_list }}
- **Slogans**:
{{ slogans_list }}

### Message Pillars

{{ message_pillars_list }}

### Phrases

{{ phrases_list }}

### Tonal Rules

{{ tonal_rules_list }}

**Identity boundaries — what we are not**:

{{ identity_boundaries_list }}

| We Say | We Never Say |
|---|---|
{{ say_never_say_rows }}

## Visual

### Colors

{{ colors_list }}

**Avoid**: {{ colors_to_avoid }}

### Typography

- **Heading**: {{ heading_font }}, {{ heading_weight }} — {{ heading_usage }}
- **Body**: {{ body_font }}, {{ body_weight }} — {{ body_usage }}
{{ mono_font_line }}
{{ display_font_line }}

### Photography

- **Mood**: {{ photo_mood }}
- **Subjects**: {{ photo_subjects }}
- **Avoid**: {{ photo_avoid }}

### Style

- **Design keywords**: {{ style_keywords }}
- **References**: {{ style_references }}
- **Direction**: {{ style_direction }}

---

<!-- For machine-enforceable rules (banned vocab with replacements, tone matrix, output constraints, refusal triggers, motion tokens, platform font chains, self-validation targets, cultural anchors with anchored properties, counter bank), see ./brand.extensions.yaml -->
