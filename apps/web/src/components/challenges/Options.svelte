<script lang="ts">
	import { onMount } from 'svelte';
	import hotkeys from 'hotkeys-js';
	import Option from './Option.svelte';
	export let options;
	export let selectedOption;
	export let disabled;

	onMount(() => {
		hotkeys.unbind('1,2,3');
		hotkeys('1,2,3', (_, { key }) => {
			if (disabled) return;
			selectedOption = parseInt(key) - 1;
		});
	});
</script>

<ul class="options">
	{#each options as { formInTargetLanguage, correct, fake }, i}
		<label for={i.toString()} class:fake={fake && true}>
			<input
				type="radio"
				bind:group={selectedOption}
				value={i}
				name={i.toString()}
				id={i.toString()}
				{disabled}
			/>
			<span class="tile-number">{i + 1}</span>
			<Option
				{correct}
				active={selectedOption === i}
				inactive={selectedOption !== null && selectedOption !== i}
				{formInTargetLanguage}
			/>
		</label>
	{/each}
</ul>

<style type="text/scss">
	.options {
		list-style: none;
		padding-top: 1.5em;
		margin: 0 auto;
		max-width: 560px;
		user-select: none;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* Duolingo-style big tiles */
	input {
		position: absolute;
		opacity: 0;
		pointer-events: none;
	}

	label {
		display: flex;
		align-items: center;
		gap: 1rem;
		background: #fff;
		border: 2px solid #e5e5e5;
		border-bottom-width: 4px;
		border-radius: 16px;
		padding: 0.4rem 1.2rem;
		cursor: pointer;
		transition: all 0.1s;

		&:hover {
			background: #f7f7f7;
		}

		&:active {
			transform: translateY(2px);
			border-bottom-width: 2px;
		}

		&:has(input:checked) {
			border-color: #84d8ff;
			background: #ddf4ff;
			color: #1899d6;
		}
	}

	.tile-number {
		display: flex;
		align-items: center;
		justify-content: center;
		min-width: 30px;
		height: 30px;
		border: 2px solid #e5e5e5;
		border-radius: 8px;
		font-size: 0.9rem;
		font-weight: 700;
		color: #afafaf;
	}
</style>
