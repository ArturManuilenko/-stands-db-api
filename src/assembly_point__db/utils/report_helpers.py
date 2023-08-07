from typing import Tuple


def serializer_only_for_algoritm_and_launch_setting() -> Tuple[str, ...]:
    only = (
        # Report
        'id', 'launch', 'place', 'mac', 'serial', 'factory', 'result',
        # # Launch
        'launch.id',
        'launch.start',
        'launch.end',
        'launch.stage_count',
        # # Algoritm
        'algoritm.id',
        'algoritm.name',
        'algoritm.stage_count',
        'algoritm.descr',
    )
    return only
