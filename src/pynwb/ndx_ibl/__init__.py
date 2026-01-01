import os
from pynwb import load_namespaces, get_class

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-ibl.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-ibl.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

IblSessionData = get_class('IblSessionData', 'ndx-ibl')
IblSubject = get_class('IblSubject', 'ndx-ibl')
IblProbes = get_class('IblProbes', 'ndx-ibl')
IblProbeInsertionTrajectoryTable = get_class('IblProbeInsertionTrajectoryTable', 'ndx-ibl')
IblProbeInsertionTrajectories = get_class('IblProbeInsertionTrajectories', 'ndx-ibl')

# Remove helper imports from the package namespace
del load_namespaces, get_class, os, files
