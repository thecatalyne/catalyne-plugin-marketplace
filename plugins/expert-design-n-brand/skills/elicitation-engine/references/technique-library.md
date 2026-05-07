# Elicitation Technique Library

Complete reference of all brand discovery techniques, organized by dimension. Each technique includes instructions for the interviewer agent, expected outputs, and guidance on when to recommend it.

## Technique Selection Philosophy

- **Offer choices, don't prescribe.** Present 2-3 recommended techniques per dimension based on the person's apparent style. Always let them pick.
- **Minimum 2 per dimension.** Multiple techniques on the same dimension produce richer, more triangulated signal.
- **Adapt in real-time.** If someone gives terse analytical answers, lean toward frameworks/scales. If they're storytelling, lean toward metaphors/narratives.
- **Record everything.** Log which techniques were used in `discovery.{name}.techniques_used` — synthesis needs this context.

---

## Positioning Techniques

### Landscape Grid
**Style**: Visual/spatial | **Duration**: 10-15 min
**Best for**: Concrete thinkers who like frameworks, analytical minds

**How to run**:
1. Define two axes. Defaults: X = "Traditional ↔ Innovative", Y = "Serious ↔ Playful". The user can customize axes if defaults don't feel relevant.
2. Ask the user to place their brand on the grid (as a position from -1 to 1 on each axis).
3. Ask: "Why there? What pulls you toward that spot?"
4. Optional: place 2-3 competitors on the same grid. "Where do they sit? What's the gap?"

**Writes to**: `discovery.{name}.positioning.landscape_grid`

**Interviewer notes**: Some people struggle with abstract spatial placement. If they're hesitating, try anchoring: "Let's start with the X axis. Think of the most traditional company in your space, and the most innovative. Where are you between them?"

---

### Wolff Olins Butterfly
**Style**: Narrative | **Duration**: 10-15 min
**Best for**: Big-picture thinkers, purpose-driven founders

**How to run**:
1. Two questions, explored in depth:
   - **Left wing**: "What's truly special about you? What can you do that nobody else can?"
   - **Right wing**: "What does the world actually need? What problem is crying out for a solution?"
2. The brand lives where the two wings overlap — what's special about you AND what the world needs.
3. Probe: "If only you can do it but nobody needs it, it's a hobby. If the world needs it but anyone can do it, you're a commodity. Where's the magic overlap?"

**Writes to**: `discovery.{name}.positioning.butterfly`

**Interviewer notes**: This technique surfaces purpose. It's especially powerful for mission-driven brands. If the person says "I don't know what's special about us," pivot to evidence: "What do your customers thank you for? What do people come to you for that they can't get elsewhere?"

---

### Elevator Pitch
**Style**: Verbal/spontaneous | **Duration**: 5-10 min
**Best for**: Fast thinkers, verbal processors, people who think by talking

**How to run**:
1. "You step into an elevator with your ideal customer. You have 30 seconds. What do you say?"
2. Let them try. Don't interrupt the first attempt.
3. After: "What felt right about that? What felt forced?"
4. Try again: "Now forget the pitch. Just tell me — what do you actually do and why does it matter?"
5. Compare the two versions. The second is usually closer to truth.

**Writes to**: `discovery.{name}.positioning.elevator_pitch`

**Interviewer notes**: The first attempt is often rehearsed marketing language. The second, more casual version reveals authentic positioning. Note the difference — it's diagnostic.

---

### Brand Eulogy
**Style**: Emotional/reflective | **Duration**: 10-15 min
**Best for**: Reflective thinkers, people who access meaning through emotion

**How to run**:
1. "Imagine your brand disappears tomorrow. Completely gone. What do your customers lose?"
2. Let them sit with it. Don't rush.
3. Follow up: "What would they have to settle for instead? What gap would exist?"
4. Then: "What would your team lose? What work would go unmade?"
5. Synthesize: "The things that would be lost — that's your brand's irreplaceable value."

**Writes to**: `discovery.{name}.positioning.brand_eulogy`

