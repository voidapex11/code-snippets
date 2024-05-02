var videoElement = document.querySelector("video")
var audioCtx = new AudioContext()
var source = audioCtx.createMediaElementSource(videoElement)
var gainNode = audioCtx.createGain()
gainNode.gain.value = parseInt(prompt('vol multiplyer'))// get the volume
source.connect(gainNode)
gainNode.connect(audioCtx.destination)
