<script lang="ts">
	import '../app.css';

	import { getCurrentWeek, matchupWeeks, type MatchupWeek } from '$lib';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { Nav } from '@skeletonlabs/skeleton-svelte';
	import { Trophy } from 'lucide-svelte';

	type Route = 'week' | 'standings';

	let current_week: number = $state(getCurrentWeek(new Date()));
	let selected_menuitem: Route = $state('week');
	let selected_week: MatchupWeek | 'current' = $state(5);

	let weeks = $derived(['current', ...matchupWeeks.filter((week) => week !== current_week)]);

	$effect(() => {
		switch (selected_week) {
			case 'current':
				goto('/');
				break;
			default:
				goto(`/week/${selected_week}`);
				break;
		}
	});

	$effect(() => {
		selected_week = 'current';
		switch (selected_menuitem) {
			case 'week':
				goto('/');
				break;
			case 'standings':
				goto('/standings');
				break;
		}
	});
</script>

<div
	class="card m-auto grid h-svh max-w-[80%] grid-rows-[auto_1fr_auto] pb-5 border-surface-100-900"
>
	<header>
		<h1 class="h1 text-center">Memes Bowl 2024</h1>
		<h6 class="h6 text-center text-secondary-300">Current Week: {current_week}</h6>
	</header>

	<main class="h-full overflow-hidden">
		<!-- svelte-ignore slot_element_deprecated -->
		<slot />
	</main>

	<footer class="px-10">
		<Nav.Bar bind:value={selected_menuitem} classes="rounded-lg">
			<Nav.Tile id="standings" label="Standings" onclick={() => (selected_menuitem = 'standings')}>
				<Trophy />
			</Nav.Tile>
			<Nav.Tile id="week" label="Matchups" onclick={() => (selected_menuitem = 'week')}>
				<select bind:value={selected_week} class="select p-1 text-center text-sm">
					{#each weeks as week}
						{#if week === 'current'}
							<option value="current" selected={selected_week === week}>Current Week</option>
						{:else}
							<option value={week} selected={selected_week === week}>Week {week}</option>
						{/if}
					{/each}
				</select>
			</Nav.Tile>
		</Nav.Bar>
	</footer>
</div>
