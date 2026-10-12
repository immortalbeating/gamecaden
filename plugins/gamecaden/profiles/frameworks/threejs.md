<a id="threejs-框架-profile"></a>
# Three.js framework profile

<a id="触发与现场边界"></a>
## Triggers and local boundaries

Read this when the actual runtime root uses Three.js, or current design explicitly selects it. First check package, lockfile/installed version, entry, renderer and addons; design selection does not establish installation. Actual browser targets add [Web](../platforms/web.md); for other explicit targets, check actual runtime environments, adaptation and official documentation, without treating library names as proof of target support. For React / React Three Fiber (R3F), read actual integration versions, lifecycles and resource strategies only when adopted locally, without introducing them by default.

Locate renderer/canvas, camera, update/render entries, page assembly/unmount owners, business state, controls, loaders/URLs, shared-resource consumers and DOM/3D input boundaries. For new systems, page switching/re-entry or changes to these responsibilities, read the [Three.js structure topic](../references/threejs-structure.md) as needed; quick changes read only applicable entries.

<a id="条件规则"></a>
## Conditional rules

Rule nature follows [rules](../../shared/rules.md). Required entries constrain outcomes; existing arrangements achieving the same outcomes may replace default entries.

| ID | Nature and trigger | Requirement or default approach | Observable validation |
|---|---|---|---|
| THREE-ENTRY | Required: identifying runtime roots or changing hosts | Confirm version, renderer/canvas, camera, actual entry and target rendering capabilities; check addons' core versions/import methods locally. | Current entry uses expected canvas/camera, and target hosts actually render. |
| THREE-OWNER | Required: new pages/levels or shared state | Scene/Object3D/Group are rendering/transform trees; specify page lifecycle, business state and physics/runtime management responsibilities. | Expected state persists/resets on entry, exit and new sessions; consumers are locatable. |
| THREE-LOOP | Required: update, mounting or pause changes | The same responsibility must not be updated/rendered twice; specify clocks, pause/resume, mounting and loop removal. Explicit coordinators may arrange multiple passes/views. | Update counts and time behavior match design after remount, background return and pause. |
| THREE-ASYNC | Required: asynchronous loading or cross-lifecycle listeners | On exit, remove own external listeners/controls; accept/release asynchronous results according to valid runtime identity, with cancellation capabilities determined by actual loaders. | Loading results after exit do not write old pages; re-entry does not duplicate events. |
| THREE-ASSET | Required: loading/reusing formal resources | Connect URLs, deployment base paths, GLTFLoader and decoders for relevant extensions to actual consumers; distinguish instance state from shared geometry/materials/textures. | Actual entry displays/plays target assets; multiple instances do not interfere with state and shared consumers remain valid. |
| THREE-DISPOSE | Required: replacing/unmounting GPU resources | Removing from Scene does not mean release; explicitly release unused geometry/material/texture and other resources through local APIs, checking other consumers/owners first. | Object/resource usage trends after round trips match retention strategies; surviving consumers are not mistakenly released. |
| THREE-INPUT-SIZE | Required: UI, camera, size or input changes | Align CSS sizes, drawing buffers, camera projection and pointer conversion; specify controls, 3D picking, DOM focus and event consumption. | Display/hits agree at target sizes; UI operations do not unexpectedly drive cameras/gameplay. |
| THREE-MODEL | Default: rules and display start constraining each other | Ordinary JS/TS models hold reusable rules, assemblers connect rendering objects; simple local rules may remain in current modules, retaining valid existing architecture. | Model owners, display consumers and release entries are directly locatable. |

<a id="阶段交接与来源"></a>
## Stage handoff and sources

`flow/init` identifies local facts; `design` writes applicable owners, lifetimes and plans into original Task/design or Spec; `develop/assets` wire consumers, with asset status following [asset handoff](../../shared/asset-handoff.md); `verify/close` add actual affected coverage under the [verification contract](../../shared/verification.md), while original records still own Evidence and Decision.

Documentation checked on 2026-10-01: official [Object3D](https://threejs.org/docs/pages/Object3D.html) describes hierarchy/removal and shared resources; [WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html) covers canvas, loops, sizes and release; [GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html) covers URLs and addons/decoders; [OrbitControls](https://threejs.org/docs/pages/OrbitControls.html) covers camera controls. These current official pages do not prove fixed-version compatibility; check local versions before adopting APIs. Business organization and lifecycle ownership are workflow choices. This round did not install/run engines or actual projects, and did not validate any local versions or R3F integrations.
