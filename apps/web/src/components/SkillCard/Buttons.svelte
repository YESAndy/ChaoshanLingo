<script lang="ts">
	import Button from 'components/Button.svelte';
	import Translate from 'components/Translate.svelte';

	export let practiceHref;
	export let completed;
	export let started;
</script>

<div class="container">
	{#if completed}
		<Button style="primary" href={practiceHref}>
			<Translate key="course_page.button_practice">연습하기</Translate>
		</Button>
	{:else if started}
		<Button style="primary" href={practiceHref}>
			<Translate key="course_page.button_continue">이어서 학습</Translate>
		</Button>
	{:else}
		<Button style="primary" href={practiceHref}>
			<Translate key="course_page.button_learn">학습하기</Translate>
		</Button>
	{/if}
</div>

<style>
	.container {
		display: flex;
		justify-content: center;
	}
</style>
