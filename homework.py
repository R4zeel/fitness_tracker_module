from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (
            self.get_distance()
            / (
                self.duration
                * self.MIN_IN_H
            )
            * self.MIN_IN_H
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError('Ошибка: метод не переопределён')

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
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (
                self.duration
                * self.MIN_IN_H
            )
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    KMH_INTO_MS = 0.278
    CM_INTO_METERS = 100

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return (
            (
                self.WEIGHT_MULTIPLIER_1
                * self.weight
                + (
                    (
                        self.get_mean_speed()
                        * self.KMH_INTO_MS
                    )
                    ** 2
                    / (
                        self.height
                        / self.CM_INTO_METERS
                    )
                )
                * self.WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * (
                self.duration
                * self.MIN_IN_H
            )
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_MULTIPLIER = 1.1
    MEAN_SPEED_MULTIPLIER_2 = 2

    def __init__(
            self,
            action,
            duration,
            weight,
            length_pool,
            count_pool
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self):
        return (
            (
                self.get_mean_speed()
                + self.MEAN_SPEED_MULTIPLIER
            )
            * self.MEAN_SPEED_MULTIPLIER_2
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types: dict[str: object] = {
        'SWM': Swimming,
        'WLK': SportsWalking,
        'RUN': Running
    }
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
