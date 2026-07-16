<script lang="ts">
	import { locale } from 'svelte-i18n';
	import NavBar from 'components/NavBar.svelte';
	import Content from 'components/Content.svelte';
	import Footer from 'components/Footer.svelte';
	import Column from 'components/Column.svelte';
	import Columns from 'components/Columns.svelte';
	import type { ModulesType } from 'types/ModulesType';
	import { page } from '$app/state';
	import { base } from '$app/paths';
	import { progress, displayStreak } from '$lib/gamification';

	export const courseName = page.data.course.courseName;
	export let modules: ModulesType = page.data.course.modules;
	export let languageName = page.data.course.languageName;
	export const repositoryURL = page.data.course.repositoryURL;
	export let uiLanguage = 'ko';
	locale.set(uiLanguage);

	// Flatten skills across modules to determine the "current" (first uncompleted) skill
	$: allSkills = modules.flatMap((m) => m.skills);
	$: completedIds = new Set(
		allSkills.filter((s) => ($progress.completedSkills[s.id] || 0) > 0).map((s) => s.id)
	);
	$: currentId = allSkills.find((s) => !completedIds.has(s.id))?.id;

	const hrefFor = (skill) => `${base}/course/${courseName}/skill/${skill.practiceHref}`;

	// Korean display names + topical icons per skill (URLs stay English)
	const skillMeta: Record<string, { label: string; icon: string }> = {
		Numbers: { label: '숫자', icon: '🔢' },
		Pronouns: { label: '대명사', icon: '👤' },
		'This and That': { label: '이것저것', icon: '👆' },
		'Being Polite': { label: '예의 표현', icon: '🙏' },
		'Question Words': { label: '의문사', icon: '❓' },
		'Time and Days': { label: '시간과 날짜', icon: '🕒' }
	};
	const labelFor = (skill) => skillMeta[skill.title]?.label ?? skill.title;
	const iconFor = (skill) => skillMeta[skill.title]?.icon ?? '★';

	// snake offsets, Duolingo-style
	const offsets = [0, 45, 75, 45, 0, -45, -75, -45];
</script>

<svelte:head>
	<title>LibreLingo - learn {languageName} for free</title>
</svelte:head>

