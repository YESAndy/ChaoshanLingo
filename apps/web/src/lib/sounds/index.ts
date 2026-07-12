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

export default sound;
