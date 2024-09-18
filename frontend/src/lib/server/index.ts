import { NODE_ENV } from '$env/static/private';
import { error } from '@sveltejs/kit';

export async function fetchFromAPI<T>(endpoint: string): Promise<T> {
	const baseUrl = NODE_ENV === 'production' ? 'http://flask:5000' : 'http://localhost:5000';
	console.info('Fetching from: ', endpoint);
	try {
		const response = await fetch(`${baseUrl}/${endpoint}`);
		if (!response.ok) {
			throw new Error(`HTTP error. Status: ${response.status}`);
		}
		const data: T = await response.json();
		return data;
	} catch (e) {
		console.error('API request failed:', e);
		error(403, `Failed to get data from ${endpoint}.`);
	}
}
