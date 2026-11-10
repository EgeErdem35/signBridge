import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { AnimationMixer, REVISION } from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

const joints = ['index', 'middle', 'ring', 'little'].flatMap(finger => [
  `${finger}_base`,
  `${finger}_tip`
])

console.log(`Node ${process.version} · Three.js r${REVISION}`)
for (const [fixture, movingJoints] of [
  ['index-curl', joints.slice(0, 2)],
  ['four-finger-curl', joints]
]) {
  const bytes = await readFile(new URL(`./${fixture}.glb`, import.meta.url))
  const { scene, animations } = await new GLTFLoader().parseAsync(new Uint8Array(bytes).buffer, '')
  assert.equal(animations.length, 1)
  const [clip] = animations
  assert.equal(clip.name, fixture)
  assert.equal(clip.duration, 2)
  assert.equal(scene.getObjectByProperty('isSkinnedMesh', true)?.skeleton.bones.length, 10)
  const mixer = new AnimationMixer(scene)
  mixer.clipAction(clip).play()
  mixer.setTime(0)
  const start = joints.map(name => scene.getObjectByName(name).quaternion.clone())
  mixer.setTime(1)
  const observed = joints.filter((name, index) => {
    const angle = scene.getObjectByName(name).quaternion.angleTo(start[index])
    return angle > 0.1
  })
  assert.deepEqual(observed, movingJoints)
  mixer.setTime(1.99)
  for (const [index, name] of joints.entries()) {
    assert.ok(scene.getObjectByName(name).quaternion.angleTo(start[index]) < 0.01)
  }
  console.log(`PASS ${fixture} · ${clip.duration.toFixed(2)} s · ${observed.join(', ')}`)
}

for (const fixture of ['tid-many', 'tid-maternal-aunt']) {
  const bytes = await readFile(new URL(`./${fixture}.glb`, import.meta.url))
  const { scene, animations } = await new GLTFLoader().parseAsync(new Uint8Array(bytes).buffer, '')
  assert.equal(animations.length, 1)
  const [clip] = animations
  assert.equal(clip.name, fixture)
  assert.equal(clip.duration, 1.5)
  assert.ok(scene.getObjectByName('Head'))
  const hand = scene.getObjectByName('SyntheticHand')
  assert.ok(hand)
  const index = scene.getObjectByName('index_base')
  const ring = scene.getObjectByName('ring_base')
  const mixer = new AnimationMixer(scene)
  mixer.clipAction(clip).play()
  mixer.setTime(0)
  const initialLocation = hand.position.clone()
  const initialIndex = index.quaternion.clone()
  const initialRing = ring.quaternion.clone()
  mixer.setTime(1.25)
  if (fixture === 'tid-many') {
    assert.ok(hand.position.distanceTo(initialLocation) < 0.1)
    assert.ok(index.quaternion.angleTo(initialIndex) > 0.3)
    assert.ok(ring.quaternion.angleTo(initialRing) > 0.3)
  } else {
    assert.ok(initialLocation.x < -0.4)
    assert.ok(hand.position.x > 0.4)
    assert.ok(index.quaternion.angleTo(initialIndex) < 0.01)
    assert.ok(ring.quaternion.angleTo(initialRing) < 0.01)
    assert.ok(index.quaternion.angleTo(ring.quaternion) > 0.7)
  }
  console.log(`PASS ${fixture} · ${clip.duration.toFixed(2)} s · reference feature checks`)
}
