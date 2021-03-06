.. _examples:

***************
Examples
***************

This page shows some examples of using the PFx Brick API.

Brick Enumeration, Connection, Info Query
-----------------------------------------

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to retrieve basic information about the
  # brick including its identity and configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks

  bricks = find_bricks(True)
  print('%d PFx Bricks found' % (len(bricks)))

  if bricks:
      for b in bricks:
          brick = PFxBrick()
          res = brick.open(b)
          if not res:
              print("Unable to open session to PFx Brick")
          else:
              print('PFx Brick Status / Identity')
              print('===========================')
              print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
              brick.get_name()
              print('PFx Brick name        : %s' %(brick.name))
              brick.get_status()
              brick.print_status()
              print('PFx Brick Configuration')
              print('=======================')
              brick.get_config()
              brick.print_config()
              brick.close()

Changing Configuration
----------------------

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to showing modification to the
  # brick configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks
  from pfxbrick.pfx import *

  bricks = find_bricks()
  print('%d PFx Bricks found' % (len(bricks)))

  if bricks:
      brick = PFxBrick()
      res = brick.open()
      if not res:
          print("Unable to open session to PFx Brick")
      else:
          print('PFx Brick Configuration')
          print('=======================')
          brick.get_config()
          brick.print_config()

          print("Change the volume beep setting...")
          if brick.config.settings.volumeBeep == PFX_CFG_VOLBEEP_ON:
              brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_OFF
          else:
              brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_ON
          brick.set_config()

          print('PFx Brick Updated Configuration')
          print('===============================')
          brick.get_config()
          brick.print_config()

          brick.close()

Modifying the Event/Action LUT
------------------------------

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to show access to the event/action LUT

  import hid
  import time
  import copy
  from pfxbrick import PFxBrick, PFxAction, find_bricks
  from pfxbrick.pfx import *

  brick = PFxBrick()
  brick.open()

  left_button_ch1 = brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0)
  print("Get action for Left Button Ch 1 on Speed Remote...")
  print(left_button_ch1)

  print("Add a light effect to this action...")
  new_left_action = copy.copy(left_button_ch1)
  new_left_action.light_on([1,2,3,4])
  print(new_left_action)

  print("Save new action back to brick...")
  brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, new_left_action)
  print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))
  time.sleep(1)

  print("Restore the original action without the change...")
  brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, left_button_ch1)
  print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))

  brick.close()

Copying Audio Files
-------------------

Copy file to PFx Brick specified by command line arguments:

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to show copying files to the PFx Brick

  import hid
  from pfxbrick import PFxBrick
  from sys import argv

  if len(argv) < 3:
      print("Usage: ./filecopy.py <filename> <id>")
      print("  where <filename> is the local file to copy")
      print("        <id> is the unique file ID to assign the file on the PFx Brick")
  else:
      brick = PFxBrick()
      brick.open()

      fn = argv[1]
      fid = int(argv[2])
      print("Copying %s to brick with id %d..." % (fn, fid))
      brick.put_file(fid, fn)
      brick.refresh_file_dir()
      print(brick.filedir)

      brick.close()

Copy a list of files to the PFx Brick:

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to show copying files to the PFx Brick

  import hid
  from pfxbrick import PFxBrick
  from sys import argv

  files = ['beep1.wav', 'beep2.wav', 'siren1.wav', 'anthem.wav']

  brick = PFxBrick()
  brick.open()

  for i,file in enumerate(files):
      print("Copying %s to brick with id %d..." % (file, i))
      brick.put_file(i, file, show_progres=True)

  brick.refresh_file_dir()
  print(brick.filedir)

  brick.close()

Scripting Actions
-----------------

A demonstration of scripting multiple actions involving motors, lighting, and sound:

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to demonstrate multiple scripted actions

  import hid
  import time
  import random
  from pfxbrick import PFxBrick, PFxAction
  from pfxbrick.pfx import *

  brick = PFxBrick()
  brick.open()

  audiofile = 2
  max_speed = 100

  # start looped audio playback and set volume
  brick.test_action(PFxAction().repeat_audio_file(audiofile))
  brick.test_action(PFxAction().set_volume(75))

  # ramp up the motor speed gradually to max_speed
  for x in range(max_speed):
      brick.test_action(PFxAction().set_motor_speed([1], x))
      # show a random light pattern
      y = random.randint(1,8)
      brick.test_action(PFxAction().light_toggle([y]))
      time.sleep(0.1)

  # ramp down the motor speed gradually to 0%

  for x in range(max_speed):
      brick.test_action(PFxAction().set_motor_speed([1], max_speed-x-1))
      # show a random light pattern
      y = random.randint(1,8)
      brick.test_action(PFxAction().light_toggle([y]))
      time.sleep(0.1)

  # stop motor and turn off audio and lights
  brick.test_action(PFxAction().stop_motor([1]))
  brick.test_action(PFxAction().stop_audio_file(audiofile))
  brick.test_action(PFxAction().light_off(range(1,9))

  brick.close()



