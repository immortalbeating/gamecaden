<a id="threejs-结构渲染树运行寿命与资源"></a>
# Three.js structure: rendering trees, runtime lifetimes and resources

<a id="何时读取"></a>
## When to read

For new systems, page/level round trips, state/loop ownership, asynchronous loading, instance reuse or DOM/3D UI boundary changes, read applicable sections; local quick changes read only affected entries and acceptance checks. Follow rule IDs from the [Three.js profile](../frameworks/threejs.md), without synonymous Gates. Common triggers, adoption boundaries and record ownership follow the [structure contract](structure-contract.md): lasting agreements belong in original Spec, current approaches in original Task/design, runtime facts in Evidence, acceptance in Decision.

<a id="真实类型与责任"></a>
## Actual types and responsibilities

Scene is a rendering scene, Object3D supplies hierarchy/transforms, Group composes objects, and Mesh connects geometry/materials; these types do not automatically supply game page/level lifecycles, authoritative gameplay state, physics or runtime management. Rendering trees cannot replace business-lifetime diagrams. Ordinary JS/TS models, assembly functions or local framework components may provide rules and page coordination, without fixed file counts, directories or naming. Official basis: [Scene](https://threejs.org/docs/pages/Scene.html), [Object3D](https://threejs.org/docs/pages/Object3D.html), [Mesh](https://threejs.org/docs/pages/Mesh.html).

| Required outcome and trigger | Workflow default / permitted alternatives | Typical counterexamples | Observable acceptance |
|---|---|---|---|
| Page entry/exit and cross-page state are locatable | Page assemblers create scene objects, connect models and release; cross-page model lifetimes follow existing design. Single-page local state may stay in current modules; existing ECS/components may serve the same responsibility. | Treating Group as a level manager; assuming score resets automatically after removing Mesh; UI creating another inventory. | State at entry/exit/new session follows retention/reset rules, with consistent writers/consumers. |
| renderer/canvas, camera and advancement responsibilities are explicit | By default one host coordinates loops, active pages and rendering; explicit division is allowed for multiple views/passes or on-demand rendering. Choose local clock APIs by pause, background recovery and simulation needs. | New RAF on every mount; two modules updating one model; pausing only by hiding Scene. | Remounting does not increase update counts, pause/resume does not jump, canvas/camera are correct. |
| controls, listeners and asynchronous results do not exceed lifetime | Creators remove own listeners/controls; runtime identity or validity checks handle late results, with cancellation used only when actually supported. | Departed loads adding to old Scene; clearing shared buses to remove own listeners. | Leave and return during loading; old results do not contaminate current pages, input is not duplicated. |
| Content sources to multi-instance consumers are traceable | Code factories/actual asset exports and URLs are locatable; instantiate GLTFLoader results as needed, using locally suitable tools for skeletal models; geometry/materials/textures may be shared, with explicit copies when independent mutation is needed. | Adding one Object3D to two parents simultaneously; treating clone as deep-copying every resource; paths working only at development root. | Deployment paths load; two instances have independent transforms/animations; shared changes follow agreements. |
| Unmount releases resources without harming surviving consumers | Owners dispose resources under local APIs after final use ends; handle tree removal separately from resource release, using existing cache/reference strategies if appropriate. | Claiming GPU release after scene.remove; traversing pages to dispose textures still used elsewhere. | Resource trends after round trips follow cache policy, other consumers still render correctly; counts need not all return to zero. |
| Screen size, UI and input mapping agree | Specify canvas CSS/buffer sizes, camera projection and picking conversions; choose DOM UI, 3D UI or local components according to lifetime/accessibility needs. | Enlarging canvas without camera projection updates; DOM buttons triggering raycast and controls too. | Display/hits remain correct at target-size changes, UI toggles and focus changes. |

See [WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html) for loop/size facts and [OrbitControls](https://threejs.org/docs/pages/OrbitControls.html) for controls/update conditions. Current websites do not directly establish local API versions. Required time APIs follow installed versions, without mandating old Clock or new Timer.

<a id="资源与框架条件"></a>
### Resource and framework conditions

[GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html) is an explicitly imported addon; check corresponding decoders, paths and runtime capabilities for relevant compression/extensions, without loading every tool for each asset. Geometry, materials and textures each have release mechanisms: [BufferGeometry](https://threejs.org/docs/pages/BufferGeometry.html), [Material](https://threejs.org/docs/pages/Material.html), [Texture](https://threejs.org/docs/pages/Texture.html). Current Object3D documentation also includes its own dispose; do not assume all older versions have the same interface. Even when objects support dispose, handle shared geometry/materials/textures separately by ownership. Also check handling of image bitmaps used by GLTFLoader.

If React/R3F is selected, first read mounting, frame-loop, cache and automatic/manual disposal strategies for actual integration versions; this page's imperative defaults cannot directly become universal cleanup for all renderer frameworks. Actual browser targets use [Web](../platforms/web.md); for other explicit targets, check actual runtime environments, renderer/adaptation and corresponding official documentation, arranging work according to current conditions.

<a id="候选例子"></a>
## Candidate examples

These are design illustrations only, unrun.

**Simple single page: click to rotate a cube.** One host owns renderer/canvas, camera, loop and Mesh; local angle may stay in the page module, with pointer picking using current canvas coordinates. Exit removes input and loops, releasing owned resources after their final consumers end. Acceptance checks click counts, size changes and unmount/remount, without first creating global services for one page.

**Cross-page: character selection → gameplay → results → new session.** A session model retains selection and session results; the host coordinates active pages, with page assemblers owning rendering trees and input. Asset caches share geometry/textures, character instances own independent transforms/animation state; late loading checks current runtime identity. Gameplay exit removes objects and releases instance-only resources; shared assets follow consumer lifetimes. Acceptance checks two round trips, page switching during loading, return after pause, two characters without state interference and UI/controls input.

<a id="输入来源与工作流交接"></a>
## Input sources and workflow handoff

When page exits, shared models, multiple instances or late loading changes, reference page assembly/loop code, loading/cache implementations, model sources and actual resource consumers to locate update responsibility, instance/shared resource lifetimes and asynchronous exit relationships; do not manually copy full Object3D trees or resource ownership tables. Readable rendering trees cannot independently explain business lifetimes; future relationships differing from current ones still require differences in original design. Where owners or exit semantics are unclear, form necessary local relationship/timing expressions, selecting methods under [material references](../../skills/design/references/game-deliverables.md).

When Three.js is selected but no project exists, first form necessary initial design and mark assembly, model and resource sources as pending creation; planned relationships do not establish integration/runtime success. Camera/canvas/DOM/picking mappings follow mechanisms here; browser common conditions use [Web handoff](../platforms/web.md#handoff-to-skill-stages). develop implements actual consumers; verify checks exit, multiple instances and surviving resources according to current claims, with results in original Evidence/Decision records.

<a id="核对与验证边界"></a>
## Checking and validation boundaries

The official sources above were checked on 2026-10-01; current websites are changing references, so check package/lock/local versions and corresponding source/documentation before implementation. Organization, valid runtime identities and cache strategies in the table are workflow defaults/candidates, not engine-mandated business architecture. This round checked only documentation and links, without running actual projects/examples or checking local dependencies/frameworks and target devices. Record actual scope under [verification](../../shared/verification.md); static checks do not equal runtime or human acceptance.
