<script lang="ts">
	import '../app.css';

	import { Nav } from '@skeletonlabs/skeleton-svelte';
	import { Trophy, Calendar } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	$: selected_menuitem = 'week';
</script>

<div
	class="card m-auto grid h-svh max-w-[95%] grid-rows-[auto_1fr_auto] pb-5 border-surface-100-900 lg:max-w-[80%]"
>
	<header>
		<h1 class="h1 text-center">Memes Bowl 2024</h1>
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
