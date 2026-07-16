<script lang="ts">
  import { page } from '$app/state';
  import { base } from '$app/paths';

  export let hasAuth = false;
  export let repositoryURL: string | null = null;

  const courseName = page.params?.courseName || '';
  const homepageLink = `${base}/course/${courseName}`;
</script>

<nav class="navbar" aria-label="main navigation">
  <div class="navbar__left">
    <a class="brand" href={homepageLink}>Chaoshan</a>
  </div>
</nav>

<style>
  .navbar {
    display: flex;
    align-items: center;
    width: 100%;
    min-height: var(--deprecated-navbar-height);
    padding: var(--deprecated-navbar-padding-vertical) var(--deprecated-navbar-padding-horizontal);
    background: var(--color-primary, #58cc02);
    border-bottom: 4px solid var(--color-primary-shadow, #58a700);
  }

  .navbar__left {
    display: flex;
    align-items: center;
    height: 100%;
  }

  .brand {
    color: #fff;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    text-decoration: none;
    padding: 0.2rem 0.6rem;
  }
</style>
