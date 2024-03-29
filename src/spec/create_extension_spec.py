# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="""IBL sessions specific metadata""",
        name="""ndx-ibl""",
        version="""0.1.0""",
        author=list(map(str.strip, """Cody Baker""".split(','))),
        contact=list(map(str.strip, """cody.baker@catlystneuro.com""".split(',')))
    )

    ns_builder.include_type('LabMetaData', namespace='core')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('Device', namespace='core')

    session_data = [
        {'name': 'location', 'doc': 'location', 'dtype': 'text', 'quantity': '?'},
        {'name': 'project', 'doc': 'project this session is part of', 'dtype': 'text', 'quantity': '?'},
        {'name': 'type', 'doc': 'type of session', 'dtype': 'text', 'quantity': '?'},
        {'name': 'number', 'doc': 'session number', 'dtype': 'int', 'quantity': '?'},
        {'name': 'end_time', 'doc': 'session end time', 'dtype': 'text', 'quantity': '?'},
        {'name': 'parent_session', 'doc': 'parent session', 'dtype': 'text', 'quantity': '?'},
        {'name': 'url', 'doc': 'url of the session metadata', 'dtype': 'text', 'quantity': '?'},
        {'name': 'qc', 'doc': 'qc', 'dtype': 'text', 'quantity': '?'},
        {'name': 'extended_qc', 'doc': 'extended_qc', 'dtype': 'text', 'quantity': '?'},
        {'name': 'wateradmin_session_related', 'doc': 'wateradmin_session_related', 'dtype': 'text', 'quantity': '?',
         'shape': (None,)},
        {'name': 'notes', 'doc': 'notes dictionary from sessions file', 'dtype': 'text', 'quantity': '?',
         'shape': (None,)},
        {'name': 'json', 'doc': 'json', 'dtype': 'text', 'quantity': '?'}
        ]
    ibl_session = NWBGroupSpec(
        name='Ibl_session_data',
        neurodata_type_def='IblSessionData',
        neurodata_type_inc='LabMetaData',
        doc=('IBL sessions metadata')
    )

    for i in session_data:
        ibl_session.add_dataset(**i)


    subject_data = [
        {'name': 'nickname', 'doc': 'name of the mouse', 'dtype': 'text', 'quantity': '?'},
        {'name': 'url', 'doc': 'url location of the subject metadata', 'dtype': 'text', 'quantity': '?'},
        {'name': 'responsible_user', 'doc': 'user in charge of the subject', 'dtype': 'text', 'quantity': '?'},
        {'name': 'death_date', 'doc': 'date of sacrifice of the mouse', 'dtype': 'text', 'quantity': '?'},
        {'name': 'litter', 'doc': 'litter of the mouse', 'dtype': 'text', 'quantity': '?'},
        {'name': 'strain', 'doc': 'strain of mouse', 'dtype': 'text', 'quantity': '?'},
        {'name': 'source', 'doc': 'source', 'dtype': 'text', 'quantity': '?'},
        {'name': 'line', 'doc': 'line of this mouse', 'dtype': 'text', 'quantity': '?'},
        {'name': 'projects', 'doc': 'ibl project involving this mouse', 'dtype': 'text', 'quantity': '?', 'shape': (None,)},
        {'name': 'session_projects', 'doc': 'session projects', 'dtype': 'text', 'quantity': '?', 'shape': (None,)},
        {'name': 'lab', 'doc': 'lab', 'dtype': 'text', 'quantity': '?'},
        {'name': 'alive', 'doc': 'alive/dead', 'dtype': 'bool', 'required': False},
        {'name': 'last_water_restriction', 'doc': 'last water restriction', 'dtype': 'text', 'quantity': '?'},
        {'name': 'expected_water', 'doc': 'expected water', 'dtype': 'float', 'quantity': '?'},
        {'name': 'remaining_water', 'doc': 'remaining water', 'dtype': 'float', 'quantity': '?'},
        {'name': 'weighings', 'doc': 'weighings', 'dtype': 'text', 'quantity': '?','shape': (None,)},
        {'name': 'water_administrations', 'doc': 'water_administrations', 'dtype': 'text', 'quantity': '?',
         'shape': (None,)}
    ]

    ibl_subject = NWBGroupSpec(
        name='subject',
        neurodata_type_def='IblSubject',
        neurodata_type_inc='Subject',
        doc=('IBL mice data'),
        attributes=[NWBAttributeSpec(
            **{'name': 'alive', 'doc': 'alive/dead', 'dtype': 'bool', 'required': False}
        )]
    )

    for i in subject_data:
        if i['dtype']=='bool':
            continue
        ibl_subject.add_dataset(**i)

    probes_metadata = [
        {'name': 'id', 'doc': 'id', 'dtype': 'text', 'quantity': '?'},
        {'name': 'model', 'doc': 'model', 'dtype': 'text', 'quantity': '?'},
        {'name': 'trajectory_estimate', 'doc': 'dict containing trajectory info for each probe',
         'dtype': 'text', 'quantity': '?', 'shape': (None,)}
    ]

    ibl_probes = NWBGroupSpec(
        doc='Neuro Pixels probes',
        neurodata_type_def='IblProbes',
        neurodata_type_inc='Device',
    )

    for i in probes_metadata:
        ibl_probes.add_dataset(**i)


    new_data_types = [ibl_session, ibl_subject, ibl_probes]

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    output_dir2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pynwb','ndx_ibl', 'spec'))
    # export_spec(ns_builder, new_data_types, output_dir)
    export_spec(ns_builder, new_data_types, output_dir2)

if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
