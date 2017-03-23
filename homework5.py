#!/usr/bin/env python3.5

from random import randint

GASOLINE = 0
DIESEL = 1


class Car(object):
    DEFAULT_CAR_COST = 10000

    TRAVEL_CALCULATION_LENGTH = 1000

    GASOLINE_COST = 2.4
    DIESEL_COST = 1.8

    GASOLINE_CONSUMPTION = 8 / 100
    DIESEL_CONSUMPTION = 6 / 100

    REPAIR_MILEAGE_GASOLINE = 100000
    REPAIR_MILEAGE_DIESEL = 150000

    REPAIR_GASOLINE_COST = 500
    REPAIR_DIESEL_COST = 700

    GASOLINE_COST_CHANGE = 9.5
    DIESEL_COST_CHANGE = 10.5

    def __init__(self, tank_volume):
        self._initial_cost = self.DEFAULT_CAR_COST
        self._current_cost = self.DEFAULT_CAR_COST
        self._tank = tank_volume
        self._fuel_amount = 0
        self._fuel_spent_cost = 0
        self._refuel_times = 0
        self._tachograph = 0
        self._fuel_consumption_change = 1.01

    def refuel(self):
        need_fuel = self._tank - self._fuel_amount
        self._fuel_spent_cost += need_fuel * self._fuel_cost
        self._fuel_amount += need_fuel
        self._refuel_times += 1

    def travel(self, length):
        path = 0
        while length > 0:
            if self._fuel_amount == 0:
                self.refuel()

            fuel_path = self._fuel_amount / self._current_fuel_consumption

            if fuel_path > length:
                fuel_path = length

            if path + fuel_path > self.TRAVEL_CALCULATION_LENGTH:
                fuel_path = self.TRAVEL_CALCULATION_LENGTH - path

            path += fuel_path

            self._tachograph += fuel_path

            self._fuel_amount -= fuel_path * self._current_fuel_consumption

            if path >= 1000:
                self._current_fuel_consumption *= self._fuel_consumption_change
                self._current_cost -= self._cost_change
                path -= self.TRAVEL_CALCULATION_LENGTH

            if self._tachograph >= self._next_repair_mileage:
                self._current_cost += self._repair_cost
                self._next_repair_mileage += self._repair_mileage

            length -= fuel_path

    def get_information(self):
        return "Mileage: {mileage}, Cost {cost}, Fuel cost {fuel_cost}, " \
               "Refuel times {refuels}, Repair mileage {repair_mileage}".format(
            mileage=self._tachograph,
            cost=self._current_cost,
            fuel_cost=self._fuel_spent_cost,
            refuels=self._refuel_times,
            repair_mileage=(self._next_repair_mileage - self._tachograph)
        )


class GasolineCar(Car):
    def __init__(self, tank_volume):
        super(GasolineCar, self).__init__(tank_volume=tank_volume)
        self._type = GASOLINE
        self._current_fuel_consumption = self.GASOLINE_CONSUMPTION
        self._repair_mileage = self.REPAIR_MILEAGE_GASOLINE
        self._next_repair_mileage = self.REPAIR_MILEAGE_GASOLINE
        self._repair_cost = self.REPAIR_GASOLINE_COST
        self._cost_change = self.GASOLINE_COST_CHANGE
        self._fuel_cost = self.GASOLINE_COST


class DieselCar(Car):
    def __init__(self, tank_volume):
        super(DieselCar, self).__init__(tank_volume=tank_volume)
        self._type = DIESEL
        self._current_fuel_consumption = self.DIESEL_CONSUMPTION
        self._repair_mileage = self.REPAIR_MILEAGE_DIESEL
        self._next_repair_mileage = self.REPAIR_MILEAGE_DIESEL
        self._repair_cost = self.REPAIR_DIESEL_COST
        self._cost_change = self.DIESEL_COST_CHANGE
        self._fuel_cost = self.DIESEL_COST


class Taxopark(object):
    def __init__(self):
        self._cars = []

    def create_cars(self, amount=100):
        for i in range(0, amount):
            tv = 60
            if i % 5 == 0:
                tv = 75

            if i % 3 == 0:
                car = DieselCar(tank_volume=tv)
            else:
                car = GasolineCar(tank_volume=tv)

            self._cars.append(car)

    def travel(self, min_path=55000, max_path=286000):
        for car in self._cars:
            car.travel(randint(min_path, max_path))

    def print(self):
        for car in self._cars:
            print(car.get_information())


if __name__ == "__main__":
    tp = Taxopark()
    tp.create_cars()
    tp.travel()
    tp.print()
