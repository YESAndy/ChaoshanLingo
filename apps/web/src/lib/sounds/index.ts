import { Howl, Howler } from 'howler';
import { base } from '$app/paths';

const sound = {
	correct: new Howl({
		src: [`${base}/sound/correct.mp3`]
	}),
	wrong: new Howl({
		src: [`${base}/sound/wrong.mp3`]
	}),
	fanfare: new Howl({
		src: [`${base}/sound/fanfare.mp3`]
	})
};

export const playAudio = (type, filename) => {
	new Howl({
		src: [`${base}/${type}/${filename}.mp3`]
	}).play();
};

/**
 * Play the recorded voice for a target-language text. Audio files are named
 * sha256("<language>|<text>") by the librelingo audio pipeline.
 */
export const playVoiceForText = async (text: string, languageName = 'teochew') => {
	if (typeof crypto === 'undefined' || !crypto.subtle) return;
	const data = new TextEncoder().encode(`${languageName.toLowerCase()}|${text}`);
	const digest = await crypto.subtle.digest('SHA-256', data);
	const hash = [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
	playAudio('voice', hash);
};

export default sound;
