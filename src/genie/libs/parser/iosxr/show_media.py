''' show_media.py
 IOSXR parsers for the following show commands:
    * 'show media'
    * 'show filesystem'
    * 'show controllers fabric plane all'
'''

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Optional
import re

# =======================================================
# Schema for `show media`
# ========================================================

class ShowMediaSchema(MetaParser):
	schema = {
		'partition': {
			Any(): {
			'size': str,
			'used': str,
			'percent': str,
			'avail': str,
			}
		}
	}

class ShowMedia(ShowMediaSchema):
	"""Parser for show media interface on iosxr routers
	parser class - implements detail parsing mechanisms for cli output.
	"""
	cli_command = 'show media'
	
	"""
	Tue Apr 13 18:43:17.452 UTC
	Media info for node0_RP0_CPU0
	------------------------------------------------------------
	Partition                    Size     Used  Percent    Avail
	disk2:                       3.8G     945M      25%     2.9G
	disk0:                       3.4G     9.6M       1%     3.2G
	/var/lib/docker              5.6G      12M       1%     5.3G
	harddisk:                     51G    1016M       3%      48G
	log:                         4.5G     253M       6%     4.0G
	------------------------------------------------------------
	log: = system log files (read-only)

	"""

	def cli(self, output=None):
		if output is None:
			out = self.device.execute(self.cli_command)
		else:
			out = output
		media_dict = {}
		result_dict = {}
		
		"""
		Variables Parsed:
		partition = Partition
		size = Size
		used = Used
		percent = Percent
		avail = Avail
		"""
		
		p0 = re.compile(r'^(?P<partition>(\w+:|\/\S+))\s+(?P<size>\S+)\s+(?P<used>\S+)\s+(?P<percent>\d+%)\s+(?P<avail>\S+)$')
		
		for line in out.splitlines():
			line = line.strip()
			m = p0.match(line)
			if m:
				if 'partition' not in media_dict:
					result_dict = media_dict.setdefault('partition',{})
				size = m.groupdict()['size']
				used = m.groupdict()['used']
				percent = m.groupdict()['percent']
				avail = m.groupdict()['avail']
				partition = m.groupdict()['partition']
				result_dict[partition] = {}
				result_dict[partition]['size'] = size
				result_dict[partition]['used'] = used
				result_dict[partition]['percent'] = percent
				result_dict[partition]['avail'] = avail
				continue
		return media_dict


# ==========================
# Parser for 'show filesystem'
# ==========================


# =======================================================
# Schema for `show filesystem`
# ========================================================

class FileSystemSchema(MetaParser):
	schema = {
		'prefixes': {
			Any(): {
			'size': str,
			'free': str,
			'type': str,
			'flags': str,
			}
		}
	}

class ShowFileSystem(FileSystemSchema):
	"""Parser for show filesystem interface on iosxr routers
	parser class - implements detail parsing mechanisms for cli output.
	"""
	cli_command = 'show filesystem'
	
	"""
Fri Apr 16 21:22:35.610 UTC
File Systems:

      Size(b)      Free(b)        Type  Flags  Prefixes
  48648003584  42960728064       flash     rw  /misc/config
            0            0     network     rw  tftp:
   4008443904   3018457088  flash-disk     rw  disk2:
            0            0     network     rw  ftp:
  54744576000  53680197632    harddisk     rw  harddisk:
   3590602752   3580395520  flash-disk     rw  disk0:

	"""

	def cli(self, output=None):
		if output is None:
			out = self.device.execute(self.cli_command)
		else:
			out = output
		filesystem_dict = {}
		result_dict = {}
		
		"""
		Variables Parsed:
		size = Size
		free = Free
		type = Type
		flags = Flags
		prefixes = Prefixes 
		"""
		
		p0 = re.compile(r'^(?P<size>\s*\d+)\s+(?P<free>\d+)\s+(?P<type>(\w+|\w+-\w+))\s+(?P<flags>\w+)\s+(?P<prefixes>(\w+:|.?\w+)*)')
		
		for line in out.splitlines():
			line = line.strip()
			m = p0.match(line)
			if m:
				if 'prefixes' not in filesystem_dict:
					result_dict = filesystem_dict.setdefault('prefixes',{})
				size = m.groupdict()['size']
				free = m.groupdict()['free']
				type_ = m.groupdict()['type']
				flags = m.groupdict()['flags']
				prefixes = m.groupdict()['prefixes']
				result_dict[prefixes] = {}
				result_dict[prefixes]['size'] = size
				result_dict[prefixes]['free'] = free
				result_dict[prefixes]['type'] = type_
				result_dict[prefixes]['flags'] = flags
				continue
		return filesystem_dict


# ==========================
# Parser for 'show controllers fabric plane all'
# ==========================

# =======================================================
# Schema for `show controllers fabric plane all`
# ========================================================

class ControllersFabricPlaneAllSchema(MetaParser):
	schema = {
		'plane_id': {
			Any(): {
			'admin_state': str,
			'plane_state': str,
			'ud_counter': str,
			'mcast_counter': str,
			}
		}
	}

class ShowControllersFabricPlaneAll(ControllersFabricPlaneAllSchema):
	"""Parser for show controller fabric plane all interface on iosxr routers
	parser class - implements detail parsing mechanisms for cli output.
	"""
	cli_command = 'show controllers fabric plane all'
	
	"""
	Thu Jul 30 13:16:17.593 UTC

	Plane Admin Plane    up->dn  up->mcast
	Id    State State    counter   counter
	--------------------------------------
	0     UP    UP             0         0 
	1     UP    UP             0         0 
	2     UP    DN             0         0 
	3     UP    DN             0         0 
	4     UP    DN             0         0 
	5     UP    DN             0         0 
	6     UP    DN             0         0 
	7     UP    DN             0         0 

	"""

	def cli(self, output=None):
		if output is None:
			out = self.device.execute(self.cli_command)
		else:
			out = output
		cfabric_dict = {}
		result_dict = {}
		
		"""
		Variables Parsed:
		plane_id = Plane ID
		admin_state = Admin State
		plane_state = Plane State
		ud_counter = up->down counter
		mcast_counter = mcast counter 
		"""
		
		p0 = re.compile(r'^(?P<plane_id>\d+)\s+(?P<admin_state>\w+)\s+(?P<plane_state>\w+)\s+(?P<ud_counter>\d+)\s+(?P<mcast_counter>\d+)')
		
		for line in out.splitlines():
			line = line.strip()
			m = p0.match(line)
			if m:
				if 'plane_id' not in cfabric_dict:
					result_dict = cfabric_dict.setdefault('plane_id',{})
				plane_id = m.groupdict()['plane_id']
				admin_state = m.groupdict()['admin_state']
				plane_state = m.groupdict()['plane_state']
				ud_counter = m.groupdict()['ud_counter']
				mcast_counter = m.groupdict()['mcast_counter']
				result_dict[plane_id] = {}
				result_dict[plane_id]['admin_state'] = admin_state
				result_dict[plane_id]['plane_state'] = plane_state
				result_dict[plane_id]['ud_counter'] = ud_counter
				result_dict[plane_id]['mcast_counter'] = mcast_counter
				continue
		return cfabric_dict


