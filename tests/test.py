
def calculate_post_scores(ids, likes, dislikes):
    scores = []
    for i in range(len(ids)):
        score = likes[i] * 3 - dislikes[i] * 1
        scores.append((ids[i], score))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    sorted_ids = [x[0] for x in sorted_scores]
    sorted_scores_list = [x[1] for x in sorted_scores]
    
    return sorted_ids, sorted_scores_list


def test_calculate_post_scores():

    ids = [2, 3, 32, 12, 5]
    likes = [2, 3, 6, 3, 1]
    dislikes = [1, 2, 0, 2, 3]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([32, 3, 12, 2, 5], [18, 7, 7, 5, 0]), "Тест 1 не пройден"

    ids = [1, 2, 3, 4, 5]
    likes = [2, 2, 2, 2, 2]
    dislikes = [0, 0, 0, 0, 0]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([1, 2, 3, 4, 5], [6, 6, 6, 6, 6]), "Тест 2 не пройден"

    ids = [1, 2, 3]
    likes = [5, 5, 5]
    dislikes = [5, 5, 5]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([1, 2, 3], [10, 10, 10]), "Тест 3 не пройден"

    ids = [1, 2, 3]
    likes = [0, 0, 0]
    dislikes = [2, 4, 1]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([3, 1, 2], [-1, -2, -4]), "Тест 4 не пройден"

    ids = [1, 2]
    likes = [-1, -2]
    dislikes = [0, 0]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([1, 2], [-3, -6]), "Тест 5 не пройден"

    ids = []
    likes = []
    dislikes = []
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([], []), "Тест 6 не пройден"

    ids = [1]
    likes = [0]
    dislikes = [0]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([1], [0]), "Тест 7 не пройден"

    ids = [1]
    likes = [10]
    dislikes = [5]
    result = calculate_post_scores(ids, likes, dislikes)
    assert result == ([1], [25]), "Тест 8 не пройден"

    print("Все тесты пройдены!")


test_calculate_post_scores()
