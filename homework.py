from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        mess: str = (f'Тип тренировки: {self.training_type}; '
                     f'Длительность: {self.duration:.3f} ч.; '
                     f'Дистанция: {self.distance:.3f} км; '
                     f'Ср. скорость: {self.speed:.3f} км/ч; '
                     f'Потрачено ккал: {self.calories:.3f}.')
        return mess


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    min_in_hour: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    formula_coeff_1: int = 18
    formula_coeff_2: int = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.formula_coeff_1 * self.get_mean_speed()
                            - self.formula_coeff_2) * self.weight
                           / self.M_IN_KM * (self.duration
                                             * self.min_in_hour))
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    formula_coeff_3: float = 0.035
    formula_coeff_4: float = 0.029

    def get_spent_calories(self) -> float:
        calories: float = ((self.formula_coeff_3 * self.weight
                            + (self.get_mean_speed()**2 // self.height)
                            * self.formula_coeff_4 * self.weight)
                           * (self.duration * self.min_in_hour))
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38
    formula_coeff_5: float = 1.1
    formula_coeff_6: int = 2

    def get_distance(self) -> float:
        return super().get_distance()

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.formula_coeff_5)
                           * self.formula_coeff_6 * self.weight)
        return calories

    def get_mean_speed(self) -> float:
        speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                        / self.duration)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_pack: dict[str, list]
    dict_pack = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict_pack[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
