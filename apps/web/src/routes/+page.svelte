<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import Mascot from 'components/Mascot.svelte';

	let coursesFs = page.data.coursesFs;
	// First available course; fall back to the Teochew course path
	const coursePath = coursesFs?.[0]?.path || 'tc-from-ko';
	const courseHref = `${base}/course/${coursePath}`;
</script>

<svelte:head>
	<title>Chaoshan - 조주어 배우기</title>
	<meta name="description" content="조주어(潮州話, Teochew)를 무료로 배워 보세요. 재미있는 레슨으로 차오산 방언을 공부하는 웹 앱입니다." />
</svelte:head>

<main class="landing">
	<div class="landing__inner">
		<div class="landing__mascot">
			<Mascot shadow={false} />
		</div>

		<h1 class="landing__title">Chaoshan</h1>
		<p class="landing__tagline">조주어(潮州話)를 배워 보세요</p>
		<p class="landing__sub">
			재미있는 레슨으로 배우는 차오산 방언 — 발음(Peng'im)·한자·중국어 설명과 함께.
			무료이며 가입도 필요 없습니다.
		</p>

		<a class="landing__cta" href={courseHref} data-test="start-course">시작하기</a>

		<p class="landing__credit">
			콘텐츠 출처: <a href="https://learnteochew.com" target="_blank" rel="noreferrer">Learn Teochew</a>
			· 오픈 소스 (<a href="https://opensource.org/licenses/AGPL-3.0" target="_blank" rel="noreferrer">AGPL-3.0</a>,
			<a href="https://codeberg.org/LibreLingoRelive" target="_blank" rel="noreferrer">LibreLingoRelive</a> 기반)
		</p>
	</div>
</main>

<style lang="scss">
	.landing {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: linear-gradient(180deg, #ffffff 0%, #f0ffe0 100%);
		text-align: center;
		padding: 2rem 1.5rem;
	}

	.landing__inner {
		max-width: 560px;
	}

	.landing__mascot {
		width: 180px;
		margin: 0 auto 1rem;
	}

	.landing__title {
		font-size: 3rem;
		font-weight: 900;
		color: var(--color-primary, #58cc02);
		letter-spacing: 0.01em;
		margin: 0 0 0.5rem;
	}

	.landing__tagline {
		font-size: 1.5rem;
		font-weight: 800;
		color: #3c3c3c;
		margin: 0 0 0.8rem;
	}

	.landing__sub {
		color: #777;
		line-height: 1.6;
		margin: 0 0 2rem;
	}

	.landing__cta {
		display: inline-block;
		background: var(--color-primary, #58cc02);
		color: #fff;
		font-size: 1.2rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		text-decoration: none;
		padding: 1rem 3.5rem;
		border-radius: 16px;
		border-bottom: 4px solid var(--color-primary-shadow, #58a700);
		transition: all 0.1s;

		&:hover {
			filter: brightness(1.05);
		}

		&:active {
			transform: translateY(2px);
			border-bottom-width: 2px;
		}
	}

	.landing__credit {
		margin-top: 3rem;
		font-size: 0.8rem;
		color: #aaa;

		a {
			color: #999;
			text-decoration: underline;
		}
	}
</style>
