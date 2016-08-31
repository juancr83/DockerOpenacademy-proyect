# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This create global test to sessions
    '''
    # Seudo-constructor method
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['session']
        self.partner_vauxoo = self.env.ref('base.res_partner_23')
        self.course = self.env.ref('openacademy.course1')
        self.partner_attende = self.env.ref('base.res_partner_5')

    # Generic methods

    # Test methods
    def test_10_instructor_is_attende(self):
        '''
        Check that raise of 'A sessio's instructor can't be an attendee'
        '''

        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
            ):
            self.session.create({
                'name': 'Session test 1',
                'seats': '2',
                'instructor': self.partner_vauxoo.id,
                'attendees': [(6, 0, [self.partner_vauxoo.id])],
                'course': self.course.id,
            })

    
    def test_20_wkf_done(self):
        '''
        Check that the workflow work fine!
        '''
        session_test = self.session.create({
            'name': 'Session test 1',
            'seats': '1',
            'instructor': self.partner_vauxoo.id,
            'attendees': [(6, 0, [self.partner_attende.id])],
            'course': self.course.id,
        })
        #print "*****************"*10,   "llegue aqui bien"
        # Check initial state
        self.assertEqual(session_test.state, 'draft', 'Initial State should be in draft')
        
        # Change next state and check it
        session_test.signal_workflow('button_confirm')
        #print '*'*20, "session_test.state , ", session_test.state
        self.assertEqual(session_test.state, 'confirmed', "Singnal confirm don't worw")

        # Change next state and check it
        session_test.signal_workflow('button_done')
        self.assertEqual(session_test.state, 'done', "Singnal done don't worw")
        # self.env.cr.commit()

