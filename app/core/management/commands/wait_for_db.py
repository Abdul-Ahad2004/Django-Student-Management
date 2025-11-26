"""
Django management command to wait for the database to be ready.
"""

import time
import socket
from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings

class Command(BaseCommand):
    """Django command to wait for the database to be available."""

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=60,
            help='Maximum time to wait for database (seconds)'
        )

    def handle(self, *args, **options):
        timeout = options['timeout']
        self.stdout.write('Waiting for database connection...')
        
        db_config = settings.DATABASES['default']
        host = db_config['HOST']
        port = int(db_config['PORT'])
        
        # First check network connectivity
        start_time = time.time()
        connected = False
        
        while not connected and (time.time() - start_time) < timeout:
            try:
                # Test socket connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    connected = True
                    self.stdout.write(f'Network connection to {host}:{port} established')
                else:
                    self.stdout.write(f'Network unreachable to {host}:{port}, retrying in 2 seconds...')
                    time.sleep(2)
            except Exception as e:
                self.stdout.write(f'Network error: {e}, retrying in 2 seconds...')
                time.sleep(2)

        if not connected:
            self.stderr.write(
                self.style.ERROR(
                    f'Failed to establish network connection to {host}:{port} within {timeout} seconds'
                )
            )
            return

        # Now test database connection
        db_up = False
        self.stdout.write('Testing database connection...')
        
        while not db_up and (time.time() - start_time) < timeout:
            try:
                # Test database connection
                connection = connections['default']
                connection.cursor()
                db_up = True
            except (OperationalError, Psycopg2Error) as e:
                self.stdout.write(f'Database unavailable: {e}, waiting 2 seconds...')
                time.sleep(2)

        if db_up:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stderr.write(
                self.style.ERROR(
                    f'Database connection failed within {timeout} seconds'
                )
            )