import pytest
from crawler.transformers.common import clean_price, clean_rating

@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("$1,299", 1299),
        (299, 299),            
        (None, None),          
        ("", None),           
        ("價格待定", None),
    ]
)
def test_clean_price(input_value, expected_output):
    assert clean_price(input_value) == expected_output


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("4.8/5", 4.8),
        ("4.5", 4.5),
        (None, None),
        ("", None),
        ("尚無評價", None)
    ]
)
def test_clean_rating(input_value, expected_output):
    assert clean_rating(input_value) == expected_output
