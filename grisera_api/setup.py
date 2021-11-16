from channel.channel_service import ChannelService
from channel.channel_model import ChannelIn, Type
from modality.modality_service import ModalityService
from modality.modality_model import ModalityIn, Modality
from life_activity.life_activity_service import LifeActivityService
from life_activity.life_activity_model import LifeActivityIn, LifeActivity
from measure_name.measure_name_service import MeasureNameService
from measure_name.measure_name_model import MeasureNameIn, MeasureName
from activity.activity_service import ActivityService
from activity.activity_model import ActivityIn, Activity
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_model import ArrangementIn, Arrangement
import os
from time import sleep


class SetupNodes:
    """
    Class to init nodes in graph database
    """

    def set_activities(self):
        """
        Initialize values of activities
        """
        activity_service = ActivityService()
        if not os.path.exists("lock_activities"):
            open("lock_activities", "w").write("Busy")
            sleep(40)
            created_activities = [activity.activity for activity in activity_service.get_activities().activities]
            [activity_service.save_activity(ActivityIn(activity=activity_activity.value))
             for activity_activity in Activity
             if activity_activity.value not in created_activities]
            os.remove("lock_activities")

    def set_channels(self):
        """
        Initialize values of channels
        """
        channel_service = ChannelService()
        if not os.path.exists("lock_channels"):
            open("lock_channels", "w").write("Busy")
            sleep(40)
            created_types = [channel.type for channel in channel_service.get_channels().channels]
            [channel_service.save_channel(ChannelIn(type=channel_type.value))
             for channel_type in Type
             if channel_type.value not in created_types]
            os.remove("lock_channels")

    def set_arrangements(self):
        """
        Initialize values of arrangement distances
        """
        if not os.path.exists("lock_arrangement"):
            arrangement_service = ArrangementService()
            open("lock_arrangement", "w").write("Busy")
            sleep(60)
            created_arrangements = \
                [arrangement.arrangement_distance
                 for arrangement in
                 arrangement_service.get_arrangements().arrangements]
            [arrangement_service.save_arrangement(
                ArrangementIn(arrangement_type=arrangement.value[0], arrangement_distance=arrangement.value[1]))
                for arrangement in Arrangement
                if arrangement.value[1] not in created_arrangements]
            os.remove("lock_arrangement")

    def set_modalities(self):
        """
        Initialize values of modalities
        """
        modality_service = ModalityService()
        if not os.path.exists("lock_modalities"):
            open("lock_modalities", "w").write("Busy")
            sleep(40)
            created_modalities = [modality.modality for modality in modality_service.get_modalities().modalities]
            [modality_service.save_modality(ModalityIn(modality=modality_modality.value))
             for modality_modality in Modality
             if modality_modality.value not in created_modalities]
            os.remove("lock_modalities")

    def set_life_activities(self):
        """
        Initialize values of life activities
        """
        life_activity_service = LifeActivityService()
        if not os.path.exists("lock_life_activities"):
            open("lock_life_activities", "w").write("Busy")
            sleep(40)
            created_types = [life_activity.life_activity for life_activity in
                             life_activity_service.get_life_activities().life_activities]

            [life_activity_service.save_life_activity(LifeActivityIn(life_activity=life_activity_life_activity.value))
             for life_activity_life_activity in LifeActivity
             if life_activity_life_activity.value not in created_types]
            os.remove("lock_life_activities")

    def set_measure_names(self):
        """
        Initialize values of measure names
        """
        if not os.path.exists("lock_measure_names"):
            measure_name_service = MeasureNameService()
            open("lock_measure_names", "w").write("Busy")
            sleep(40)
            created_names = [measure_name.name for measure_name in
                             measure_name_service.get_measure_names().measure_names]
            [measure_name_service.save_measure_name(
                MeasureNameIn(name=measure_name.value[0], type=measure_name.value[1]))
                for measure_name in MeasureName
                if measure_name.value[0] not in created_names]
            os.remove("lock_measure_names")
