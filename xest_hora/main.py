#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xest_hora.optimization_model import OptimizationModel
from xest_hora.example import example
import logging as log


def main():
    # Datos del modelo
    log.info("Get the input data")
    data = example()

    log.info("Solve the problem")
    optimization_model = OptimizationModel(data=data)
    calendars = optimization_model.execute()

    log.info("Save the calendars")
    for calendar in calendars:
        calendar.plot()


if __name__ == "__main__":
    main()
