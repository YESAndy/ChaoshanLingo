<script lang="ts">
	import { base } from '$app/paths';
	import NavBar from 'components/NavBar.svelte';
	import { Howl } from 'howler';

	// Source: https://en.wikipedia.org/wiki/Peng%27im (alphabet section).
	// Korean column = approximate pronunciation hints (근사치), not exact equivalents.
	// `syl` = attested syllable for the example character, looked up in the
	// teochew-g2p pronunciation dictionary — used as the audio filename
	// (static/voice-bank/<syl>.mp3, native recordings).

	const initials = [
		{ p: 'b', ipa: '[p]', ex: '比', syl: 'bi2', ko: 'ㅃ (된소리, 숨 없이)' },
		{ p: 'p', ipa: '[pʰ]', ex: '皮', syl: 'puê5', ko: 'ㅍ (거센소리)' },
		{ p: 'bh', ipa: '[b]', ex: '米', syl: 'bhi2', ko: '유성 ㅂ (영어 b)' },
		{ p: 'm', ipa: '[m]', ex: '毛', syl: 'mo5', ko: 'ㅁ' },
		{ p: 'd', ipa: '[t]', ex: '都', syl: 'dou1', ko: 'ㄸ (된소리)' },
		{ p: 't', ipa: '[tʰ]', ex: '臺', syl: 'tai5', ko: 'ㅌ (거센소리)' },
		{ p: 'n', ipa: '[n]', ex: '年', syl: 'ni5', ko: 'ㄴ' },
		{ p: 'l', ipa: '[l]', ex: '來', syl: 'lai5', ko: 'ㄹ' },
		{ p: 'z', ipa: '[ts]', ex: '書', syl: 'ze1', ko: 'ㅉ (된소리)' },
		{ p: 'c', ipa: '[tsʰ]', ex: '菜', syl: 'cai3', ko: 'ㅊ (거센소리)' },
		{ p: 's', ipa: '[s]', ex: '士', syl: 'se6', ko: 'ㅅ/ㅆ' },
		{ p: 'r', ipa: '[(d)z]', ex: '爾', syl: 're2', ko: '유성 ㅈ (영어 z와 비슷)' },
		{ p: 'g', ipa: '[k]', ex: '歌', syl: 'go1', ko: 'ㄲ (된소리)' },
		{ p: 'k', ipa: '[kʰ]', ex: '可', syl: 'ko2', ko: 'ㅋ (거센소리)' },
		{ p: 'gh', ipa: '[g]', ex: '鵝', syl: 'gho5', ko: '유성 ㄱ (영어 g)' },
		{ p: 'ng', ipa: '[ŋ]', ex: '雅', syl: 'ngia2', ko: '응 (받침 ㅇ 소리로 시작)' },
		{ p: 'h', ipa: '[h]', ex: '海', syl: 'hai2', ko: 'ㅎ' },
		{ p: '(없음)', ipa: '[ʔ]', ex: '衣', syl: 'i1', ko: '모음으로 시작 (영성모)' }
	];

	const vowels = [
		{ p: 'i', ipa: '[i]', ex: '衣', syl: 'i1', ko: '이' },
		{ p: 'u', ipa: '[u]', ex: '汙', syl: 'u1', ko: '우' },
		{ p: 'a', ipa: '[a]', ex: '亞', syl: 'a1', ko: '아' },
		{ p: 'ia', ipa: '[ia]', ex: '呀', syl: 'ia1', ko: '야' },
		{ p: 'ua', ipa: '[ua]', ex: '娃', syl: 'ua1', ko: '와' },
		{ p: 'o', ipa: '[o]', ex: '窩', syl: 'o1', ko: '오' },
		{ p: 'io', ipa: '[io]', ex: '腰', syl: 'io1', ko: '요' },
		{ p: 'ê', ipa: '[e]', ex: '啞', syl: 'ê2', ko: '에' },
		{ p: 'uê', ipa: '[ue]', ex: '鍋', syl: 'uê1', ko: '웨' },
		{ p: 'e', ipa: '[ɯ]', ex: '余', syl: 'e5', ko: '으' },
		{ p: 'ai', ipa: '[ai]', ex: '哀', syl: 'ai1', ko: '아이' },
		{ p: 'uai', ipa: '[uai]', ex: '歪', syl: 'uai1', ko: '와이' },
		{ p: 'oi', ipa: '[oi]', ex: '鞋', syl: 'oi5', ko: '오이' },
		{ p: 'ui', ipa: '[ui]', ex: '威', syl: 'ui1', ko: '우이' },
		{ p: 'ao', ipa: '[au]', ex: '歐', syl: 'ao1', ko: '아우' },
		{ p: 'ou', ipa: '[ou]', ex: '烏', syl: 'ou1', ko: '오우' },
		{ p: 'iou', ipa: '[iou]', ex: '夭', syl: 'iou1', ko: '요우' },
		{ p: 'iu', ipa: '[iu]', ex: '憂', syl: 'iu1', ko: '유' }
	];

	const nasalVowels = [
		{ p: 'in', ipa: '[ĩ]', ex: '丸', syl: 'in5', ko: '이 (콧소리)' },
		{ p: 'an', ipa: '[ã]', ex: '噯', syl: 'an6', ko: '아 (콧소리)' },
		{ p: 'ian', ipa: '[ĩã]', ex: '營', syl: 'ian5', ko: '야 (콧소리)' },
		{ p: 'uan', ipa: '[ũã]', ex: '鞍', syl: 'uan1', ko: '와 (콧소리)' },
		{ p: 'ion', ipa: '[ĩõ]', ex: '羊', syl: 'ion5', ko: '요 (콧소리)' },
		{ p: 'ên', ipa: '[ẽ]', ex: '楹', syl: 'ên5', ko: '에 (콧소리)' },
		{ p: 'en', ipa: '[ɯ̃]', ex: '秧', syl: 'en1', ko: '으 (콧소리)' },
		{ p: 'ain', ipa: '[ãĩ]', ex: '愛', syl: 'ain3', ko: '아이 (콧소리)' },
		{ p: 'oin', ipa: '[õĩ]', ex: '閑', syl: 'oin5', ko: '오이 (콧소리)' }
	];

	const nasalCoda = [
		{ p: 'im', ipa: '[im]', ex: '音', syl: 'im1', ko: '임' },
		{ p: 'am', ipa: '[am]', ex: '庵', syl: 'am1', ko: '암' },
		{ p: 'iam', ipa: '[iam]', ex: '淹', syl: 'iam1', ko: '얌' },
		{ p: 'uam', ipa: '[uam]', ex: '凡', syl: 'huam5', ko: '왐' },
		{ p: 'ing', ipa: '[iŋ]', ex: '因', syl: 'ing1', ko: '잉' },
		{ p: 'ung', ipa: '[uŋ]', ex: '溫', syl: 'ung1', ko: '웅' },
		{ p: 'ang', ipa: '[aŋ]', ex: '按', syl: 'ang3', ko: '앙' },
		{ p: 'iang', ipa: '[iaŋ]', ex: '央', syl: 'iang1', ko: '양' },
		{ p: 'uang', ipa: '[uaŋ]', ex: '汪', syl: 'uang1', ko: '왕' },
		{ p: 'ong', ipa: '[oŋ]', ex: '翁', syl: 'ong1', ko: '옹' },
		{ p: 'iong', ipa: '[ioŋ]', ex: '雍', syl: 'iong1', ko: '용' },
		{ p: 'êng', ipa: '[eŋ]', ex: '英', syl: 'êng1', ko: '엥' }
	];

	const checked = [
		{ p: 'ih', ipa: '[iʔ]', ex: '裂', syl: 'lih8', ko: '이 (급히 끊음)' },
		{ p: 'ah', ipa: '[aʔ]', ex: '鴨', syl: 'ah4', ko: '아 (급히 끊음)' },
		{ p: 'iah', ipa: '[iaʔ]', ex: '益', syl: 'iah4', ko: '야 (급히 끊음)' },
		{ p: 'uah', ipa: '[uaʔ]', ex: '活', syl: 'uah8', ko: '와 (급히 끊음)' },
		{ p: 'oh', ipa: '[oʔ]', ex: '學', syl: 'oh8', ko: '오 (급히 끊음)' },
		{ p: 'ioh', ipa: '[ioʔ]', ex: '約', syl: 'ioh4', ko: '요 (급히 끊음)' },
		{ p: 'êh', ipa: '[eʔ]', ex: '厄', syl: 'êh4', ko: '에 (급히 끊음)' },
		{ p: 'oih', ipa: '[oiʔ]', ex: '狹', syl: 'oih8', ko: '오이 (급히 끊음)' },
		{ p: 'ib', ipa: '[ip̚]', ex: '邑', syl: 'ib4', ko: '입 (ㅂ받침)' },
		{ p: 'ab', ipa: '[ap̚]', ex: '盒', syl: 'ab8', ko: '압 (ㅂ받침)' },
		{ p: 'iab', ipa: '[iap̚]', ex: '壓', syl: 'iab4', ko: '얍 (ㅂ받침)' },
		{ p: 'uab', ipa: '[uap̚]', ex: '法', syl: 'huab4', ko: '왑 (ㅂ받침)' },
		{ p: 'ig', ipa: '[ik̚]', ex: '乙', syl: 'ig4', ko: '익 (ㄱ받침)' },
		{ p: 'ug', ipa: '[uk̚]', ex: '熨', syl: 'ug4', ko: '욱 (ㄱ받침)' },
		{ p: 'ag', ipa: '[ak̚]', ex: '惡', syl: 'ag4', ko: '악 (ㄱ받침)' },
		{ p: 'iag', ipa: '[iak̚]', ex: '躍', syl: 'iag4', ko: '약 (ㄱ받침)' },
		{ p: 'uag', ipa: '[uak̚]', ex: '獲', syl: 'uag8', ko: '왁 (ㄱ받침)' },
		{ p: 'og', ipa: '[ok̚]', ex: '屋', syl: 'og4', ko: '옥 (ㄱ받침)' },
		{ p: 'iog', ipa: '[iok̚]', ex: '育', syl: 'iog8', ko: '욕 (ㄱ받침)' },
		{ p: 'êg', ipa: '[ek̚]', ex: '液', syl: 'êg8', ko: '엑 (ㄱ받침)' }
	];

	const tones = [
		{ n: 1, name: '음평 (陰平)', value: '33', ex: '詩', syl: 'si1', ko: '중간 높이로 평평하게' },
		{ n: 2, name: '음상 (陰上)', value: '52', ex: '死', syl: 'si2', ko: '높은 데서 뚝 떨어짐' },
		{ n: 3, name: '음거 (陰去)', value: '213', ex: '世', syl: 'si3', ko: '낮게 내렸다 살짝 올림' },
		{ n: 4, name: '음입 (陰入)', value: '2', ex: '薛', syl: 'sih4', ko: '낮고 짧게 끊음' },
		{ n: 5, name: '양평 (陽平)', value: '55', ex: '時', syl: 'si5', ko: '높게 평평하게' },
		{ n: 6, name: '양상 (陽上)', value: '35', ex: '是', syl: 'si6', ko: '중간에서 위로 올림' },
		{ n: 7, name: '양거 (陽去)', value: '11', ex: '示', syl: 'si7', ko: '낮게 평평하게' },
		{ n: 8, name: '양입 (陽入)', value: '4', ex: '蝕', syl: 'sih8', ko: '중간 높이로 짧게 끊음' }
	];

	// Audio: only real native recordings are played (static/voice-bank/<syl>.mp3).
	// Missing files mark the row as "녹음 준비 중" — no synthetic fallback, to
	// avoid teaching wrong pronunciation.
	let missing: Record<string, boolean> = {};
	let playing: string | null = null;

	const play = (syl: string) => {
		if (missing[syl]) return;
		playing = syl;
		const howl = new Howl({
			src: [`${base}/voice-bank/${syl}.mp3`],
			onloaderror: () => {
				missing = { ...missing, [syl]: true };
				playing = null;
			},
			onend: () => (playing = null)
		});
		howl.play();
	};
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
			🔊 버튼은 원어민 녹음이 준비된 항목만 재생됩니다.
		</p>

		{#each [
			{ title: '성모 (초성, 18개)', rows: initials, note: '' },
			{ title: '운모 — 모음', rows: vowels, note: '' },
			{ title: '운모 — 비모음 (콧소리, -n 표기)', rows: nasalVowels, note: '-n은 받침이 아니라 모음 전체를 콧소리로 내는 표시입니다.' },
			{ title: '운모 — 비음 받침 (-m, -ng)', rows: nasalCoda, note: '' },
			{ title: '운모 — 입성 (-h, -b, -g: 짧게 끊는 소리)', rows: checked, note: '' }
		] as section}
			<h2>{section.title}</h2>
			{#if section.note}<p class="note">{section.note}</p>{/if}
			<table>
				<thead><tr><th>Peng'im</th><th>IPA</th><th>예</th><th>한국어 근사 발음</th><th>듣기</th></tr></thead>
				<tbody>
					{#each section.rows as r}
						<tr>
							<td class="p">{r.p}</td>
							<td>{r.ipa}</td>
							<td>{r.ex} <span class="syl">{r.syl}</span></td>
							<td>{r.ko}</td>
							<td>
								<button
									type="button"
									class="play"
									class:play--missing={missing[r.syl]}
									class:play--playing={playing === r.syl}
									title={missing[r.syl] ? '녹음 준비 중' : `${r.syl} 듣기`}
									on:click={() => play(r.syl)}
								>{missing[r.syl] ? '🚫' : '🔊'}</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/each}

		<h2>성조 (8성)</h2>
		<table>
			<thead><tr><th>번호</th><th>이름</th><th>조값</th><th>예</th><th>한국어 설명</th><th>듣기</th></tr></thead>
			<tbody>
				{#each tones as t}
					<tr>
						<td class="p">{t.n}</td>
						<td>{t.name}</td>
						<td>{t.value}</td>
						<td>{t.ex} <span class="syl">{t.syl}</span></td>
						<td>{t.ko}</td>
						<td>
							<button
								type="button"
								class="play"
								class:play--missing={missing[t.syl]}
								class:play--playing={playing === t.syl}
								title={missing[t.syl] ? '녹음 준비 중' : `${t.syl} 듣기`}
								on:click={() => play(t.syl)}
							>{missing[t.syl] ? '🚫' : '🔊'}</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>

		<p class="credit">
			자료 출처: <a href="https://en.wikipedia.org/wiki/Peng%27im" target="_blank" rel="noreferrer">Wikipedia — Peng'im</a>
			(성조 기준: 汕头 Swatow 방언) ·
			예시 음절 발음 표기: <a href="https://github.com/p1an-lin-jung/teochew-g2p" target="_blank" rel="noreferrer">teochew-g2p</a> 사전
		</p>
	</div>
</main>

<style lang="scss">
	.dict {
		max-width: 800px;
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

	.syl {
		color: #999;
		font-size: 0.85rem;
	}

	.play {
		background: none;
		border: 2px solid #e5e5e5;
		border-radius: 10px;
		padding: 0.15rem 0.5rem;
		cursor: pointer;
		font-size: 0.95rem;
		transition: all 0.1s;

		&:hover {
			background: #f0ffe0;
		}

		&--playing {
			border-color: var(--color-primary, #58cc02);
			background: #f0ffe0;
		}

		&--missing {
			opacity: 0.45;
			cursor: not-allowed;
		}
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
