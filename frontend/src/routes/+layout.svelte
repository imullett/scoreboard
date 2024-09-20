<script lang="ts">
	import '../app.css';

	import header from '$lib/images/header.gif';

	import { Nav } from '@skeletonlabs/skeleton-svelte';
	import { Trophy, Calendar, Flame} from 'lucide-svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	$: selected_menuitem = $page.url.pathname.split('/')[1]
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
			<Nav.Tile id="week" label="Matchups" active='bg-secondary-500' onclick={() => goto('/week')}>
				<Calendar />
			</Nav.Tile>
			<Nav.Tile id="standings" label="Standings" active='bg-secondary-700' onclick={() => goto('/standings')}>
				<Trophy />
			</Nav.Tile>
			<Nav.Tile id="luke" label="Luke" active='bg-secondary-700' onclick={() => goto('/luke')}>
				<Flame />
			</Nav.Tile>
		</Nav.Bar>
	</footer>
</div>
