<script lang="ts">
	import { base } from '$app/paths';

	export let shadow = true;
	export let glow = false;

	let imageURL =
		shadow === true ? `${base}/images/mascot-jetpack.svg` : `${base}/images/mascot-jetpack-noshadow.svg`;
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
