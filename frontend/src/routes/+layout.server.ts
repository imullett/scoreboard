import { getCurrentWeek } from '$lib';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async () => {
	return {
		currentWeek: getCurrentWeek(new Date())
	};
};
