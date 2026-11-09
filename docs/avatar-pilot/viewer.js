import * as THREE from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

const selector = document.querySelector('#fixture')
const play = document.querySelector('#play')
const midpoint = document.querySelector('#midpoint')
const status = document.querySelector('#status')
const scene = new THREE.Scene()
scene.background = new THREE.Color(0x1d333a)
const camera = new THREE.PerspectiveCamera(35, 600 / 400, 0.1, 50)
camera.position.set(2.2, -2.1, 2.7)
camera.lookAt(0, 0, -0.8)

const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(600, 400)
document.querySelector('#viewport').append(renderer.domElement)
scene.add(new THREE.HemisphereLight(0xe9fcff, 0x5c566c, 2))
const key = new THREE.DirectionalLight(0xffffff, 2)
key.position.set(2, 4, 2)
scene.add(key)

const loader = new GLTFLoader()
let current
let request = 0
let playing = false

async function loadFixture() {
  const id = ++request
  const fixture = selector.value
  play.disabled = midpoint.disabled = true
  playing = false
  status.textContent = 'Loading…'
  if (current) {
    scene.remove(current.model)
    current.mixer.uncacheRoot(current.model)
    current.model.traverse(object => {
      object.geometry?.dispose()
      object.material?.dispose()
      if (object.isSkinnedMesh) object.skeleton.dispose()
    })
    current = undefined
  }
  try {
    const gltf = await loader.loadAsync(`./${fixture}.glb`)
    const [clip] = gltf.animations
    if (!clip) throw new Error('Animation clip missing')
    const mixer = new THREE.AnimationMixer(gltf.scene)
    mixer.clipAction(clip).play()
    if (id !== request) return
    current = { model: gltf.scene, mixer, clip }
    scene.add(current.model)
    mixer.setTime(0)
    play.disabled = midpoint.disabled = false
    status.textContent = `${fixture} · ${clip.duration.toFixed(2)} seconds`
  } catch (error) {
    if (id === request) status.textContent = `Load failed: ${error.message}`
  }
}

selector.addEventListener('change', loadFixture)
play.addEventListener('click', () => { playing = !playing })
midpoint.addEventListener('click', () => {
  playing = false
  current.mixer.setTime(current.clip.duration / 2)
})

let previous = performance.now()
renderer.setAnimationLoop(now => {
  if (playing) current.mixer.update((now - previous) / 1000)
  previous = now
  renderer.render(scene, camera)
})
loadFixture()
