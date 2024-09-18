import { getCurrentWeek, matchupWeeks, type MatchupWeek } from '$lib';
import { fail, redirect, type ActionFailure, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from '../$types';

type ChangeWeekMode = 'increment' | 'decrement';

export interface Team {
	gameId: number;
	manager: string;
	profilePicture: string;
	projectedPoints: number;
	teamId: number;
	teamName: string;
	totalPoints: number;
	weekNumber: number;
	yahooId: string;
}

export interface DivisionalMatchup {
	team1: Team;
	team2: Team;
	team3: Team;
}

export interface WeeklyMatchup {
	median: {
		current: number;
		projected: number;
	};
	results: Array<DivisionalMatchup>;
	week: number;
}

export const load: PageServerLoad = async () => {
	const current_week = getCurrentWeek(new Date());
	return redirect(303, `/week/${current_week}`);
};

function convertToMatchupWeek(
	week: number | string
): MatchupWeek | ActionFailure<{ week: boolean }> {
	if (matchupWeeks.includes(week as MatchupWeek)) {
		return week as MatchupWeek;
	} else {
		if (week === 'current') {
			return getCurrentWeek(new Date());
		} else {
			return fail(400, { week: false });
		}
	}
}

function changeWeek(mode: ChangeWeekMode, week: number): number {
	switch (mode) {
		case 'increment': {
			return week + 1;
		}
		case 'decrement':
			return week - 1;
	}
}

function isValidMatchupWeek(week: number): boolean {
	return matchupWeeks.includes(week as MatchupWeek);
}

function handleWeekChange(week: MatchupWeek, mode: ChangeWeekMode) {
	const newWeek = changeWeek(mode, week);
	if (isValidMatchupWeek(newWeek)) {
		return redirect(303, `/week/${newWeek}`);
	} else {
		return fail(400, { week: false });
	}
}

export const actions: Actions = {
	increment: async ({ request }) => {
		const data = await request.formData();
		const weekString = data.get('selected_week') as string;
		const weekConverted = weekString === 'current' ? 'current' : Number(weekString);
		const week = convertToMatchupWeek(weekConverted) as MatchupWeek;
		return handleWeekChange(week, 'increment');
	},
	decrement: async ({ request }) => {
		const data = await request.formData();
		const weekString = data.get('selected_week') as string;
		const weekConverted = weekString === 'current' ? 'current' : Number(weekString);
		const week = convertToMatchupWeek(weekConverted) as MatchupWeek;
		return handleWeekChange(week, 'decrement');
	}
};
