<script lang="ts">
	import sound from '$lib/sounds';
	import DeckChallenge from './DeckChallenge/DeckChallenge.svelte';
	import OptionChallenge from './OptionChallenge/OptionChallenge.svelte';
	import ListeningChallenge from './ListeningChallenge.svelte';
	import ChipsChallenge from './ChipsChallenge/index.svelte';
	import FanfareScreen from '../FanfareScreen.svelte';
	import ProgressBar from '../ProgressBar.svelte';
	import shuffle from 'lodash.shuffle';
	import { fade, scale } from 'svelte/transition';
	// TODO: deal with this ignore comment
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	//import db from '../db/db';
	import isBrowser from 'utils/isBrowser';

	export let rawChallenges;
	export let languageName;
	export let languageCode;
	export let specialCharacters;
	export let sortChallengeGroups;
	export let courseURL;
	export let skillId;
	export let expectedNumberOfChallenges;

	const testChallenge =
		isBrowser() && new URLSearchParams(window.location.search).get('testChallenge');

	type CardChallengeType = {
		id: string;
		type: 'cards';
		pictures: Array<string>;
	};

	type ListeningChallengeType = {
		id: string;
		type: 'listeningExercise';
	};

	type OptionsChallengeType = {
		id: string;
		type: 'options';
	};

	type ShortInputChallengeType = {
		id: string;
		type: 'shortInput';
	};

	type ChipsChallengeType = {
		id: string;
		type: 'chips';
	};

	type ChallengeType =
		| CardChallengeType
		| ListeningChallengeType
		| OptionsChallengeType
		| ShortInputChallengeType
		| ChipsChallengeType;

	// shortInput (free typing) is disabled: without a physical keyboard the
	// special-character input is impractical; the word-bank exercises cover it.
	let challenges: Array<ChallengeType> = sortChallengeGroups(
		shuffle(rawChallenges.filter((c) => c.type !== 'shortInput')),
		expectedNumberOfChallenges
	);

	let remainingChallenges = testChallenge
		? [
				...[...challenges].filter((challenge) => challenge.id === testChallenge),
				...[...challenges].filter((challenge) => challenge.id !== testChallenge)
			]
		: [...challenges];

	let currentChallenge = remainingChallenges.shift();
	let solvedChallenges = [];

	let progress = 0;
	let stats = {
		correct: 0,
		incorrect: 0,
		skipped: 0
	};

	// Duolingo-style in-lesson hearts (per lesson, not persisted)
	const MAX_HEARTS = 5;
	let hearts = MAX_HEARTS;
	let failed = false;

	const preloadImage = (imageName: string) => {
		if (typeof Image === 'undefined') return;
		new Image().src = `/images/${imageName}`;
	};

	challenges &&
		challenges.map((c: any) => c.pictures && c.pictures.map(preloadImage));

	$: alternativeChallenges =
		currentChallenge && rawChallenges.filter(({ id }) => id !== currentChallenge.id);

	$: registerResult = (isCorrect: boolean) => {
		if (isCorrect) {
			stats.correct++;
			sound.correct.play();
			solvedChallenges.push(currentChallenge);
		} else {
			stats.incorrect++;
			hearts = Math.max(0, hearts - 1);
			sound.wrong.play();
			remainingChallenges.push(currentChallenge);
			if (hearts === 0) {
				failed = true;
			}
		}
	};

	$: progress = (solvedChallenges.length + stats.skipped) / challenges.length;

	$: resolveChallenge = () => {
		if (remainingChallenges) {
			currentChallenge = remainingChallenges.shift();
		}
	};

	$: skipChallenge = () => {
		stats.skipped++;
		resolveChallenge();
	};

	$: skipAllChallenges = async () => {
		if (solvedChallenges.length == 0) {
			window.location.replace(courseURL);
			return;
		}
		stats.skipped++;
		remainingChallenges.forEach(() => stats.skipped++);
		remainingChallenges = [];
		currentChallenge = undefined;
	};

	$: skipAllVoice = () => {
		let filteredRemainingChallenges = remainingChallenges.filter((challenge) => {
			if (challenge.type === 'listeningExercise') {
				stats.skipped++;
				return false;
			} else {
				return true;
			}
		});

		remainingChallenges.splice(0, remainingChallenges.length, ...filteredRemainingChallenges);
		stats.skipped++;
		resolveChallenge();
	};
