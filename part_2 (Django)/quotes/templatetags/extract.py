from bson.objectid import ObjectId
from django import template
from ..utils import get_mongodb

register = template.Library()


def get_author(id):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id)})
    return author['fullname']


register.filter('author', get_author)
