def pit_stop_needed(fuel, tire_wear):

    return (
        fuel < 15 or
        tire_wear > 0.8
    )