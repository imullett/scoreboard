<script lang="ts">
	import type { PageData } from '../$types';
	import type { Scoreboard } from './proxy+page.server';

	let { data } = $props<{ data: PageData }>();

	let filter = $state('ppr');
	let scores = $state<Scoreboard[]>(data.scores);

	$effect(() => {
		scores = scores.sort((a, b) => {
			switch (filter) {
				case 'wins': {
					const primary_delta = Number(b.wins) - Number(a.wins);
					if (primary_delta !== 0) {
						return primary_delta;
					} else {
						return b.totalPoints - a.totalPoints;
					}
				}
				default:
					return b.totalPoints - a.totalPoints;
			}
		});
	});
</script>

<div class="m-auto h-full w-3/4 space-y-2 pt-4">
	<div class="flex flex-row justify-start gap-4 rounded-lg bg-surface-900 px-4 py-4">
		<label for="filter" class="label w-fit text-nowrap">Rank By</label>
		<select bind:value={filter} id="filter" class="select">
			<option value="ppr">Total PPR</option>
			<option value="wins">League Wins</option>
		</select>
	</div>
	<div class="table-wrap h-[80%]">
		<table class="table">
			<thead class="sticky top-0">
				<tr class="text-secondary bg-secondary-800 text-white">
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
