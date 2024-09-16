import { error } from "@sveltejs/kit"
import type { PageServerLoad } from './$types';

export interface Scoreboard {
	teamName: string;
	totalPoints: number;
	wins: string | number;
}

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const response = await fetch('http://localhost:5172/scoreboard');

		if (!response.ok) {
			throw new Error(`HTTP error. Status: ${response.status}`);
		}

		const data: Scoreboard[] = await response.json();

		return {
			scores: data
		};
	} catch (e) {
		error(403, "Failed to get data from the scoreboard.")
	}
};