**Interviewer notes**: This technique bypasses the "what do we do" question (which gets functional answers) and goes straight to "why does it matter" (which gets emotional truth). Give people time to think. Silence is productive here.

---

### Competitive Mapping
**Style**: Analytical | **Duration**: 15-20 min
**Best for**: Data-oriented founders, differentiation-focused, strategic thinkers

**How to run**:
1. List 3-5 direct competitors (or the user names them).
2. For each competitor: "In one sentence, what's their thing? What are they known for?"
3. "Now — where are you different? Not better, but *different*. What's the dimension where you occupy unique space?"
4. "Where do you overlap with them? Is that okay, or do you need to differentiate there too?"
5. "If a customer chose you over [competitor], what was the deciding factor?"

**Writes to**: `discovery.{name}.positioning.competitive_map` (array of {name, x, y, notes})

**Interviewer notes**: Watch for "we're better at everything" answers — probe for specifics. The most useful output is identifying the *axis of differentiation* — the dimension where the brand is genuinely unique, not just incrementally better.

---

## Personality Techniques

### Archetype Selection
**Style**: Recognition/narrative | **Duration**: 15-20 min
**Best for**: People who think in stories and characters, intuitive decision-makers

**How to run**:
1. Based on what you've learned so far, present 3-4 relevant archetypes from `archetype-profiles.md`. Read the short description and key question for each.
2. Ask: "Which of these feels most like your brand? Not which you wish it was, but which it actually is?"
3. Once they pick a primary: "What drew you to that one? What specifically resonated?"
4. "Now, is there a secondary? Most brands are a blend. What adds nuance to the primary?"
5. If none resonate: "What's missing? What would the right archetype feel like?" (This often reveals a specific blend.)

**Writes to**: `discovery.{name}.personality.archetypes`, `discovery.{name}.personality.method_used = "archetype-selection"`

**Interviewer notes**: Have `archetype-profiles.md` reference loaded. If the person picks aspirationally, gently probe: "Is that who you are today, or who you want to become? Both are useful — but they inform different design decisions."

---

### Aaker Spectrum Sliders
**Style**: Quantitative | **Duration**: 10-15 min
**Best for**: Analytical thinkers who like scales, people comfortable with numbers

**How to run**:
1. Explain the five dimensions briefly (one sentence each).
2. For each dimension, present the spectrum with anchors:
   - Sincerity: "1 = deliberately impersonal/transactional, 10 = deeply personal/community-centered"
   - Excitement: "1 = measured/calm, 10 = bold/energetic"
   - Competence: "1 = scrappy/experimental, 10 = polished/authoritative"
   - Sophistication: "1 = accessible/casual, 10 = premium/refined"
   - Ruggedness: "1 = gentle/cerebral, 10 = tough/outdoorsy"
3. Ask them to rate each 1-10.
4. For any score above 7 or below 3: "Why so [high/low]? Give me an example of what that looks like for your brand."
5. Read back the profile: "So you're a [sincerity score] sincerity, [excitement score] excitement... Does that feel right?"

**Writes to**: `discovery.{name}.personality.aaker_scores`, `discovery.{name}.personality.method_used = "aaker-sliders"`

**Interviewer notes**: Load `personality-dimensions.md` reference for detailed scoring guides. The most diagnostic questions are about extreme scores (above 7 or below 3). Middle-of-the-road scores (4-6) on everything suggest the person hasn't committed — push gently on which dimensions matter most.

---

### Keyword Distillation
**Style**: Verbal/reductive | **Duration**: 10-15 min
**Best for**: Writers, word-oriented people, those who think in language

**How to run**:
1. "Give me 10-12 words that describe your brand's personality. Don't filter — just free-associate."
2. Write them all down.
3. "Now cross out 4 that matter least."
4. "Of the remaining 8, which 4 could you absolutely not lose?"
5. "Look at your final 4. Do any overlap? Could you combine two into something more precise?"
6. Final output: 4 keywords that define the brand personality.

**Writes to**: `discovery.{name}.personality.keywords`, `discovery.{name}.personality.method_used = "keyword-distillation"`

