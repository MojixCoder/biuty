from pydantic import BaseModel


class ProvinceSchema(BaseModel):
    """
    Province schema
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    """
    City schema
    """

    id: int
    province: ProvinceSchema
    name: str

    class Config:
        orm_mode = True
