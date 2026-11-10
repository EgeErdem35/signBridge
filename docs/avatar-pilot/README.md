# SB-40 · Avatar feasibility pilot

[Jira SB-40](https://el-dili.atlassian.net/browse/SB-40) · [SB-25 research](../SB-25-3D-Avatar-Approach-Research.md) · [Statement of Work](https://el-dili.atlassian.net/wiki/spaces/SIGNBRIDGE/pages/5046283)

## Method and permitted inputs

This quick pilot uses the manual keyframe method proposed in SB-25. A Blender script builds an original, simplified 10-bone hand with a skinned mesh. It authors two fixtures at 24 fps, each with a rest pose, a midpoint curl and a return to rest. The expected output is one named, two-second clip per GLB, playable with Three.js in Chromium. Keyframes are authored explicitly in the script, with no motion estimation.

- Blender 4.5.3 LTS (build `67807e1800cc`) for rigging, keyframes and GLB export. Blender's [license](https://www.blender.org/about/license/) covers the application and distinguishes it from artwork it produces. The Blender Python script carries a GPL-3.0-or-later SPDX identifier.
- Three.js 0.180.0, [MIT](https://github.com/mrdoob/three.js/blob/r180/LICENSE), for [GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html), AnimationMixer and WebGL rendering. It is installed from npm and is not bundled in the repo.
- Original geometry and motion values generated locally by `make_fixtures.py`. The two curls are synthetic test movements. There are no third-party rigs, recordings, AUTSL data, participant material or uploads to an external processing service.

## Watch the animations locally

Requires Node.js with npm (tested on Node.js 24), Python 3 and a WebGL2 browser. The repository includes the GLBs, so playback uses the files as checked out.

From the repository root:

```sh
cd docs/avatar-pilot
npm ci
node verify.mjs
python -m http.server 8040 --bind 127.0.0.1
```

Open [http://127.0.0.1:8040/](http://127.0.0.1:8040/) in a WebGL2 browser. In the **Fixture** menu, choose either synthetic curl or **TİD · Çok** / **TİD · Teyze**, then click **Play / pause**. **Midpoint** jumps to the middle of the selected clip. The TİD clips hold their final pose. Press **Play / pause** again to replay. For the negative case, block the request to `index-curl.glb` in the browser, switch from the other fixture back to Index curl, and verify that the viewer shows a load error and disables both controls. Unblock the request afterward.

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

## Follow-up with documented TİD signs

Two lexical signs were manually approximated from the start/end photo sequences in §2.1.1 of *A Grammar of Turkish Sign Language* (Meltem Kelepir, ed., SIGN-HUB, 2020). [Reference sequences](https://thesignhub.eu/node/692) · [Source and license statement](https://thesignhub.eu/assets/grammar/641/signhub_grammar_tid.pdf). The photo sequences are linked for comparison. The repo contains original geometry, manually authored pose adaptations and rendered results. The two pose datasets (`tid_many.py`, `tid_maternal_aunt.py`), their GLBs and their paired screenshots are shared under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) as noncommercial adaptations of those references. The generator code carries its own SPDX notice.

| Example | Handshape, location and movement compared with the reference | Correction made | Measured execution |
| --- | --- | --- | --- |
| ÇOK (MANY) | One right hand near the upper chest, to the side. Spread fingers gather with limited wrist translation, matching the reference aperture change qualitatively. Palm angle and fingertip contact are approximate. [Start and end](tid-many.png) | Increased finger convergence after the first export. | First Blender scene/keyframe build 0.424 s and export 0.633 s. Correction command, including Blender restart and re-export, 16.728 s wall time. |
| TEYZE (MATERNAL_AUNT) | Index and middle fingers stay extended together as the hand passes from the signer's right cheek to left. The middle path and depth, fingertip contact, and exact orientation are approximate. [Start and end](tid-maternal-aunt.png) | Moved both endpoints closer to the cheeks and adjusted the final horizontal placement. | First Blender scene/keyframe build 0.350 s and export 0.481 s. Correction command, including Blender restart and re-export, 8.078 s wall time. |

Timing is for this scripted execution only. Source inspection, designing the pose parameters and reviewing the renders were not independently timed. The correction timings include process startup, with different runtime loads, so neither timing is a human authoring estimate or a basis for extrapolating to 300 signs.

From this directory, regenerate the two additional clips with `blender --background --python-exit-code 1 --python make_tid_fixtures.py` (tested with Blender 4.3.2). Run `node verify.mjs` and serve the viewer as described above. Select either TİD example and press **Play / pause**. At completion the viewer holds the end pose and the next press restarts the clip. Three.js verified the GLB names, duration, and motion properties. Chromium 141 rendered both start and end poses, held the end pose and restarted on replay. The original two synthetic clips also passed the Node verifier.

The still sequences establish reference endpoints, so the 1.5-second duration and the in-between path are authoring choices. The model represents a simplified hand with head and shoulder landmarks. It lacks a full arm, facial expression and mouth articulation. This comparison is a technical inspection against the reference poses. Signer comprehension, independent linguistic fidelity, and video motion extraction and retargeting remain untested.

## Decision and next steps

Blender-authored GLB clips played in the browser for both synthetic finger motion and the two documented TİD approximations. Recognition, video landmark extraction, retargeting, facial animation, independent TİD fidelity, mobile performance and user comprehension remain untested. The O4 target of at least 300 signs plus fingerspelling remains unvalidated.

Review ÇOK and TEYZE with a qualified TİD user before expanding the sample to two-handed signs, complex handshapes and non-manual cues. Check the use and redistribution rights for each additional reference and rig. Record active authoring, correction and review time separately. Compare desktop and mobile playback, then test retargeting against the manual baseline before extrapolating effort. Participant studies follow the project's ethics process.
