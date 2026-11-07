---
name: frontend-design
description: "Intentional visual design for new or reshaped UI, including improving pages that already look plain or templated. Covers aesthetic direction, typography, hierarchy, spacing, color, and — for admin consoles and back-office screens — enhancing an existing component library instead of replacing it. Use when building a page, redesigning or beautifying one, or when the user says 美化、太丑、不好看、高级感、视觉优化、界面重做、UI 设计、dashboard 设计、页面风格."
license: Complete terms in LICENSE.txt
---

# Frontend Design

Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's. This client has already rejected proposals that felt cliché or templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk if justified.

## Ground your designs in the subject matter

If the brief does not identify what the product or subject matter is, identify it yourself before designing, and confirm with the client. You can come up with one concrete subject, the design's audience, and the design's primary job, as a proposal. If there's any information in your memory about the client's preferences or context about what they're building, use that as a hint. The subject's industry, subject matter, materials, and vernacular are where distinctive visual choices come from — a design for a toy for girls aged 8–11 will be very aesthetically different from a dashboard for financial analysts. Build with the brief's real content and subject matter throughout.

## Design principles

For web designs, the hero is the first thing viewers will see. Open with the most characteristic thing in the subject's world, in the form that is most appropriate: a headline, an image, an animation, a live demo, an interactive moment, or other treatments. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option.

Typography carries the personality of the page. You don't need a different typeface for display or headline text and body content: use one family or two, and if two, make them clearly distinct.

Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style with intentional weights, widths, and spacing. When type is used as a headline or visual element, use the type treatment itself as an active part of the design, not a neutral delivery vehicle for the content.

Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.

Avoid these default typographic treatments; they are the commonest tells of a generated page:
- Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
- Using all caps for labels.
- Adding unnecessary typographic labels above content.

Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence — like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.

Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Process: plan, review against the brief, build, critique

For calibration, AI-generated design right now clusters around some traits:
1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757 — Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text.

All traits are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly — the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. As with a hired human designer, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.

Work in two passes. First, brainstorm a short design plan based on the client's design brief: create a compact token system with color, type, layout, and principles.
- Color: describe the core base palette as 4–6 named hex values.
- Type: the typefaces and their roles.
- Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare. Include alignment guidance; should the content be left aligned, center aligned, justified?
- Principles: the high-level guidance for what makes this page unique.

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief — revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and an element-based selector like .cta). This can happen often with padding/margin between sections.

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes. Critique your own work as you build, taking screenshots to review if your environment supports it — a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creatives have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

### Craft floor checklist

The quality floor above is a set of claims — verify each one on the rendered page, not on the source. These four are the failures that most often survive a self-review:

- **No unintended horizontal overflow.** No element pushes the page sideways at any supported width; wide tables and long unbroken strings are contained, not clipped or scrolled away. Check at a narrow width, not just your dev window.
- **Button labels never wrap.** A button's text stays on one line — in every locale and at the smallest supported width. A wrapping button means the container is too tight, not that the label is too long.
- **Dark-mode contrast holds.** If the surface supports a dark theme, body text, secondary text, borders and disabled states stay legible against their backgrounds in dark mode, not just light.
- **No z-index collisions.** Dialogs, dropdowns, date pickers, tooltips and drawers stack in the intended order and are never cut off or hidden behind another layer.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.

Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.

---

*Modified by Magpie on 2026-11-07: added the "Inside an existing design system" mode below, the "Craft floor checklist" section above, and the cheap-AI tells list inside Enhance mode. The original guidance is unchanged.*

## Inside an existing design system

Not every page is a fresh identity. Admin consoles, back-office CRUD screens, and internal dashboards already have a component library, a token set and a house style, and the job there is **raising the quality bar inside that system**, not replacing it. Read this mode instead of the studio-identity approach above when the target page already lives in a product with an established component library.

### The split that decides everything

Classify the surface before designing anything:

| Surface | Mode |
|---|---|
| Business CRUD page (list, form, detail, dialog) | **Enhance** — inherit the system, spend effort on hierarchy and finish |
| Login page, dashboard, workbench home, ops/status screen, standalone showcase page | **Design** — the studio approach above applies freely (dark themes, high-contrast metric cards and chart work belong here) |

Applying studio-identity thinking to a CRUD page produces exactly the failure the user is complaining about: the layout gets decorated, the table loses its familiar behavior, and the page becomes worse to use.

### Enhance mode

The component library is the design system. Its table, form, dialog, pagination, tag, and empty-state components are the vocabulary; your job is composition and finish.

**What to inherit, not reimplement:**

- Existing theme tokens and CSS variables. Adjust the accent or a small token set at the theme level; do not hard-code hex values across components.
- The shared layout, spacing scale, and type scale already in the product.
- Existing table, form, dialog, drawer, tag, and empty-state components. Replacing them with hand-rolled markup loses sorting, validation, keyboard behavior, accessibility, and every future framework fix.
- Existing permission, dictionary, and pagination wiring — those are behavior, not styling.

**Where the leverage actually is:**

- **Hierarchy.** One clear focus per screen: what the page is about, what the primary action is, what is secondary. Most "ugly" admin pages are not under-decorated — they are flat, with every element at the same visual weight.
- **Density and rhythm.** Consistent vertical rhythm, deliberate spacing between page header, filters, table, and pagination. Fewer borders; let whitespace group things instead.
- **Summary layer.** A small, honest set of metrics above a table, when the data supports it. Numbers that answer a real question, not decoration.
- **Semantic color.** Status tags and state colors that mean something and stay consistent across the product.
- **States.** Loading, empty, error, and no-permission states are usually missing entirely. A well-written empty state improves perceived quality more than a gradient does.
- **Detail surfaces.** A drawer or detail panel with a readable label/value rhythm often upgrades a dense table more than any header treatment.

**What to leave alone:** global stylesheet overrides that leak into other pages, per-page copies of the same card, new fonts for one screen, animation on every row, and anything that makes a familiar control behave unexpectedly.

**Cheap-AI tells to avoid (product surfaces):** three things mark a page as machine-decorated rather than designed, and none of them earn their place on an operate surface:

- **Side-stripe borders** — a thick coloured bar stuck down the left edge of a card or list item to make it "pop". It carries no information and reads as a template.
- **Gradient text** — gradient applied to body copy or headings. It hurts contrast and legibility, and it is the single most recognizable generated-page tell.
- **Glassmorphism for its own sake** — stacked blur/translucency with no depth or layering reason behind it; it muddies text and slows rendering.

The same rule as the calibration list above applies: these are banned as **defaults on operate/product surfaces**, not as techniques. In Experience mode a gradient, a glass panel, or a coloured edge can be a deliberate choice if it serves a stated purpose — say what that purpose is.

### Enhancement pass

1. Read the existing tokens, components, and two or three sibling pages. Name the actual conventions you found.
2. State the concrete problem — flat hierarchy, inconsistent spacing, missing states, weak status color — rather than "make it modern".
3. Propose changes confined to the page's own scope, expressed in the system's vocabulary.
4. Implement the smallest set that fixes the stated problem.
5. Look at the rendered page, not the source. Then remove one thing.

Finish in enhance mode means the page reads as a deliberate, coherent member of the product — not as a small standalone site wearing the product's components.
