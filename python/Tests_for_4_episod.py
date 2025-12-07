"""
Тесты для проверки функций приложения Robot Manipulator UI
"""
import unittest
import ctypes
import os
import sys

# Добавляем путь к модулю ui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui import rm, RM_Manipulator
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что RobotManipulator.dll собран и находится в правильной директории")
    sys.exit(1)


class TestRobotManipulator(unittest.TestCase):
    """Тесты для функций манипулятора"""
    
    def setUp(self):
        """Создание манипулятора перед каждым тестом"""
        self.manip = rm.rm_create_manipulator()
        self.assertIsNotNone(self.manip, "Не удалось создать манипулятор")
    
    def tearDown(self):
        """Уничтожение манипулятора после каждого теста"""
        if self.manip:
            rm.rm_destroy_manipulator(self.manip)
    
    def test_create_manipulator(self):
        """Тест создания манипулятора"""
        manip = rm.rm_create_manipulator()
        self.assertIsNotNone(manip, "Манипулятор должен быть создан")
        rm.rm_destroy_manipulator(manip)
    
    def test_add_movable_link(self):
        """Тест добавления подвижного звена"""
        # Добавляем первое звено (ID=1, prev=0)
        result = rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        self.assertEqual(result, 1, "Не удалось добавить первое звено")
        
        # Добавляем второе звено (ID=2, prev=1)
        result = rm.rm_add_link(self.manip, 2, 1, 1.0, 0.5, 0.3, 0.0)
        self.assertEqual(result, 1, "Не удалось добавить второе звено")
    
    def test_add_gripper(self):
        """Тест добавления захвата"""
        # Сначала добавляем базовое звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Добавляем захват
        result = rm.rm_add_gripper(self.manip, 2, 1, 0.5, 0.0, 0.0, 0.0, 0.2)
        self.assertEqual(result, 1, "Не удалось добавить захват")
    
    def test_add_camera(self):
        """Тест добавления камеры"""
        # Сначала добавляем базовое звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Добавляем камеру
        result = rm.rm_add_camera(self.manip, 2, 1, 0.3, 0.0, 0.0, 0.0, 1.57)
        self.assertEqual(result, 1, "Не удалось добавить камеру")
    
    def test_set_direction(self):
        """Тест установки ориентации звена"""
        # Добавляем звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Устанавливаем ориентацию
        result = rm.rm_set_direction(self.manip, 1, 0.5, 0.3, 0.1)
        self.assertEqual(result, 1, "Не удалось установить ориентацию")
    
    def test_open_close_gripper(self):
        """Тест открытия и закрытия захвата"""
        # Добавляем звено и захват
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        rm.rm_add_gripper(self.manip, 2, 1, 0.5, 0.0, 0.0, 0.0, 0.2)
        
        # Открываем захват
        result = rm.rm_open_gripper(self.manip, 2, 0.5)
        self.assertEqual(result, 1, "Не удалось открыть захват")
        
        # Закрываем захват
        result = rm.rm_close_gripper(self.manip, 2)
        self.assertEqual(result, 1, "Не удалось закрыть захват")
    
    def test_take_photo(self):
        """Тест съёмки камерой"""
        # Добавляем звено и камеру
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        rm.rm_add_camera(self.manip, 2, 1, 0.3, 0.0, 0.0, 0.0, 1.57)
        
        # Делаем снимок
        result = rm.rm_take_photo(self.manip, 2)
        self.assertEqual(result, 1, "Не удалось сделать снимок")
    
    def test_calculate_position(self):
        """Тест вычисления позиции звена"""
        # Добавляем несколько звеньев
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        rm.rm_add_link(self.manip, 2, 1, 1.0, 0.5, 0.3, 0.0)
        
        # Вычисляем позицию
        x = ctypes.c_double()
        y = ctypes.c_double()
        z = ctypes.c_double()
        result = rm.rm_calculate_position(self.manip, 2, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        
        self.assertEqual(result, 1, "Не удалось вычислить позицию")
        self.assertIsInstance(x.value, float, "X должна быть числом")
        self.assertIsInstance(y.value, float, "Y должна быть числом")
        self.assertIsInstance(z.value, float, "Z должна быть числом")
    
    def test_print_structure(self):
        """Тест вывода структуры манипулятора"""
        # Добавляем несколько звеньев
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        rm.rm_add_gripper(self.manip, 2, 1, 0.5, 0.0, 0.0, 0.0, 0.2)
        rm.rm_add_camera(self.manip, 3, 2, 0.3, 0.0, 0.0, 0.0, 1.57)
        
        # Вывод структуры не должен вызывать ошибок
        try:
            rm.rm_print_structure(self.manip)
        except Exception as e:
            self.fail(f"Вывод структуры вызвал ошибку: {e}")
    
    def test_duplicate_id(self):
        """Тест добавления звена с дублирующимся ID"""
        # Добавляем первое звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Пытаемся добавить звено с тем же ID (должно вернуть 0)
        result = rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        self.assertEqual(result, 0, "Должна быть ошибка при дублировании ID")
    
    def test_invalid_link_id(self):
        """Тест работы с несуществующим ID звена"""
        # Пытаемся установить ориентацию несуществующего звена
        result = rm.rm_set_direction(self.manip, 999, 0.5, 0.3, 0.1)
        self.assertEqual(result, 0, "Должна быть ошибка для несуществующего звена")
    
    def test_chain_of_links(self):
        """Тест создания цепочки из нескольких звеньев"""
        # Создаём цепочку: базовое звено -> захват -> камера
        result1 = rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        result2 = rm.rm_add_gripper(self.manip, 2, 1, 0.5, 0.0, 0.0, 0.0, 0.2)
        result3 = rm.rm_add_camera(self.manip, 3, 2, 0.3, 0.0, 0.0, 0.0, 1.57)
        
        self.assertEqual(result1, 1, "Не удалось добавить базовое звено")
        self.assertEqual(result2, 1, "Не удалось добавить захват")
        self.assertEqual(result3, 1, "Не удалось добавить камеру")
        
        # Проверяем позицию последнего звена
        x = ctypes.c_double()
        y = ctypes.c_double()
        z = ctypes.c_double()
        result = rm.rm_calculate_position(self.manip, 3, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        self.assertEqual(result, 1, "Не удалось вычислить позицию последнего звена")
    
    def test_multiple_links_chain(self):
        """Тест создания длинной цепочки звеньев"""
        # Создаём цепочку из 5 звеньев
        for i in range(1, 6):
            prev_id = 0 if i == 1 else (i - 1)
            result = rm.rm_add_link(self.manip, i, prev_id, 1.0, 0.1 * i, 0.05 * i, 0.0)
            self.assertEqual(result, 1, f"Не удалось добавить звено с ID={i}")
        
        # Проверяем позицию последнего звена
        x = ctypes.c_double()
        y = ctypes.c_double()
        z = ctypes.c_double()
        result = rm.rm_calculate_position(self.manip, 5, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        self.assertEqual(result, 1, "Не удалось вычислить позицию последнего звена")
    
    def test_gripper_on_non_gripper(self):
        """Тест попытки управления захватом на обычном звене"""
        # Добавляем обычное звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Пытаемся открыть захват на обычном звене (должно вернуть 0)
        result = rm.rm_open_gripper(self.manip, 1, 0.5)
        self.assertEqual(result, 0, "Должна быть ошибка при попытке открыть захват на обычном звене")
    
    def test_camera_on_non_camera(self):
        """Тест попытки сделать снимок с обычного звена"""
        # Добавляем обычное звено
        rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        
        # Пытаемся сделать снимок с обычного звена (должно вернуть 0)
        result = rm.rm_take_photo(self.manip, 1)
        self.assertEqual(result, 0, "Должна быть ошибка при попытке сделать снимок с обычного звена")
    
    def test_calculate_position_invalid_id(self):
        """Тест вычисления позиции несуществующего звена"""
        # Пытаемся вычислить позицию несуществующего звена
        x = ctypes.c_double()
        y = ctypes.c_double()
        z = ctypes.c_double()
        result = rm.rm_calculate_position(self.manip, 999, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        self.assertEqual(result, 0, "Должна быть ошибка при вычислении позиции несуществующего звена")
    
    def test_complex_manipulator(self):
        """Тест создания сложного манипулятора с разными типами звеньев"""
        # Создаём сложную структуру: базовое звено -> захват -> звено -> камера
        result1 = rm.rm_add_link(self.manip, 1, 0, 1.0, 0.0, 0.0, 0.0)
        result2 = rm.rm_add_gripper(self.manip, 2, 1, 0.5, 0.2, 0.1, 0.0, 0.3)
        result3 = rm.rm_add_link(self.manip, 3, 2, 0.8, 0.3, 0.2, 0.0)
        result4 = rm.rm_add_camera(self.manip, 4, 3, 0.2, 0.1, 0.0, 0.0, 1.2)
        
        self.assertEqual(result1, 1, "Не удалось добавить базовое звено")
        self.assertEqual(result2, 1, "Не удалось добавить захват")
        self.assertEqual(result3, 1, "Не удалось добавить промежуточное звено")
        self.assertEqual(result4, 1, "Не удалось добавить камеру")
        
        # Проверяем все функции
        rm.rm_set_direction(self.manip, 1, 0.5, 0.3, 0.0)
        rm.rm_open_gripper(self.manip, 2, 0.6)
        rm.rm_take_photo(self.manip, 4)
        
        # Вычисляем позицию камеры
        x = ctypes.c_double()
        y = ctypes.c_double()
        z = ctypes.c_double()
        result = rm.rm_calculate_position(self.manip, 4, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
        self.assertEqual(result, 1, "Не удалось вычислить позицию камеры")


if __name__ == "__main__":
    print("=" * 60)
    print("Запуск тестов для Robot Manipulator")
    print("=" * 60)
    print()
    unittest.main(verbosity=2)