<main class="course-page app-page">
	<NavBar hasAuth {repositoryURL} />

	<div class="stats-bar">
		<span class="stat" title="연속 학습">🔥 {displayStreak($progress)}</span>
		<span class="stat" title="XP">⚡ {$progress.xp} XP</span>
	</div>

	<div class="path-container">
		{#each modules as module, mi}
			<section class="unit">
				<header class="unit-banner">
					<div class="unit-banner__label">유닛 {mi + 1}</div>
					<h2 class="unit-banner__title">{module.title}</h2>
				</header>

				<div class="path">
					{#each module.skills as skill, si}
						{@const done = completedIds.has(skill.id)}
						{@const isCurrent = skill.id === currentId}
						{@const locked = !done && !isCurrent}
						<div class="node-row" style="transform: translateX({offsets[si % offsets.length]}px)">
							{#if isCurrent}
								<div class="start-bubble">시작</div>
							{/if}
							{#if locked}
								<div class="node node--locked" aria-disabled="true" title="이전 레슨을 먼저 완료하세요">
									<span class="node__icon">🔒</span>
								</div>
							{:else}
								<a
									class="node {done ? 'node--done' : 'node--active'}"
									href={hrefFor(skill)}
									data-test="skill node"
								>
									<span class="node__icon">{done ? '✓' : iconFor(skill)}</span>
								</a>
							{/if}
							<span class="node-label" class:node-label--locked={locked}>{labelFor(skill)}</span>
						</div>
					{/each}
				</div>
			</section>
		{/each}
	</div>

	<Footer>
		<Content>
			<Columns>
				<Column>
					<strong>LibreLingoRelive</strong> is a fork from LibreLingoCommunity, which is a fork from
					<strong>LibreLingo</strong> by
					<a href="https://github.com/kantord">Dániel Kántor</a>
					and
					<a href="https://github.com/LibreLingo/LibreLingo#contributors"> various contributors. </a>
				</Column>
				<Column>
					The source code is licensed
					<a href="https://opensource.org/licenses/AGPL-3.0">AGPL-3.0.</a>
					<br />
					<a href="https://codeberg.org/LibreLingoRelive"> Source code available on Codeberg. </a>
				</Column>
				<Column />
			</Columns>
			<p></p>
		</Content>
	</Footer>
</main>

<style lang="scss">
	.stats-bar {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
		max-width: 640px;
		margin: 0.5rem auto 0;
		padding: 0 1rem;
	}

	.stat {
		font-weight: 700;
		font-size: 1.1rem;
		color: #4b4b4b;
	}

	.path-container {
		max-width: 640px;
		margin: 0 auto;
		padding: 1rem 1rem 4rem;
	}

	.unit {
		margin-bottom: 2rem;
	}

	.unit-banner {
		background: var(--color-primary, #58cc02);
		border-radius: 16px;
		box-shadow: 0 4px 0 var(--color-primary-shadow, #58a700);
		color: #fff;
		padding: 1rem 1.5rem;
		margin-bottom: 2rem;
	}

	.unit-banner__label {
		font-size: 0.85rem;
		font-weight: 700;
		text-transform: uppercase;
		opacity: 0.85;
	}

	.unit-banner__title {
		font-size: 1.4rem;
		font-weight: 800;
		margin: 0;
	}

	.path {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.6rem;
	}

	.node-row {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 120px;
	}

	.node {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 70px;
		height: 64px;
		border-radius: 50% / 46%;
		font-size: 1.8rem;
		color: #fff;
		text-decoration: none;
		user-select: none;
		transition: transform 0.1s;
	}

	.node--active {
		background: var(--color-primary, #58cc02);
		box-shadow: 0 8px 0 var(--color-primary-shadow, #58a700);
	}

	.node--done {
		background: var(--color-gold, #ffc800);
		box-shadow: 0 8px 0 #e6a800;
	}

	.node--locked {
		background: var(--color-locked, #e5e5e5);
		box-shadow: 0 8px 0 var(--color-locked-shadow, #afafaf);
		cursor: not-allowed;
	}

	.node:active:not(.node--locked) {
		transform: translateY(4px);
		box-shadow: 0 4px 0 var(--color-primary-shadow, #58a700);
	}

	.node-label {
		margin-top: 0.9rem;
		font-weight: 700;
		font-size: 0.9rem;
		color: #4b4b4b;
		text-align: center;
	}

	.node-label--locked {
		color: #afafaf;
	}

	.start-bubble {
		position: absolute;
		top: -2.4rem;
		background: #fff;
		color: var(--color-primary, #58cc02);
		border: 2px solid #e5e5e5;
		border-radius: 10px;
		font-weight: 800;
		font-size: 0.85rem;
		text-transform: uppercase;
		padding: 0.25rem 0.7rem;
		animation: bounce 1.2s ease-in-out infinite;
		z-index: 1;

		&::after {
			content: '';
			position: absolute;
			left: 50%;
			bottom: -7px;
			transform: translateX(-50%) rotate(45deg);
			width: 12px;
			height: 12px;
			background: #fff;
			border-right: 2px solid #e5e5e5;
			border-bottom: 2px solid #e5e5e5;
		}
	}

	/* Mobile polish */
	@media (max-width: 480px) {
		.node {
			width: 62px;
			height: 56px;
			font-size: 1.5rem;
		}

		.unit-banner {
			padding: 0.8rem 1.1rem;
		}

		.unit-banner__title {
			font-size: 1.15rem;
		}

		.node-row {
			width: 100px;
		}

		.path {
			gap: 1.2rem;
		}
	}

	@keyframes bounce {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-6px);
		}
	}
</style>
