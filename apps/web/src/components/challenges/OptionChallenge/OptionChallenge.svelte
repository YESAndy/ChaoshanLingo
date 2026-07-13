<script lang="ts">
	import { onMount } from 'svelte';
	import hotkeys from 'hotkeys-js';
	import Options from '../Options.svelte';
	import ChallengePanel from '../ChallengePanel.svelte';
	import { prepareChallenge } from '$lib/generic';

	export let currentChallenge;
	export let alternativeChallenges;
	export let resolveChallenge;
	export let registerResult;
	export let skipChallenge;
	export let skipAllChallenges;

	let selectedOption = null;
	let submitted = false;

	$: options = prepareChallenge({
		currentChallenge,
		alternativeChallenges,
		typeToSelect: 'options'
	});

	$: finishChallenge = () => {
		selectedOption = null;
		submitted = false;
		resolveChallenge();
	};

	$: submitChallenge = () => {
		registerResult(options[selectedOption]?.correct);
		submitted = true;
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
	});
</script>

<p class="is-size-1 is-size-2-tablet is-size-4-mobile has-text-centered">
	다음 중
	<strong data-test="meaning-in-source-language">
		{currentChallenge.meaningInSourceLanguage}
	</strong>
	은(는) 어느 것일까요?
</p>

<form on:submit|preventDefault={submitChallenge}>
	<Options {options} bind:selectedOption disabled={submitted} />

	{#if !submitted && selectedOption !== null}
		<ChallengePanel
			message=""
			buttonText="제출"
			submit
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
		/>
	{/if}

	{#if !submitted && selectedOption === null}
		<ChallengePanel
			message=""
			buttonText=""
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
		/>
	{/if}

	{#if submitted}
		{#if options[selectedOption].correct}
			<ChallengePanel
				message="정답입니다!"
				buttonText="계속"
				correct
				buttonAction={finishChallenge}
			/>
		{/if}
		{#if !options[selectedOption].correct}
			<ChallengePanel
				message="틀렸습니다!"
				messageDetail={`정답: ${currentChallenge.formInTargetLanguage}`}
				buttonText="계속"
				incorrect
				buttonAction={finishChallenge}
			/>
		{/if}
	{/if}
</form>
