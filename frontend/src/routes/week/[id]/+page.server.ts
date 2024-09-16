import type { PageServerLoad } from './$types';
import { matchupWeeks, type MatchupWeek } from "$lib"
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params }) => {
	if (matchupWeeks.includes(Number(params.id) as MatchupWeek)) {
		return {
			week: params.id
		}
	} else {
		error(403, "Not a valid matchup week")
	}
};
