#!/usr/bin/env python3

from app import app
from models import db, Plant


with app.app_context():

    Plant.query.delete()

    aloe = Plant(
        id=1,
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
        is_in_stock=True,
    )

    zz_plant = Plant(
        id=2,
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
        is_in_stock=False,
    )
    dandelion = Plant(
        id=3,
        name="Dandelion",
        image="./images/dandelion.jpg",
        price=5.00,
        is_in_stock=True,
    )
    jade_plant = Plant(
        id=4,
        name="Jade Plant",
        image="./images/jade-plant.jpg",
        price=15.00,
        is_in_stock=True,
    )
    pothos = Plant(
        id=5,
        name="Pothos",
        image="./images/pothos.jpg",
        price=20.00,
        is_in_stock=False,
    )   
        

    db.session.add_all([aloe, zz_plant, dandelion, jade_plant, pothos])
    db.session.commit()
