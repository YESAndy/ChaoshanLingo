<script lang="ts">
	import { base } from '$app/paths';
	import NavBar from 'components/NavBar.svelte';

	// Source: https://en.wikipedia.org/wiki/Peng%27im (alphabet section).
	// Korean column = approximate pronunciation hints (근사치), not exact equivalents.

	const initials = [
		{ p: 'b', ipa: '[p]', ex: '比', ko: 'ㅃ (된소리, 숨 없이)' },
		{ p: 'p', ipa: '[pʰ]', ex: '皮', ko: 'ㅍ (거센소리)' },
		{ p: 'bh', ipa: '[b]', ex: '米', ko: '유성 ㅂ (영어 b)' },
		{ p: 'm', ipa: '[m]', ex: '毛', ko: 'ㅁ' },
		{ p: 'd', ipa: '[t]', ex: '都', ko: 'ㄸ (된소리)' },
		{ p: 't', ipa: '[tʰ]', ex: '臺', ko: 'ㅌ (거센소리)' },
		{ p: 'n', ipa: '[n]', ex: '年', ko: 'ㄴ' },
		{ p: 'l', ipa: '[l]', ex: '來', ko: 'ㄹ' },
		{ p: 'z', ipa: '[ts]', ex: '書', ko: 'ㅉ (된소리)' },
		{ p: 'c', ipa: '[tsʰ]', ex: '菜', ko: 'ㅊ (거센소리)' },
		{ p: 's', ipa: '[s]', ex: '士', ko: 'ㅅ/ㅆ' },
		{ p: 'r', ipa: '[(d)z]', ex: '爾', ko: '유성 ㅈ (영어 z와 비슷)' },
		{ p: 'g', ipa: '[k]', ex: '歌', ko: 'ㄲ (된소리)' },
		{ p: 'k', ipa: '[kʰ]', ex: '可', ko: 'ㅋ (거센소리)' },
		{ p: 'gh', ipa: '[g]', ex: '鵝', ko: '유성 ㄱ (영어 g)' },
		{ p: 'ng', ipa: '[ŋ]', ex: '雅', ko: '응 (받침 ㅇ 소리로 시작)' },
		{ p: 'h', ipa: '[h]', ex: '海', ko: 'ㅎ' },
		{ p: '(없음)', ipa: '[ʔ]', ex: '-', ko: '모음으로 시작 (영성모)' }
	];

	const vowels = [
		{ p: 'i', ipa: '[i]', ex: '衣', ko: '이' },
		{ p: 'u', ipa: '[u]', ex: '汙', ko: '우' },
		{ p: 'a', ipa: '[a]', ex: '亞', ko: '아' },
		{ p: 'ia', ipa: '[ia]', ex: '呀', ko: '야' },
		{ p: 'ua', ipa: '[ua]', ex: '娃', ko: '와' },
		{ p: 'o', ipa: '[o]', ex: '窩', ko: '오' },
		{ p: 'io', ipa: '[io]', ex: '腰', ko: '요' },
		{ p: 'ê', ipa: '[e]', ex: '啞', ko: '에' },
		{ p: 'uê', ipa: '[ue]', ex: '鍋', ko: '웨' },
		{ p: 'e', ipa: '[ɯ]', ex: '余', ko: '으' },
		{ p: 'ai', ipa: '[ai]', ex: '哀', ko: '아이' },
		{ p: 'uai', ipa: '[uai]', ex: '歪', ko: '와이' },
		{ p: 'oi', ipa: '[oi]', ex: '鞋', ko: '오이' },
		{ p: 'ui', ipa: '[ui]', ex: '威', ko: '우이' },
		{ p: 'ao', ipa: '[au]', ex: '歐', ko: '아우' },
		{ p: 'ou', ipa: '[ou]', ex: '烏', ko: '오우' },
		{ p: 'iou', ipa: '[iou]', ex: '夭', ko: '요우' },
		{ p: 'iu', ipa: '[iu]', ex: '憂', ko: '유' }
	];

	const nasalVowels = [
		{ p: 'in', ipa: '[ĩ]', ex: '丸', ko: '이 (콧소리)' },
		{ p: 'an', ipa: '[ã]', ex: '噯', ko: '아 (콧소리)' },
		{ p: 'ian', ipa: '[ĩã]', ex: '營', ko: '야 (콧소리)' },
		{ p: 'uan', ipa: '[ũã]', ex: '鞍', ko: '와 (콧소리)' },
		{ p: 'ion', ipa: '[ĩõ]', ex: '羊', ko: '요 (콧소리)' },
		{ p: 'ên', ipa: '[ẽ]', ex: '楹', ko: '에 (콧소리)' },
		{ p: 'en', ipa: '[ɯ̃]', ex: '秧', ko: '으 (콧소리)' },
		{ p: 'ain', ipa: '[ãĩ]', ex: '愛', ko: '아이 (콧소리)' },
		{ p: 'oin', ipa: '[õĩ]', ex: '閑', ko: '오이 (콧소리)' }
	];

	const nasalCoda = [
		{ p: 'im', ipa: '[im]', ex: '音', ko: '임' },
		{ p: 'am', ipa: '[am]', ex: '庵', ko: '암' },
		{ p: 'iam', ipa: '[iam]', ex: '淹', ko: '얌' },
		{ p: 'uam', ipa: '[uam]', ex: '凡', ko: '왐' },
		{ p: 'ing', ipa: '[iŋ]', ex: '因', ko: '잉' },
		{ p: 'ung', ipa: '[uŋ]', ex: '溫', ko: '웅' },
		{ p: 'ang', ipa: '[aŋ]', ex: '按', ko: '앙' },
		{ p: 'iang', ipa: '[iaŋ]', ex: '央', ko: '양' },
		{ p: 'uang', ipa: '[uaŋ]', ex: '汪', ko: '왕' },
		{ p: 'ong', ipa: '[oŋ]', ex: '翁', ko: '옹' },
		{ p: 'iong', ipa: '[ioŋ]', ex: '雍', ko: '용' },
		{ p: 'êng', ipa: '[eŋ]', ex: '英', ko: '엥' }
	];

	const checked = [
		{ p: 'ih', ipa: '[iʔ]', ex: '裂', ko: '이 (급히 끊음)' },
		{ p: 'ah', ipa: '[aʔ]', ex: '鴨', ko: '아 (급히 끊음)' },
		{ p: 'iah', ipa: '[iaʔ]', ex: '益', ko: '야 (급히 끊음)' },
		{ p: 'uah', ipa: '[uaʔ]', ex: '活', ko: '와 (급히 끊음)' },
		{ p: 'oh', ipa: '[oʔ]', ex: '學', ko: '오 (급히 끊음)' },
		{ p: 'ioh', ipa: '[ioʔ]', ex: '約', ko: '요 (급히 끊음)' },
		{ p: 'êh', ipa: '[eʔ]', ex: '厄', ko: '에 (급히 끊음)' },
		{ p: 'oih', ipa: '[oiʔ]', ex: '狹', ko: '오이 (급히 끊음)' },
		{ p: 'ib', ipa: '[ip̚]', ex: '邑', ko: '입 (ㅂ받침)' },
		{ p: 'ab', ipa: '[ap̚]', ex: '盒', ko: '압 (ㅂ받침)' },
		{ p: 'iab', ipa: '[iap̚]', ex: '壓', ko: '얍 (ㅂ받침)' },
		{ p: 'uab', ipa: '[uap̚]', ex: '法', ko: '왑 (ㅂ받침)' },
		{ p: 'ig', ipa: '[ik̚]', ex: '乙', ko: '익 (ㄱ받침)' },
		{ p: 'ug', ipa: '[uk̚]', ex: '熨', ko: '욱 (ㄱ받침)' },
		{ p: 'ag', ipa: '[ak̚]', ex: '惡', ko: '악 (ㄱ받침)' },
		{ p: 'iag', ipa: '[iak̚]', ex: '躍', ko: '약 (ㄱ받침)' },
		{ p: 'uag', ipa: '[uak̚]', ex: '獲', ko: '왁 (ㄱ받침)' },
		{ p: 'og', ipa: '[ok̚]', ex: '屋', ko: '옥 (ㄱ받침)' },
		{ p: 'iog', ipa: '[iok̚]', ex: '育', ko: '욕 (ㄱ받침)' },
		{ p: 'êg', ipa: '[ek̚]', ex: '液', ko: '엑 (ㄱ받침)' }
	];

	const tones = [
		{ n: 1, name: '음평 (陰平)', value: '33', ex: '詩 si1', ko: '중간 높이로 평평하게' },
		{ n: 2, name: '음상 (陰上)', value: '52', ex: '死 si2', ko: '높은 데서 뚝 떨어짐' },
		{ n: 3, name: '음거 (陰去)', value: '213', ex: '世 si3', ko: '낮게 내렸다 살짝 올림' },
		{ n: 4, name: '음입 (陰入)', value: '2', ex: '薛 sih4', ko: '낮고 짧게 끊음' },
		{ n: 5, name: '양평 (陽平)', value: '55', ex: '時 si5', ko: '높게 평평하게' },
		{ n: 6, name: '양상 (陽上)', value: '35', ex: '是 si6', ko: '중간에서 위로 올림' },
		{ n: 7, name: '양거 (陽去)', value: '11', ex: '示 si7', ko: '낮게 평평하게' },
		{ n: 8, name: '양입 (陽入)', value: '4', ex: '蝕 sih8', ko: '중간 높이로 짧게 끊음' }
	];
