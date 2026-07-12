<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { base } from '$app/paths';

	onMount(() => {
		goto(`${base}/`);
	});
</script>

<p>Redirecting to the homepage…</p>
