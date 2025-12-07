#ifndef C_API_H
#define C_API_H

#ifdef _WIN32
#  define RM_EXPORT __declspec(dllexport)
#else
#  define RM_EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef void* RM_Manipulator;
// СБОРКА
RM_EXPORT RM_Manipulator rm_create_manipulator();
RM_EXPORT void rm_destroy_manipulator(RM_Manipulator manip);

// Добавляет MovableLink.
// Параметры:
// - manip: дескриптор манипулятора
// - id: уникальный идентификатор звена
// - prev_id: идентификатор предыдущего звена в цепи (0, если нет)
// - r: длина звена
// - pitch/yaw/roll: ориентация звена относительно предыдущего
// Возврат: 1 — успех, 0 — ошибка/исключение.
RM_EXPORT int rm_add_link(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll);

RM_EXPORT int rm_add_gripper(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll, double open_angle);

RM_EXPORT int rm_add_camera(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll, double fov);



// УПРАВЛЕНИЕ
// Устанавливает ориентацию звена по id.
// Параметры: id звена и новые углы (pitch/yaw/roll).
RM_EXPORT int rm_set_direction(RM_Manipulator manip, int id, double pitch, double yaw, double roll);

// Открывает захват на заданный угол.
// Параметры: id захвата, угол открытия.
RM_EXPORT int rm_open_gripper(RM_Manipulator manip, int id, double angle);

// Закрывает захват.
// Параметры: id захвата.
RM_EXPORT int rm_close_gripper(RM_Manipulator manip, int id);

// Делает снимок камерой по id.
RM_EXPORT int rm_take_photo(RM_Manipulator manip, int id);


//ЗАПРОСЫ
// Вычисляет позицию звена.
// Параметры:
// - id: идентификатор звена
// - out_x/out_y/out_z: указатели на double, куда будет записана позиция
RM_EXPORT int rm_calculate_position(RM_Manipulator manip, int id, double* out_x, double* out_y, double* out_z);
// Печатает структуру манипулятора в stdout (консоль).
// Параметры: manip — дескриптор манипулятора.
RM_EXPORT void rm_print_structure(RM_Manipulator manip);

#ifdef __cplusplus
}
#endif

#endif // C_API_H

