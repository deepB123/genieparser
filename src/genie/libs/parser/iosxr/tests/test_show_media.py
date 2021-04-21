import unittest
from unittest.mock import Mock

from pyats.topology import Device
from pyats.topology import loader

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.iosxr.show_media import (ShowMedia, ShowFileSystem, ShowControllersFabricPlaneAll)

# ==============================
#  Unit test for 'show media'
# ==============================

class test_show_media(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output_brief = {
        'partition':{
            'disk2:':{
                'size':'3.8G',
                'used':'945M',
                'percent':'25%',
                'avail':'2.9G'
            },
            'disk0:':{
                'size':'3.4G',
                'used':'9.6M',
                'percent':'1%',
                'avail':'3.2G'
            },
            '/var/lib/docker':{
                'size':'5.6G',
                'used':'12M',
                'percent':'1%',
                'avail':'5.3G'
            },
            'harddisk:':{
                'size':'51G',
                'used':'1016M',
                'percent':'3%',
                'avail':'48G'
            },
            'log:':{
                'size':'4.5G',
                'used':'253M',
                'percent':'6%',
                'avail':'4.0G'
            }
        }
    }

    golden_output_brief = {'execute.return_value': '''
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
        '''}

    

    def test_show_media(self):

        self.device = Mock(**self.golden_output_brief)
        obj = ShowMedia(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_brief)


# ==============================
#  Unit test for 'show filesystem'
# ==============================

class test_show_filesystem(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output_brief = {
        'prefixes':{
            '/misc/config':{
                'size':'48648003584',
                'free':'42960707584',
                'type':'flash',
                'flags':'rw'
            },
            'tftp:':{
                'size':'0',
                'free':'0',
                'type':'network',
                'flags':'rw'
            },
            'disk2:':{
                'size':'4008443904',
                'free':'3018457088',
                'type':'flash-disk',
                'flags':'rw'
            },
            'ftp:':{
                'size':'0',
                'free':'0',
                'type':'network',
                'flags':'rw'
            },
            'harddisk:':{
                'size':'54744576000',
                'free':'53680197632',
                'type':'harddisk',
                'flags':'rw'
            },
            'disk0:':{
                'size':'3590602752',
                'free':'3580395520',
                'type':'flash-disk',
                'flags':'rw'
            }
        }
    }

    golden_output_brief = {'execute.return_value': '''
    Fri Apr 16 21:22:35.610 UTC
    File Systems:

          Size(b)      Free(b)        Type  Flags  Prefixes
      48648003584  42960728064       flash     rw  /misc/config
                0            0     network     rw  tftp:
       4008443904   3018457088  flash-disk     rw  disk2:
                0            0     network     rw  ftp:
      54744576000  53680197632    harddisk     rw  harddisk:
       3590602752   3580395520  flash-disk     rw  disk0:
        '''}

    

    def test_show_filesystem(self):

        self.device = Mock(**self.golden_output_brief)
        obj = ShowFileSystem(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_brief)

# ==============================
#  Unit test for 'show controllers fabric plane all'
# ==============================

class test_show_controllers_fabric_plane_all(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output_brief = {
        "plane_id":{
            "0":{
                "admin_state":"01",
                "plane_state":"01",
                "ud_counter":"08",
                "mcast_counter":"00"
            },
            "1":{
                "admin_state":"01",
                "plane_state":"01",
                "ud_counter":"08",
                "mcast_counter":"00"
            },
            "2":{
                "admin_state":"01",
                "plane_state":"01",
                "ud_counter":"08",
                "mcast_counter":"00"
            },
            "3":{
                "admin_state":"01",
                "plane_state":"01",
                "ud_counter":"08",
                "mcast_counter":"00"
            },
            "4":{
                "admin_state":"01",
                "plane_state":"01",
                "ud_counter":"08",
                "mcast_counter":"00"
            }
        }
    }

    golden_output_brief = {'execute.return_value': '''
    Wed Apr 21 12:57:31.330 UTC

    Flags: Admin State: 1-Up 2-Down 12-UnPowered 16-Shutdown
        Oper  State: 1-Up 2-Down 3-Admin Down

    Summary for All Fabric Planes:

    Plane Id   Admin State     Oper State      Links Up    Links Down  In Pkt Count    Out Pkt count
    =============================================================================================
    0            01              01              08          00          124213051            139057223
    1            01              01              08          00          97892932            97892932
    2            01              01              08          00          97700144            97700144
    3            01              01              08          00          100769940            100769940
    4            01              01              08          00          100787722            100787722
    '''}

    

    def test_show_controllers_fabric_plane_all(self):

        self.device = Mock(**self.golden_output_brief)
        obj = ShowControllersFabricPlaneAll(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_brief)


if __name__ == '__main__':
    unittest.main()