**Interviewer notes**: The distillation process (cutting from 12 to 4) is where the real insight happens. Watch which words are hard to cut — those are the core. If two keywords feel synonymous, ask: "What's the nuance between [word A] and [word B]? Is there a single word that captures both?"

---

### "If Brand Was A..."
**Style**: Metaphorical/playful | **Duration**: 10-15 min
**Best for**: Creative thinkers, people who access preferences through analogy

**How to run**:
1. Ask a series of metaphorical questions. Pick 4-6 that feel relevant:
   - "If your brand were a car, what kind?"
   - "If your brand were a restaurant, what kind?"
   - "If your brand were a song, what song?"
   - "If your brand were a celebrity, who?"
   - "If your brand were a city, which one?"
   - "If your brand were a fabric/material, what?"
   - "If your brand were a decade, which one?"
   - "If your brand were a drink, what drink?"
2. For each: "Why that one? What specifically about it maps to your brand?"
3. Look for patterns across metaphors: "Your car is a Tesla, your restaurant is a tasting-menu place, your city is Tokyo. I'm seeing innovation + refinement + forward-looking. Does that resonate?"

**Writes to**: `discovery.{name}.personality.metaphors`, `discovery.{name}.personality.method_used = "metaphors"`

**Interviewer notes**: The "why" is more valuable than the answer. "A Tesla" could mean electric/sustainable, or futuristic/tech-forward, or premium/exclusive. The reasoning reveals the actual personality signal.

---

### Celebrity Casting
**Style**: Cultural reference | **Duration**: 5-10 min
**Best for**: Pop-culture-aware people, fast intuitive reads

**How to run**:
1. "If your brand were a person — a celebrity, public figure, or fictional character — who would it be?"
2. "Why them? What specific qualities do they have that match your brand?"
3. "Who would your brand definitely NOT be? Why not?"
4. "If your brand had to give a TED talk, what's the topic and what's the vibe?"

**Writes to**: `discovery.{name}.personality.celebrity_cast`, `discovery.{name}.personality.method_used = "celebrity-casting"`

**Interviewer notes**: This surfaces personality quickly but can be shallow. Best as a supplementary technique combined with something more structured. The anti-cast ("who would you NOT be") is often more revealing.

---

### Brand Playlist
**Style**: Emotional/sensory | **Duration**: 10-15 min
**Best for**: Music-oriented people, those who process emotion through sound

**How to run**:
1. "Pick 3-5 songs that feel like your brand. They don't have to be related — each one should capture a different facet."
2. For each song: "What about this song feels like your brand? Is it the lyrics, the energy, the mood, the production?"
3. "Now — is there a song that's the opposite of your brand?"
4. "If you had to pick just one song as your brand anthem, which one?"
5. Look for patterns: energy level, genre, era, emotional register.

**Writes to**: `discovery.{name}.personality.playlist`, `discovery.{name}.personality.method_used = "brand-playlist"`

**Interviewer notes**: Music accesses emotional territory that direct questions often miss. Pay attention to the energy level and emotional register across their picks — that's personality data. If they pick all high-energy songs, that maps to high excitement. All introspective songs maps to high sincerity.

---

## Visual Techniques

**Important**: All visual techniques use **recognition mode** — presenting options for the person to react to. Nobody is asked to design anything. "Which of these resonates?" not "What do you want?"

### Visual Direction Presentation

Before diving into specific techniques, understand the distinction between **moodboards** and **stylescapes**, and the **Hot/Medium/Mild framework** for presenting directions.

**Moodboard vs. Stylescape**:
- A **moodboard** is a loose collage capturing general feel — images, textures, colors thrown together to evoke a mood. Good for early exploration.
- A **stylescape** (popularized by Chris Do of The Futur) is more curated and intentional — it includes imagery, typography, colors, textures, and UI components arranged with hierarchy. It's "a mood board on steroids" and represents a specific, actionable visual direction.

During discovery, you're gathering the *inputs* for moodboards/stylescapes, not creating them. But understanding the distinction helps frame visual conversations: "Are you describing a general mood, or a specific visual direction?"

