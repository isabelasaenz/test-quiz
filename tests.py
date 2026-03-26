import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_choice_text_empty():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')

def test_choice_text_too_long():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_choice_ids_sequential():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    assert question.choices[0].id == 1
    assert question.choices[1].id == 2

def test_remove_choice_valid_id():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(1)
    assert len(question.choices) == 1
    assert question.choices[0].id == 2

def test_remove_choice_invalid_id():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choice_single():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.set_correct_choices([2])
    assert question.choices[1].is_correct == True

def test_set_correct_choices_multiple():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.set_correct_choices([1, 3])
    assert question.choices[0].is_correct == True
    assert question.choices[2].is_correct == True

def test_set_correct_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.set_correct_choices([999])

def test_max_selections_limit():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', True)
    question.add_choice('b', False)
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2])

@pytest.fixture
def sample_question():
    question = Question(title='Sample Question', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)
    return question

def test_fixture_choices_count(sample_question):
    assert len(sample_question.choices) == 3

def test_fixture_correct_choices(sample_question):
    assert sample_question.choices[0].is_correct == True
    assert sample_question.choices[1].is_correct == False
    assert sample_question.choices[2].is_correct == True

def test_fixture_correct_selected(sample_question):
    selected = [sample_question.choices[0].id, sample_question.choices[1].id]
    result = sample_question.correct_selected_choices(selected)
    assert len(result) == 1
    assert result[0] == sample_question.choices[0].id