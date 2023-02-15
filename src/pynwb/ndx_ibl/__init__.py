import os
from pynwb import load_namespaces, get_class

ibl_metadata_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-ibl.namespace.yaml'
)

if not os.path.exists(ibl_metadata_specpath):
    ibl_metadata_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-ibl.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ibl_metadata_specpath)

IblSessionData = get_class('IblSessionData', 'ndx-ibl')
IblSubject = get_class('IblSubject', 'ndx-ibl')
IblProbes = get_class('IblProbes', 'ndx-ibl')
