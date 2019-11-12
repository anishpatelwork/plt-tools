from plttools import plt_calculator, ep_curve
import pytest
import pandas as pd

def test_calculate_plt():
  aal = plt_calculator.calculate_AAL(test_plt, 5)
  assert aal == pytest.approx(900, rel=1)
    
def test_calculate_oep_curve():
  oep = plt_calculator.calculate_OEP_curve(test_plt, 5)
  assert type(oep) is ep_curve.EPCurve
  assert oep.loss_at_a_given_return_period(5) == 900
  assert oep.loss_at_a_given_return_period(2.5) == 800
  assert oep.loss_at_a_given_return_period(5/3) == 300
  assert oep.loss_at_a_given_return_period(1.25) == 100
  assert oep.loss_at_a_given_return_period(1) == 0
  

def test_calculate_aep_curve():
  aep = plt_calculator.calculate_AEP_curve(test_plt, 5)
  assert type(aep) is ep_curve.EPCurve
  assert aep.loss_at_a_given_return_period(5) == 3000
  assert aep.loss_at_a_given_return_period(2.5) == 900
  assert aep.loss_at_a_given_return_period(5/3) == 500
  assert aep.loss_at_a_given_return_period(1.25) == 100
  assert aep.loss_at_a_given_return_period(1) == 0


data = [
  {
    "periodId": 1,
    "eventId": 3500016,
    "lossDate": "3/13/2016 12:00:00 AM",
    "eventDate": "03/10/2016 00:00",
    "loss": 100
  },
  {
    "periodId": 3,
    "eventId": 3500129,
    "lossDate": "8/25/2016 12:00:00 AM",
    "eventDate": "8/24/2016 12:00:00 AM",
    "loss": 200
  },
  {
    "periodId": 3,
    "eventId": 3500140,
    "lossDate": "01/01/2017 00:00",
    "eventDate": "12/29/2016 12:00:00 AM",
    "loss": 300
  },
  {
    "periodId": 4,
    "eventId": 3500141,
    "lossDate": "01/10/2016 00:00",
    "eventDate": "01/09/2016 00:00",
    "loss": 400
  },
  {
    "periodId": 4,
    "eventId": 3500141,
    "lossDate": "01/11/2016 00:00",
    "eventDate": "01/09/2016 00:00",
    "loss": 500
  },
  {
    "periodId": 4,
    "eventId": 3500141,
    "lossDate": "1/13/2016 12:00:00 AM",
    "eventDate": "01/09/2016 00:00",
    "loss": 600
  },
  {
    "periodId": 4,
    "eventId": 3500141,
    "lossDate": "1/14/2016 12:00:00 AM",
    "eventDate": "01/09/2016 00:00",
    "loss": 700
  },
  {
    "periodId": 4,
    "eventId": 3500151,
    "lossDate": "8/19/2016 12:00:00 AM",
    "eventDate": "8/19/2016 12:00:00 AM",
    "loss": 800
  },
  {
    "periodId": 5,
    "eventId": 3500166,
    "lossDate": "9/19/2016 12:00:00 AM",
    "eventDate": "9/19/2016 12:00:00 AM",
    "loss": 900
  }
]

test_plt = pd.DataFrame(data)