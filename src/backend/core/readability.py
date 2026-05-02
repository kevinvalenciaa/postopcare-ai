"""POC-006: Readability scoring for patient handouts.

Pure-Python Flesch-Kincaid Grade Level + Flesch Reading Ease.
Target: 6th-8th grade for patient-friendly content.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_VOWELS = "aeiouy"
_WORD = re.compile(r"\b[a-zA-Z]+\b")
_SENTENCE = re.compile(r"[.!?]+")


def count_syllables(word: str) -> int:
    """Estimate syllables in a single English word. Heuristic, ~95% accurate.

    Algorithm: count vowel groups, subtract trailing 'e', floor at 1.
    """
    word = word.lower()
    if not word:
        return 0
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in _VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


@dataclass
class ReadabilityScore:
    grade_level: float
    ease: float
    word_count: int
    sentence_count: int
    syllable_count: int
    complex_words: list[str]
    suggestions: list[str]

    def to_dict(self) -> dict:
        return {
            "grade_level": round(self.grade_level, 2),
            "ease": round(self.ease, 2),
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "syllable_count": self.syllable_count,
            "complex_words": self.complex_words[:20],
            "suggestions": self.suggestions,
        }


def score(text: str) -> ReadabilityScore:
    """Compute readability metrics for a passage of text.

    Returns ReadabilityScore with Flesch-Kincaid grade, Flesch ease,
    list of 3+ syllable words, and human-readable suggestions.
    """
    words = _WORD.findall(text)
    sentences = [s for s in _SENTENCE.split(text) if s.strip()]
    word_count = len(words)
    sentence_count = max(1, len(sentences))
    syllables_per_word = [count_syllables(w) for w in words]
    syllable_count = sum(syllables_per_word)

    if word_count == 0:
        return ReadabilityScore(0.0, 0.0, 0, 0, 0, [], ["Empty text"])

    asl = word_count / sentence_count
    asw = syllable_count / word_count

    grade = 0.39 * asl + 11.8 * asw - 15.59
    ease = 206.835 - 1.015 * asl - 84.6 * asw

    complex_words = sorted({w for w, s in zip(words, syllables_per_word) if s >= 3})

    suggestions: list[str] = []
    if grade > 8:
        suggestions.append(
            f"Reading level is grade {grade:.1f}; target is 6-8. Shorten sentences and replace long words."
        )
    if asl > 20:
        suggestions.append(f"Average sentence length is {asl:.1f} words — break up long sentences.")
    if len(complex_words) > 0:
        ratio = len(complex_words) / max(1, len(set(words)))
        if ratio > 0.15:
            suggestions.append(
                f"{len(complex_words)} unique words have 3+ syllables ({ratio:.0%} of vocabulary). "
                "Consider plainer alternatives."
            )

    return ReadabilityScore(
        grade_level=grade,
        ease=ease,
        word_count=word_count,
        sentence_count=sentence_count,
        syllable_count=syllable_count,
        complex_words=complex_words,
        suggestions=suggestions,
    )


def passes(text: str, target_grade: float = 8.0) -> bool:
    """True if the text is at or below the target grade level."""
    return score(text).grade_level <= target_grade


if __name__ == "__main__":
    sample = (
        "After your knee replacement, you may feel some pain. "
        "Take your medicine on time. Use ice to help with swelling. "
        "Walk a little each day. Call your doctor if you see redness or fever."
    )
    s = score(sample)
    for k, v in s.to_dict().items():
        print(f"  {k}: {v}")
    print("passes 8th-grade:", passes(sample))
