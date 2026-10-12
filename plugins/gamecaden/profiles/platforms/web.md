<a id="web-浏览器平台-profile"></a>
# Web browser platform profile

<a id="触发与版本边界"></a>
## Triggers and version boundaries

Add this page when actual runtime targets include browser pages: native HTML/JS, Phaser, Three.js and browser outputs of Godot/Unity/Cocos Creator all apply. First confirm runtime roots, target browsers and release methods under [rule selection](../../shared/rules.md); do not load for non-browser runtime. These are platform rules, without choosing game engines or requiring Node, Vite, React or TypeScript. Browser behavior is determined by actual target-environment tests; consult corresponding profiles and project configuration separately for particular bundler/engine versions.

For WebGL/WebGPU selection, objects/resources and render loops, use entries for the actual framework: [Three.js](../frameworks/threejs.md) or the current other stack. Check APIs, resources and delivery conditions for other targets against actual runtime environments; browser evidence retains its own scope.

<a id="需现场识别的事实"></a>
## Facts to identify in the project

- Whether HTML loads directly, through development/preview servers or as deployed pages; page origin, base path, asset URLs and build-output locations.
- Who manages game display/DOM overlay size, scaling, scrolling, device pixel ratio and input focus; target devices and pointer, keyboard and touch requirements.
- Whether state persists across refresh; actual storage medium, version, recovery entry and user-visible failure behavior.
- Committed browsers, background/foreground, audio startup, offline or deployment conditions; do not expand checks when unaffected.

<a id="条件规则"></a>
## Conditional rules

Rule nature follows [rules](../../shared/rules.md): required conditions apply when triggered; default approaches may change according to valid designs. Each row collects evidence only for applicable consumers.

| ID | Nature and trigger | Requirement or default approach | Observable validation |
|---|---|---|---|
| WEB-RUNTIME | Required: confirming browser game runtime roots | Confirm page, script, asset and service paths from actual entries and build/deployment configuration; identify sidecar Web panels separately as their own product surfaces. | Point to actual entries/resource requests; files in local project trees do not prove pages can load. |
| WEB-COORD | Required: input, display or DOM overlays involve coordinates | Confirm owners of CSS/canvas scaling, viewport changes and input-coordinate conversion; keep hit areas aligned with visible positions. | Actual clicks, drags or hits reach the same targets at target sizes, zoom and touch/pointer paths. |
| WEB-FOCUS | Required: keyboard, touch or page controls participate together | Define game focus, form focus, pause/resume and default browser-behavior boundaries; intercept only input needed now. | Returning from page controls to game or switching tabs and back does not lose or incorrectly trigger input. |
| WEB-VISIBILITY | Default: background affects time advancement, audio or network behavior | Use page visibility and actual time sources to choose pause, clamping, catch-up or continuation strategies; avoid undesigned large simulation jumps on recovery. | After hiding tabs for a time and returning, timing, animation and state follow current rules. |
| WEB-AUDIO | Required: this work includes audible media/audio | Design startup after first user interaction and failure fallback according to browser autoplay limits; successful initialization does not establish audible output. | First entry in new sessions, after user actions and rejection all have observable outcomes. |
| WEB-STORAGE | Required: local saves/settings are promised | Actual consumers own reading, writing, version parsing and corrupt/denied-storage handling; successful calls or file existence do not establish recovery. | Save, refresh and restore through actual UI paths; denial/corruption tests do not falsely claim success. |
| WEB-DEPLOY | Required: delivering deployable browser versions | Check resource URLs, routing/refresh, fonts/audio and relevant dependencies using target-service base paths and actual outputs; development-server success does not prove release outputs. | Start actual outputs from delivery paths and observe network requests, initial screen and target user paths. |
| WEB-INPUT-MODES | Default: targets include touchscreens and desktop | Check pointer types, gestures, touch scrolling and touchable areas against the established device set; all-platform certification for uncommitted devices is unnecessary. | Complete current natural input paths under representative devices or simulated conditions. |
| WEB-REAL-PATH | Required: delivery claims involve actual page presentation or user paths | Check actual page paths supporting current results, especially affected cross-page/refresh, first-frame, black-screen and overlay behavior. Reuse other areas sufficiently covered by static/simulated tests directly. | Evidence identifies browser, URL, build baseline and actual user paths, without substituting test counts. |

<a id="路径与状态责任"></a>
## Path and state responsibilities

This platform does not prescribe directories such as `src/`, `public/` or `dist/`. Record the project's entries, output directories, deployment prefixes and resource consumers; see [project structure](../project-structure.md) for directory suggestions and the [profiles overview](../README.md)/[common boundaries](../common.md) for shared working methods. Browser `localStorage` is isolated by origin and may be denied by policy; check whether page drafts, caches or local feedback enter authoritative sources under [asset handoff](../../shared/asset-handoff.md).

<a id="与-skill-阶段交接"></a>
## Handoff to Skill stages

- `flow/init`: Identify browser runtime roots and effective project rules; existing projects register only relevant sources, without migrating every directory.
- `brainstorm/design`: Specify user paths, owners and observable outcomes only when current commitments are affected by input, size, saves, background, audio or deployment. Paths/deployment reuse build/page configuration and actual URLs; canvas/DOM input reuses layout/runtime implementation; storage recovery reuses original data and recovery entries. Reference sufficient existing sources; when targets change or focus, recovery or path meanings are unclear, add changed relationships to original design, forming local flow/timing expressions when needed, without another copied configuration table.
- `develop/assets`: Wire actual consumers; browser previews prove only preview scope, with asset adoption/formal integration following shared rules.
- `verify/close`: Reuse valid same-baseline evidence and add only target-browser/delivery-path gaps; see the [verification contract](../../shared/verification.md) for conclusion boundaries. Use original Task/Evidence/Decision records, without another Web state ledger.

The browser common conditions above are maintained centrally here; framework topics add only their own mechanisms. With no project but a selected browser target, form initial arrangements first and mark configuration/runtime sources as pending creation; planned URLs, wiring and recovery strategies do not represent deployment or runtime success. Take related interaction, save and platform uses from [game material references](../../skills/design/references/game-deliverables.md) as needed.

<a id="官网依据与未验证范围"></a>
## Official basis and unverified scope

- MDN: [Page Visibility API](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API) (background-tab timing may be throttled), [Pointer Events](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events), [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) (origin-scoped and may throw `SecurityError`), [Autoplay](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay).
- Directories, validation paths and state responsibilities here are workflow judgments, without claiming MDN requires a particular architecture. This round checked only documentation and existing project experience, without starting browsers, building or deploying actual projects; browser compatibility still requires tests against target versions.
