<script lang="ts">
	import { base } from '$app/paths';

	export let shadow = true;
	export let glow = false;

	// Chaoshan mascot (shadow variant is built into the SVG)
	let imageURL = `${base}/images/chaoshan-mascot.svg`;
</script>

<img
	data-test="mascot-jetpack"
	src={imageURL}
	alt="LibreLingo Mascot"
	class="mascot"
	class:mascot--glow={glow}
/>

<style>
	img {
		min-width: 200px;
		object-fit: contain;
	}
</style>
