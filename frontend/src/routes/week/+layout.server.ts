import { getCurrentWeek } from "$lib"
import type { LayoutServerLoad } from "./$types"

export const load: LayoutServerLoad = () => {
	return { currentWeek: getCurrentWeek(new Date()) }
}