</script>

<svelte:head>
	<title>Peng'im 발음표 - Chaoshan</title>
</svelte:head>

<main class="app-page">
	<NavBar />

	<div class="dict">
		<h1>Peng'im 발음표</h1>
		<p class="intro">
			조주어 병음(潮州話拼音方案, Peng'im)은 1960년 광둥성 교육부가 공표한 로마자 표기법입니다.
			성조는 숫자 1~8로 음절 뒤에 표기합니다 (예: si1, sih4).
			한국어 발음은 <strong>근사치</strong>입니다.
		</p>

		<h2>성모 (초성, 18개)</h2>
		<table>
			<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th></tr></thead>
			<tbody>
				{#each initials as r}
					<tr><td class="p">{r.p}</td><td>{r.ipa}</td><td>{r.ex}</td><td>{r.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<h2>운모 — 모음</h2>
		<table>
			<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th></tr></thead>
			<tbody>
				{#each vowels as r}
					<tr><td class="p">{r.p}</td><td>{r.ipa}</td><td>{r.ex}</td><td>{r.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<h2>운모 — 비모음 (콧소리, -n 표기)</h2>
		<p class="note">-n은 받침이 아니라 모음 전체를 콧소리로 내는 표시입니다.</p>
		<table>
			<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th></tr></thead>
			<tbody>
				{#each nasalVowels as r}
					<tr><td class="p">{r.p}</td><td>{r.ipa}</td><td>{r.ex}</td><td>{r.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<h2>운모 — 비음 받침 (-m, -ng)</h2>
		<table>
			<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th></tr></thead>
			<tbody>
				{#each nasalCoda as r}
					<tr><td class="p">{r.p}</td><td>{r.ipa}</td><td>{r.ex}</td><td>{r.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<h2>운모 — 입성 (-h, -b, -g: 짧게 끊는 소리)</h2>
		<table>
			<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th></tr></thead>
			<tbody>
				{#each checked as r}
					<tr><td class="p">{r.p}</td><td>{r.ipa}</td><td>{r.ex}</td><td>{r.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<h2>성조 (8성)</h2>
		<table>
			<thead><tr><th>번호</th><th>이름</th><th>조값</th><th>예</th><th>한국어 설명</th></tr></thead>
			<tbody>
				{#each tones as t}
					<tr><td class="p">{t.n}</td><td>{t.name}</td><td>{t.value}</td><td>{t.ex}</td><td>{t.ko}</td></tr>
				{/each}
			</tbody>
		</table>

		<p class="credit">
			자료 출처: <a href="https://en.wikipedia.org/wiki/Peng%27im" target="_blank" rel="noreferrer">Wikipedia — Peng'im</a>
			(성조 기준: 汕头 Swatow 방언)
		</p>
	</div>
</main>

<style lang="scss">
	.dict {
		max-width: 760px;
		margin: 0 auto;
		padding: 1.5rem 1rem 4rem;
	}

	h1 {
		font-size: 1.8rem;
		font-weight: 800;
		color: var(--color-primary, #58cc02);
		margin-bottom: 0.5rem;
	}

	h2 {
		font-size: 1.2rem;
		font-weight: 800;
		color: #3c3c3c;
		margin: 2rem 0 0.6rem;
	}

	.intro,
	.note {
		color: #666;
		line-height: 1.6;
	}

	.note {
		font-size: 0.9rem;
		margin-bottom: 0.5rem;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		background: #fff;
		border-radius: 12px;
		overflow: hidden;
		border: 2px solid #e5e5e5;
	}

	th {
		background: #f7f7f7;
		text-align: left;
		padding: 0.5rem 0.8rem;
		font-size: 0.85rem;
		color: #777;
		text-transform: uppercase;
	}

	td {
		padding: 0.45rem 0.8rem;
		border-top: 1px solid #f0f0f0;
	}

	td.p {
		font-weight: 800;
		color: var(--color-primary, #58cc02);
	}

	.credit {
		margin-top: 2rem;
		font-size: 0.8rem;
		color: #aaa;

		a {
			color: #999;
		}
	}
</style>
