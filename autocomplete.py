from typing import Dict, List, Tuple

from rapidfuzz import fuzz, process


class Autocomplete:
    def __init__(self, data: Dict[str, str]):
        self.data = data

    def autocomplete(
        self,
        sentence: str = None,
        num_of_sugg: int = 2,
        match_score: float = 90.0,
        n_grams: int = 2,
        with_score: bool = False,
    ) -> Dict[str, List[Tuple[str, float, float]]]:
        """
        Provide word suggestions based on user input.

        Args:
        sentence (str): The words typed by the user, which will be used to suggest the next word/words.
        word_dict (dict): A dictionary of custom entities to be autocompleted from.
        num_of_sugg (int): The number of words to be suggested per key from word_dict.
        match_score (float): The matching score between the typed text and the suggested word.
            A higher score indicates a better matching between strings, and vice versa.
        n_grams (int, optional): The number of words from the user's input sentence to be considered
            for suggesting new words. Defaults to 2, meaning the last two words will be considered.

        Returns:
             A Dictionary of suggested words based on user input and the specified criteria.
    """

        words = sentence.split(" ")
        last_n_words = " ".join(words[-n_grams:])
        suggestions_with_score = dict()

        for key in self.data.keys():
            sugg = []
            extract = process.extract(last_n_words, self.data[key], limit=num_of_sugg, scorer=fuzz.partial_ratio)

            for i in range(len(extract)):
                if extract[i][1] > match_score:
                    sugg.append(extract[i])

            if len(sugg) > 0:
                suggestions_with_score[key] = sugg

        if with_score:
            return suggestions_with_score
        else:
            suggestions_without_score = {
                key: [item[0] for item in suggestions_with_score[key]] for key in suggestions_with_score
            }

        return suggestions_without_score

    def autocomplete_with_key(
        self,
        key: str,
        sentence: str = None,
        num_of_sugg: int = 2,
        match_score: float = 90.0,
        n_grams: int = 2,
        with_score: bool = False,
    ) -> Dict[str, List[Tuple[str, float, float]]]:
        """
        Autocomplete will be give hints for next words, depending upon the custom entities.

        Args:
        key : key from json from which suggestions to be shown from
        sentence (str): The words typed by the user, which will be used to suggest the next word/words.
        word_dict (dict): A dictionary of custom entities to be autocompleted from.
        num_of_sugg (int): The number of words to be suggested per key from word_dict.
        match_score (float): The matching score between the typed text and the suggested word.
            A higher score indicates a better matching between strings, and vice versa.
        n_grams (int, optional): The number of words from the user's input sentence to be considered
            for suggesting new words. Defaults to 2, meaning the last two words will be considered.

        Returns:
             A Dictionary of suggested words based on user input and the specified criteria.

        """
        words = sentence.split(" ")
        last_n_words = " ".join(words[-n_grams:])
        suggestions_with_score = dict()

        sugg = []
        extract = process.extract(last_n_words, self.data[key], limit=num_of_sugg, scorer=fuzz.partial_ratio)

        for i in range(len(extract)):
            if extract[i][1] > match_score:
                sugg.append(extract[i])

        if len(sugg) > 0:
            suggestions_with_score[key] = sugg

        if with_score:
            return suggestions_with_score
        else:
            suggestions_without_score = {
                key: [item[0] for item in suggestions_with_score[key]] for key in suggestions_with_score
            }

        return suggestions_without_score
