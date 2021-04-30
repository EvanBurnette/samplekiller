<script>
	// import {onMount} from 'svelte';
	let fileInput = {'files': []}
	let samples = []
	let handleChange = () => {
		samples = Array.from(fileInput.files).sort((a, b) => a.size - b.size)
	}
</script>

<main>
	<input multiple type="file" id="fileInput" on:change={handleChange} bind:this={fileInput}>
	{#each samples as sample}
	<p>{sample.size}</p>
	{/each}
</main>