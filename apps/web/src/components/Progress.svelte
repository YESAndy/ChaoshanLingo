<script>
  export let value = 0.0
  export let max = 1.0
</script>

<progress {value} {max}>
  {value * 100}%
</progress>

<style>
  progress {
    appearance: none;
    display: block;
    width: 100%;
    height: 16px;
    border-radius: 8px;
    overflow: hidden;
    border: none;
    background-color: #e5e5e5;
    padding: 0;
  }

  progress::-webkit-progress-bar {
    background-color: #e5e5e5;
  }

  progress::-webkit-progress-value {
    background-color: var(--color-primary, #58cc02);
    border-radius: 8px;
    transition: width 0.3s ease;
  }

  progress::-moz-progress-bar {
    background-color: var(--color-primary, #58cc02);
    border-radius: 8px;
  }
</style>
