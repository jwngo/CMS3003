from .models import *

def saveIncidentToFirebase(request):
  data = request.POST.copy()
  i_type = data.getlist('type_of_incident')
  num_of_casualties = data.get('num_of_casualties')
  assitance_requested = data.getlist('assitance_requested')
  num_ambulance = data.get('num_ambulance_requested')
  num_firetruck = data.get('num_firetruck_requested')
  num_police = data.get('num_police_requested')
  num_gasleak = data.get('num_gasleak_requested')
  reporter_name = data.get('reporter_name')
  reporter_number = data.get('reporter_number')
  i_address = data.get('i_address')
  i_postalcode = data.get('i_postalcode')
  i_description = data.get('i_description')
  managedBy = request.user.username

  