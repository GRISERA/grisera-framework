from typing import Union
from models.not_found_model import NotFoundByIdModel
from personality.personality_model import PersonalitiesOut, PersonalityBigFiveIn, PersonalityBigFiveOut, PersonalityPanasIn, PersonalityPanasOut
from rdb_api_service import RdbApiService, Collections
from personality.personality_service import PersonalityService


class PersonalityServiceRelational(PersonalityService):
    
    def __init__(self):
        self.rdb_api_service = RdbApiService()
        self.table_name = Collections.PERSONALITY
    

    def save_personality_big_five(self, personality: PersonalityBigFiveIn):
        if not self.is_valid_big_five(personality):
            return PersonalityBigFiveOut(**personality.dict(), errors={"Value of one of the parameters is not in range <0,1>"})
        
        personality_data = {
            "type": "big_five",
            "agreeableness": personality.agreeableness,
            "conscientiousness": personality.conscientiousness,
            "extroversion": personality.extroversion,
            "neuroticism": personality.neuroticism,
            "openess": personality.openess
        }

        saved_personality_dict = self.rdb_api_service.post(self.table_name, personality_data)
        if saved_personality_dict["errors"] is not None:
            return PersonalityBigFiveOut(errors=saved_personality_dict["errors"])
        return PersonalityBigFiveOut(**saved_personality_dict["records"])


    def save_personality_panas(self, personality: PersonalityPanasIn):
        if not self.is_valid_panas(personality):
            return PersonalityPanasOut(**personality.dict(), errors={"Value of one of the parameters is not in range <0,1>"})  
    
        personality_data = {
            "type": "panas",
            "negative_affect": personality.negative_affect,
            "positive_affect": personality.positive_affect
        }

        saved_personality_dict = self.rdb_api_service.post(self.table_name, personality_data)
        if saved_personality_dict["errors"] is not None:
            return PersonalityPanasOut(errors=saved_personality_dict["errors"])
        return PersonalityPanasOut(**saved_personality_dict["records"])


    def get_personality(self, personality_id: Union[int, str], depth: int = 0, source: str = ""):
        import participant_state.participant_state_service_relational as ps_rel
        participant_state_service = ps_rel.ParticipantStateServiceRelational()
        
        personality_dict = self.rdb_api_service.get_with_id(self.table_name, personality_id)
        if not personality_dict:
            return NotFoundByIdModel(id=personality_id, errors={"Entity not found."})
        
        if depth > 0 and source != Collections.PARTICIPANT_STATE:
            personality_dict["participant_states"] = participant_state_service.get_multiple_from_proxy_with_foreign_id(personality_id, depth - 1, self.table_name)

        if personality_dict["type"] == "big_five":
            return PersonalityBigFiveOut(**personality_dict)
        else:
            return PersonalityPanasOut(**personality_dict)


    def get_personalities(self):
        results = self.rdb_api_service.get(self.table_name)
        personalities = []
        for personality_dict in results:
            if personality_dict["type"] == "big_five":
                personalities.append(PersonalityBigFiveOut(**personality_dict))
            else:
                personalities.append(PersonalityPanasOut(**personality_dict))
        return PersonalitiesOut(personalities=personalities)


    def delete_personality(self, personality_id: Union[int, str]):
        get_response = self.get_personality(personality_id)
        if type(get_response) != NotFoundByIdModel:
            self.rdb_api_service.delete_with_id(self.table_name, personality_id)
        return get_response
    

    def update_personality_big_five(self, personality_id: Union[int, str], personality: PersonalityBigFiveIn):
        if not self.is_valid_big_five(personality):
            return PersonalityBigFiveOut(errors="Value of one of the parameters is not in range <0,1>")
        
        get_response = self.get_personality(personality_id)
        if type(get_response) is PersonalityPanasOut:
            return NotFoundByIdModel(id=personality_id, errors="Entity not found")
        if type(get_response) == NotFoundByIdModel:
            return get_response
        
        put_response = self.rdb_api_service.put(self.table_name, personality_id, personality.dict())
        if put_response["errors"] is not None:
            return PersonalityBigFiveOut(errors=put_response["errors"])
        return PersonalityBigFiveOut(**put_response["records"])
    

    def update_personality_panas(self, personality_id: Union[int, str], personality: PersonalityPanasIn):
        if not self.is_valid_panas(personality):
            return PersonalityPanasOut(errors="Value of one of the parameters is not in range <0,1>")
        
        get_response = self.get_personality(personality_id)
        if type(get_response) is PersonalityBigFiveOut:
            return NotFoundByIdModel(id=personality_id, errors="Entity not found")
        if type(get_response) == NotFoundByIdModel:
            return get_response
        
        put_response = self.rdb_api_service.put(self.table_name, personality_id, personality.dict())
        if put_response["errors"] is not None:
            return PersonalityPanasOut(errors=put_response["errors"])
        return PersonalityPanasOut(**put_response["records"])


    def get_multiple_from_proxy_with_foreign_id(self, id: Union[int, str], depth: int = 0, source: str = ""):
        personality_proxy_list = self.rdb_api_service.get_records_with_foreign_id(Collections.PARTICIPANT_STATE_PERSONALITY, source + "_id", id)["records"]
        personalities = []
        for personality_proxy in personality_proxy_list:
            personalities.append(self.get_personality(personality_proxy["personality_id"], depth, source))
        return personalities
    

    def is_valid_big_five(self, personality: PersonalityBigFiveIn):
        return (0 <= personality.agreeableness <= 1 and
                0 <= personality.conscientiousness <= 1 and
                0 <= personality.extroversion <= 1 and
                0 <= personality.neuroticism <= 1 and
                0 <= personality.openess <= 1)
    

    def is_valid_panas(self, personality: PersonalityPanasIn):
        return (0 <= personality.negative_affect <= 1 and
                0 <= personality.positive_affect <= 1)
    
