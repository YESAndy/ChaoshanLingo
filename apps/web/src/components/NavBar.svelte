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
    <a class="brand" href={homepageLink}>
      <img class="brand__mark" src="{base}/images/chaoshan-mascot.svg" alt="" />
      Chaoshan
    </a>
  </div>

  <div class="navbar__right">
    <a class="nav-btn" href="{base}/pengim">📖 발음표</a>
  </div>
</nav>

<style>
  .navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
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
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #fff;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    text-decoration: none;
    padding: 0.2rem 0.6rem;
  }

  .brand__mark {
    width: 38px;
    height: 38px;
  }

  .nav-btn {
    display: inline-block;
    background: rgba(255, 255, 255, 0.18);
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-bottom-width: 4px;
    border-radius: 12px;
    color: #fff;
    font-weight: 800;
    text-decoration: none;
    padding: 0.35rem 0.9rem;
    transition: all 0.1s;
  }

  .nav-btn:active {
    transform: translateY(2px);
    border-bottom-width: 2px;
  }
</style>
