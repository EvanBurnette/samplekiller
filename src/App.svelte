<script>
	// import {onMount} from 'svelte';
	let fileInput = {'files': []}
	let samples = []
	let sampleReaders = []
	let samplesSrc = []
	let samplesAudio = []
	let linkList = []
	// let audioSrc = '#'
	const reader = new FileReader()
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
</script>

<main>
	<input multiple accept="audio/*" type="file" id="fileInput"
	on:change={handleChange}
	bind:this={fileInput}>

	<!-- svelte-ignore a11y-media-has-caption -->
	<!-- <audio src={audioSrc} controls></audio> -->
	<ul>
	{#each samples as sample, index}
	<button bind:this={linkList[index]}
	on:focus={linkList[index].click()}
	on:blur={() => {
		samplesAudio[index].pause()
		samplesAudio[index].currentTime = 0
		}
	}
	on:click={samplesAudio[index].play()}
	><li><p>{sample.name} size:{sample.size}</p>

		<audio src={samplesSrc[index]} bind:this={samplesAudio[index]}></audio>
	</li></button>
	
	{/each}
</ul>
</main>

<style>
	ul {
		list-style: none;
	}
</style>