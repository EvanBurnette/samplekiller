<script>
	// import {onMount} from 'svelte';
	class Bucket {
		constructor(name){
			this.name = name;
			this.samples = []
			this.shortcut = this.name.charAt(0)
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
	'clap',
	'melody',
	'riser',
]

	buckets = defaultBuckets.map(item => new Bucket(item))

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
</script>
	<!-- svelte-ignore a11y-media-has-caption -->
	<!-- <audio src={audioSrc} controls></audio> -->
	<main>
	<ul class="samples">
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
<ul class="buckets">
	{#each Object.keys(buckets) as bucket}
	<button class="bucket"><li><p>{buckets[bucket].name}</p><p>{buckets[bucket].samples.length}</p></li></button>
	{/each}
</ul>
</main>
<input multiple accept="audio/*" type="file" id="fileInput"
	on:change={handleChange}
	bind:this={fileInput}>

<style>
	main {
		display: grid;
		grid-template-columns: auto auto;
	}
	.samples {
		display: flex;
		flex-direction: column;
		list-style: none;
	}
	.bucket li {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}
	.buckets {
		position: relative;
		display: grid;
		grid-template-columns: 1fr 1fr;
	}
</style>