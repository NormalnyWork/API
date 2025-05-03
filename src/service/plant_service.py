from sqlalchemy.orm import joinedload

import appException
from database.plant import Plant, Care
from schema.plant import PlantIn, CareOut, CareIn, PlantOut, PlantWithCareIn
from service.service import DefaultService


class PlantService(DefaultService):
    def create_plant_with_care(self, user_id: int, plant: PlantWithCareIn) -> int:
        db_plant = Plant(name=plant.name, image=plant.image, user_id=user_id)
        self.session.add(db_plant)
        self.session.commit()

        plant_id = db_plant.id

        for care_type, care_data in plant.dict().items():
            if care_type not in ["name", "image"]:
                if care_data:
                    care_db = Care(
                        type=care_type.upper(),
                        interval=care_data['interval'],
                        count=care_data['count'],
                        plant_id=plant_id,
                        user_id=user_id
                    )
                    self.session.add(care_db)

        self.session.commit()

        return plant_id

    def get_plants(self, user_id: int) -> list[PlantOut]:
        plants = (
            self.session.query(Plant)
            .options(joinedload(Plant.care))
            .filter_by(user_id=user_id)
            .all()
        )

        if not plants:
            raise appException.PlantNotFound()

        result = []

        for plant in plants:
            care_fields = {}

            for care in plant.care:
                care_type = care.type
                care_fields[care_type] = {
                    "id": care.id,
                    "interval": care.interval,
                    "count": care.count
                }

            plant_data = {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                **care_fields
            }

            result.append(PlantOut(**plant_data))

        return result

    def update_plant(
            self, plant_id: int, user_id: int, patch: PlantIn
    ) -> None:
        plant = (
            self.session.query(Plant)
            .filter_by(id=plant_id, user_id=user_id)
            .first()
        )

        if not plant:
            raise appException.plant.PlantNotFound()

        self.session.query(Plant).filter_by(
            id=plant_id, user_id=user_id
        ).update(
            values=patch.model_dump(exclude_none=True)
        )
        self.session.commit()

    def delete_plant(self, plant_id: int, user_id: int) -> None:
        plant = self.session.query(Plant).filter_by(id=plant_id, user_id=user_id).first()
        if not plant:
            raise appException.plant.PlantNotFound()
        self.session.delete(plant)
        self.session.commit()

    def get_care(self, care_id: int, user_id: int) -> CareOut:
        care = self.session.query(Care).filter_by(id=care_id, user_id=user_id).first()
        if not care:
            raise appException.plant.CareNotFound()

        return care

    def update_care(self, care_id: int, user_id: int, care_patch: CareIn) -> None:
        care = (
            self.session.query(Care)
            .filter_by(id=care_id, user_id=user_id)
            .first()
        )

        if not care:
            raise appException.plant.CareNotFound()

        self.session.query(Care).filter_by(
            id=care_id, user_id=user_id
        ).update(
            values=care_patch.model_dump(exclude_none=True)
        )
        self.session.commit()

    def delete_care(self, care_id: int, user_id: int):
        care = self.session.query(Care).filter_by(id=care_id, user_id=user_id).first()

        if not care:
            raise appException.plant.CareNotFound()

        self.session.delete(care)
        self.session.commit()


    # def create_care(self, plant_id: int, user_id: int, care: list[CareIn]) -> list[int]:
    #     plant = self.session.query(Plant).filter_by(id=plant_id, user_id=user_id).first()
    #     if not plant:
    #         raise appException.plant.PlantNotFound()
    #
    #     care_db_list = []
    #     for care in care:
    #         care_db = Care(
    #             type=care.type,
    #             interval=care.interval,
    #             count=care.count,
    #             plant_id=plant_id,
    #             user_id=user_id
    #         )
    #         care_db_list.append(care_db)
    #         self.session.add(care_db)
    #
    #     self.session.commit()
    #     return [care.id for care in care_db_list]
    # def create_plant(self, user_id: int, plant: PlantIn) -> int:
    #     db_plant = Plant(name=plant.name, image=plant.image, user_id=user_id)
    #     self.session.add(db_plant)
    #     self.session.commit()
    #     return db_plant.id