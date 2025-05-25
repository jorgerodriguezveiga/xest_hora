import logging as log
from pyomo.environ import (
    ConcreteModel,
    Set,
    Param,
    Var,
    Binary,
    NonNegativeIntegers,
    Constraint,
    Objective,
    minimize,
    SolverFactory,
)
import pandas as pd
import functools

from xest_hora.input.input_data import InputData
from xest_hora.output.calendar import Calendar


def check_constraint_expression_decorator(func):
    """Decorator that checks if constraint expression is boolean. In case it is True, the constraints is skipped. In
    case it is False, an error message is display. Otherwise nothing.

    Args:
        func (function): constraint rule.

    Returns:
        Constraint.Skip if the returned value of the constraint rule is True otherwise the same value returned by
        constraint rule.

    Example:
        >>> from optimization_autobots.autobots.optimus_prime.algorithm.network_to_optimus_prime_model_serializer \
import check_constraint_expression_decorator
        >>> @check_constraint_expression_decorator
        ... def test_True_func():
        ...     return True
        >>> test_True_func()
        <class 'pyomo.core.base.indexed_component.IndexedComponent.Skip'>
        >>> @check_constraint_expression_decorator
        ... def test_False_func():
        ...     return False
        >>> test_False_func()
        False
        >>> @check_constraint_expression_decorator
        ... def test_other_func():
        ...     return 1
        >>> test_other_func()
        1
    """

    @functools.wraps(func)
    def wrapper_decorator(*args, **kargs):
        value = func(*args, **kargs)
        args_repr = ", ".join([str(a) for a in args] + [f"{k}={v}" for k, v in kargs])
        if value is True:
            return Constraint.Skip
        elif value is False:
            log.error(f"Infeasible constraint: {func.__name__}({args_repr})")
            return value
        else:
            return value

    return wrapper_decorator


