
from app.bot_handlers import get_converted_remain, get_converted_sum, identify_type_of_spend


def test_identify_type_of_spend():
    
    title = "Экстренные расходы"
    type_of_spend = identify_type_of_spend(title)
    
    assert type_of_spend["title"] == "Экстренные расходы"
    
    title = "Экстренные расходы"
    type_of_spend = identify_type_of_spend(title)
    
    assert type_of_spend["title"] == "Экстренные расходы"

def test_get_converted_sum():
    
    sum = 1.00
    
    converted_sum = get_converted_sum(sum)
    
    assert converted_sum > 20

# dont test them in one test session

def test_get_converted_remain():
    
    sum = 35.0
    
    converted_remain = get_converted_remain(sum)
    
    assert converted_remain < 2