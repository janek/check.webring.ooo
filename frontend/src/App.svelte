<script>
	import { onMount } from 'svelte';
	import domainsCSV from './domains.csv?raw';

	let domains = [];
	let displayedDomains = [];
	let searchTerm = '';
	let isSearching = false;
	let isLoading = true;
	let searchInput;
	let limit = 10; // Configurable limit for both random and search results

	// Parse CSV data
	function parseCSV(csv) {
		const lines = csv.trim().split('\n');
		const headers = lines[0].split(',');
		
		const data = [];
		for (let i = 1; i < lines.length; i++) {
			const values = lines[i].split(',');
			if (values.length === headers.length) {
				const row = {};
				headers.forEach((header, index) => {
					row[header] = values[index];
				});
				data.push(row);
			}
		}
		return data;
	}

	// Get random sample of domains
	function getRandomDomains(domainsArray, count = limit) {
		const shuffled = [...domainsArray].sort(() => 0.5 - Math.random());
		return shuffled.slice(0, count);
	}

	// Search domains
	function searchDomains() {
		if (!searchTerm.trim()) {
			displayedDomains = getRandomDomains(domains);
			isSearching = false;
			return;
		}

		isSearching = true;
		const filtered = domains.filter(domain => 
			domain.domain.toLowerCase().includes(searchTerm.toLowerCase()) ||
			domain.status.toLowerCase().includes(searchTerm.toLowerCase())
		);
		displayedDomains = filtered.slice(0, limit); // Limit results for performance
	}

	// Handle search input
	function handleSearch(event) {
		searchTerm = event.target.value;
		searchDomains();
	}

	// Clear search
	function clearSearch() {
		searchTerm = '';
		displayedDomains = getRandomDomains(domains);
		isSearching = false;
		searchInput?.focus();
	}

	// Initialize on mount
	onMount(() => {
		domains = parseCSV(domainsCSV);
		displayedDomains = getRandomDomains(domains);
		isLoading = false;
	});
</script>

<svelte:head>
	<title>check.webring.ooo</title>
	<meta name="description" content="Search .ooo domain availability" />
</svelte:head>

<main class="min-h-screen bg-gray-50">
	<div class="container mx-auto px-3 py-6 max-w-md sm:px-4 sm:py-8">
		<!-- Header -->
		<div class="mb-6 text-center sm:mb-8">
			<h1 class="text-2xl font-bold text-gray-900 mb-2 sm:text-3xl md:text-4xl">
				check.webring.ooo
			</h1>
			<p class="text-gray-600 text-sm md:text-base">
				Check if your name.ooo is available and join the <a href="https://webring.ooo" class="text-blue-500 hover:text-blue-600">webring</a>!
			</p>
		</div>

		{#if !isLoading}
			<!-- Results count -->
			<div class="mb-3 text-center text-sm text-gray-500 sm:mb-4">
				{#if searchTerm.trim()}
					{#if displayedDomains.length === limit}
						showing first {limit} results for "{searchTerm}"
					{:else}
						found {displayedDomains.length.toLocaleString()} result{displayedDomains.length !== 1 ? 's' : ''} for "{searchTerm}"
					{/if}
				{:else}
					showing {limit} random domains
				{/if}
			</div>

			<!-- Search and Table Container -->
			<div class="mx-auto">
				<div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
					<!-- Search -->
					<div class="p-4 border-b border-gray-200">
						<div class="relative">
							<input
								bind:this={searchInput}
								type="text"
								placeholder="Search..."
								bind:value={searchTerm}
								on:input={handleSearch}
								class="w-full px-4 py-3 pr-20 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
							/>
							<div class="absolute inset-y-0 right-0 flex items-center">
								{#if searchTerm}
									<button
										on:click={clearSearch}
										class="p-2 mr-1 text-gray-400 hover:text-gray-600 transition-colors duration-200"
										aria-label="Clear search"
									>
										<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
										</svg>
									</button>
								{/if}
								<div class="pr-3 flex items-center pointer-events-none">
									<svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
									</svg>
								</div>
							</div>
						</div>
					</div>

					<!-- Table -->
					<div class="overflow-x-auto">
						<table class="w-full divide-y divide-gray-200">
							<thead class="bg-gray-50">
								<tr>
									<th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-4">
										Domain
									</th>
									<th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-4 w-24">
										Status
									</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								{#each displayedDomains as domain, index}
									<tr class="hover:bg-gray-50 transition-colors duration-150">
										<td class="px-3 py-3 text-sm text-gray-900 font-mono break-all sm:px-4 sm:break-normal">
											{domain.domain}
										</td>
										<td class="px-3 py-3 text-sm sm:px-4">
											<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {domain.status === 'free' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'} sm:px-2.5">
												{domain.status}
											</span>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>

					{#if displayedDomains.length === 0}
						<div class="text-center py-12">
							<div class="text-gray-400 text-lg mb-2">Nothing found in registry</div>
							<p class="text-gray-500 text-sm">Search-for-any-domain available soon!</p>
						</div>
					{/if}
				</div>
			</div>

			<!-- Footer info -->
			<div class="mt-6 text-center text-xs text-gray-400 sm:mt-8">
				<p>{domains.length.toLocaleString()} total domains in registry</p>
				<p class="mt-1">Last updated: 2025-06-12</p>
			</div>
		{:else}
			<!-- Loading state -->
			<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
				<div class="text-gray-400 text-lg mb-2">Loading...</div>
			</div>
		{/if}
	</div>
</main>

<style>
	@import './app.css';
</style> 