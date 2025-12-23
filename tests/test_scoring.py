"""
test_scoring.py
"""
import pytest
from datetime import datetime, timedelta
from scoring import calculate_importance_score, calculate_recency_score, calculate_final_score

def test_importance_score():
    assert calculate_importance_score("이것은 평범한 대화입니다.") == 3
    assert calculate_importance_score("나는 너에게 고백할 것이 있어.") >= 5  # 고백(+2), 나(+1), 너(+1)
    assert calculate_importance_score("정말 화가 난다!") >= 4 # 화남(+1)

def test_recency_score():
    now = datetime.now()
    yesterday = now - timedelta(hours=24)
    score = calculate_recency_score(yesterday, now, decay_factor=0.99)
    assert 0.0 < score < 1.0
    assert calculate_recency_score(now, now) == 1.0

def test_final_score():
    score = calculate_final_score(similarity=0.9, recency=0.5, importance=10) # imp norm = 1.0
    # 0.9 + 0.5 + 1.0 = 2.4
    assert score == 2.4
