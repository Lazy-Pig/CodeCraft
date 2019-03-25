from schedulers.BaseScheduler import BaseScheduler


class Scheduler(BaseScheduler):
    """
    按照answer.txt的计划一辆一辆的发车
    """
    def __init__(self, id_2_cars, id_2_roads, id_2_cross):
        super(Scheduler, self).__init__(id_2_cars, id_2_roads, id_2_cross)

    def scheduling(self, global_tick):
        # 找出能够开始出发的车辆
        cars_just_run = []
        for car_id in self._not_start_cars_ids:
            car = self._id_2_cars[car_id]
            if global_tick >= car.get_begin_tick():
                first_raod, first_raod_direction = car.get_path()[0]
                if all([l.is_full() for l in first_raod.get_lanes(first_raod_direction)]):
                    continue
                cars_just_run.append(car)
                car.start_running(global_tick)
                self._running_cars.append(car.get_id())
        for car in cars_just_run:
            self._not_start_cars_ids.remove(car.get_id())
