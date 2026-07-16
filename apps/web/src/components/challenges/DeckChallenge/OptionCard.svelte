<script lang="ts">
	import Card from 'components/Card.svelte';
	import Stack from 'components/Stack.svelte';

	export let active: boolean;
	export let inactive: boolean;
	export let correct: boolean;
	export let number: number;
	export let picture: string;
	export let formInTargetLanguage: string;
	export let meaningInSourceLanguage: string = '';

	// Mandarin bridge, e.g. "하나 (一)" -> "一"
	$: mandarin = (meaningInSourceLanguage?.match(/[（(]([^()（）]*[一-鿿][^()（）]*)[)）]/) || [])[1] || '';
</script>

<li class:active class:inactive>
	<Card
		data-test={active ? 'active' : inactive ? 'inactive' : 'neutral'}
		data-test-correct={correct}
	>
		<div slot="media">
			{#if picture}
				<img src={`/images/${picture}`} alt="" data-test={`card-img-${number}`} />
			{/if}
		</div>
		<div slot="footer">
			<Stack justify="center">
				<div class="card-text" data-test={`card-text-${number}`}>
					<div class="card-text__form">{formInTargetLanguage}</div>
					{#if mandarin}
						<div class="card-text__mandarin">中: {mandarin}</div>
					{/if}
				</div>
			</Stack>
		</div>
	</Card>
</li>

<style type="text/scss">
	li {
		border: 3px solid transparent;
		display: flex;
		flex-direction: column;
		width: 100%;
		max-width: 20em;
		margin: 0;
		transition:
			opacity 0.15s,
			border-color 0.2s;
		cursor: pointer;
		transition: transform 0.1s;
		background: white;
		overflow: hidden;
		border-radius: 16px;
	}

	.card-text {
		text-align: center;
		padding: 1.2rem 0.5rem;
	}

	.card-text__form {
		font-size: 1.25rem;
		font-weight: 700;
		color: #3c3c3c;
	}

	.card-text__mandarin {
		margin-top: 0.4rem;
		font-size: 0.95rem;
		color: #999;
	}

	li.inactive {
		opacity: 0.65;
		border-color: rgba(0, 0, 0, 0);
		transform: scale(0.95);
	}

	li:hover {
		border-color: $link-active-border;
	}

	li.active {
		border-color: $info;
		box-sizing: content-box;
		transform: scale(1.05);
	}
</style>
