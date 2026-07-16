<script lang="ts">
	export let background: 'default' | 'success' | 'failure' | 'info' = 'default';
</script>

<div class="panel" data-background={background}>
	<div class="content">
		<slot name="left" />
		<slot name="right" />
	</div>
</div>

<style type="text/scss">
	.panel {
		position: fixed;
		display: block;
		left: 0;
		bottom: 0;
		right: 0;
		padding: var(--deprecated-spacing-medium);

		border-top: 2px solid #e5e5e5;
		padding-top: 1rem;
		padding-bottom: 1rem;

		&[data-background='default'] {
			background: var(--deprecated-panel-background);
		}

		&[data-background='success'] {
			background: #d7ffb8;
			color: #58a700;
			border-top-color: #d7ffb8;
			font-weight: 700;
		}

		&[data-background='failure'] {
			background: #ffdfe0;
			color: #ea2b2b;
			border-top-color: #ffdfe0;
			font-weight: 700;
		}

		&[data-background='info'] {
			background: #fff5d8;
			color: #b8860b;
			border-top-color: #fff5d8;
			font-weight: 700;
		}

		.content {
			display: flex;
			max-width: 960px;
			margin: auto;
			align-items: center;
			gap: 0.5rem;

			:global([slot='left']) {
				flex-grow: 1;
			}

			:global([slot='right']) {
				flex-grow: 0;
			}
		}

		@media (max-width: 640px) {
			.content {
				flex-wrap: wrap;

				:global([slot='right']) {
					width: 100%;

					:global([ref='lluis-button']) {
						width: 100%;
					}
				}
			}
		}
	}
</style>
