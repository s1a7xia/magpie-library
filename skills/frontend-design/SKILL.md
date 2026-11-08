---
name: frontend-design
description: "Intentional UI design for new, redesigned, or plain-looking pages. Use for React/Ant Design CRUD pages, admin consoles, dashboards, login pages, styling and layout changes. Enhance existing components instead of replacing them; use full visual direction only for standalone pages. Triggers: 美化、太丑、不好看、高级感、视觉优化、UI 设计、页面风格、页面改版."
license: Complete terms in LICENSE.txt
---

# Frontend Design

先判断页面属于哪一种模式，再开始设计。模式判断错误，比缺少装饰更伤页面。

## 先选模式

| 页面 | 模式 | 判断 |
|---|---|---|
| 业务 CRUD 页：列表、表单、详情、弹窗、配置、审批 | **Enhance** | 页面已经属于某个产品，有既有组件库、主题和交互习惯 |
| 登录页、工作台首页、态势大屏、独立展示页 | **Design** | 页面是一次性进入、要传达品牌或数据的独立表面 |

业务页不要套用独立站的“工作室视觉”。那会把表格、表单和弹窗装饰化，破坏用户已经熟悉的行为。独立展示页也不要被 Ant Design 组件限制，可以按完整视觉方向设计。

如果项目有自己的 UI 规范，先读项目规范；RuoYi-Vue-Plus 6.x + React 项目读 [前端规范和样式边界](../ruoyi6/references/frontend.md#样式与设计)，本技能负责设计方法，项目规范负责收敛边界。

## Enhance mode

The component library is the design system. Its table, form, dialog, pagination, tag, and empty-state components are the vocabulary; your job is composition and finish.

### What to inherit, not reimplement

- Existing theme tokens and CSS variables. Adjust the accent or a small token set at the theme level; do not hard-code hex values across components.
- The shared layout, spacing scale, and type scale already in the product.
- Existing table, form, dialog, drawer, tag, and empty-state components. Replacing them with hand-rolled markup loses sorting, validation, keyboard behavior, accessibility, and every future framework fix.
- Existing permission, dictionary, and pagination wiring — those are behavior, not styling.

### Where the leverage actually is

- **Hierarchy.** One clear focus per screen: what the page is about, what the primary action is, what is secondary. Most "ugly" admin pages are not under-decorated — they are flat, with every element at the same visual weight.
- **Density and rhythm.** Consistent vertical rhythm, deliberate spacing between page header, filters, table, and pagination. Fewer borders; let whitespace group things instead.
- **Summary layer.** A small, honest set of metrics above a table, when the data supports it. Numbers that answer a real question, not decoration.
- **Semantic color.** Status tags and state colors that mean something and stay consistent across the product.
- **States.** Loading, empty, error, and no-permission states are usually missing entirely. A well-written empty state improves perceived quality more than a gradient does.
- **Detail surfaces.** A drawer or detail panel with a readable label/value rhythm often upgrades a dense table more than any header treatment.

### What to leave alone

Global stylesheet overrides that leak into other pages, per-page copies of the same card, new fonts for one screen, animation on every row, and anything that makes a familiar control behave unexpectedly.

### Cheap-AI tells to avoid on product surfaces

Three things mark a page as machine-decorated rather than designed, and none of them earn their place on an operate surface:

- **Side-stripe borders** — a thick coloured bar stuck down the left edge of a card or list item to make it "pop". It carries no information and reads as a template.
- **Gradient text** — gradient applied to body copy or headings. It hurts contrast and legibility, and it is the single most recognizable generated-page tell.
- **Glassmorphism for its own sake** — stacked blur/translucency with no depth or layering reason behind it; it muddies text and slows rendering.

These are banned as **defaults on operate/product surfaces**, not as techniques. In Design mode a gradient, a glass panel, or a coloured edge can be a deliberate choice if it serves a stated purpose — say what that purpose is.

### Enhancement pass

1. Read the existing tokens, components, and two or three sibling pages. Name the actual conventions you found.
2. State the concrete problem — flat hierarchy, inconsistent spacing, missing states, weak status color — rather than "make it modern".
3. Propose changes confined to the page's own scope, expressed in the system's vocabulary.
4. Implement the smallest set that fixes the stated problem.
5. Before handing off, re-read the changed files and name what was deliberately left alone.

Finish in Enhance mode means the page reads as a deliberate, coherent member of the product — not as a small standalone site wearing the product's components.

## Design mode

Use the full studio approach only for login pages, dashboards, workbench homes, ops/status screens, and standalone showcase pages. Read [references/studio-design.md](references/studio-design.md) before designing; it contains the complete visual-direction method, typography rules, calibration against generic AI design, and copywriting guidance.

In short:

- Establish the subject, audience, and one memorable visual idea before choosing colors.
- Pick a deliberate type scale and a small token system; do not default to cream-and-terracotta, near-black-and-acid-green, or the SaaS-card kit.
- Spend boldness in one place; keep everything around it quiet.
- Responsive down to mobile, visible keyboard focus, reduced motion respected, accessible contrast.

## Craft floor checklist

Verify each item on the rendered page, not on the source. These four failures most often survive a self-review:

- **No unintended horizontal overflow.** No element pushes the page sideways at any supported width; wide tables and long unbroken strings are contained, not clipped or scrolled away. Check at a narrow width, not just your dev window.
- **Button labels never wrap.** A button's text stays on one line — in every locale and at the smallest supported width. A wrapping button means the container is too tight, not that the label is too long.
- **Dark-mode contrast holds.** If the surface supports a dark theme, body text, secondary text, borders and disabled states stay legible against their backgrounds in dark mode, not just light.
- **No z-index collisions.** Dialogs, dropdowns, date pickers, tooltips and drawers stack in the intended order and are never cut off or hidden behind another layer.

## 参考范式（参考，不照抄）

需要判断“成熟后台应该长什么样”时，可以看这些公开范式，重点看信息层级、密度和状态设计，而不是复制视觉皮肤：

- **Ant Design Pro**：页头、筛选区、表格、分页的节奏，状态徽标和空状态写法。
- **Arco Design Pro**：高密度后台布局、详情抽屉、表单分组与留白。
- **shadcn/ui 的 dashboard 示例**：克制的中性色、统一的间距刻度、可访问的交互状态。

借鉴的是结构和判断，不是颜色、字体或某个具体组件。最终仍以当前项目的组件库、主题和 UI 规范为准。

## Output

交付时说明：

- 页面属于 Enhance 还是 Design 模式；
- 实际读过的项目规范、主题 token 和 2–3 个同类页面；
- 改动的具体问题与最小改动集；
- craft floor 四项哪些已在渲染页面核对，哪些留给 `page-acceptance`；
- 明确没有改变权限、字典、分页、校验和弹窗生命周期。