**Hot/Medium/Mild Framework**:
When presenting visual direction options (palettes, type pairings, or synthesized directions during `/brand-synthesize`), present **2-3 distinct directions** along a spectrum:
- **Hot**: The bold/radical option — unexpected, distinctive, potentially polarizing
- **Medium**: The balanced option — modern, appropriate, safer
- **Mild**: The conservative option — traditional, familiar, least risk

Each must represent a genuinely different direction, not slight variations. This framework prevents the common trap of presenting three options that are all minor tweaks of the same idea.

**When to use this during discovery**: If a user is struggling to choose between palettes or type pairings, reframe the options using Hot/Medium/Mild: "Let me present these as three levels of boldness — which end of the spectrum pulls you?"

### Palette Recognition
**Style**: Visual choice | **Duration**: 10-15 min
**Best for**: Everyone — this is the most reliable visual technique

**How to run**:
1. Present 5-6 curated palettes from `curated-option-sets.md`. Each palette has a name, hex values, and character description.
2. For each palette: "Does this resonate, feel neutral, or feel wrong for your brand?"
3. For resonating palettes: "What specifically draws you to it? The warmth? The contrast? The mood?"
4. For rejected palettes: "What feels off? Too [what]?"
5. If offering image generation: "I can create visual prompts so you can see these palettes in context — mood boards, applied to a sample layout. Which image generation tool do you use?"
6. **Generate a checkpoint HTML** using the template at `${CLAUDE_PLUGIN_ROOT}/skills/design-system/assets/palette-recognition-test.html`. Substitute the palettes being discussed and write to `brand-assets/{name}-tests/palette-recognition-test.html`. Tell the user the file is ready and wait for their reactions before moving on. See the Checkpoint Artifacts section in `brand-discover/SKILL.md` for the full protocol (iteration rounds, quote capture).

**Writes to**: `discovery.{name}.visual.color_preferences`, `discovery.{name}.visual.method_used = "palette-recognition"`

**Interviewer notes**: Rejections are as valuable as selections. "I hate that because it feels corporate" tells you more than "I like blue." Always ask *why*. Load `curated-option-sets.md` for the actual palettes.

---

### Type Pairing Recognition
**Style**: Visual choice | **Duration**: 10-15 min
**Best for**: Everyone — works alongside palette recognition

**How to run**:
1. Present 3-4 typography pairings from `curated-option-sets.md`. Each has a character description and sample text.
2. For each: "Does this feel like your brand? Too formal? Too casual? Too playful?"
3. Probe on specific qualities: "Is it the weight that feels right, or the letterforms? The spacing?"
4. Ask about formality: "On a scale of formal to casual, where does your brand's text sit?"
5. Ask about warmth: "Does your brand feel warm and approachable in text, or cool and precise?"
6. **Generate a checkpoint HTML** using the template at `${CLAUDE_PLUGIN_ROOT}/skills/design-system/assets/type-pairing-test.html`. Substitute the pairings being discussed and write to `brand-assets/{name}-tests/type-pairing-test.html`. Tell the user the file is ready and wait for their reactions. See the Checkpoint Artifacts section in `brand-discover/SKILL.md` for the full protocol.

**Writes to**: `discovery.{name}.visual.typography_preferences`, `discovery.{name}.visual.method_used = "type-pairing"`

**Interviewer notes**: Most non-designers can't articulate typography preferences directly, but they absolutely can react to examples. Present real pairings, not abstract descriptions.

---

### Mood Board Description
**Style**: Verbal/reference | **Duration**: 10-15 min
**Best for**: People who can name specific sites, apps, spaces, or products that "feel right"

**How to run**:
1. "Think of 3-5 websites, apps, physical spaces, or products that feel like what your brand should feel like. They don't have to be in your industry."
2. For each: "What specifically about the visual feel resonates? The colors? The layout? The photography? The overall mood?"
3. "Now name something that looks good but feels wrong for your brand. What's off about it?"
4. Synthesize: "So you're drawn to [X quality] and [Y quality] but not [Z]. Does that sound right?"

