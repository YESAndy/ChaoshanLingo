<script lang="ts">
	import { scale } from 'svelte/transition';
	import sound from '$lib/sounds';
	import hotkeys from 'hotkeys-js';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Mascot from './Mascot.svelte';
	import Button from 'components/Button.svelte';
	import { completeLesson, progress, displayStreak } from '$lib/gamification';

	export let courseURL;
	export let skillId;
	export let stats;

	let earnedXP = 0;

	// CSS confetti
	const colors = ['#58CC02', '#1CB0F6', '#FFC800', '#FF4B4B', '#CE82FF'];
	const confetti = Array.from({ length: 40 }, (_, i) => ({
		left: Math.random() * 100,
		color: colors[i % colors.length],
		delay: Math.random() * 1.2,
		dur: 2.2 + Math.random() * 1.8,
		size: 7 + Math.random() * 6,
		spin: Math.random() > 0.5 ? 1 : -1
	}));

	$: accuracy =
		stats.correct + stats.incorrect > 0
			? Math.round((stats.correct / (stats.correct + stats.incorrect)) * 100)
			: 100;

	onMount(() => {
		sound.fanfare.play();
		earnedXP = completeLesson(skillId, stats.correct);
	});

	onMount(() => {
		hotkeys.unbind('enter');
		hotkeys('enter', () => {
			goto(courseURL);
		});
	});
</script>

<div class="confetti-layer" aria-hidden="true">
	{#each confetti as c}
		<span
			class="confetti"
			style="left:{c.left}%; background:{c.color}; animation-delay:{c.delay}s; animation-duration:{c.dur}s; width:{c.size}px; height:{c.size * 1.4}px; --spin:{c.spin}"
		></span>
	{/each}
</div>

<section class="finish">
	<div in:scale>
		<div class="finish__mascot">
			<Mascot />
		</div>
		<h1 class="finish__title">레슨 완료!</h1>

		<div class="finish__stats">
			<div class="stat-card stat-card--xp">
				<div class="stat-card__label">획득 XP</div>
				<div class="stat-card__value">⚡ {earnedXP}</div>
			</div>
			<div class="stat-card stat-card--accuracy">
				<div class="stat-card__label">정확도</div>
				<div class="stat-card__value">🎯 {accuracy}%</div>
			</div>
			<div class="stat-card stat-card--streak">
				<div class="stat-card__label">연속 학습</div>
				<div class="stat-card__value">🔥 {displayStreak($progress)}일</div>
			</div>
		</div>

		<div class="finish__action">
			<Button size="medium" href={courseURL} style="primary">계속하기</Button>
		</div>
	</div>
</section>

<style lang="scss">
	.confetti-layer {
		position: fixed;
		inset: 0;
		pointer-events: none;
		overflow: hidden;
		z-index: 10;
	}

	.confetti {
		position: absolute;
		top: -20px;
		border-radius: 2px;
		opacity: 0.9;
		animation-name: confetti-fall;
		animation-timing-function: linear;
		animation-iteration-count: 1;
		animation-fill-mode: forwards;
	}

	@keyframes confetti-fall {
		to {
			transform: translateY(110vh) rotate(calc(720deg * var(--spin)));
			opacity: 0.6;
		}
	}

	.finish {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 80vh;
		text-align: center;
	}

	.finish__mascot {
		width: 180px;
		margin: 0 auto 1rem;
	}

	.finish__title {
		font-size: 2rem;
		font-weight: 800;
		color: var(--color-gold, #ffc800);
		margin-bottom: 1.5rem;
	}

	.finish__stats {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		margin-bottom: 2rem;
	}

	.stat-card {
		border-radius: 16px;
		border: 2px solid;
		padding: 0.3rem;
		min-width: 130px;
		overflow: hidden;

		&--xp {
			border-color: var(--color-gold, #ffc800);
			.stat-card__label {
				background: var(--color-gold, #ffc800);
			}
		}

		&--accuracy {
			border-color: var(--color-primary, #58cc02);
			.stat-card__label {
				background: var(--color-primary, #58cc02);
			}
		}

		&--streak {
			border-color: var(--color-danger, #ff4b4b);
			.stat-card__label {
				background: var(--color-danger, #ff4b4b);
			}
		}
	}

	.stat-card__label {
		color: #fff;
		font-size: 0.8rem;
		font-weight: 800;
		text-transform: uppercase;
		border-radius: 12px 12px 0 0;
		padding: 0.25rem;
	}

	.stat-card__value {
		font-size: 1.4rem;
		font-weight: 800;
		color: #4b4b4b;
		padding: 0.6rem 0.5rem 0.4rem;
	}
</style>
