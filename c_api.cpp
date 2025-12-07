#include "c_api.h"
#include "Manipulator.h"
#include "MovableLink.h"
#include "Gripper.h"
#include "Camera.h"

#include <new>

extern "C" {

RM_Manipulator rm_create_manipulator() {
    // Создаёт и возвращает новый C++ объект Manipulator как непрозрачный дескриптор.
    try {
        Manipulator* manip = new(std::nothrow) Manipulator();
        return reinterpret_cast<RM_Manipulator>(manip);
    } catch (...) {
        return nullptr;
    }
}

void rm_destroy_manipulator(RM_Manipulator manip) {
    // Уничтожает объект по дескриптору. Допустимо передать nullptr.
    if (!manip) return;
    Manipulator* m = reinterpret_cast<Manipulator*>(manip);
    delete m;
}

int rm_add_link(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll) {
    // Добавляет MovableLink. Возвращает 1/0.
    if (!manip) return 0;
    Manipulator* m = reinterpret_cast<Manipulator*>(manip);
    MovableLink* link = nullptr;
    try {
        link = new MovableLink(id, prev_id, r, pitch, yaw, roll);
        m->addLink(link);
        return 1;
    } catch (...) {
        delete link;
        return 0;
    }
}

int rm_add_gripper(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll, double open_angle) {
    // Добавляет Gripper с углом раскрытия open_angle. Возвращает 1/0.
    if (!manip) return 0;
    Manipulator* m = reinterpret_cast<Manipulator*>(manip);
    Gripper* grip = nullptr;
    try {
        grip = new Gripper(id, prev_id, r, pitch, yaw, roll, open_angle);
        m->addLink(grip);
        return 1;
    } catch (...) {
        delete grip;
        return 0;
    }
}

int rm_add_camera(RM_Manipulator manip, int id, int prev_id, double r, double pitch, double yaw, double roll, double fov) {
    // Добавляет Camera с углом обзора fov. Возвращает 1/0.
    if (!manip) return 0;
    Manipulator* m = reinterpret_cast<Manipulator*>(manip);
    Camera* cam = nullptr;
    try {
        cam = new Camera(id, prev_id, r, pitch, yaw, roll, fov);
        m->addLink(cam);
        return 1;
    } catch (...) {
        delete cam;
        return 0;
    }
}

int rm_set_direction(RM_Manipulator manip, int id, double pitch, double yaw, double roll) {
    // Устанавливает ориентацию звена (pitch/yaw/roll). Возвращает 1/0.
    if (!manip) return 0;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        m->setDirection(id, pitch, yaw, roll);
        return 1;
    } catch (...) {
        return 0;
    }
}

int rm_open_gripper(RM_Manipulator manip, int id, double angle) {
    // Открывает захват на заданный угол. Возвращает 1/0.
    if (!manip) return 0;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        m->openGripper(id, angle);
        return 1;
    } catch (...) {
        return 0;
    }
}

int rm_close_gripper(RM_Manipulator manip, int id) {
    // Закрывает захват. Возвращает 1/0.
    if (!manip) return 0;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        m->closeGripper(id);
        return 1;
    } catch (...) {
        return 0;
    }
}

int rm_take_photo(RM_Manipulator manip, int id) {
    // Делает снимок с камеры. Возвращает 1/0.
    if (!manip) return 0;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        m->takePhoto(id);
        return 1;
    } catch (...) {
        return 0;
    }
}

int rm_calculate_position(RM_Manipulator manip, int id, double* out_x, double* out_y, double* out_z) {
    // Вычисляет позицию звена и записывает в переданные указатели. Возвращает 1/0.
    if (!manip || !out_x || !out_y || !out_z) return 0;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        auto pos = m->calculatePosition(id);
        *out_x = std::get<0>(pos);
        *out_y = std::get<1>(pos);
        *out_z = std::get<2>(pos);
        return 1;
    } catch (...) {
        return 0;
    }
}

void rm_print_structure(RM_Manipulator manip) {
    // Печатает структуру манипулятора в stdout (консоль).
    if (!manip) return;
    try {
        Manipulator* m = reinterpret_cast<Manipulator*>(manip);
        m->printStructure();
    } catch (...) {
        // swallow
    }
}

} // extern "C"

