import type { PageServerLoad } from './$types';
import { grades, matchupWeeks, type MatchupWeek, type RankingGrade } from '$lib';
import { error } from '@sveltejs/kit';
import { type Team, type WeeklyMatchup } from '../+page.server';
import { fetchFromAPI } from '$lib/server';

export const load: PageServerLoad = async ({ params }) => {
	const week = Number(params.id) as MatchupWeek;
	if (matchupWeeks.includes(week)) {
		const data = await fetchFromAPI<WeeklyMatchup>(`matchups/${week}`);
		return {
			matchups: {
				...data,
				results: assignGrades(data.results)
			}
		};
	} else {
		error(403, 'Not a valid matchup week');
	}
};

export type GradedTeam = Team & { grade?: RankingGrade };
export type GradedWeeklyMatchup = {
	team1: GradedTeam;
	team2: GradedTeam;
	team3: GradedTeam;
};

function assignGrades(divisions: WeeklyMatchup['results']): GradedWeeklyMatchup[] {
	const flattenedTeams = divisions.flatMap((obj) => [obj.team1, obj.team2, obj.team3]);
	const sortedTeams = flattenedTeams.sort((a, b) => b.projectedPoints - a.projectedPoints);
	const gradedTeams: GradedTeam[] = sortedTeams.map((st, i) => ({
		...st,
		grade: grades[i]
	}));

	const gradedDivisions = [...divisions];
	return gradedDivisions.map((d) => ({
		team1: gradedTeams.find((gt) => gt.teamId === d.team1.teamId),
		team2: gradedTeams.find((gt) => gt.teamId === d.team2.teamId),
		team3: gradedTeams.find((gt) => gt.teamId === d.team3.teamId)
	})) as GradedWeeklyMatchup[];
}
