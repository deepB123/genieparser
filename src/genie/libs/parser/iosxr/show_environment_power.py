''' show_environment_power.py
 IOSXR parsers for the following show commands:
    * 'show environment power'
'''

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Optional
import re


# =======================================================
# Schema for `show environment power`
# ========================================================

class ShowEnvironmentPowerSchema(MetaParser):
	schema = {
		'power_module': {
			Any(): {
			'supply_type': str,
			'input_volts': str,
			'input_amps': str,
			'output_volts': str,
			'output_amps': str,			
			'status': str,
			}
		}
	}

class ShowEnvironmentPower(ShowEnvironmentPowerSchema):
	"""Parser for show environment power on iosxr routers
	parser class - implements detail parsing mechanisms for cli output.
	"""
	cli_command = 'show environment power'
	
	""" 
Sat Apr 24 16:14:56.842 UTC
================================================================================
CHASSIS LEVEL POWER INFO: 0
================================================================================
   Total output power capacity (Group 0 + Group 1) :    1000W +     1000W
   Total output power required                     :    1400W
   Total power input                               :     223W
   Total power output                              :     141W

Power Group 0:
================================================================================
   Power       Supply         ------Input----   ------Output---     Status
   Module      Type            Volts     Amps    Volts     Amps
================================================================================
   0/PM0       PSU2KW-ACPI     117.5     1.1     12.0      7.7      OK

Total of Group 0:              129W/1.1A         92W/7.7A

Power Group 1:
================================================================================
   Power       Supply         ------Input----   ------Output---     Status
   Module      Type            Volts     Amps    Volts     Amps
================================================================================
   0/PM1       PSU2KW-ACPI     117.5     0.8     12.1      4.1      OK

Total of Group 1:               94W/0.8A         49W/4.1A

================================================================================
   Location     Card Type               Power       Power        Status
                                        Allocated   Used
                                        Watts       Watts
================================================================================
   0/RP0/CPU0   8201-SYS                1275        -            ON
   0/FT0        FAN-1RU-PI              25          -            ON
   0/FT1        FAN-1RU-PI              25          -            ON
   0/FT2        FAN-1RU-PI              25          -            ON
   0/FT3        FAN-1RU-PI              25          -            ON
   0/FT4        FAN-1RU-PI              25          -            ON

	"""

	def cli(self, output=None):
		if output is None:
			out = self.device.execute(self.cli_command)
		else:
			out = output
		power_dict = {}
		result_dict = {}
		
		"""
		Variables Parsed:
		power_module: Power Module
		supply_type: Supply Type
		input_volts: Input Volts
		input_amps: Input Amps
		output_volts: Output Volts
		output_amps: Output Amps
		status: Status
		"""
		
		p0 = re.compile(r'^\s+(?P<power_module>\d\/\S+)\s+(?P<supply_type>\S+)\s+(?P<input_volts>\S+)\s+(?P<input_amps>\S+)\s+(?P<output_volts>\d+\.\d+)\s+(?P<output_amps>\d+\.\d+)\s+(?P<status>.+)$')
		
		for line in out.splitlines():
			#line = line.strip()
			m = p0.match(line)
			if m:
				if 'power_module' not in power_dict:
					result_dict = power_dict.setdefault('power_module',{})
				supply_type = m.groupdict()['supply_type']
				input_volts = m.groupdict()['input_volts']
				input_amps = m.groupdict()['input_amps']
				output_volts = m.groupdict()['output_volts']
				output_amps = m.groupdict()['output_amps']
				status = m.groupdict()['status']
				power_module = m.groupdict()['power_module']
				result_dict[power_module] = {}
				result_dict[power_module]['input_volts'] = input_volts
				result_dict[power_module]['input_amps'] = input_amps
				result_dict[power_module]['output_volts'] = output_volts
				result_dict[power_module]['output_amps'] = output_amps
				result_dict[power_module]['supply_type'] = supply_type
				result_dict[power_module]['status'] = status
				continue
		return power_dict

