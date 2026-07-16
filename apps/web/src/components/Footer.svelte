<script lang="typescript">
	import Stack from './Stack.svelte';
</script>

<div class="main-footer">
	<Stack align="center" direction="column" spacing="s">
		<slot />
	</Stack>
</div>

<style>
	.main-footer {
		padding-top: 2rem;
		padding-bottom: 2rem;
	}
</style>
