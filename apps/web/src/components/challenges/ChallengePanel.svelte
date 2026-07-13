<script lang="ts">
	import Button from 'components/Button.svelte';
	import Panel from 'components/Panel.svelte';

	export let buttonText;
	export let buttonAction = null;
	export let correct = false;
	export let incorrect = false;
	export let typo = false;
	export let message;
	export let messageDetail = null;
	export let submit = null;
	export let skipAction = null;
	export let skipAllAction = null;
	export let skipAllVoice = null;

	let background: 'default' | 'success' | 'failure' | 'info' = (() => {
		if (correct) {
			return 'success';
		}
		if (incorrect) {
			return 'failure';
		}
		if (typo) {
			return 'info';
		}

		return 'default';
	})();
</script>

<Panel {background}>
	<div slot="left">
		{#if skipAction}
			<Button on:click={skipAction}>건너뛰기</Button>
		{/if}
		<Button on:click={skipAllAction}>취소</Button>
		{#if skipAllVoice}
			<Button on:click={skipAllVoice}>지금 들을 수 없어요</Button>
		{/if}
		{#if message}<b>{message}</b>{/if}
		{#if messageDetail}
			<p>{messageDetail}</p>
		{/if}
	</div>

	<div slot="right">
		{#if buttonAction}
			<Button style="primary" type="submit" on:click={buttonAction}>
				{buttonText}
			</Button>
		{/if}
		{#if submit}
			<Button style="primary" type="submit">제출</Button>
		{/if}
	</div>
</Panel>
