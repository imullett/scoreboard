export const matchupWeeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] as const;

export type MatchupWeek = typeof matchupWeeks[number];

export function getCurrentWeek(date: Date): MatchupWeek {
	const seasonStart = new Date('2024-09-03T01:00:00Z');
	const timeDifference = date.getTime() - seasonStart.getTime();
	const daysDifference = timeDifference / (1000 * 60 * 60 * 24);
	const weekNumber = Math.floor(daysDifference / 7) + 1;
	return Math.min(Math.max(1, weekNumber), 18) as MatchupWeek;
}

