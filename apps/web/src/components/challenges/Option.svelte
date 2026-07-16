<script lang="ts">
	export let active;
	export let inactive;
	export let correct;
	export let formInTargetLanguage;
	export let meaningInSourceLanguage: string = '';

	// Mandarin bridge, e.g. "세 시 반 (三点半)" -> "三点半"
	$: mandarin = (meaningInSourceLanguage?.match(/[（(]([^()（）]*[一-鿿][^()（）]*)[)）]/) || [])[1] || '';
</script>

<li class:active class:inactive>
	<div
		class="option"
		data-test={active ? 'active' : inactive ? 'inactive' : 'neutral'}
		data-test-correct={correct}
	>
		<div class="option-content">
			<div class="is-size-5 is-size-6-mobile">{formInTargetLanguage}</div>
			{#if mandarin}
				<div class="option-mandarin">中: {mandarin}</div>
			{/if}
		</div>
	</div>
</li>

<style type="text/scss">

	.option {
		padding: 0.75em 0;
		transition:
			opacity 0.15s,
			outline 0.2s;
		cursor: pointer;
	}

	.option-mandarin {
		margin-top: 0.2rem;
		font-size: 0.9rem;
		color: #999;
	}

	.inactive .option {
		opacity: 0.65;
	}

	@include mobile {
		.option-content {
			padding: $size-7;
		}
	}
</style>
