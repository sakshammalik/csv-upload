from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import random

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
    statuses = ['active', 'inactive']
    for product in products:
        status = random.choice(statuses)
        prod = models.Product(sku=product['sku'], name=product['name'],
                              description=product['description'], status=status)
        session.merge(prod)
        session.commit()
    return 'success'
