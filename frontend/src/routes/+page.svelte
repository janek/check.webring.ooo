<script>
	import { onMount } from 'svelte';
	import domainsCSV from '../domains.csv?raw';

	let domains = [];
	let displayedDomains = [];
	let searchTerm = '';
	let isSearching = false;
	let isLoading = true;
	let searchInput;

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
	function getRandomDomains(domainsArray, count = 50) {
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
		displayedDomains = filtered.slice(0, 100); // Limit to 100 results for performance
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

	// Format TTL for display
	function formatTTL(seconds) {
		const hours = Math.floor(seconds / 3600);
		const days = Math.floor(hours / 24);
		
		if (days > 0) {
			return `${days}d ${hours % 24}h`;
		} else if (hours > 0) {
			return `${hours}h`;
		} else {
			return `${seconds}s`;
		}
	}
</script>

<svelte:head>
	<title>Domain Registry ॱ Check</title>
	<meta name="description" content="Search .ooo domain availability" />
</svelte:head>

<div class="container mx-auto px-3 py-6 max-w-6xl sm:px-4 sm:py-8">
	<!-- Header -->
	<div class="mb-6 text-center sm:mb-8">
		<h1 class="text-2xl font-bold text-gray-900 mb-2 sm:text-3xl md:text-4xl">
			Domain Registry ॱ Check
		</h1>
		<p class="text-gray-600 text-sm md:text-base">
			{#if isLoading}
				Loading domains...
			{:else if isSearching}
				Search results for "{searchTerm}"
			{:else}
				Showing 50 random .ooo domains
			{/if}
		</p>
	</div>

	<!-- Search -->
	<div class="mb-4 sm:mb-6">
		<div class="relative max-w-md mx-auto">
			<input
				bind:this={searchInput}
				type="text"
				placeholder="Search domains..."
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

	{#if !isLoading}
		<!-- Results count -->
		<div class="mb-3 text-center text-sm text-gray-500 sm:mb-4">
			{displayedDomains.length.toLocaleString()} domain{displayedDomains.length !== 1 ? 's' : ''}
			{#if searchTerm.trim()}
				found
			{:else}
				shown
			{/if}
		</div>

		<!-- Table -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-4">
								Domain
							</th>
							<th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sm:px-4">
								Status
							</th>
							<th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell sm:px-4">
								TTL
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
								<td class="px-3 py-3 text-sm text-gray-500 hidden sm:table-cell font-mono sm:px-4">
									{formatTTL(parseInt(domain.ttl_seconds))}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			{#if displayedDomains.length === 0}
				<div class="text-center py-12">
					<div class="text-gray-400 text-lg mb-2">☰ No domains found</div>
					<p class="text-gray-500 text-sm">Try adjusting your search terms</p>
				</div>
			{/if}
		</div>

		<!-- Footer info -->
		<div class="mt-6 text-center text-xs text-gray-400 sm:mt-8">
			<p>{domains.length.toLocaleString()} total domains in registry</p>
			<p class="mt-1">Data updated: 2025-06-12</p>
		</div>
	{:else}
		<!-- Loading state -->
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
			<div class="text-gray-400 text-lg mb-2">⧗ Loading domains...</div>
			<p class="text-gray-500 text-sm">This may take a moment</p>
		</div>
	{/if}
</div>