</script>

{#if failed}
	<div class="container">
		<div class="fail-screen" in:scale>
			<div class="fail-screen__icon">💔</div>
			<h1 class="fail-screen__title">하트를 모두 잃었어요!</h1>
			<p class="fail-screen__subtitle">괜찮아요, 다시 도전해 보세요.</p>
			<div class="fail-screen__actions">
				<a class="fail-btn fail-btn--retry" href={typeof window !== 'undefined' ? window.location.href : '#'}>다시 시도</a>
				<a class="fail-btn fail-btn--quit" href={courseURL}>코스로 돌아가기</a>
			</div>
		</div>
	</div>
{:else if currentChallenge}
	<div class="container" in:scale>
		<section class="section">
			<div class="lesson-topbar">
				<a class="quit-x" href={courseURL} aria-label="레슨 종료" title="레슨 종료">✕</a>
				<div class="lesson-topbar__progress">
					<ProgressBar value={progress} />
				</div>
				<div class="hearts" title="하트">
					<span class="hearts__icon">❤️</span>
					<span class="hearts__count">{hearts}</span>
				</div>
			</div>
			{#each challenges as challenge, i (challenge.id)}
				{#if challenge.id === currentChallenge.id}
					<div
						class="challenge"
						in:fade|local={{ duration: 300, delay: 350 }}
						out:fade|local={{ duration: 300 }}
					>
						{#if challenge.type === 'cards'}
							<DeckChallenge
								{skipChallenge}
								{currentChallenge}
								{alternativeChallenges}
								{resolveChallenge}
								{registerResult}
								{skipAllChallenges}
							/>
						{/if}
						{#if challenge.type === 'options'}
							<OptionChallenge
								{skipChallenge}
								{currentChallenge}
								{alternativeChallenges}
								{resolveChallenge}
								{registerResult}
								{skipAllChallenges}
							/>
						{/if}
						{#if challenge.type === 'listeningExercise'}
							<ListeningChallenge
								{skipChallenge}
								{languageCode}
								{specialCharacters}
								{registerResult}
								{resolveChallenge}
								{challenge}
								{skipAllChallenges}
								{skipAllVoice}
							/>
						{/if}
						{#if challenge.type === 'chips'}
							<ChipsChallenge
								{registerResult}
								{resolveChallenge}
								{challenge}
								{skipChallenge}
								{skipAllChallenges}
							/>
						{/if}
					</div>
				{/if}
			{/each}
		</section>
	</div>
{/if}

{#if !currentChallenge}
	<div class="container">
		<FanfareScreen {courseURL} {skillId} {stats} />
	</div>
{/if}

<style lang="scss">
	.section {
		padding: 1.5em;
	}
	.challenge {
		padding: 2em 0;
	}

	.lesson-topbar {
		display: flex;
		align-items: center;
		gap: 1rem;
		max-width: 720px;
		margin: 0 auto 0.5rem;
	}

	.lesson-topbar__progress {
		flex: 1;
	}

	.quit-x {
		font-size: 1.4rem;
		font-weight: 700;
		color: #afafaf;
		text-decoration: none;
		line-height: 1;
		padding: 0.2rem;

		&:hover {
			color: #4b4b4b;
		}
	}

	.hearts {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		font-weight: 800;
		color: #ff4b4b;
		font-size: 1.1rem;
	}

	.fail-screen {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 70vh;
		text-align: center;
		gap: 0.6rem;
	}

	.fail-screen__icon {
		font-size: 4rem;
	}

	.fail-screen__title {
		font-size: 1.8rem;
		font-weight: 800;
		color: #4b4b4b;
	}

	.fail-screen__subtitle {
		color: #777;
	}

	.fail-screen__actions {
		display: flex;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.fail-btn {
		display: inline-block;
		padding: 0.7rem 1.6rem;
		border-radius: 16px;
		font-weight: 800;
		text-transform: uppercase;
		text-decoration: none;
		border-bottom: 4px solid;

		&--retry {
			background: var(--color-primary, #58cc02);
			border-bottom-color: var(--color-primary-shadow, #58a700);
			color: #fff;
		}

		&--quit {
			background: #fff;
			border: 2px solid #e5e5e5;
			border-bottom: 4px solid #e5e5e5;
			color: #777;
		}
	}
</style>
