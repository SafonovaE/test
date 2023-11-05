from api import PetFriends
from tests.settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Позитивный тест получения ключа авторизации"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email=valid_email, password='13579'):
    """Тестируем получение ключа авторизации с несуществующим паролем"""
    status, result = pf.get_api_key(email, password)
    assert status != 200


def test_create_pet_simple_success(name='Дениска', animal_type='Динозавр', age='2000130'):
    """Проверяем, что запрос создает питомца с заданными именем, типом и возрастом животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_create_pet_simple_no_name_unsuccess(name=None, animal_type='Динозавр', age='10000000000'):
    """Проверяем, что запрос может создаь питомца без имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status != 200


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем, что запрос всех питомцев не возвращает списка питомцев при введении неверного ключа авторизации"""
    status, result = pf.get_list_of_pets({'key': 'bad_key'}, filter)
    assert status != 200


def test_create_pet_success():
    """Создаем питомца"""
    pet_photo = 'images/kvokka.jpg'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet(auth_key, 'Дмитрий', 'Квокка', 13, pet_photo)
    assert status == 200
    assert result['name'] == 'Дмитрий'
    assert result['animal_type'] == 'Квокка'
    assert result['age'] == '13'
    assert 'pet_photo' in result


def test_create_pet_no_animal_type_unsuccess():
    """Нельзя создать питомца без типа питомца"""
    pet_photo = 'images/kvokka.jpg'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet(auth_key, 'Дмитрий', None, 13, pet_photo)
    assert status != 200


def test_create_pet_no_age_unsuccess():
    """Нельзя создать питомца без указания возраста питомца"""
    pet_photo = 'images/kvokka.jpg'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet(auth_key, 'Дмитрий', 'Квокка', None, pet_photo)
    assert status != 200


def test_delete_existing_pet_success():
    """Удаляем питомца. Для этого создаем нового питомцаб затем его удаляемб используя auth_key и pet_id"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, 'Дмитрий', 'Квокка', 13)
    status, result = pf.delete_pet(auth_key, result['id'])
    assert status == 200


def test_delete_existing_pet_with_bad_auth_key_unsuccess():
    """Нельзя удалить питомца с неверным auth_key"""
    status, result = pf.delete_pet({'key': 'bad_key'}, 'pet_id')
    assert status != 200


def test_update_pet_success(name='Дмитрий', animal_type='Квокка', age='15'):
    """Обновляем информацию о питомце."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    new_name = 'лже' + name
    new_animal_type = 'лже' + animal_type
    new_age = str(int(age) + 1)
    status, result = pf.update_pet(auth_key, result['id'], new_name, new_animal_type, new_age)
    assert status == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age


def test_update_none_existing_pet_unsuccess():
    """Нельзя обновить информацию о питомце, используя невалидный auth_key."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet(auth_key, 'bad_id', 'new_name', 'new_animal_type', '1')
    assert status != 200


def test_set_photo_success():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = 'images/TR.jpeg'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.create_pet_simple(auth_key, 'Дениска', 'Динозавр', 2000130)
    status, result = pf.set_photo(auth_key, result['id'], pet_photo)
    assert status == 200
    assert 'pet_photo' in result

def test_set_photo_bad_format_unsuccess():
    """Проверям, что нельзя создать питомца, если изображение не соответсвует ожидаемому формату.
    Использьуем файл txt для изображения питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = 'images/tinki-vinki.txt'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.create_pet_simple(auth_key, 'Дениска', 'Динозавр', 2000130)
    status, result = pf.set_photo(auth_key, result['id'], pet_photo)
    assert status != 200