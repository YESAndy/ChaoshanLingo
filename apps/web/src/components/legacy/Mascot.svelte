<script lang="ts">
  import { base } from '$app/paths';

  export let shadow = true
  export let glow = false
  let imageURL =
    shadow === true
        ? `${base}/images/mascot-jetpack.svg`
        : `${base}/images/mascot-jetpack-noshadow.svg`
</script>

<img data-test="mascot-jetpack" src="{imageURL}" alt="" class:glow />

<style type="text/scss">
  .glow {
    filter: drop-shadow(0 0 2em #ffffff1c);
  }
</style>
