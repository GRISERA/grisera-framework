import json
from typing import Union
from models.not_found_model import NotFoundByIdModel
from participant_state.participant_state_model import ParticipantStateIn, ParticipantStateOut, ParticipantStatePropertyIn, ParticipantStateRelationIn, ParticipantStatesOut
from participant_state.participant_state_service import ParticipantStateService
from rdb_api_service import RdbApiService, Collections

class ParticipantStateServiceRelational(ParticipantStateService):
    
    def __init__(self) -> None:
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.PARTICIPANT_STATE


    def save_participant_state(self, participant_state: ParticipantStateIn):
        for appearance_id in participant_state.appearance_ids:
            appearance_dict = self.rdb_api_service.get_with_id(Collections.APPEARANCE, appearance_id)
            if appearance_dict is None:
                return NotFoundByIdModel(errors={"Appearance entity not found"})

        for personality_id in participant_state.personality_ids:
            personality_dict = self.rdb_api_service.get_with_id(Collections.PERSONALITY, personality_id)
            if personality_dict is None:
                return NotFoundByIdModel(errors={"Personality entity not found"})

        participant_state_data= {
            "participant_id": participant_state.participant_id,
            "age": participant_state.age,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in participant_state.additional_properties
            ])
        }

        saved_participant_dict = self.rdb_api_service.post(self.table_name, participant_state_data)
        if saved_participant_dict["errors"] is not None:
            return ParticipantStateOut(errors=saved_participant_dict["errors"])

        for appearance_id in participant_state.appearance_ids:
            participant_state_appearance_data = {
                "participant_state_id": saved_participant_dict["records"]["id"],
                "appearance_id": appearance_id
            }
            saved_participant_state_appearance = self.rdb_api_service.post(Collections.PARTICIPANT_STATE_APPEARANCE, participant_state_appearance_data)
            if saved_participant_state_appearance["errors"] is not None:
                return ParticipantStateOut(errors=saved_participant_state_appearance["errors"])
            
        for personality_id in participant_state.personality_ids:
            perticipant_state_personality_data = {
                "participant_state_id": saved_participant_dict["records"]["id"],
                "personality_id": personality_id
            }
            saved_participant_state_personality = self.rdb_api_service.post(Collections.PARTICIPANT_STATE_PERSONALITY, perticipant_state_personality_data)
            if saved_participant_state_personality["errors"] is not None:
                return ParticipantStateOut(errors=saved_participant_state_personality["errors"])
            
        return ParticipantStateOut(**saved_participant_dict["records"])
    

    def get_participant_states(self):
        results = self.rdb_api_service.get(self.table_name)
        return ParticipantStatesOut(participant_states=results)
    

    def get_participant_state(self, participant_state_id: Union[int, str], depth: int = 0, source: str = ""):
        participant_state_dict = self.rdb_api_service.get_with_id(self.table_name, participant_state_id)
        if not participant_state_dict:
            return NotFoundByIdModel(id=participant_state_id, errors={"Entity not found."})
        
        # import participation.participation_service_relational
        import participant.participant_service_relational
        # import appearance.appearance_service_relational
        # import personality.personality_service_relational
        # participation_service = participation.participation_service_relational.ParticipationServiceRelational()
        participant_service = participant.participant_service_relational.ParticipantServiceRelational()
        # appearance_service = appearance.appearance_service_relational.AppearanceServiceRelational()
        # personality_service = personality.personality_service_relational.PersonalityServiceRelational()

        if depth > 0:
            # if source != Collections.PARTICIPATION:
            #     participant_state_dict["participations"] = participation_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)
            if source != Collections.PARTICIPANT:
                participant_state_dict["participant"] = participant_service.get_participant(participant_state_dict["participant_id"], depth - 1, self.table_name)
            # if source != Collections.APPEARANCE:
            #     participant_state_dict["appearances"] = appearance_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)
            # if source != Collections.PERSONALITY:
            #     participant_state_dict["personalities"] = personality_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)

        return ParticipantStateOut(**participant_state_dict)
    

    def delete_participant_state(self, participant_state_id: Union[int, str]):
        result = self.get_participant_state(participant_state_id)
        if type(result) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, participant_state_id)
        return result


    def update_participant_state(self, participant_state_id: Union[int, str], participant_state: ParticipantStatePropertyIn):
        participant_state_data_dict = {
            "age": participant_state.age,
            "additional_properties": json.dumps([
                {
                    "key": p.key,
                    "value": p.value
                } for p in participant_state.additional_properties
            ])
        }

        result = self.get_participant_state(participant_state_id)
        if type(result) == NotFoundByIdModel:
            return result
        
        put_result = self.rdb_api_service.put(self.table_name, participant_state_id, participant_state_data_dict)
        if put_result["errors"] is not None:
            return ParticipantStateOut(errors = put_result["errors"])
        return ParticipantStateOut(**put_result["records"])
    

    def update_participant_state_relationships(self, participant_state_id: Union[int, str], participant_state: ParticipantStateRelationIn):
        result = self.get_participant_state(participant_state_id)
        if type(result) == NotFoundByIdModel:
            return result
        
        for appearance_id in participant_state.appearance_ids:
            appearance_dict = self.rdb_api_service.get_with_id(Collections.APPEARANCE, appearance_id)
            if appearance_dict is None:
                return NotFoundByIdModel(errors={"Appearance entity not found"})

        for personality_id in participant_state.personality_ids:
            personality_dict = self.rdb_api_service.get_with_id(Collections.PERSONALITY, personality_id)
            if personality_dict is None:
                return NotFoundByIdModel(errors={"Personality entity not found"})
        
        participant_state_data = {
            "participant_id": participant_state.participant_id
        }
        updated_participant_state = self.rdb_api_service.put(self.table_name, participant_state_id, participant_state_data)
        if updated_participant_state["errors"] is not None:
            return ParticipantStateOut(errors=updated_participant_state["errors"])
        
        self.rdb_api_service.delete_by_column_value(Collections.PARTICIPANT_STATE_APPEARANCE, self.table_name + "_id", participant_state_id)
        self.rdb_api_service.delete_by_column_value(Collections.PARTICIPANT_STATE_PERSONALITY, self.table_name + "_id", participant_state_id)

        for appearance_id in participant_state.appearance_ids:
            participant_state_appearance_data = {
                "participant_state_id": participant_state_id,
                "appearance_id": appearance_id
            }
            self.rdb_api_service.post(Collections.PARTICIPANT_STATE_APPEARANCE, participant_state_appearance_data)
            
        for personality_id in participant_state.personality_ids:
            perticipant_state_personality_data = {
                "participant_state_id": participant_state_id,
                "personality_id": personality_id
            }
            self.rdb_api_service.post(Collections.PARTICIPANT_STATE_PERSONALITY, perticipant_state_personality_data)

        return ParticipantStateOut(**updated_participant_state["records"])
    

    def get_multiple_with_foreign_id(self, id: Union[int, str], depth: int = 0, source = ""):
        # import participation.participation_service_relational
        import participant.participant_service_relational
        # import appearance.appearance_service_relational
        # import personality.personality_service_relational
        # participation_service = participation.participation_service_relational.ParticipationServiceRelational()
        participant_service = participant.participant_service_relational.ParticipantServiceRelational()
        # appearance_service = appearance.appearance_service_relational.AppearanceServiceRelational()
        # personality_service = personality.personality_service_relational.PersonalityServiceRelational()

        participant_state_dict_list = self.rdb_api_service.get_records_with_foreign_id(self.table_name, source + "_id", id)
        if participant_state_dict_list["errors"] is not None:
            return []
        
        if depth <= 0:
            return participant_state_dict_list["records"]
        
        for participant_state_dict in participant_state_dict_list["records"]:
            # if source != Collections.PARTICIPATION:
            #     participant_state_dict["participations"] = participation_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)
            if source != Collections.PARTICIPANT:
                participant_state_dict["participant"] = participant_service.get_participant(participant_state_dict["participant_id"], depth - 1, self.table_name)
            # if source != Collections.APPEARANCE:
            #     participant_state_dict["appearances"] = appearance_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)
            # if source != Collections.PERSONALITY:
            #     participant_state_dict["personalities"] = personality_service.get_multiple_with_foreign_id(participant_state_id, depth - 1, self.table_name)

        return participant_state_dict_list["records"]

    def get_multiple_from_proxy_with_foreign_id(self, id: Union[int, str], depth: int = 0, source = ""):
        proxy_table_name = str()
        if source == Collections.APPEARANCE:
            proxy_table_name = Collections.PARTICIPANT_STATE_APPEARANCE
        elif source == Collections.PERSONALITY:
            proxy_table_name = Collections.PARTICIPANT_STATE_PERSONALITY
        else:
            return []
        
        participant_state_proxy_list = self.rdb_api_service.get_records_with_foreign_id(proxy_table_name, source + "_id", id)["records"]

        participant_states_list = list()
        for participant_state_proxy in participant_state_proxy_list:
            participant_state = self.get_participant_state(participant_state_proxy["participant_state_id"], depth, source)
            participant_states_list.append(participant_state)

        return participant_states_list