class OptimizationModel:

    def __init__(self, data: InputData):
        self.data = data

    def execute(self) -> list[Calendar]:
        model = self.create_model()
        solution = self.solve(model)
        self.check_solver_status(model, solution)
        class_calendars = self.get_class_calendars(model)
        teacher_calendars = self.get_teacher_calendars(model)
        return class_calendars + teacher_calendars

    def create_model(self):
        # Modelo
        model = ConcreteModel()

        # Conjuntos
        model.P = Set(initialize=self.data.teachers)
        model.T = Set(initialize=self.data.tasks)
        model.C = Set(initialize=self.data.calendars)
        model.Cl = Set(initialize=self.data.classes)
        model.D = Set(initialize=self.data.days)
        model.H = Set(initialize=self.data.times)

        model.CT = Set(
            dimen=2,
            within=model.C * model.T,
            initialize=self.data.calendar_tasks.index.to_list(),
        )

        A = [
            (teacher, calendar, task, day, time)
            for teacher, calendar, task in self.data.teacher_calendar_tasks.index
            for day in self.data.days
            for time in self.data.times
        ]

        model.A = Set(
            dimen=5, within=model.P * model.C * model.T * model.D * model.H, initialize=A
        )  # Conjunto de tareas que puede hacer cada profesor en cada clase e instante de tiempo

        B = [
            (calendar, task, day, time)
            for calendar, task in model.CT
            for day in self.data.days
            for time in self.data.times
        ]

        model.B = Set(
            dimen=4, within=model.C * model.T * model.D * model.H, initialize=B
        )  # Conjunto de tareas que puede tener una clase en cada instante de tiempo

        # Parametros
        model.min_numero_horas_tareas_calendario = Param(
            model.CT, initialize=self.data.calendar_tasks.data_idx["min_time_periods"].to_dict()
        )
        model.max_numero_horas_tareas_calendario = Param(
            model.CT, initialize=self.data.calendar_tasks.data_idx["max_time_periods"].to_dict()
        )
        model.max_numero_horas_tareas_dia_calendario = Param(
            model.CT, initialize=self.data.calendar_tasks.data_idx["max_time_period_per_day"].to_dict()
        )
        model.num_teachers = Param(model.CT, initialize=self.data.calendar_tasks.data_idx["num_teachers"].to_dict())

        # Variables
        model.x = Var(model.A, domain=Binary)
        model.y = Var(model.B, domain=Binary)
        model.maximo_horas_garda = Var(domain=NonNegativeIntegers)  # Máximo de horas de garda

        # Fijar las horas libres de los profesores
        for teacher, c, task, day, time in self.data.fixed_teacher_calendar_task_day_times.index:
            model.x[teacher, c, task, day, time].fix(1)

        for calendar, task, day, time in model.B:
            if task == self.data.playtime.name:
                value = 0
                if (calendar, day, time) in self.data.playtime.index:
                    value = 1
                model.y[calendar, task, day, time].fix(value)

        # Cada profesor tiene que hacer una tarea por hora
        # (no se puede hacer más de una tarea a la vez)
        @check_constraint_expression_decorator
        def one_task_per_teacher_day_time_rule(model, p, d, h):
            tasks = [
                model.x[profesor, calendario, tarea, dia, hora]
                for profesor, calendario, tarea, dia, hora in model.A
                if (profesor, dia, hora) == (p, d, h)
            ]
            return (
                sum(tasks)
                == 1
                + model.slack_pos_oneTaskPerTeacherDayTime[p, d, h]
                - model.slack_neg_oneTaskPerTeacherDayTime[p, d, h]
            )

        model.slack_pos_oneTaskPerTeacherDayTime = Var(model.P, model.D, model.H, domain=NonNegativeIntegers)
        model.slack_neg_oneTaskPerTeacherDayTime = Var(model.P, model.D, model.H, domain=NonNegativeIntegers)
        model.oneTaskPerTeacherDayTime = Constraint(model.P, model.D, model.H, rule=one_task_per_teacher_day_time_rule)

        # La clase tiene que estar atendida por un profesor
        @check_constraint_expression_decorator
        def cubrir_hora_clase_rule(model, c, d, h):
            return (
                sum(
                    model.y[calendario, tarea, dia, hora]
                    for calendario, tarea, dia, hora in model.B
                    if (calendario, dia, hora) == (c, d, h)
                )
                == 1
            )

        model.cubrirHoraClase = Constraint(model.Cl, model.D, model.H, rule=cubrir_hora_clase_rule)

        # Tiene que haber el número indicado de profesores para cubrir las tareas
        @check_constraint_expression_decorator
        def assign_teachers_to_tasks_rule(model, c, t, d, h):
            return model.num_teachers[c, t] * model.y[c, t, d, h] == sum(
                model.x[profesor, calendario, tarea, dia, hora]
                for profesor, calendario, tarea, dia, hora in model.A
                if (calendario, tarea, dia, hora) == (c, t, d, h)
            )

        model.assignTeachersToTasks = Constraint(model.CT, model.D, model.H, rule=assign_teachers_to_tasks_rule)

        # No se pueden superar las horas máximas de la tarea en el calendario
        @check_constraint_expression_decorator
        def horas_max_tareas_calendario_rule(model, c, t):
            return (
                sum(
                    model.y[calendario, tarea, dia, hora]
                    for calendario, tarea, dia, hora in model.B
                    if (calendario, tarea) == (c, t)
                )
                <= model.max_numero_horas_tareas_calendario[c, t] + model.slack_pos_horasMaxTareasCalendario[c, t]
            )

        model.slack_pos_horasMaxTareasCalendario = Var(model.CT, domain=NonNegativeIntegers)
        model.horasMaxTareasCalendario = Constraint(model.CT, rule=horas_max_tareas_calendario_rule)

        # Hay que asegurar el minimo de horas de la tarea en la calendario
        @check_constraint_expression_decorator
        def horas_min_tareas_calendario_rule(model, c, t):
            return (
                sum(
                    model.y[calendario, tarea, dia, hora]
                    for calendario, tarea, dia, hora in model.B
                    if (calendario, tarea) == (c, t)
                )
                >= model.min_numero_horas_tareas_calendario[c, t] - model.slack_neg_horasMaxTareasCalendario[c, t]
            )

        model.slack_neg_horasMaxTareasCalendario = Var(model.CT, domain=NonNegativeIntegers)
        model.horasMinTareasCalendario = Constraint(model.CT, rule=horas_min_tareas_calendario_rule)

        @check_constraint_expression_decorator
        def horas_max_tareas_calendario_rule(model, c, t, d):
            if (c, t) not in model.max_numero_horas_tareas_dia_calendario:
                return True

            return (
                sum(
                    model.y[calendario, tarea, dia, hora]
                    for calendario, tarea, dia, hora in model.B
                    if (calendario, tarea, dia) == (c, t, d)
                )
                <= model.max_numero_horas_tareas_dia_calendario[c, t]
            )

        model.HorasMaxTareasDiaCalendario = Constraint(model.CT, model.D, rule=horas_max_tareas_calendario_rule)

        # Numero maximo de horas de garda por profesor
        @check_constraint_expression_decorator
        def horas_garda_max_profesor_rule(model, p):
            return (
                sum(
                    model.x[profesor, calendario, tarea, dia, hora]
                    for profesor, calendario, tarea, dia, hora in model.A
                    if (profesor, tarea) == (p, "garda")
                )
                <= model.maximo_horas_garda
            )

        model.HorasGuardiaMaxProfesor = Constraint(model.P, rule=horas_garda_max_profesor_rule)

        # Función objetivo (ejemplo): minimizar numero máximo de horas de garda
        model.obj = Objective(
            expr=model.maximo_horas_garda
            + 1000
            * (
                sum(
                    [
                        model.slack_pos_horasMaxTareasCalendario[c, t] + model.slack_neg_horasMaxTareasCalendario[c, t]
                        for c, t in model.CT
                    ]
                )
                + sum(
                    [
                        model.slack_pos_oneTaskPerTeacherDayTime[p, d, h]
                        + model.slack_neg_oneTaskPerTeacherDayTime[p, d, h]
                        for p in model.P
                        for d in model.D
                        for h in model.H
                    ]
                )
            ),
            sense=minimize,
        )
        return model

    def solve(self, model):
        log.info("Solving the optimization model...")
        solver = SolverFactory("cbc")
        solution = solver.solve(model, tee=True)
        log.info("The optimization model was solved")

        return solution

    def check_solver_status(self, model, solution):
        # Imprimir resultados
        log.info(f"- Solver status: {solution.solver.termination_condition}")
        log.info(f"Objective function: {model.obj()}")

        infeasibilities = []
        for constraint in list(model.component_objects(Constraint)):
            constraint_name = constraint.name
            slack_pos = None
            slack_pos_name = f"slack_pos_{constraint_name}"
            if hasattr(model, slack_pos_name):
                slack_pos = getattr(model, slack_pos_name)

            slack_neg = None
            slack_neg_name = f"slack_neg_{constraint_name}"
            if hasattr(model, slack_neg_name):
                slack_neg = getattr(model, slack_neg_name)

            if slack_pos is not None or slack_neg is not None:
                for i in constraint:
                    constraint_idx = constraint[i]
                    slack_pos_idx = 0
                    if slack_pos is not None:
                        slack_pos_idx = slack_pos[i].value

                    slack_neg_idx = 0
                    if slack_neg is not None:
                        slack_neg_idx = slack_neg[i].value

                    slack_value = slack_pos_idx - slack_neg_idx
                    if slack_value != 0:
                        infeasibilities.append(
                            {
                                "constraint": constraint_name,
                                "index": i,
                                "slack": slack_value,
                                "expression": str(constraint_idx.expr),
                            }
                        )
        infeasibilities_df = pd.DataFrame(infeasibilities)

        if len(infeasibilities_df) > 0:
            log.warning(f"\n{infeasibilities_df.to_string()}")

    def get_teacher_calendars(self, model):
        calendars = {
            teacher: {
                (d, t): self.data.playtime.name if (teacher, d, t) in self.data.playtime.index else ""
                for d in self.data.days
                for t in self.data.times
            }
            for teacher in self.data.teachers
        }
        for teacher, calendar, task, day, time in model.A:
            if model.x[teacher, calendar, task, day, time].value > 0:
                calendars[teacher][(day, time)] = (
                    task if task == self.data.playtime.name or calendar == teacher else f"{task} ({calendar})"
                )

        calendars = [
            Calendar(
                days=self.data.days,
                times=self.data.times,
                data=pd.DataFrame([{"day": d, "time": t, "task": task} for (d, t), task in v.items()]),
                name=c,
            )
            for c, v in calendars.items()
        ]

        return calendars

    def get_class_calendars(self, model) -> list[Calendar]:
        calendars = {
            c: {
                (d, t): self.data.playtime.name if (c, d, t) in self.data.playtime.index else ""
                for d in self.data.days
                for t in self.data.times
            }
            for c in self.data.classes
        }
        for calendar, task, day, time in model.B:
            if calendar in calendars and model.y[calendar, task, day, time].value > 0:
                teachers = [
                    p
                    for p, c, tsk, d, t in model.A
                    if (calendar, task, day, time) == (c, tsk, d, t) and model.x[p, calendar, task, day, time].value > 0
                ]
                if len(teachers) > 0 or task == self.data.playtime.name:
                    calendars[calendar][(day, time)] = (
                        task if task == self.data.playtime.name else f"{task} ({', '.join(teachers)})"
                    )

        calendars = [
            Calendar(
                days=self.data.days,
                times=self.data.times,
                data=pd.DataFrame([{"day": d, "time": t, "task": task} for (d, t), task in v.items()]),
                name=c,
            )
            for c, v in calendars.items()
        ]

        return calendars
