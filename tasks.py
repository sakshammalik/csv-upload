from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

celery = Celery(
    'tasks',
    broker='amqp://admin:saksham007@localhost:5672/vhost'
)

engine = create_engine('postgresql:///products')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@celery.task()
def upload_file(products):
    for product in products:
        prod = models.Product(sku=product['sku'], name=product['name'],
                              description=product['description'], status='active')
        session.merge(prod)
        session.commit()
    return 'success'
