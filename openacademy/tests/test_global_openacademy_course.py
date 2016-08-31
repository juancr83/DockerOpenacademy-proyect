# -*- coding: utf-8 -*-
from psycopg2 import IntegrityError

from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    '''

    Global test to openacademy course model.
    Test create course and trigger contraints.
    '''

    #Metodo seudo - constructor del test setUp
    def setUp(self):
        # Definie las variables globales para los metodos test.
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'hola mundo'
        self.course = self.env['course']

    #Metodos de clase global que no es test
    def create_course(self, course_name, course_description, course_responsible_id):
        # Crea un courso con los parametros recibidos
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible':course_responsible_id
        })
        return course_id

    #Silencio para el error openerp.sql_db
    @mute_logger('openerp.sql_db')
    #Metodos de test se identificar por el prefijo 'def test_*(self):'
    def test_01_same_name_descripction(self):
        '''
        Test create a course with same name and description.
        To test constraint of name different to descripction.
        '''
        # Error esperado Raiser con el mensaje
        with self.assertRaisesRegexp(
                IntegrityError,
                'new row for relation "course" violates '
                'check constraint "course_name_description_check"'
                ):
            # Create un courso con el mismo nombre que la descripcion para el error raiser
            self.create_course('test','test',None)

