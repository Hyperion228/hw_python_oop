class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE_TEMPLATE = ('Тип тренировки: {training_type}; Длительность: '
                        '{duration:.3f} ч.; Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; Потрачено ккал: '
                        '{calories:.3f}.')

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""
        return self.MESSAGE_TEMPLATE.format(training_type=self.training_type,
                                            duration=self.duration,
                                            distance=self.distance,
                                            speed=self.speed,
                                            calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    MIN_IN_HR = 60
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод get_spent_calories должен быть '
                                  'реализован в дочернем классе.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    AVERAGE_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.AVERAGE_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER = 0.035
    SPEED_MULTIPLIER = 0.029
    SPEED_TRANSLATER = 0.278
    HEIGHT_TRANSLATER = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        avg_speed = self.get_mean_speed()
        calories_burn = ((self.WEIGHT_MULTIPLIER * self.weight + ((avg_speed
                         * self.SPEED_TRANSLATER)**2 / (self.height
                         / self.HEIGHT_TRANSLATER)) * self.SPEED_MULTIPLIER
                                                    * self.weight)
                         * self.duration * self.MIN_IN_HR)
        return calories_burn


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    AVG_SPEED_OFFSET = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # def get_distance(self) -> float:
    #     """Получить дистанцию в км."""
    #     distance = self.action * self.LEN_STEP / self.M_IN_KM
    #     return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_spd = (self.length_pool * self.count_pool
                   / self.M_IN_KM / self.duration)
        return avg_spd

    def get_spent_calories(self) -> float:
        avg_spd = self.get_mean_speed()
        calories_burn = ((avg_spd + self.AVG_SPEED_OFFSET)
                         * self.SPEED_MULTIPLIER * self.weight * self.duration)
        return calories_burn


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: dict[str, list[float]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workouts:
        workout_class = workouts[workout_type]
        return workout_class(*data)
    raise ValueError(f"Неподдерживаемый тип тренировки: {workout_type}")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
