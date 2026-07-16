// Lightweight gamification state, persisted in localStorage.
// No accounts/backend needed — works on static hosting (GitHub Pages).
import { writable } from 'svelte/store';

const KEY = 'chaoshanlingo-progress-v1';

export type Progress = {
	xp: number;
	streak: number;
	lastActiveDay: string; // YYYY-MM-DD
	completedSkills: Record<string, number>; // skillId -> times completed
};

const empty: Progress = { xp: 0, streak: 0, lastActiveDay: '', completedSkills: {} };

function load(): Progress {
	if (typeof localStorage === 'undefined') return { ...empty };
	try {
		return { ...empty, ...JSON.parse(localStorage.getItem(KEY) || '{}') };
	} catch {
		return { ...empty };
	}
}

export const progress = writable<Progress>(load());

progress.subscribe((value) => {
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem(KEY, JSON.stringify(value));
	}
});

function today(): string {
	return new Date().toISOString().slice(0, 10);
}

function yesterday(): string {
	const d = new Date();
	d.setDate(d.getDate() - 1);
	return d.toISOString().slice(0, 10);
}

/** Call when a lesson is completed. Returns XP earned. */
export function completeLesson(skillId: string, correct: number): number {
	const earned = 10 + Math.min(correct, 20); // 10 base + 1 per correct answer (cap 20)
	progress.update((p) => {
		const t = today();
		let streak = p.streak;
		if (p.lastActiveDay === t) {
			// same day, streak unchanged
		} else if (p.lastActiveDay === yesterday()) {
			streak += 1;
		} else {
			streak = 1;
		}
		return {
			...p,
			xp: p.xp + earned,
			streak,
			lastActiveDay: t,
			completedSkills: {
				...p.completedSkills,
				[skillId]: (p.completedSkills[skillId] || 0) + 1
			}
		};
	});
	return earned;
}

/** Streak shown in UI: 0 if the chain is already broken. */
export function displayStreak(p: Progress): number {
	if (p.lastActiveDay === today() || p.lastActiveDay === yesterday()) return p.streak;
	return 0;
}
