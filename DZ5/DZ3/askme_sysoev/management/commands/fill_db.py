from django.core.management.base import BaseCommand

from askme_sysoev.management.commands.real import *
from askme_sysoev.management.commands.fake import *
from askme_sysoev.management.commands.fake_likes import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
        parser.add_argument('type', type=str)


    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        type = kwargs['type']

        if type == 'real':
            RealUsers(ratio, self)
        elif type == 'fake':
            FakeUsers(ratio, self)

        fill_likes(ratio * 100)
