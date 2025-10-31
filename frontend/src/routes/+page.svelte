<script lang="ts">
  import { onMount } from 'svelte';
  import { getPersons, type Person } from '$lib/api';
  import { goto } from '$app/navigation';

  let persons: Person[] = [];
  let loading = true;
  let error: string | null = null;

  onMount(async () => {
    try {
      persons = await getPersons();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Falha ao carregar pessoas';
    } finally {
      loading = false;
    }
  });
</script>

<div class="container">
  <h1>pessoas</h1>

  {#if loading}
    <p>carregando...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if persons.length === 0}
    <p>Ainda não há pessoas cadastradas.</p>
  {:else}
    <div class="people-grid-wrapper">
      <div class="people-grid">
        {#each persons as person (person.id)}
          <div class="person-card" on:click={() => goto(`/person/${person.id}`)} role="button" tabindex="0">
            <div class="pfp-container">
              {#if person.pfp_image}
                <img src={person.pfp_image} alt={person.name} />
              {:else}
                <div class="pfp-placeholder">
                  <span>{person.name.charAt(0).toUpperCase()}</span>
                </div>
              {/if}
            </div>
            <p class="name">{person.name}</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.5rem 3rem;
  }

  h1 {
    margin-bottom: 2.5rem;
    margin-top: 0.5rem;
    font-size: 2.5rem;
  }

  .error {
    color: red;
  }

  .people-grid-wrapper {
    width: 100%;
  }

  .people-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem 1rem; /* row-gap column-gap */
    justify-content: center;
  }

  .person-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
    width: 200px;
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }

  .person-card:hover {
    transform: translateY(-3px);
  }

  .pfp-container {
    width: 150px;
    height: 150px;
    border-radius: 8px;
    overflow: hidden;
    background: #e0e0e0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pfp-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .pfp-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #bdbdbd;
    font-size: 3rem;
    font-weight: bold;
    color: white;
  }

  .name {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 500;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 180px;
  }

  @media (max-width: 768px) {
    .people-grid {
      justify-content: space-between;
    }
    
    .container {
      padding: 1rem;
      margin: 0 0.5rem;
    }

    h1 {
      font-size: 1.75rem;
      margin-bottom: 1.5rem;
      text-align: center;
    }

    .person-card {
      width: calc(50% - 0.5rem);
      max-width: 150px;
    }

    .pfp-container {
      width: 120px;
      height: 120px;
    }

    .pfp-placeholder {
      font-size: 2.5rem;
    }

    .name {
      font-size: 0.95rem;
      max-width: 130px;
    }
  }
</style>
