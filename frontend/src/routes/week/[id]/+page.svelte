<script lang="ts">
	import { Accordion, Avatar } from '@skeletonlabs/skeleton-svelte';
	import type { PageData } from './$types';
	import type { DivisionalMatchup } from '../+page.server';
	import { round2 } from '$lib';
	import type { GradedTeam, GradedWeeklyMatchup } from './proxy+page.server';

	const grades = ['A', 'B', 'C', 'D', 'E', 'F'];

	function capitalize(s: string) {
		return s.charAt(0).toUpperCase() + s.slice(1);
	}

	function getMatchupTitle(matchup: DivisionalMatchup): string {
		return (
			Object.entries(matchup)
				// eslint-disable-next-line @typescript-eslint/no-unused-vars
				.map(([key, value]) => capitalize(value.manager))
				.join(', ')
		);
	}

	function getGroupTotalProjected(matchup: DivisionalMatchup): string {
		const groupProjection = Object.entries(matchup).reduce(
			// eslint-disable-next-line @typescript-eslint/no-unused-vars
			(acc, [key, value]) => acc + (value.projectedPoints ?? 0),
			0
		);
		return round2(groupProjection);
	}

	function getGroupTotalPoints(matchup: DivisionalMatchup): string {
		const groupTotal = Object.entries(matchup).reduce(
			// eslint-disable-next-line @typescript-eslint/no-unused-vars
			(acc, [key, value]) => acc + (value.totalPoints ?? 0),
			0
		);
		return round2(groupTotal);
	}

	function getRelativeGroupRanking(matchup: GradedWeeklyMatchup, teamId: number): string | null {
		const flattened = Object.values(matchup);
		const sortedGroup = flattened.sort((a, b) => b.totalPoints - a.totalPoints);
		const teamRank = sortedGroup.findIndex((a) => a.teamId === teamId);
		switch (teamRank) {
			case 0:
				return '🥇' + ' ' + beatTheMedian(sortedGroup[teamRank]);
			case 1:
				return '🥈' + ' ' + beatTheMedian(sortedGroup[teamRank]);
			case 2:
				return '🤡' + ' ' + beatTheMedian(sortedGroup[teamRank]);
			default:
				return null;
		}
	}

	export let data: PageData;

	$: isCompletedWeek = data.matchups.median.current > 0;
	$: groupRankings = rankMatchup(data.matchups.results);

	function rankMatchup(dm: GradedWeeklyMatchup[]): number[] {
		const totals: [number, number][] = dm.map((m, i) => {
			// eslint-disable-next-line @typescript-eslint/no-unused-vars
			return [Object.entries(m).reduce((acc, [key, value]) => value.totalPoints + acc, 0), i];
		});
		totals.sort((a, b) => b[0] - a[0]);
		const rankings = new Array(totals.length);
		totals.forEach((item, rank) => {
			rankings[item[1]] = rank + 1;
		});
		return rankings;
	}

	function beatTheMedian(t: GradedTeam): '✅' | '💩' {
		return t.totalPoints > data.matchups.median.current ? '✅' : '💩';
	}
</script>

{#snippet projected(n: number)}
	<span class="badge text-xs preset-tonal-tertiary"><strong>P{round2(n)}</strong></span>
{/snippet}

{#snippet lettergrade(g: string)}
	{#if g.includes('A')}
		<span class="badge text-xs preset-filled-warning-500"><strong>{g}</strong></span>
	{:else}
		<span class="badge text-xs preset-filled-tertiary-500"><strong>{g}</strong></span>
	{/if}
{/snippet}

<div class="mt-2 h-[78%] space-y-2 overflow-auto">
	<div class="card sticky top-0 z-10 p-2 preset-filled-surface-100-900">
		<div class="space-y-2">
			<div class="flex gap-2">
				<div class="badge max-w-20 preset-tonal-tertiary">
					{round2(data.matchups.median.projected)}
				</div>
				<div>Projected Median</div>
			</div>
			{#if isCompletedWeek}
				<div class="flex gap-2">
					<div class="badge max-w-20 preset-filled">
						{round2(data.matchups.median.current)}
					</div>
					<div>Actual Median</div>
				</div>
			{/if}
		</div>
	</div>
	{#each data.matchups.results as matchup, i}
		<Accordion collapsible class="overflow-y-scroll">
			<Accordion.Item value={grades[i]}>
				{#snippet lead()}
					<p>{grades[i]}</p>
				{/snippet}
				{#snippet control()}
					<p>
						{#if groupRankings[i] === 1 && isCompletedWeek}
							<span>💰</span>
						{/if}
						{getMatchupTitle(matchup)}
						{#if isCompletedWeek}
							({getGroupTotalPoints(matchup)})
						{:else}
							({getGroupTotalProjected(matchup)})
						{/if}
					</p>
				{/snippet}
				{#snippet panel()}
					<div
						class="grid grid-cols-1 grid-rows-3 gap-y-2 overflow-hidden lg:grid-cols-3 lg:grid-rows-1 lg:gap-x-2"
					>
						<!-- eslint-disable-next-line @typescript-eslint/no-unused-vars -->
						{#each Object.entries(matchup) as [_, value]}
							<div class="card space-y-1 p-2 preset-filled-surface-100-900">
								<header class="flex w-full justify-between gap-1">
									<Avatar classes="shrink-0" src={value.profilePicture} name={value.manager} />
									<div>
										{@render projected(value.projectedPoints)}
										{@render lettergrade(value.grade as string)}
									</div>
								</header>

								<article>
									<p class="text-xs">
										{#if isCompletedWeek}
											<span>{getRelativeGroupRanking(matchup, value.teamId)}</span>
										{/if}
										{value.teamName}
									</p>
								</article>

								<footer>
									<div class="flex justify-between text-xs">
										<span class="badge text-lg preset-filled">{round2(value.totalPoints)}</span>
									</div>
								</footer>
							</div>
						{/each}
					</div>
				{/snippet}
			</Accordion.Item>
			{#if i < data.matchups.results.length - 1}
				<hr class="hr" />
			{/if}
		</Accordion>
	{/each}
</div>
