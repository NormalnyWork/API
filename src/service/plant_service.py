import appException
from database.plant import Plant
from schema.plant import PlantIn, PlantOut
from service.service import DefaultService


class PlantService(DefaultService):
    def create_plant(self, user_id: int, plant: PlantIn) -> int:
        db_plant = Plant(name=plant.name,
                         image=plant.image,
                         user_id=user_id)
        self.session.add(db_plant)
        self.session.commit()
        return db_plant.id

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

    def get_plants(self, user_id: int) -> list[PlantOut]:
        plants = self.session.query(Plant).filter_by(user_id=user_id).all()

        if not plants:
            raise appException.PlantNotFound()

        return plants #доделать

    def delete_plant(self, plant_id: int, user_id: int) -> None:
        plant = self.session.query(Plant).filter_by(id=plant_id, user_id=user_id).first()
        if not plant:
            raise appException.plant.PlantNotFound()
        self.session.delete(plant)
        self.session.commit()