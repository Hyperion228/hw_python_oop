class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.2f} ч.; Дистанция: {self.distance:.2f} км; Ср. '
                f'скорость: {self.speed:.2f} км/ч; Потрачено ккал: '
                f'{self.calories:.2f}.')


M_IN_KM = 1000
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    LEN_GREB = 1.38

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
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        avg_spd = distance / self.duration
        return avg_spd

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        avg_speed = self.get_mean_speed
        calories_burn = (CALORIES_MEAN_SPEED_MULTIPLIER * avg_speed
                         + CALORIES_MEAN_SPEED_SHIFT) * self.weight / \
            M_IN_KM * self.duration
        return calories_burn


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        avg_speed = self.get_mean_speed
        avg_speed_mps = avg_speed / 3.6
        height_m = self.height / 100
        duration_m = self.duration * 60
        calories_burn = ((0.035 * self.weight + (avg_speed_mps**2 / height_m)
                                * 0.029 * self.weight) * duration_m)
        return calories_burn


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_spd = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return avg_spd

    def get_spent_calories(self) -> float:
        avg_spd = self.get_mean_speed()
        calories_burn = (avg_spd + 1.1) * 2 * self.weight * self.duration
        return calories_burn


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workouts:
        # Если код тренировки существует, получаем соответствующий класс
        workout_class = workouts[workout_type]
        # Создаем объект тренировки, передав параметры из списка data в качестве аргументов
        return workout_class(*data)


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
