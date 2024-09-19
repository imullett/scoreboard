<script lang="ts">
	import '../app.css';

	import header from '$lib/images/header.gif';

	import { Nav } from '@skeletonlabs/skeleton-svelte';
	import { Trophy, Calendar } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	$: selected_menuitem = 'week';
</script>

<div
	class="m-auto grid h-svh max-w-[95%] grid-rows-[auto_1fr_auto] pb-5 border-surface-100-900 lg:max-w-[80%]"
>
	<header class="bg-[url('$lib/images/football.gif')]">
		<div class="flex justify-center p-6">
			<img src={header} alt="memesbowl" />
		</div>
	</header>

	<main class="h-full overflow-hidden">
		<slot />
	</main>

	<footer class="px-8">
		<Nav.Bar bind:value={selected_menuitem} classes="rounded-lg">
			<Nav.Tile id="week" label="Matchups" onclick={() => goto('/week')}>
				<Calendar />
			</Nav.Tile>
			<Nav.Tile id="standings" label="Standings" onclick={() => goto('/standings')}>
				<Trophy />
			</Nav.Tile>
		</Nav.Bar>
	</footer>
</div>
