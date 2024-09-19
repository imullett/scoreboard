import type { PageServerLoad } from './$types';
import { standingsFilters, type RankingGrade, type RankingGroup, type RankingSort } from '$lib';
import { fail, redirect, type Actions } from '@sveltejs/kit';
import { fetchFromAPI } from '$lib/server';

export interface Scoreboard {
	teamName: string;
	totalPoints: number;
	wins: string;
	division: number;
}

function sortTeams(teams: Scoreboard[], filter: RankingSort, showRank = false): Scoreboard[] {
	const [key, tiebreak]: (keyof Scoreboard)[] =
		filter === 'wins' ? ['wins', 'totalPoints'] : ['totalPoints', 'wins'];
	const sorted = teams.sort((a, b) => {
		const valueA = a[key];
		const valueB = b[key];

		if (valueA === valueB) {
			return Number(b[tiebreak]) - Number(a[tiebreak]);
		}

		return Number(valueB) - Number(valueA);
	});

	if (filter === 'wins' && showRank) {
		sorted[0].teamName = '🥇 ' + sorted[0].teamName;
		sorted[1].teamName = '🥈 ' + sorted[1].teamName;
		sorted[2].teamName = '🥉 ' + sorted[2].teamName;
	}

	return sorted;
}
export const load: PageServerLoad = async ({ url }) => {
	const data = await fetchFromAPI<Scoreboard[]>('scoreboard');

	const filter = url.searchParams.get('filter') as RankingSort;
	const grouping = url.searchParams.get('grouping') as RankingGroup;

	let output: Scoreboard[] | Scoreboard[][] = [...data];

	if (grouping === "divisional") {
		output = splitIntoDivisions(data)
		if (standingsFilters.includes(filter)) {
			return { scores: output.map(div => sortTeams(div, filter)), grouping }
		}
		else {
			return { scores: output.map(div => sortTeams(div, 'wins')), grouping }
		}
	} else {
		if (standingsFilters.includes(filter)) {
			return { scores: sortTeams(data, filter, true), grouping: "overall" };
		}
		return { scores: sortTeams(data, 'wins', true), grouping: "overall" };
	}
};

export const actions = {
	default: async ({ request, url }) => {
		const data = await request.formData();
		const filter = data.get('filter') as RankingSort;
		const grouping = data.get('grouping') as RankingGroup;

		if (!filter || !grouping) {
			return fail(400, { filter, grouping, missing: true });
		}

		url.searchParams.set('filter', filter);
		url.searchParams.set('grouping', grouping);

		redirect(303, url);
	}
} satisfies Actions;

function splitIntoDivisions(s: Scoreboard[]): Scoreboard[][] {
	return s.reduce((acc, t) => { acc[t.division - 1].push(t); return acc; }, [[], [], []] as Scoreboard[][])
}
