import pandas as pd

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


class DataLoader:
    def __init__(self, settings):
        self.settings = settings

    def get_data_from_run(self, run_name):
        event_acc = EventAccumulator(self.settings["path_to_trainings"] + run_name)
        event_acc.Reload()

        run_data = pd.DataFrame()
        for metric in self.settings["criteria"]:
            steps = []
            values = []
            for event in event_acc.Scalars(metric):
                steps.append(event.step)
                values.append(event.value)
            run_data[metric] = values
        run_data["Step"] = steps

        return run_data

    def get_data_from_all_runs(self, training_type):
        training_data = {}
        for run_name in self.settings["trainings"][training_type]:
            training_data[f"{training_type}_{run_name.split('/')[-1]}"] = self.get_data_from_run(run_name).copy()

        return training_data
