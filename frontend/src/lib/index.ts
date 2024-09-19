export const standingsGroups = ['overall', 'divisional'] as const;
export const standingsFilters = ['ppr', 'wins'] as const;
export const matchupWeeks = [
	1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
] as const;
export const grades = [
	'A+',
	'A',
	'A-',
	'B+',
	'B',
	'B-',
	'C+',
	'C',
	'C-',
	'D+',
	'D',
	'D-',
	'F+',
	'F',
	'F-'
] as const;

export type RankingGroup = (typeof standingsGroups)[number];
export type RankingGrade = (typeof grades)[number];
export type RankingSort = (typeof standingsFilters)[number];
export type MatchupWeek = (typeof matchupWeeks)[number];

export function getCurrentWeek(date: Date): MatchupWeek {
	const seasonStart = new Date('2024-09-03T01:00:00Z');
	const timeDifference = date.getTime() - seasonStart.getTime();
	const daysDifference = timeDifference / (1000 * 60 * 60 * 24);
	const weekNumber = Math.floor(daysDifference / 7) + 1;
	return Math.min(Math.max(1, weekNumber), 18) as MatchupWeek;
}

export function round2(num: number): string {
	const rounded = Number(Math.round(Number(num + 'e' + 2)) + 'e-' + 2);
	return rounded.toFixed(2);
}
