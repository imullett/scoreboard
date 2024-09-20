<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { getCurrentWeek, type RankingGroup, type RankingSort } from '$lib';
	import { round2 } from '$lib';
	import { Segment } from '@skeletonlabs/skeleton-svelte';
	import type { Scoreboard } from './+page.server';

	let filterForm: HTMLFormElement;
	let currentWeek = getCurrentWeek(new Date());
	let banner = `Week ${currentWeek - 1} Standings`;

	let { data } = $props();

	let selectedDivision: 1 | 2 | 3 = $state(1);
	let grouping: RankingGroup = $state(
		(($page.url.searchParams.get('grouping') as RankingGroup) || data.grouping) ?? 'overall'
	);
	let filter: RankingSort = $state(($page.url.searchParams.get('filter') as RankingSort) ?? 'wins');

	let scores: Scoreboard[] = $derived.by(() => {
		if (Array.isArray(data.scores[0])) {
			const divs = data.scores as Scoreboard[][];
			const di = divs.findIndex((d) => d[0].division === selectedDivision);
			return data.scores[di] as Scoreboard[];
		} else {
			return data.scores as Scoreboard[];
		}
	});

	function onFormChange() {
		filterForm.requestSubmit();
	}
</script>

{#snippet standings_table(scores: Scoreboard[])}
	<div class="table-wrap h-[80%] border-spacing-1">
		<table class="table table-fixed">
			<thead class="sticky top-0">
				<tr class="text-secondary bg-secondary-500 text-white">
					<th class="w-1/2">Name</th>
					<th class="w-1/4 !text-right">Total Points</th>
					<th class="w-1/4 !text-right">Wins</th>
				</tr>
			</thead>
			<tbody class="w-full overflow-y-scroll hover:[&>tr]:preset-tonal-primary">
				{#each scores as score}
					<tr>
						<td>{score.teamName}</td>
						<td>{round2(score.totalPoints)}</td>
						<td class="text-right">{score.wins}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/snippet}

<div class="m-auto h-full w-full space-y-2 pt-1 lg:w-3/4">
	<h6 class="h6 text-center text-secondary-300">{banner}</h6>
	<form
		method="POST"
		use:enhance
		onchange={onFormChange}
		bind:this={filterForm}
		class="m-auto flex w-fit flex-col items-center gap-2"
	>
		<div>
			<Segment name="grouping" bind:value={grouping}>
				<Segment.Item value="overall">Overall</Segment.Item>
				<Segment.Item value="divisional">Divisional</Segment.Item>
			</Segment>
		</div>
		<div>
			<Segment name="filter" bind:value={filter}>
				<Segment.Item value="ppr">Points</Segment.Item>
				<Segment.Item value="wins">Wins</Segment.Item>
			</Segment>
		</div>
	</form>
	{#if grouping === 'divisional'}
		<div class="flex w-full justify-center">
			<Segment name="division" bind:value={selectedDivision}>
				<Segment.Item value={1}>1</Segment.Item>
				<Segment.Item value={2}>2</Segment.Item>
				<Segment.Item value={3}>3</Segment.Item>
			</Segment>
		</div>
	{/if}
	{@render standings_table(scores)}
</div>
