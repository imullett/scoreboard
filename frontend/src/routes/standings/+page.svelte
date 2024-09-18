<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { getCurrentWeek, round2, type RankingSort } from '$lib';
	import type { PageData } from './$types';

	let filterForm: HTMLFormElement;
	let currentWeek = getCurrentWeek(new Date());
	let banner = `standings after ${currentWeek - 1} weeks`;

	let { data } = $props<{ data: PageData }>();

	let filter: RankingSort = $state(($page.url.searchParams.get('filter') as RankingSort) ?? 'wins');
	let scores = $derived(
		data.scores.map((score) => ({ ...score, totalPoints: round2(score.totalPoints) }))
	);

	function onFilterChange() {
		filterForm.requestSubmit();
	}
</script>

<div class="m-auto h-full w-full space-y-2 pt-1 lg:w-3/4">
	<h6 class="h6 text-center text-secondary-300">{banner}</h6>
	<form
		method="POST"
		use:enhance
		bind:this={filterForm}
		class="flex flex-row justify-start gap-4 rounded-lg bg-surface-900 px-4 py-4"
	>
		<label for="filter" class="label w-fit text-nowrap">Rank By</label>
		<select name="filter" bind:value={filter} id="filter" class="select" onchange={onFilterChange}>
			<option value="ppr">Total PPR</option>
			<option value="wins">League Wins</option>
		</select>
	</form>
	<div class="table-wrap h-[80%]">
		<table class="table">
			<thead class="sticky top-0">
				<tr class="text-secondary bg-secondary-700 text-white">
					<th>Name</th>
					<th>Total PPR</th>
					<th>League Points</th>
				</tr>
			</thead>
			<tbody class="w-full overflow-y-scroll hover:[&>tr]:preset-tonal-primary">
				{#each scores as score}
					<tr>
						<td>{score.teamName}</td>
						<td>{score.totalPoints}</td>
						<td>{score.wins}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