**Writes to**: `discovery.{name}.visual.mood_references`, `discovery.{name}.visual.method_used = "mood-board"`

**Interviewer notes**: If the user wants to show you actual sites/images, work with what they share. If offering image generation: "I can create mood board prompts based on these references so you can see the aesthetic blended together."

---

### Form Language Cards
**Style**: Visual categorization | **Duration**: 5-10 min
**Best for**: Quick intuitive reads on geometric vs. organic vs. mixed

**How to run**:
1. Present three categories:
   - **Geometric**: Sharp corners, straight lines, circles/squares/triangles, mathematical precision
   - **Organic**: Curves, irregular shapes, natural forms, hand-drawn quality, flowing lines
   - **Mixed**: Geometric structure with organic detail, or organic forms with geometric precision
2. "Which of these matches your brand's energy?"
3. "Is that about the shapes themselves, or what they communicate? (Geometric = precision/control, Organic = warmth/naturalness, Mixed = both)"
4. Follow up with specifics: "Sharp corners or rounded? Heavy borders or none? Dense or spacious?"

**Writes to**: `discovery.{name}.visual.form_language`, `discovery.{name}.visual.method_used = "form-language"`

**Interviewer notes**: This is a quick-read technique — good as a supplement to palette or type recognition. The three categories are broad enough that almost everyone can place themselves quickly.

---

### Anti-Inspiration
**Style**: Elimination | **Duration**: 10-15 min
**Best for**: People who know what they don't want more clearly than what they do

**How to run**:
1. "Show me what you absolutely don't want your brand to look like. Name specific brands, sites, or styles."
2. For each: "What specifically feels wrong? The colors? The complexity? The mood? The associations?"
3. "If you had to describe the visual 'enemy' of your brand in one word, what is it?"
4. Invert: "So if you hate [X quality], does the opposite feel right? What would that look like?"
5. Map the anti-inspiration to positive preferences by inverting.

**Writes to**: `discovery.{name}.visual.anti_inspiration`, `discovery.{name}.visual.method_used = "anti-inspiration"`

**Interviewer notes**: This technique is often more revealing than positive preference exercises. People are more confident about what they dislike. Use the rejections to triangulate toward what they want.

---

### Texture & Material
**Style**: Sensory/metaphorical | **Duration**: 5-10 min
**Best for**: People who think in physical, sensory terms

**How to run**:
1. "If your brand were a physical material, what would it be? Brushed metal? Worn leather? Smooth marble? Soft cotton? Rough concrete? Polished glass?"
2. "What about that material captures your brand? The weight? The temperature? The texture?"
3. "Is your brand matte or glossy? Heavy or light? Warm to the touch or cool?"
4. These map to visual choices: matte→flat design, glossy→gradients, heavy→bold weights, light→thin weights, warm→warm tones, cool→cool tones.

**Writes to**: `discovery.{name}.visual.texture_material`, `discovery.{name}.visual.method_used = "texture-material"`

**Interviewer notes**: This is a bridging technique — it connects personality (how the brand feels) to visual decisions (how the brand looks) through physical metaphor. Best paired with form language cards.

---

## Voice & Tone Techniques

### Sample Writing
**Style**: Generative | **Duration**: 10-15 min
**Best for**: People comfortable writing, verbal processors

**How to run**:
1. Give three prompts, one at a time:
   - "Write a tweet (under 280 characters) as your brand."
   - "Your product just had a major outage. Write the first two sentences of the apology."
   - "You just shipped something amazing. Write the announcement opening."
2. After each: "Read it back. Does it sound like you? What would you change?"
3. Compare all three: "Your tweet is [casual/formal], your apology is [casual/formal], your announcement is [casual/formal]. Is that consistent, or does the brand code-switch?"

**Writes to**: `discovery.{name}.voice.sample_tweet`, `.sample_apology`, `.sample_celebration`

**Interviewer notes**: People often write how they think a brand "should" sound, not how their brand actually sounds. After the first draft, ask: "Now write it the way you'd actually say it to a friend." The gap between those two is the gap between aspirational and authentic voice.

---

