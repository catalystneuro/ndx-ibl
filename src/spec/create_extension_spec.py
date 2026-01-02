# -*- coding: utf-8 -*-

import os.path

from hdmf.spec import RefSpec
from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="""IBL sessions specific metadata""",
        name="""ndx-ibl""",
        version="""0.2.0""",
        author=list(map(str.strip, """Cody Baker""".split(','))),
        contact=list(map(str.strip, """cody.baker@catlystneuro.com""".split(',')))
    )

    ns_builder.include_type('LabMetaData', namespace='core')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('Device', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')

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
        {'name': 'uuid', 'doc': 'unique identifier of the subject in Alyx database', 'dtype': 'text', 'quantity': '?'},
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
        {'name': 'expected_water_ml', 'doc': 'expected water in milliliters', 'dtype': 'float', 'quantity': '?'},
        {'name': 'remaining_water_ml', 'doc': 'remaining water in milliliters', 'dtype': 'float', 'quantity': '?'},
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

    # IblProbeInsertionTrajectoryTable - DynamicTable for storing probe insertion geometry
    trajectory_table = NWBGroupSpec(
        neurodata_type_def='IblProbeInsertionTrajectoryTable',
        neurodata_type_inc='DynamicTable',
        doc='Probe insertion trajectory parameters for a single probe. Each row represents a trajectory '
            'estimate from a different provenance level, progressing from theoretical to validated: '
            'Planned (pre-surgical target), Micro-manipulator (recorded during surgery), '
            'Histology track (traced from post-mortem brain slices), and Ephys aligned histology track '
            '(histology refined using electrophysiology). '
            'Insertion point coordinates (x, y, z) are bregma-centered with units in micrometers: '
            'x is ML (medio-lateral, positive=right), y is AP (anterior-posterior, positive=anterior), '
            'z is DV (dorso-ventral, positive=dorsal). '
            'Angles characterize the spatial orientation of the probe: '
            'theta is polar angle from vertical (0=straight down into brain, 90=horizontal), '
            'phi is azimuth angle from the AP axis (0=tilted anteriorly, 90=tilted left, 180=posteriorly), '
            'roll defines the electrode-facing direction (rotation around probe axis). '
            'Depth is the insertion distance along the probe axis from the brain surface entry point to the probe tip.',
        datasets=[
            NWBDatasetSpec(
                name='device',
                neurodata_type_inc='VectorData',
                dtype=RefSpec(target_type='Device', reftype='object'),
                doc="Reference to the Device object (e.g., NeuropixelsProbe) being localized. "
                    "This links the trajectory to the actual probe device in the NWB file."
            ),
            NWBDatasetSpec(
                name='x',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Insertion point ML (medio-lateral) coordinate in micrometers, bregma-centered. "
                    "Positive values are right of midline, negative are left. This is where the probe "
                    "enters the brain surface. For histology-derived trajectories, computed from the "
                    "intersection of the fitted probe track with brain surface."
            ),
            NWBDatasetSpec(
                name='y',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Insertion point AP (anterior-posterior) coordinate in micrometers, bregma-centered. "
                    "Positive values are anterior to bregma, negative are posterior. This is where the probe "
                    "enters the brain surface. For histology-derived trajectories, computed from the "
                    "intersection of the fitted probe track with brain surface."
            ),
            NWBDatasetSpec(
                name='z',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Insertion point DV (dorso-ventral) coordinate in micrometers, bregma-centered. "
                    "Typically negative values (brain surface is below bregma skull landmark level). "
                    "Values vary with AP position due to brain surface curvature. This is where the probe "
                    "enters the brain surface. For histology-derived trajectories, computed from the "
                    "intersection of the fitted probe track with brain surface."
            ),
            NWBDatasetSpec(
                name='depth_um',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Insertion depth in micrometers, measured along the probe axis from the brain surface "
                    "insertion point to the probe tip. This indicates how far the probe travels into the brain. "
                    "For histology-derived trajectories, computed as the Euclidean distance between entry point "
                    "and the deepest traced point projected onto the fitted trajectory line."
            ),
            NWBDatasetSpec(
                name='theta',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Polar angle in degrees measuring probe tilt from vertical. 0 degrees means the probe "
                    "is inserted straight down into the brain (along DV axis), 90 degrees means horizontal. "
                    "For histology-derived trajectories, computed using spherical coordinates: "
                    "theta = arccos(dz/depth) where dz is the vertical component of the entry-to-tip vector."
            ),
            NWBDatasetSpec(
                name='phi',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Azimuth angle in degrees defining the direction of probe tilt in the horizontal plane. "
                    "Measured counter-clockwise from the positive AP axis when viewed from above: "
                    "0 = tilted anteriorly, 90 = tilted left, 180 = tilted posteriorly, 270 = tilted right. "
                    "For histology-derived trajectories, computed using spherical coordinates: phi = arctan2(dy, dx)."
            ),
            NWBDatasetSpec(
                name='roll',
                neurodata_type_inc='VectorData',
                dtype='float',
                doc="Probe rotation around its own longitudinal axis in degrees. Determines which direction "
                    "the electrode sites face. A value of 0 typically indicates electrodes facing anterior.",
                quantity='?'
            ),
            NWBDatasetSpec(
                name='provenance',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc="Method used to determine this trajectory estimate, representing increasing confidence: "
                    "'Planned' (pre-surgical target coordinates from experimental design), "
                    "'Micro-manipulator' (coordinates recorded from stereotaxic manipulator during surgery), "
                    "'Histology track' (traced from post-mortem brain slices by fitting a line through "
                    "manually picked points), 'Ephys aligned histology track' (histology refined by aligning "
                    "detected unit depths with the histology trace).",
                quantity='?'
            ),
        ]
    )

    # IblProbeInsertionTrajectories - LabMetaData wrapper containing multiple IblProbeInsertionTrajectoryTable objects
    # This follows the same pattern as ndx-anatomical-localization's Localization container
    # Each probe gets its own table named simply "Probe00", "Probe01" etc. (nesting provides context)
    probe_trajectories = NWBGroupSpec(
        name='ibl_probe_insertion_trajectories',
        neurodata_type_def='IblProbeInsertionTrajectories',
        neurodata_type_inc='LabMetaData',
        doc='Container for IBL probe insertion trajectory information stored as lab metadata. Contains one '
            'IblProbeInsertionTrajectoryTable per probe, with insertion geometry parameters. Each table is '
            'named after the probe (e.g., "Probe00", "Probe01").',
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='IblProbeInsertionTrajectoryTable',
                doc='Table of probe insertion trajectory parameters for a single probe',
                quantity='*'
            )
        ]
    )

    new_data_types = [ibl_session, ibl_subject, ibl_probes, trajectory_table, probe_trajectories]

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)

if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
