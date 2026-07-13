<script lang="ts">
	export let phrase;

	// Hide parenthesized Mandarin bridge tokens, e.g. "(现在几点？)" — they can
	// give away the answer when the phrase is shown as an exercise prompt.
	$: visiblePhrase = phrase.filter(
		({ word }) => !/^[（(].*[一-鿿].*[）)]$/.test(word)
	);
</script>

<b class="phrase">
	{#each visiblePhrase as { word, definition }}
		{#if definition}
			<span class="has-tooltip-bottom" data-tooltip={definition}>{word}</span>
		{:else}<span>{word}</span>{/if}
	{/each}
</b>

<style type="text/scss">

	.phrase span {
		margin: 0 0.15em;

		&.has-tooltip-bottom {
			text-decoration: dotted underline rgba($blue, 0.5);
		}

		&:first-child {
			margin-left: 0;
		}
		&:last-child {
			margin-left: 0;
		}
	}
</style>
