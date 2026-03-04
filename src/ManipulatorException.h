#ifndef MANIPULATOR_EXCEPTION_H
#define MANIPULATOR_EXCEPTION_H

#include <stdexcept>
#include <string>

// Специальный класс исключения для ошибок манипулятора
// Используется для передачи информации об ошибке из библиотеки в интерфейс
class ManipulatorException : public std::runtime_error {
public:
    explicit ManipulatorException(const std::string& message) 
        : std::runtime_error(message) {}
};

#endif // MANIPULATOR_EXCEPTION_H

