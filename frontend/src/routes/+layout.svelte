<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { goto } from '$app/navigation';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header>
    <h1 on:click={() => goto('/')} role="button" tabindex="0">fofoquinha</h1>
</header>

{@render children()}

<style>
    header {
        text-align: center;
		position: sticky;
		top: 0;
		z-index: 100;
		padding: 1rem 0;
	}

    header h1 {
		margin: 0;
		font-size: 1.5rem;
		display: inline-block;
		background: linear-gradient(90deg,
			#ff9ec4,
			#ffc477,
			#fff06a,
			#7ee2b8,
			#8ecaff,
			#c39bff,
			#ff9ec4
		);
		background-size: 250% 250%;
		animation: rainbow 12s linear infinite;
		padding: 0.5rem 1.5rem;
		border-radius: 8px;
		color: #000;
		font-weight: 700;
		text-shadow: none;
        cursor: pointer;
		transition: transform 0.2s ease;
	}

	@keyframes rainbow {
		0% { background-position: 0% 50%; }
		50% { background-position: 100% 50%; }
		100% { background-position: 0% 50%; }
	}

    header h1:hover {
		transform: translateY(-3px);
	}

    header h1:focus {
		outline: 2px solid #007bff;
		outline-offset: 2px;
	}
</style>
