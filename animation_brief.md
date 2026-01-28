#   Example Animation prompt for future animation projects

# Animation Title
<short name>

## Goal (1–2 sentences)
What should the viewer understand/do after watching?

## Audience
- Level: (beginner / undergrad / engineer)
- Context: (YouTube / lab meeting / lecture / TikTok)

## Length + Format
- Target duration: (e.g., 45–75s)
- Resolution/FPS: (e.g., 1920x1080 @ 60fps)
- Output: (mp4, gif, transparent webm, etc.)
- Voice: (none / voiceover later / provide script now)
- Music/SFX: (none / subtle / provided assets)

## Style Rules (non-negotiables)
- Fonts: (e.g., Inter / SF Pro / Computer Modern)
- Color palette: (hex codes or “use repo theme tokens”)
- Line thickness rules: (e.g., wires 6px, text stroke 0)
- Motion rules: (e.g., smooth ease-in-out, no bouncy easing)
- Camera rules: (e.g., slow pans only, no spins)
- Text rules: (max words on screen, casing, how to show units)+

## Content Scope
- Must include:
  1) ...
  2) ...
- Must NOT include:
  1) ...
  2) ...
- Terminology glossary (define your preferred wording):
  - CP = Control Pilot
  - PP = Proximity Pilot
  - etc.

## Storyboard (high-level)
Give 5–12 bullets for the flow.
Example:
1) Hook: show problem (5s)
2) Introduce circuit block (10s)
3) Explain signal behavior (20s)
4) Edge cases (10s)
5) Summary + takeaway (5s)

## Scene List (detailed)
(Repeat this block for each scene)

### Scene S01 — <Name>
- Purpose: <what it teaches>
- Visuals:
  - <what appears on screen, in order>
- On-screen text (exact):
  - "<text line 1>"
  - "<text line 2>"
- Animations:
  - <fade in>, <draw>, <highlight>, <zoom>, etc.
- Timing:
  - Target duration: <e.g., 8s>
  - Beat timings: <e.g., 0–2s hook, 2–6s explain, 6–8s transition>
- Assets used:
  - <path/to/svg>, <path/to/image>
- Acceptance criteria:
  - <what makes this “done”>

## Math / Technical Details (if applicable)
- Equations (latex or plain):
- Parameter values:
- Assumptions:
- Edge cases to demonstrate:

## Deliverables
- [ ] Final render
- [ ] Source code committed
- [ ] A “render_all” script
- [ ] Short README: how to reproduce
- [ ] (Optional) separate alpha/transparent version

## Review Plan
- Preview checkpoints:
  - v0: style + motion only
  - v1: full scenes, rough timings
  - v2: final polish
