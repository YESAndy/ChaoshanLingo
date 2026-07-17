<script lang="ts">
	import { onMount } from 'svelte';
	import hotkeys from 'hotkeys-js';
	import shuffle from 'lodash.shuffle';
	import ChallengePanel from './ChallengePanel.svelte';
	import Icon from 'components/Icon.svelte';
	import { playAudio } from '$lib/sounds';
	import Button from 'components/Button.svelte';
	import { page } from '$app/state';

	export let challenge;
	export let registerResult;
	export let resolveChallenge;
	export let languageCode;
	export let specialCharacters;
	export let skipChallenge;
	export let skipAllChallenges;
	export let skipAllVoice;

	const CJK = /[㐀-鿿豈-﫿]/g;
	const clean = (s: string) => s.replace(CJK, '').replace(/[?？!！.,。，]/g, '').trim();

	// Teochew character annotations (same source as ChipsChallenge)
	const annotationModules = import.meta.glob('../../courses/*/annotations.json', {
		eager: true
	});
	const annotations: Record<string, string> =
		(annotationModules[`../../courses/${page.params?.courseName}/annotations.json`] as any)
			?.default ?? {};
	const hanziFor = (tok: string) => annotations[tok] || annotations[tok.toLowerCase()] || '';

	// The answer as peng'im tokens, e.g. "Zi2zung5 gui2 diam2?" -> [Zi2zung5, gui2, diam2]
	const targetTokens: string[] = clean(challenge.answer).split(/\s+/).filter(Boolean);

	// Distractor tokens from the course-wide token list
	const distractors: string[] = shuffle(
		Object.keys(annotations).filter(
			(t) =>
				/^[a-zê]+\d?$/i.test(t) &&
				!targetTokens.some((tt) => tt.toLowerCase() === t.toLowerCase())
		)
	).slice(0, Math.min(3, Math.max(2, 5 - targetTokens.length)));

	type Chip = { id: number; token: string };
	let bank: Chip[] = shuffle(
		[...targetTokens, ...distractors].map((token, id) => ({ id, token }))
	);
	let picked: Chip[] = [];

	let submitted = false;
	let correct = null;

	const pick = (chip: Chip) => {
		if (submitted) return;
		bank = bank.filter((c) => c.id !== chip.id);
		picked = [...picked, chip];
	};

	const unpick = (chip: Chip) => {
		if (submitted) return;
		picked = picked.filter((c) => c.id !== chip.id);
		bank = [...bank, chip];
	};

	$: submitChallenge = () => {
		if (picked.length === 0 || submitted) return;
		const given = picked.map((c) => c.token.toLowerCase()).join(' ');
		const expected = targetTokens.map((t) => t.toLowerCase()).join(' ');
		correct = given === expected;
		registerResult(correct);
		submitted = true;
	};

	$: finishChallenge = () => {
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
		<p class="is-size-1 is-size-2-tablet is-size-4-mobile has-text-centered">들리는 대로 만들어 보세요</p>
	</div>

	<div class="listening">
		<Button size="large" style="primary" on:click={playChallengeVoice}>
			<Icon icon="volume-up" />
		</Button>

		<div class="answer-area" class:answer-area--filled={picked.length > 0}>
			{#if picked.length === 0}
				<span class="answer-area__hint">아래 단어를 눌러 답을 만드세요</span>
			{/if}
			{#each picked as chip (chip.id)}
				<button type="button" class="chip" on:click={() => unpick(chip)}>
					{chip.token}
					{#if hanziFor(chip.token)}<span class="chip__hanzi">{hanziFor(chip.token)}</span>{/if}
				</button>
			{/each}
		</div>

		<div class="bank">
			{#each bank as chip (chip.id)}
				<button type="button" class="chip" on:click={() => pick(chip)}>
					{chip.token}
					{#if hanziFor(chip.token)}<span class="chip__hanzi">{hanziFor(chip.token)}</span>{/if}
				</button>
			{/each}
		</div>
	</div>

	{#if picked.length > 0 && !submitted}
		<ChallengePanel
			message=""
			buttonText="제출"
			submit
			skipAction={skipChallenge}
			skipAllAction={skipAllChallenges}
			{skipAllVoice}
		/>
	{/if}

	{#if picked.length === 0 && !submitted}
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
			<ChallengePanel
				message="정답입니다!"
				messageDetail={`뜻: "${challenge.meaning}"`}
				buttonText="계속"
				correct
				buttonAction={finishChallenge}
			/>
		{/if}
	{/if}
</form>

<style lang="scss">
	.listening {
		max-width: 620px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		align-items: flex-start;
	}

	.answer-area {
		width: 100%;
		min-height: 4.2rem;
		border-bottom: 2px solid #e5e5e5;
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		align-items: center;
		padding: 0.4rem 0.2rem;
	}

	.answer-area__hint {
		color: #bbb;
	}

	.bank {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}

	.chip {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		background: #fff;
		border: 2px solid #e5e5e5;
		border-bottom-width: 4px;
		border-radius: 12px;
		padding: 0.45rem 1rem;
		font-size: 1.05rem;
		font-weight: 700;
		color: #3c3c3c;
		cursor: pointer;
		transition: all 0.1s;

		&:active {
			transform: translateY(2px);
			border-bottom-width: 2px;
		}
	}

	.chip__hanzi {
		font-size: 0.85rem;
		font-weight: 400;
		color: #999;
		line-height: 1.2;
	}
</style>
