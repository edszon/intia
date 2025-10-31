<script lang="ts">
  import { onMount } from 'svelte';
  import { getPersons, createPerson, updatePerson, deletePerson, type Person } from '$lib/api';

  let authenticated = false;
  let passwordInput = '';
  let persons: Person[] = [];
  let loading = true;
  let error: string | null = null;

  let newName = '';
  let newFile: File | null = null;
  let newFileInput: HTMLInputElement | null = null;

  function tryLogin() {
    if (passwordInput === 'edson123') {
      authenticated = true;
      localStorage.setItem('admin_ok', '1');
      load();
    } else {
      error = 'senha inválida';
    }
  }

  async function load() {
    loading = true;
    error = null;
    try {
      persons = await getPersons();
    } catch (e) {
      error = e instanceof Error ? e.message : 'falha ao carregar pessoas';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    authenticated = localStorage.getItem('admin_ok') === '1';
    if (authenticated) load();
  });

  async function createNew() {
    if (!newName.trim() || !newFile) return;
    try {
      const p = await createPerson(newName.trim(), newFile);
      persons = [...persons, p];
      newName = '';
      newFile = null;
      if (newFileInput) newFileInput.value = '';
    } catch (e) {
      error = e instanceof Error ? e.message : 'falha ao criar';
    }
  }

  async function updateExisting(p: Person, name?: string, file?: File | null) {
    try {
      const updated = await updatePerson(p.id, name, file ?? undefined);
      persons = persons.map(x => (x.id === p.id ? updated : x));
    } catch (e) {
      error = e instanceof Error ? e.message : 'falha ao atualizar';
    }
  }

  async function removePerson(p: Person) {
    if (!confirm(`remover ${p.name}?`)) return;
    try {
      await deletePerson(p.id);
      persons = persons.filter(x => x.id !== p.id);
    } catch (e) {
      error = e instanceof Error ? e.message : 'falha ao remover';
    }
  }
</script>

{#if !authenticated}
  <div class="login">
    <h1>admin</h1>
    {#if error}<p class="error">{error}</p>{/if}
    <input type="password" placeholder="senha" bind:value={passwordInput} on:keydown={(e) => e.key==='Enter' && tryLogin()} />
    <button on:click={tryLogin}>entrar</button>
  </div>
{:else}
  <div class="admin">
    <h1>crud de pessoas</h1>
    {#if loading}
      <p>carregando...</p>
    {:else}
      {#if error}<p class="error">{error}</p>{/if}

      <div class="create">
        <h2>criar</h2>
        <input placeholder="nome" bind:value={newName} />
        <input id="new-file" bind:this={newFileInput} type="file" accept="image/*" on:change={(e:any)=> newFile = e.currentTarget.files?.[0] ?? null} />
        <button on:click={createNew} disabled={!newName.trim() || !newFile}>criar</button>
      </div>

      <div class="list">
        <h2>pessoas</h2>
        {#each persons as p (p.id)}
          <div class="row">
            <div class="pfp">
              {#if p.pfp_image}
                <img src={p.pfp_image} alt={p.name} />
              {:else}
                <div class="placeholder">{p.name.charAt(0).toUpperCase()}</div>
              {/if}
            </div>
            <input class="name" value={p.name} on:change={(e:any)=>updateExisting(p, e.currentTarget.value, null)} />
            <input class="file" type="file" accept="image/*" on:change={(e:any)=>updateExisting(p, undefined, e.currentTarget.files?.[0])} />
            <button class="danger" on:click={()=>removePerson(p)}>remover</button>
          </div>
        {/each}
      </div>
    {/if}
  </div>
{/if}

<style>
  .login, .admin { max-width: 900px; margin: 0 auto; padding: 2rem 3rem; }
  h1 { margin: 0 0 1rem 0; }
  h2 { margin: 1.5rem 0 0.75rem 0; }
  .error { color: red; }

  .create, .list { background: #f5f5f5; padding: 1rem; border-radius: 8px; }
  .create input[type="text"], .create input[type="file"], .create button { margin-right: 0.5rem; }

  .row { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid #eee; }
  .row:last-child { border-bottom: none; }
  .pfp { width: 48px; height: 48px; border-radius: 6px; overflow: hidden; background: #e0e0e0; display: flex; align-items:center; justify-content:center; }
  .pfp img { width:100%; height:100%; object-fit: cover; }
  .placeholder { font-weight: 700; }
  .name { flex: 1; padding: 0.4rem 0.5rem; }
  .file { max-width: 240px; }
  .danger { background: #e53935; color: #fff; border: 0; padding: 0.5rem 0.75rem; border-radius: 6px; cursor: pointer; }
  .danger:hover { background: #c62828; }

  input, button { font-family: inherit; }
</style>


