# SB-40 · Avatar feasibility pilot

[Jira SB-40](https://el-dili.atlassian.net/browse/SB-40) · [SB-25 research](../SB-25-3D-Avatar-Approach-Research.md) · [Statement of Work](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/5046283)

## Method and permitted inputs

This quick pilot uses the manual keyframe method proposed in SB-25. A Blender script builds an original, simplified 10-bone hand with a skinned mesh. It authors two fixtures at 24 fps, each with a rest pose, a midpoint curl and a return to rest. The expected output is one named, two-second clip per GLB, playable with Three.js in Chromium. Keyframes are authored explicitly in the script, with no motion estimation.

- Blender 4.5.3 LTS (build `67807e1800cc`) for rigging, keyframes and GLB export. Blender's [license](https://www.blender.org/about/license/) covers the application and distinguishes it from artwork it produces. The Blender Python script carries a GPL-3.0-or-later SPDX identifier.
- Three.js 0.180.0, [MIT](https://github.com/mrdoob/three.js/blob/r180/LICENSE), for [GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html), AnimationMixer and WebGL rendering. It is installed from npm and is not bundled in the repo.
- Original geometry and motion values generated locally by `make_fixtures.py`. The two curls are synthetic test movements. There are no third-party rigs, recordings, AUTSL data, participant material or uploads to an external processing service.

## Reproduce

From the repository root:

```sh
cd docs/avatar-pilot
npm ci
node verify.mjs
python -m http.server 8040 --bind 127.0.0.1
```

Open [http://127.0.0.1:8040/](http://127.0.0.1:8040/) in a WebGL2 browser. For each fixture, observe the initial pose, click **Midpoint**, and click **Play / pause** to start and pause the animation. For the negative case, block the request to `index-curl.glb` in the browser, switch from the other fixture back to Index curl, and verify that the viewer shows a load error and disables both controls. Unblock the request afterward.

The generated GLBs are committed for immediate reproduction. To rebuild them with Blender 4.5.3, run:

```sh
blender --background --python-exit-code 1 --python make_fixtures.py
node verify.mjs
```

## Observed results

Run on Linux with Node.js 24.22.1 and headless Chromium 141.0.7390.0 using software WebGL. The Node verifier loaded each GLB with Three.js, checked the clip name and duration, and compared joint rotations at rest, midpoint, and near the end. Chromium loaded and rendered both fixtures. Captured canvas frames changed between rest and midpoint and again during playback.

| Case | Expected | Observed |
| --- | --- | --- |
| Index curl | Only the two index joints bend | Pass. Both index joints moved and the other tested finger joints held their pose. [Midpoint screenshot](index-curl.png) |
| Four-finger curl | All eight tested finger joints bend | Pass. All eight moved. [Midpoint screenshot](four-finger-curl.png) |
| Return to rest | Both clips return near their initial rotations | Pass. Each tested joint was within 0.01 rad of rest at 1.99 s. |
| Missing GLB | Show load error and disable playback controls | Pass. Simulated HTTP 404 produced visible feedback and no uncaught page error. |

Initial exports exposed three issues. Active Actions used the generic clip name `Animation`. Switching to Actions restored the desired name, but the first frame added one frame to the reported clip length and the second export included the previous action. Sliding the timeline to zero and removing the previous action before the next export made both fixtures pass the same verifier.

## Decision and next steps

The pilot supports using Blender-authored GLB clips for browser playback. It covers original rig authoring, export and playback of synthetic finger motion on one browser configuration. Recognition, video landmark extraction, retargeting, facial animation, real TİD sign fidelity, mobile/device performance and user comprehension remain untested. The O4 target of at least 300 signs plus fingerspelling remains unvalidated.

Next, verify the rights to use and redistribute each selected TİD reference and rig, then choose a small representative set covering one- and two-handed signs, complex handshapes and non-manual cues. Measure authoring, correction and review time separately and check linguistic fidelity with qualified TİD input. Compare desktop/mobile playback and the manual baseline with a separate retargeting experiment before extrapolating effort. Participant studies follow the project's ethics process.
