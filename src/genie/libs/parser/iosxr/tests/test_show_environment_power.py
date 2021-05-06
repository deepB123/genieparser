import unittest
from unittest.mock import Mock

from pyats.topology import Device
from pyats.topology import loader

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.iosxr.show_environment_power import (ShowEnvironmentPower)


# ==============================
#  Unit test for 'show environment power'
# ==============================

class test_show_environment_power(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output_brief = {
        'power_module':{
            '0/PM0':{
                'input_volts':'118.0',
                'input_amps':'1.1',
                'output_volts':'12.0',
                'output_amps':'7.7',
                'supply_type':'PSU2KW-ACPI',
                'status':'OK'
            },
            '0/PM1':{
                'input_volts':'117.5',
                'input_amps':'0.8',
                'output_volts':'12.1',
                'output_amps':'4.2',
                'supply_type':'PSU2KW-ACPI',
                'status':'OK'
            }
        }
    }

    golden_output_brief = {'execute.return_value': '''
    Sat Apr 24 18:25:44.364 UTC
================================================================================
CHASSIS LEVEL POWER INFO: 0
================================================================================
   Total output power capacity (Group 0 + Group 1) :    1000W +     1000W
   Total output power required                     :    1400W
   Total power input                               :     223W
   Total power output                              :     142W

Power Group 0:
================================================================================
   Power       Supply         ------Input----   ------Output---     Status
   Module      Type            Volts     Amps    Volts     Amps    
================================================================================
   0/PM0       PSU2KW-ACPI     118.0     1.1     12.0      7.7      OK

Total of Group 0:              129W/1.1A         92W/7.7A

Power Group 1:
================================================================================
   Power       Supply         ------Input----   ------Output---     Status
   Module      Type            Volts     Amps    Volts     Amps    
================================================================================
   0/PM1       PSU2KW-ACPI     117.5     0.8     12.1      4.2      OK

Total of Group 1:               94W/0.8A         50W/4.2A

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
    '''}

    

    def test_show_environment_power(self):

        self.device = Mock(**self.golden_output_brief)
        obj = ShowEnvironmentPower(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_brief)


if __name__ == '__main__':
    unittest.main()