### Formality Spectrum
**Style**: Quantitative | **Duration**: 5-10 min
**Best for**: Quick calibration, analytical thinkers

**How to run**:
1. Present the spectrum with examples at each end:
   - 1: "hey! 👋 we messed up and we're super sorry" 
   - 3: "Hey there — we hit a snag. Here's what happened."
   - 5: "We encountered an issue and are working on a fix."
   - 7: "We're aware of the disruption and have deployed a resolution."
   - 10: "We regret to inform you that a service interruption has occurred."
2. "Where does your brand sit? Give me a number."
3. "Does it change by context? Is your marketing a 4 but your legal page a 8?"
4. "Is your formality consistent across channels, or do you code-switch?"

**Writes to**: `discovery.{name}.voice.formality_score`

**Interviewer notes**: Most brands sit between 3-7. Scores at the extremes (1-2 or 9-10) are distinctive and should be explored: "That's pretty far out — is that a deliberate choice?"

---

### "Never Say" List
**Style**: Elimination | **Duration**: 5-10 min
**Best for**: People who know what they hate in brand communication

**How to run**:
1. "Name 3-5 words or phrases your brand would never use. Words that make you cringe when other brands use them."
2. Common examples to prompt: "synergy," "disrupt," "leverage," "innovative," "best-in-class," "guru," "rockstar," "circle back," "low-hanging fruit"
3. For each: "What specifically bothers you about that word? What does it signal that your brand isn't?"
4. "Now — is there a word you'd use instead? What's the [your brand] version of that concept?"

**Writes to**: `discovery.{name}.voice.never_say_words`

**Interviewer notes**: The "never say" list is a fast, high-signal technique. The words people hate reveal their values by inversion. If they hate "disrupt," they probably value humility or substance over hype. If they hate "synergy," they value plain language.

---

### Brand Voice Card Sort
**Style**: Recognition | **Duration**: 10-15 min
**Best for**: People who react well to examples, less comfortable generating from scratch

**How to run**:
1. Present 8-10 sample sentences in different brand voices (drawn from `curated-option-sets.md`).
2. For each: "Does this sound like your brand, or not?"
3. Sort into two piles: "sounds like us" and "doesn't sound like us."
4. For the "sounds like us" pile: "What ties these together? What's the common thread?"
5. For the "doesn't" pile: "What's wrong with these? What makes them not-you?"

**Writes to**: `discovery.{name}.voice.voice_card_sort`

**Interviewer notes**: This is the voice equivalent of palette recognition — showing options instead of asking people to generate. It works especially well for people who say "I'll know it when I see it."

---

### Competitor Voice Comparison
**Style**: Analytical | **Duration**: 10-15 min
**Best for**: Strategically-minded people, differentiation focus

**How to run**:
1. Pick 2-3 competitors (or have the user pick them).
2. Read a sample of each competitor's voice (from their website, emails, or social).
3. For each: "What do they do well with their voice? What feels off?"
4. "What would you keep from their approach? What would you change?"
5. "Where should your brand's voice be clearly different from all of them?"

**Writes to**: `discovery.{name}.voice.competitor_voice_notes`

**Interviewer notes**: This technique grounds voice decisions in competitive context. It's especially valuable when the person is in a crowded category where voice is a key differentiator.

---

## Second-Pass Techniques (Stress Tests)

After initial discovery is mostly complete, offer one or more stress tests to pressure-check the emerging identity. These are optional and should be offered, not forced.

### Pre-Mortem
"Assume your brand launched with this identity and completely failed to connect with your audience. Why did it fail? What was the disconnect?"

### Inversion
"What's the exact opposite of your brand? Describe the anti-brand in detail." Then check: "Is your actual brand sufficiently far from this? Where are you closer to the anti-brand than you'd like?"

### Stakeholder Lens
"You've been answering as yourself. Now put on a different hat. How would your most skeptical customer see this brand? How would your most enthusiastic supporter describe it? Are those two descriptions compatible?"

### Time Travel
"It's 3 years from now and your brand is thriving. What does it look like? What evolved? What stayed the same?" Then: "What about that future state can we capture in the identity now?"
