<script lang="ts">
	import { onMount } from 'svelte';
	import hotkeys from 'hotkeys-js';
	import leven from 'leven';
	import ChallengePanel from './ChallengePanel.svelte';
	import Icon from 'components/Icon.svelte';
	import InputFieldWithVirtualKeyboard from './InputFieldWithVirtualKeyboard/InputFieldWithVirtualKeyboard.svelte';
	import { playAudio } from '$lib/sounds';
	import Button from 'components/Button.svelte';
	import Column from 'components/Column.svelte';
	import Columns from 'components/Columns.svelte';

	export let challenge;
	export let registerResult;
	export let resolveChallenge;
	export let languageCode;
	export let specialCharacters;
	export let skipChallenge;
	export let skipAllChallenges;
	export let skipAllVoice;

	let answer = '';
	let submitted = false;
	let correct = null;
	let spellingSuggestion = '';

	const CJK_ONLY = /[㐀-鿿豈-﫿]/g;
	const NON_CJK = /[^㐀-鿿豈-﫿]/g;
	const normalize = (s: string) =>
		s
			.toLowerCase()
			.replace(/[?？!！.,。，'’]/g, '')
			.replace(/\s+/g, ' ')
			.trim();

	$: submitChallenge = () => {
		if (!answer) return;
		if (submitted) return;
		const form = challenge.answer;
		correct = false;

		// Accept the full answer, the Peng'im-only part, or the hanzi-only part
		// (the on-screen keyboard cannot type Chinese characters).
		const accepted = [form, form.replace(CJK_ONLY, ''), form.replace(NON_CJK, '')]
			.map(normalize)
			.filter(Boolean);
		const given = normalize(answer);

		if (accepted.some((a) => leven(given, a) <= 1)) {
			correct = true;
			spellingSuggestion = accepted.includes(given) ? '' : `올바른 철자: ${form}`;
		}

		registerResult(correct);
		submitted = true;
	};

	$: finishChallenge = () => {
		answer = null;
		submitted = false;
		resolveChallenge();
	};

	const playChallengeVoice = () => playAudio('voice', challenge.audio);

	onMount(() => {
		playChallengeVoice();
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

<form on:submit|preventDefault={submitChallenge}>
	<div class="section">
		<p class="is-size-1 is-size-2-tablet is-size-4-mobile has-text-centered">들리는 대로 입력하세요</p>
	</div>

	<Columns>
		<Column size="1">
			<Button size="large" style="primary" on:click={playChallengeVoice}>
				<Icon icon="volume-up" />
			</Button>
		</Column>
		<Column>
			<InputFieldWithVirtualKeyboard
				{specialCharacters}
				{languageCode}
				disabled={submitted}
				bind:value={answer}
			/>
		</Column>
	</Columns>

	{#if answer && !submitted}
		<ChallengePanel
			message=""
			buttonText="제출"
			submit
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
			{skipAllVoice}
		/>
	{/if}

	{#if answer === '' && !submitted}
		<ChallengePanel
			message={null}
			buttonText={null}
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
			{skipAllVoice}
		/>
	{/if}

	{#if submitted}
		{#if !correct}
			<ChallengePanel
				message="틀렸습니다!"
				messageDetail={`정답: ${challenge.answer}`}
				buttonText="계속"
				incorrect
				buttonAction={finishChallenge}
			/>
		{/if}

		{#if correct}
			{#if !spellingSuggestion}
				<ChallengePanel
					message="정답입니다!"
					messageDetail={`뜻: "${challenge.meaning}"`}
					buttonText="계속"
					correct
					buttonAction={finishChallenge}
				/>
			{/if}

			{#if spellingSuggestion}
				<ChallengePanel
					message="오타가 있어요!"
					messageDetail={spellingSuggestion || `뜻: "${challenge.meaning}"`}
					buttonText="계속"
					typo
					buttonAction={finishChallenge}
				/>
			{/if}
		{/if}
	{/if}
</form>
