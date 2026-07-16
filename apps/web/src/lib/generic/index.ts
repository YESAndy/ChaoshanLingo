import shuffle from "lodash.shuffle"
import uniqBy from "lodash.uniqby"

export const prepareChallenge = ({
  currentChallenge,
  alternativeChallenges,
  typeToSelect,
  hasFakeOption = null,
}) => {
  const numberOfCards = hasFakeOption ? 4 : 3
  const correctOption = {
    ...currentChallenge,
    correct: true,
  }

  // Candidates: prefer challenges of the same type, but fall back to any other
  // challenge that has a displayable target-language form. This guarantees
  // multiple options even in skills with few phrases.
  const withForm = (alternativeChallenges || []).filter(
    (c) => typeof c.formInTargetLanguage === "string" && c.formInTargetLanguage
  )
  const sameType = withForm.filter(({ type }) => type === typeToSelect)
  const otherTypes = withForm.filter(({ type }) => type !== typeToSelect)

  const incorrectOptions = uniqBy(
    [...shuffle(sameType), ...shuffle(otherTypes)],
    "formInTargetLanguage"
  )
    .filter(
      ({ formInTargetLanguage }) =>
        formInTargetLanguage !== correctOption.formInTargetLanguage
    )
    .map((challenge) => ({
      ...challenge,
      correct: false,
    }))

  const incorrectOptionsSample = incorrectOptions.slice(0, numberOfCards - 1)

  const incorrectOptionsWithFake =
    hasFakeOption && incorrectOptionsSample.length > 0
      ? [
          {
            ...incorrectOptionsSample[0],
            fake: true,
          },
          ...incorrectOptionsSample.slice(1),
        ]
      : incorrectOptionsSample

  return shuffle([correctOption, ...incorrectOptionsWithFake])
}
