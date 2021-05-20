<script>
	// import {onMount} from 'svelte';
	class Bucket {
		constructor(name){
			this.name = name;
			this.samples = new Set()
			this.shortcut = this.name.charAt(0).toUpperCase()
		}
	}
	let fileInput = {'files': []}
	let samples = []
	let sampleReaders = []
	let samplesSrc = []
	let samplesAudio = []
	let linkList = []
	let buckets = []
	let defaultBuckets = [
	'kick',
	'snare',
	'high hat',
	'tom',
	'noise',

	'effect',
	'pitch',
	'chord',
	'melody',
	'bass',
]
	

	buckets = defaultBuckets.map(item => new Bucket(item))
	// console.log(buckets[3].shortcut)
	// let audioSrc = '#'
	// const reader = new FileReader()
	let handleChange = async () => {
		// samples = Array.from(fileInput.files).sort((a, b) => a.size - b.size)
		samples = fileInput.files
		// audioSrc = reader.readAsDataURL(fileInput.files[0])
		console.log(samples)
		sampleReaders.length = samples.length
		Object.keys(samples).forEach((sample, index) => {
			sampleReaders[index] = new FileReader()
			sampleReaders[index].readAsDataURL(samples[sample])
			sampleReaders[index].onload = e => {
				samplesSrc[index] = e.target.result
			}
		})
		// console.log(sampleReaders.length)
	}
	// let download = function(name, prefix, src){
  	// 	let link = document.createElement('a')
  	// 	link.download = prefix + name
  	// 	link.href = src.toDataURL()
  	// 	link.click();
	// }
	let renameAndDownload = (prefix, originalfilename, src) => {
		let link = document.createElement('a')
		link.download = prefix + originalfilename
		// console.log(link.download)
		link.href = src
		link.click()
	}
	let exportSamples = () => {
		buckets.forEach((bucket) => {
			bucket.samples.forEach((sample) => {
				renameAndDownload(bucket.name, samples[sample].name, samplesSrc[sample])
			})
		})
		// if (samples) {
		// 	renameAndDownload('kick', samples[0].name, samplesSrc[0])
		// 	// let link = document.createElement('a')
		// 	// link.download = 'testDownload.wav'
		// 	// link.href = samplesSrc[0]
		// 	// link.click()
		// }
	}

	let position = 0
	let handleArrowKey = (code) => {
		// console.log(code + ' pressed')
		if (code == 'ArrowDown'){
			if (position < linkList.length - 1) {
				position += 1
				// console.log(position)
				// console.log(linkList.length - 1)
			}
			linkList[position].focus()
		}
		if (code == 'ArrowUp') {
			position -= 1
			if (position < 0){
				position = 0
			}
			linkList[position].focus()
		}
	}

</script>
	<!-- svelte-ignore a11y-media-has-caption -->
	<!-- <audio src={audioSrc} controls></audio> -->
<svelte:head>
	<style>
		body{
			background: black;
			padding: 0;
			margin: 0;
			color: white;
		}
	</style>
</svelte:head>

<main
on:keydown={(key) => {
	if (key.code == 'Tab' || key.code == 'Enter' || key.code == "Space"){return}
	key.preventDefault()
	if (key.code == "ArrowDown" || key.code == "ArrowUp"){
		handleArrowKey(key.code)
		return
	}
	// if (key.code.length > 1){return}
	if (key.code.slice(0,3) == 'Key'){
		// console.log(key.code + ' pressed')
		let bucketSet = false
		buckets.forEach((bucket) => {
			if (key.code.slice(3) == bucket.shortcut){
				// console.log(key.code + " is a shortcut")
				bucket.samples.add(position)
				buckets = buckets
				// console.log(bucket.samples)
				bucketSet = true
				return
			}
		})
		if (bucketSet) {
			setTimeout(()=>{handleArrowKey("ArrowDown")}, 300)
		}
	}
	}
}>
<input multiple accept="audio/*" type="file" id="fileInput"
on:change={handleChange}
bind:this={fileInput}>
<ul class="samples">
	{#each samples as sample, index}
	<button bind:this={linkList[index]}
	on:focus={() => {
	position = index
	linkList[index].click()
}
	}
	on:blur={() => {
		samplesAudio[index].pause()
		samplesAudio[index].currentTime = 0
		}
	}
	on:click={samplesAudio[index].play()}
	><li><p>{sample.name} 
	</p>
	<!-- <p>size:{sample.size}</p> -->
		<!-- svelte-ignore a11y-media-has-caption -->
		<audio src={samplesSrc[index]} bind:this={samplesAudio[index]}></audio>
	</li></button>
	{/each}
</ul>
<ul class="buckets">
	{#each Object.keys(buckets) as bucket, index}
	<button class="bucket" style="background-color: hsl({360*index/Object.keys(buckets).length}, 60%, 50%);"><li><p><u>{buckets[bucket].name[0]}</u>{buckets[bucket].name.slice(1)}</p><p>{buckets[bucket].samples.size}</p></li></button>
	{/each}
	<button id='export' on:click={exportSamples}>Export Samples</button>
</ul>
</main>

<style>
	#export {
		grid-column: 1/3;
		background: #222;
		color: #AAA;
	}
	#export:hover {
		background: #333;
		}
	#export:active {
		background: #DDD;
		color: #222;
		}

	button:hover, input:hover {
		cursor: pointer;
	}
	input {
		position: fixed;
		z-index: 200;
		background: black;
	}
	main {
		display: grid;
		grid-template-columns: auto auto;
	}
	.samples {
		position: absolute;
		top: 50px;
		/* overflow-x: hidden; */
		/* overflow-y: scroll; */
		display: flex;
		flex-direction: column;
		list-style: none;
		width: 40vw;
	}
	.samples button {
		background: #333;
		color: white;
	}
	.samples button:focus,
	.buckets button:focus
	{
		background: lightgray;
		color: black;
		box-shadow: 0 0 0 5px white;
	}
	.bucket li {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}
	.buckets {
		margin: 0;
		padding: 0;
		position: fixed;
		height: 100vh;
		width: 50vw;
		transform: translate(100%, 0);
		display: grid;
		grid-template-columns: 1fr 1fr;
	}
	.buckets button {
		color: white;
		font-size: 1.15rem;
		margin: 2px;
	}
</style>