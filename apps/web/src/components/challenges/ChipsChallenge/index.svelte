<script lang="ts">
	import { onMount } from 'svelte';
	import hotkeys from 'hotkeys-js';
	import shuffle from 'lodash.shuffle';
	import { writable } from 'svelte/store';
	import ChallengePanel from '../ChallengePanel.svelte';
	import Phrase from '../Phrase.svelte';
	import { createSortable } from './sortable';
	import { getNodeType, getChipIndex } from './chips';
	import { page } from '$app/state';

	// Teochew character annotations per token (rendered via CSS ::after so
	// drag-and-drop innerText comparison stays clean)
	const annotationModules = import.meta.glob('../../../courses/*/annotations.json', {
		eager: true
	});
	const annotations: Record<string, string> =
		(annotationModules[`../../../courses/${page.params?.courseName}/annotations.json`] as any)
			?.default ?? {};
	const hanziFor = (chip: string) =>
		annotations[chip] || annotations[chip.toLowerCase()] || '';

	export let challenge;
	export let registerResult;
	export let resolveChallenge;
	export let skipChallenge;
	export let skipAllChallenges;

	let submitted = false;
	let correct = null;
	let chipsElement: HTMLElement;
	let answerElement: HTMLElement;
	const answer = writable([]);
	let answerToRender = [];
	let chipsToRender = shuffle(challenge.chips);
	const chips = writable(chipsToRender);

	$: submitChallenge = () => {
		if (!$answer) return;
		if (submitted) return;
		correct = false;
		const answerForm = $answer.join(' ').toLowerCase();
		challenge.solutions.map((solution: string[]) => {
			correct = correct || answerForm === solution.join(' ').toLowerCase();
		});
		registerResult(correct);
		submitted = true;
	};

	$: finishChallenge = () => {
		$answer = [];
		submitted = false;
		resolveChallenge();
	};

	$: handleChipClick = (event) => {
		if (submitted) return;
		const node = event.target;
		const chipType = getNodeType(node);
		const chipText = node.innerText;
		const chipIndex = getChipIndex(node);

		if (chipType === 'chips') {
			chips.update((oldItems) => {
				const newItems = [...oldItems];
				newItems.splice(chipIndex, 1);
				return newItems;
			});
			answer.update((oldItems) => [...oldItems, chipText]);
		}

		if (chipType === 'answer') {
			answer.update((oldItems) => {
				const newItems = [...oldItems];
				newItems.splice(chipIndex, 1);
				return newItems;
			});
			chips.update((oldItems) => [...oldItems, chipText]);
		}

		rerenderSortables();
	};

	const rerenderSortables = () => {
		chipsSortable.destroy();
		answerSortable.destroy();
		answerToRender = $answer;
		chipsToRender = $chips;

		/*
        Need to wait for the re-rendering of the chips
        otherwise the svelte store and the sortable
        store will be out of sync
      */
		setTimeout(initializeDragAndDrop, 0);
	};

	let chipsSortable;
	let answerSortable;

	const initializeSortable1 = () => {
		chipsSortable = createSortable(chipsElement, chips);
	};

	const initializeSortable2 = () => {
		answerSortable = createSortable(answerElement, answer);
	};

	const initializeDragAndDrop = () => {
		initializeSortable1();
		initializeSortable2();
	};

	onMount(() => {
		hotkeys.unbind('enter');
		hotkeys('enter', () => {
			if (submitted) {
				finishChallenge();
			} else {
				submitChallenge();
			}
		});

		initializeDragAndDrop();
	});
</script>

<form on:submit|preventDefault={submitChallenge}>
	<div class="section">
		<p class="is-size-1 is-size-2-tablet is-size-4-mobile has-text-centered">
			번역하세요:
			<Phrase phrase={challenge.phrase} />
		</p>
	</div>

	<div>
		<div class="solution">
			<div id="answer" class="chips" bind:this={answerElement}>
				{#each answerToRender as chip, index}
					<span
						class="chip"
						data-id={chip}
						on:click={handleChipClick}
						on:keypress={handleChipClick}
					>
						<span class="tag is-medium" data-hanzi={hanziFor(chip)}>{chip}</span>
					</span>
				{/each}
			</div>
		</div>

		<p class="sub-instructions">이 단어들을 사용하세요:</p>
		<div id="chips" class="chips" bind:this={chipsElement}>
			{#each chipsToRender as chip, index}
				<span class="chip" data-id={chip} on:click={handleChipClick} on:keypress={handleChipClick}>
					<span class="tag is-medium" data-hanzi={hanziFor(chip)}>{chip}</span>
				</span>
			{/each}
		</div>
	</div>

	{#if $answer.length === 0 && !submitted}
		<ChallengePanel
			message={null}
			buttonText={null}
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
		/>
	{/if}

	{#if $answer.length > 0 && !submitted}
		<ChallengePanel
			message=""
			buttonText="제출"
			submit
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
		/>
	{/if}

	{#if submitted}
		{#if !correct}
			<ChallengePanel
				message="틀렸습니다!"
				messageDetail={`정답: ${challenge.formattedSolution}`}
				buttonText="계속"
				incorrect
				buttonAction={finishChallenge}
			/>
		{/if}
		{#if correct}
			<ChallengePanel
				message="정답입니다!"
				buttonText="계속"
				correct
				buttonAction={finishChallenge}
			/>
		{/if}
	{/if}
</form>

<style type="text/scss">

	.chip {
		user-select: none;
		margin: 0.5em 0.3em;
		cursor: pointer;
	}

	/* Teochew character annotation under each chip (pseudo-element keeps it
	   out of innerText, which the answer check relies on) */
	.chip :global(.tag[data-hanzi]:not([data-hanzi=''])) {
		flex-direction: column;
		height: auto;
		padding: 0.35rem 0.8rem;
	}

	.chip :global(.tag[data-hanzi]:not([data-hanzi='']))::after {
		content: attr(data-hanzi);
		display: block;
		font-size: 0.85rem;
		color: #999;
		line-height: 1.2;
	}

	.solution {
		z-index: 10;
		margin-top: -4em;
		padding-top: 4em;
		border-bottom: 2px solid rgba($blue, 0.1);
		height: 6.2em;
	}

	.sub-instructions {
		margin-top: 3em;
	}

	:global(.chips .sortable-ghost .tag) {
		background: $blue !important;
		color: transparent !important;
		opacity: 0.1;
	}

	:global(.sortable-drag) {
		opacity: 1 !important;
	}
</style>
