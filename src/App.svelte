<script>
// import { subscribe } from "svelte/internal";
	// import {onMount} from 'svelte';
	class Bucket {
		constructor(name, hslstring){
			this.name = name;
			this.samples = new Set()
			this.shortcut = this.name.charAt(0).toUpperCase()
			this.size = 0
			this.duration = 0
			this.hslstring = hslstring
		}
	}
	let editMode = {"active": false, "category": ""}
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
	'high_hat',
	'tom',
	'noise',

	'effect',
	'pitch',
	'chord',
	'melody',
	'bass',
]

	$: classified = buckets.reduce((accum, current) => {
		return accum + current.samples.size
	}, 0);
	
	$: megabytes = (buckets.reduce((accum, bucket) => {
		return accum + bucket.size
	}, 0) / (1024**2)).toFixed(3);

	$: duration = (buckets.reduce((accum, bucket) => {
		return accum + bucket.duration
	}, 0) ).toFixed(1);

	buckets = defaultBuckets.map((item, index) => new Bucket(item, `background-color: hsl(${360*index/defaultBuckets.length}, 60%, 30%);`))
	let handleChange = async () => {
		samples = fileInput.files
		sampleReaders.length = samples.length
		Object.keys(samples).forEach((_, index) => {
			sampleReaders[index] = new FileReader()
			sampleReaders[index].readAsDataURL(samples[index])
			sampleReaders[index].onload = e => {
				samplesSrc[index] = e.target.result
			}
		})
	}
	let renameAndDownload = (prefix, originalfilename, src) => {
		let link = document.createElement('a')
		link.download = prefix + originalfilename
		link.href = src
		link.click()
	}
	let exportSamples = () => {
		buckets.forEach((bucket) => {
			bucket.samples.forEach((sample) => {
				renameAndDownload(bucket.name, samples[sample].name, samplesSrc[sample])
			})
		})
	}

	let position = 0
	let handleArrowKey = (code) => {
		// let subSet = null;
			// if (editMode.active) {
				// console.log('editMode.active is true')
				// buckets.forEach((bucket) => {
				// 	if (bucket.name == editMode.category) {
				// 		subSet = bucket.samples
				// 		return
				// 	}})
				// }
		if (code == 'ArrowDown'){
			if (position < linkList.length - 1) {
				position += 1
				// console.log('down pressed')
			}
			// if (editMode.subSet.size > 0 && editMode.active) {
			// 	while (!editMode.subSet.has(position)) {
			// 		position += 1
			// 		}
			// 	}
			}
		
		if (code == 'ArrowUp') {
			position -= 1
			if (position < 0){
				position = 0
			}
		}
		linkList[position].focus()
	}

	let scrubCategories = () => {
		buckets.forEach((bucket) => {
				if (samples[position].category == bucket.name) {
					bucket.samples.delete(position)
					bucket.size -= samples[position].size
					bucket.duration -= samplesAudio[position].duration
					samples[position].hslstring = ";"
					samples[position].category = ''
					return
				}
				return
			})
	}

	let handleKeydown = (key) => {
		if (key.code == 'Tab' || key.code == 'Enter' || key.code == "Space"){
			return
		}
		if (editMode.active && key.code.slice(3) != 'X'){return}
		key.preventDefault()
		
		if (key.code == "ArrowDown" || key.code == "ArrowUp"){
		handleArrowKey(key.code)
		return
		}
		
		if (key.code.slice(0,3) == 'Key'){
			console.log(key.code.slice(3))
			let bucketSet = false
			if (key.code.slice(3) == 'X'){
				scrubCategories()
				bucketSet = true
				buckets = buckets
				// return
			}
			else {
				buckets.forEach((bucket) => {
				if (key.code.slice(3) == bucket.shortcut){
				scrubCategories()
				// console.log(key.code + " is a shortcut")
				bucketSet = true
				if (bucket.samples.has(position)){return}
				bucket.samples.add(position)
				bucket.size += samples[position].size
				bucket.duration += samplesAudio[position].duration
				samples[position].hslstring = bucket.hslstring
				samples[position].category = bucket.name
				buckets = buckets
				// console.log(bucket.samples)
				// return
			}
		})
	}
		if (bucketSet) {
			setTimeout(()=>{handleArrowKey("ArrowDown")}, 1)
		}
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
on:keydown={(key) => {handleKeydown(key)}}
>
<div id="setup">
<input multiple accept="audio/*" type="file" id="fileInput" width="200px"
on:change={handleChange}
bind:this={fileInput}>
<button id='customize'>Customize prefixes</button></div>
<ul class="samples">
	{#if editMode.active}
		<p>Press x to remove selected sample from {editMode.category} category</p>
	{/if}
	{#each samples as sample, index}
		{#if editMode.active}
			{#if sample.category == editMode.category}
			<button bind:this={linkList[index]} style={samples[index].hslstring}
			on:focus={() => {
			position = index
			linkList[index].click()
		}
			}
			on:blur={() => { //when button loses focus
				samplesAudio[index].pause()
				samplesAudio[index].currentTime = 0
				}
			}
			on:click={() => {
				if (samplesAudio[index].paused){
					samplesAudio[index].currentTime = 0
					samplesAudio[index].play()
					return
				}
				else {
					samplesAudio[index].pause()
					samplesAudio[index].currentTime = 0
				}
				}}
			><div>
				<p>{sample.category ? sample.category : ""}{sample.name}</p>
			<!-- <p>size:{sample.size}</p> -->
				<!-- svelte-ignore a11y-media-has-caption -->
				{#if Math.abs(index - position) < 20}
				<!--Added this feature to allow loading of more than 200+ samples-->
					<audio src={samplesSrc[index]} bind:this={samplesAudio[index]}></audio>
				{/if}
			</div>
		</button>
			{/if}
		{:else}
	<button bind:this={linkList[index]} style={samples[index].hslstring}
	on:focus={() => {
	position = index
	linkList[index].click()
}
	}
	on:blur={() => { //when button loses focus
		samplesAudio[index].pause()
		samplesAudio[index].currentTime = 0
		}
	}
	on:click={() => {
		if (samplesAudio[index].paused){
			samplesAudio[index].currentTime = 0
			samplesAudio[index].play()
			return
		}
		else {
			samplesAudio[index].pause()
			samplesAudio[index].currentTime = 0
		}
		}}
	><div>
		<p>{sample.category ? sample.category : ""}{sample.name}</p>
	<!-- <p>size:{sample.size}</p> -->
		<!-- svelte-ignore a11y-media-has-caption -->
		{#if Math.abs(index - position) < 10}
		<!--Added this feature to allow loading of more than 200+ samples-->
			<audio src={samplesSrc[index]} bind:this={samplesAudio[index]}></audio>
		{/if}
	</div>
</button>
	{/if}
	{/each}
	
</ul>
<ul class="buckets">
	{#each buckets as bucket, index}
	<button class="bucket"
	style={bucket.hslstring}
	><li><p>
		{#if editMode.active && editMode.category == bucket.name}
		<div class="prefixEdit">
			<label for="prefixEditInput"></label>
			<input id="prefixEditInput" class="categoryNameInput" type="text" value={bucket.name}>
		</div>
		{/if}
		<u>{bucket.name[0]}</u>{bucket.name.slice(1)}</p><p>{bucket.samples.size}</p>
		<button class='edit' on:click={() => {
			if (editMode.category == bucket.name || editMode.category == ''){
				editMode.active = !editMode.active
			}
			else if (editMode.category != bucket.name && editMode.active == false){
				editMode.active = true
			}
			editMode.category = bucket.name
			editMode.subSet = bucket.samples
		}}>Edit</button></li>
	</button>
	{/each}
	<button id='export' on:click={exportSamples}><p>Export {classified} Samples ({megabytes} MB, {duration} s)</p></button>
	<!-- <button id="rename">Rename Categories</button> -->
</ul>
</main>

<style>
	.prefixEdit {
		position: relative;
		top: 100%;
		width: 20px;
		right: 50%;
		z-index: 300;
	}
	.prefixEdit:hover{
		cursor: text;
	}
	#prefixEditInput {
		color: white;
		background: black;
	}
	.edit {
		background: #333;
	}
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

	button:hover, #fileInput:hover {
		cursor: pointer;
	}
	#setup {
		position: fixed;
		z-index: 200;
		background: black;
	}
	#customize {
		left: 40%;
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
		grid-template-columns: 1fr 1fr 1fr;
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