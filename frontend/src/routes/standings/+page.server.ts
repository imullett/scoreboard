import type { PageServerLoad } from './$types';
import { fetchFromAPI, standingsFilters, type RankingSort } from "$lib";
import { fail, redirect, type Actions } from '@sveltejs/kit';

export interface Scoreboard {
	teamName: string;
	totalPoints: number;
	wins: string;
}

function sortTeams(teams: Scoreboard[], filter: RankingSort): Scoreboard[] {
	const [key, tiebreak]: (keyof Scoreboard)[] = filter === "wins" ? ["wins", "totalPoints"] : ["totalPoints", "wins"];
	const sorted = teams.sort((a, b) => {
		const valueA = a[key];
		const valueB = b[key];

		if (valueA === valueB) {
			return Number(b[tiebreak]) - Number(a[tiebreak])
		}

		return Number(valueB) - Number(valueA)
	});

	if (filter === "wins") {
		sorted[0].teamName = "🥇 " + sorted[0].teamName;
		sorted[1].teamName = "🥈 " + sorted[1].teamName;
		sorted[2].teamName = "🥉 " + sorted[2].teamName;
	}

	return sorted;
}
export const load: PageServerLoad = async ({ url }) => {
	const data = await fetchFromAPI<Scoreboard[]>("scoreboard");
	const filter = url.searchParams.get("filter") as RankingSort;
	if (standingsFilters.includes(filter)) {
		return { scores: sortTeams(data, filter) }
	}
	return { scores: sortTeams(data, "wins") };
};

export const actions = {
	default: async ({ request, url }) => {
		const data = await request.formData();
		const filter = data.get('filter') as RankingSort;

		if (!filter) {
			return fail(400, { filter, missing: true })
		}
		url.searchParams.set("filter", filter)
		redirect(303, url)
	}
} satisfies Actions;
