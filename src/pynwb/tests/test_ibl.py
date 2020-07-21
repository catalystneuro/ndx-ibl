import datetime
import os, sys
from pynwb import NWBHDF5IO, NWBFile
import unittest

from numpy.testing import assert_equal

from src.pynwb.ndx_ibl_metadata import IblSessionData, IblSubject, IblProbes

temp_subject = {
    "nickname": "437",
    "url": "https://dev.alyx.internationalbrainlab.org/subjects/437",
    "subject_id": "c7a4c517-61b9-48ec-bfbe-30a8f419b5bb",
    "responsible_user": "ines",
    "date_of_birth": datetime.datetime(2018, 6, 26, tzinfo=datetime.timezone.utc),
    "age": "25",
    "death_date": "2018-12-21",
    "species": "Laboratory mouse",
    "sex": "M",
    "litter": None,
    "strain": None,
    "source": "CCU - Margarida colonies",
    "line": "Sert-Cre",
    "projects": [
      "ibl_behaviour_pilot_matlabrig"
    ],
    "session_projects": [
      "ibl_neuropixel_brainwide_01",
      "ibl_behaviour_pilot_matlabrig"
    ],
    "lab": "mainenlab",
    "genotype": "",
    "description": "",
    "alive": False,
    "weight": "29.0",
    "last_water_restriction": None,
    "expected_water": 1.1312,
    "remaining_water": 1.1312
  }

temp_sessions = {
    "subject": "NYU-21",
    "location": "_iblrig_angelakilab_behavior_2",
    "procedures": [
        "Behavior training/tasks"
    ],
    "project": "ibl_neuropixel_brainwide_01",
    "type": "Experiment",
    "number": 1,
    "end_time": datetime.datetime.utcnow().strftime('%Y-%M-%dT%X'),
    "narrative": "",
    "parent_session": None,
    "url": "https://dev.alyx.internationalbrainlab.org/sessions/2183d76f-3469-4a4b-be08-5f0e58ca797d",
    "extended_qc": None,
    "qc": "20",
}
temp_session_nwbfile = {
    "keywords": ["angelakilab", "jeanpaul", "IBL"],
    "experiment_description": "ibl_neuropixel_brainwide_01",
    "experimenter":"jeanpaul",
    "lab":"angelakilab",
    "protocol":"_iblrig_tasks_trainingChoiceWorld6.4.0",
    "notes":"Behavior training/tasks"
}

temp_probes = [
    {
      "id": "eda7a3ac-f038-4603-9c68-816234e9c4eb",
      "model": "3B2",
      "name": "probe00",
      "trajectory_estimate": [
        {
          "id": "99e948f4-b46d-422c-9306-4d49ed5c1b53",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Micro-manipulator",
          "x": -2208.0,
          "y": -2976.2,
          "z": -576.3,
          "depth": 4000.3,
          "theta": 15.0,
          "phi": 180.0,
          "roll": 0.0,
          "json": None
        },
        {
          "id": "ea321a80-3e8d-4cbe-b956-78c1cd5f10de",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Planned",
          "x": -2243.0,
          "y": -3000.0,
          "z": -122.0,
          "depth": 4000.0,
          "theta": 15.0,
          "phi": 180.0,
          "roll": 0.0,
          "json": None
        }
      ]
    },
    {
      "id": "dd619e10-5df1-4c79-bd62-cc00937b5d36",
      "model": "3B2",
      "name": "probe01",
      "trajectory_estimate": [
        {
          "id": "49daab43-ea10-44ba-bbd9-a574c6cf67c9",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Micro-manipulator",
          "x": -2347.0,
          "y": -2252.0,
          "z": -954.4,
          "depth": 5599.9,
          "theta": 10.0,
          "phi": 0.0,
          "roll": 0.0,
          "json": None
        },
        {
          "id": "a42f9a17-f38c-4d0d-ab14-132eb38663ad",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Planned",
          "x": -2346.0,
          "y": -2250.0,
          "z": -169.0,
          "depth": 6670.0,
          "theta": 10.0,
          "phi": 0.0,
          "roll": 0.0,
          "json": None
        }
      ]
    }
  ]

def set_up_nwbfile(**kwargs):
    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
        **kwargs
    )
    return nwbfile
#--Sessions test
session_data = IblSessionData(**temp_sessions)
for i,j in temp_sessions.items():
    assert_equal(getattr(session_data,i),j)
#--Subject test
subject_data = IblSubject(**temp_subject)
for i,j in temp_subject.items():
    assert_equal(getattr(subject_data,i),j)
#--Probes test
probe_data = []
for c,i in enumerate(temp_probes):
    name = i.pop('name')
    for y, l in enumerate(i['trajectory_estimate']):
        i['trajectory_estimate'][y] = str(l)
    probe_data.append(IblProbes(name, **i))
    for j,k in i.items():
        assert_equal(getattr(probe_data[c], j),k)


nwbfile = set_up_nwbfile(**temp_session_nwbfile)
nwbfile.add_lab_meta_data(session_data)
nwbfile.subject = subject_data
for i in probe_data:
    nwbfile.add_device(i)

with NWBHDF5IO('test.nwb', mode='w') as io:
    io.write(nwbfile)

with NWBHDF5IO('test.nwb', mode='r', load_namespaces=True) as io:
    read_nwbfile = io.read()
    for i, j in temp_sessions.items():
        if getattr(read_nwbfile.lab_meta_data,i,None):
            assert_equal(getattr(read_nwbfile.lab_meta_data, i), j)
    for i, j in temp_subject.items():
        if getattr(read_nwbfile.subject, i, None):
            assert_equal(getattr(read_nwbfile.subject, i), j)
