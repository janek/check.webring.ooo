<script>
  let searchQuery = '';
  
  // Extended list of 30 names with their status and webring membership
  const names = [
    { name: 'alice', status: 'available', webring_member: false },
    { name: 'bob', status: 'available', webring_member: false },
    { name: 'charlie', status: 'taken', webring_member: false },
    { name: 'diana', status: 'available', webring_member: false },
    { name: 'emma', status: 'available', webring_member: true },
    { name: 'frank', status: 'available', webring_member: false },
    { name: 'grace', status: 'taken', webring_member: false },
    { name: 'henry', status: 'available', webring_member: false },
    { name: 'iris', status: 'available', webring_member: true },
    { name: 'jack', status: 'taken', webring_member: false },
    { name: 'kate', status: 'available', webring_member: false },
    { name: 'liam', status: 'available', webring_member: false },
    { name: 'maya', status: 'taken', webring_member: true },
    { name: 'noah', status: 'available', webring_member: false },
    { name: 'olivia', status: 'available', webring_member: false },
    { name: 'peter', status: 'taken', webring_member: false },
    { name: 'quinn', status: 'available', webring_member: false },
    { name: 'ruby', status: 'available', webring_member: true },
    { name: 'sam', status: 'available', webring_member: false },
    { name: 'tina', status: 'taken', webring_member: false },
    { name: 'ulrich', status: 'available', webring_member: false },
    { name: 'vera', status: 'available', webring_member: true },
    { name: 'walter', status: 'taken', webring_member: false },
    { name: 'xander', status: 'available', webring_member: false },
    { name: 'yuki', status: 'available', webring_member: false },
    { name: 'zoe', status: 'taken', webring_member: true },
    { name: 'alex', status: 'available', webring_member: false },
    { name: 'blake', status: 'available', webring_member: false },
    { name: 'casey', status: 'taken', webring_member: false },
    { name: 'drew', status: 'available', webring_member: true }
  ];

  // Filter names based on search query
  $: filteredNames = names.filter(name => 
    name.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  function handleSearch() {
    // For now, just focus on filtering the existing list
    // Later this could be extended to check external domains
    console.log('Searching for:', searchQuery);
  }

  function handleKeyPress(event) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }
</script>

<main>
  <div class="container">
    <h1>check.webring.ooo</h1>
    <p>Check if your firstname.ooo domain is available ⊡</p>
    
    <div class="search-container">
      <input 
        type="text" 
        class="search-input"
        placeholder="Search or check a name..."
        bind:value={searchQuery}
        on:keypress={handleKeyPress}
      />
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Domain</th>
            <th>Status</th>
            <th>Webring Member</th>
          </tr>
        </thead>
        <tbody>
          {#each filteredNames as name}
            <tr class={name.webring_member ? 'webring-member' : ''}>
              <td>{name.name}</td>
              <td>{name.name}.ooo</td>
              <td class={name.status === 'available' ? 'status-available' : 'status-taken'}>
                {name.status}
              </td>
              <td>{name.webring_member ? '☉ Yes' : 'No'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      
      {#if filteredNames.length === 0}
        <p>No names found matching "{searchQuery}". Maybe check if it's available?</p>
      {/if}
    </div>

    <div style="margin-top: 2rem; font-size: 0.9em; color: #666;">
      <p>༺ part of the webring.ooo project ༻</p>
      <p>simple domain checking for .ooo names</p>
    </div>
  </div>
</main>