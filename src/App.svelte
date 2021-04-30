<script>
	// import {onMount} from 'svelte';
	let fileInput = {'files': []}
	let samples = []
	// let audioSrc = '#'
	const reader = new FileReader()
	let handleChange = () => {
		samples = Array.from(fileInput.files).sort((a, b) => a.size - b.size)
		// audioSrc = reader.readAsDataURL(fileInput.files[0])
		console.log(fileInput.files)
	}
</script>

<main>
	<input multiple type="file" id="fileInput" on:change={handleChange} bind:this={fileInput}>
	<!-- svelte-ignore a11y-media-has-caption -->
	<!-- <audio src={audioSrc} controls></audio> -->
	<ul>
	{#each samples as sample, index}
	<li>{sample.name} size:{sample.size} <audio src={undefined} controls></audio></li>
	
	{/each}
</ul>
</main>