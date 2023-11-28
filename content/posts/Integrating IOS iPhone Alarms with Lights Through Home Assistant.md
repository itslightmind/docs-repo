---
Title: Integrating IOS iPhone Alarms with Lights Through Home Assistant (IOS 17)
created: 2023-11-27
modified: 2023-11-28
---

Showcase (Over The Span of 30 minutes):  
![A001_11280005_C002.gif](A001_11280005_C002.gif)

## Background and Inspiration

First off, this was a fun project that started out fairly small and I've made incremental changes to the point where its been super stable and I feel like with the recent IOS changes that others might be interested in looking at the setup & code.

## Why Should You Do This?

This system has been running VERY consistently for me. And I think it's not that big of a hassle since other users have shared their work and I've built upon it to connect it all up into my system. So let's talk about the general theory about this.

## System Overview

1. Set a morning alarm on your iPhone
1. Home Assistant receives this through an Apple shortcut
1. a set amount of minutes before alarm, lights turn on, and shift from warm to daylight, as well as brighten.
1. ???

# Setting up Helper In HA

[Settings > Devices & Services > Helpers](https://my.home-assistant.io/redirect/helpers/)

1. Create a new helper, and select Date and/or time  
   ![Date_And_Time_HA_Alarm.png](Date_And_Time_HA_Alarm.png)
1. Make sure you select **Date and time** for the input that's VERY important for this to work.  
   ![create_date_and_time_HA_Alarm.png](create_date_and_time_HA_Alarm.png)  
   Now that you've added a Helper for the apple alarm. what you'll want to do is add the shortcut on mobile.  
   [HA Sync iOS 17 Sleep Alarm Shortcut](https://www.icloud.com/shortcuts/e71ab4d7795b4283833e9b0ee7d8b140)

Once you have added the shortcut, you will need to grant it access to the HA app and allow the service to call the clock as well. To prompt this, you can either try running the automation or tap the "i" button at the bottom of the screen.  
Please note that this shortcut has only one value that may require adjustment by the end user, which is the name set for the helper. By default, it is set as "input_datetime.apple_alarm_helper," so it should work without any changes if you had named the helper "apple_alarm_helper" in HA.

After making any necessary adjustments, try running the shortcut to test its functionality. If it works, you should see the time in the HA helper change accordingly.

![Pasted image 20231127224421.png](Pasted%20image%2020231127224421.png)

Now that we've gotten the alarm value in the helper working. We should add a few automations to improve the QOL so your not having to manually run the shortcut every night. The two automations that i like to run are

1. When Clock app closes run HA Sync iOS 17 Sleep Alarm Shortcut
1. At 3AM run HA Sync iOS 17 Sleep Alarm Shortcut
   1. (if you dont have a scheduled time send, the HA wont do regular alarms) 

# Final Stretch for HA

Now that we've gotten that setup we'll now move on to HA light system which is comprised of two parts the first side is an Automation under "Automations & Scenes" which calls on the light management script when its the correct time.

The general gist of the automation is that it checks every minute if its the correct time specified by the offset_minutes value. So if you set the value to 40 as in my example the lights will start coming up 40 minutes early. You can change the value of the offset as well as what time value it tries to pull from you can leave this the same unless you changed the handler in the previous steps.

````
as_timestamp(states('input_datetime.apple_alarm_helper'))
````

There is also the entity_id which is the script name that controls the lights

````
entity_id: script.wled_alarm_brightness_and_color_temperature
````

Here's the entire HA automation.

````
alias: Toggle Light Based on Alarm Time
description: Turn on light based on the alarm time difference.
trigger:
  - platform: time_pattern
    minutes: /1
condition:
  - condition: template
    value_template: >
      {% set alarm_time =
      as_timestamp(states('input_datetime.apple_alarm_helper')) %} {% set
      current_time = as_timestamp(now()) %} {% set time_diff = (alarm_time -
      current_time) / 60 %} {% if 0 < time_diff <= offset_minutes %}
        true
      {% else %}
        false
      {% endif %}
action:
  - service: script.turn_on
    target:
      entity_id: script.wled_alarm_brightness_and_color_temperature
    data:
      variables:
        offset_minutes: "{{ offset_minutes }}"
variables:
  offset_minutes: 40 # Change the time here
mode: single
````

And here's the second part on the HA side. This will be added under the "Scripts" section under "Automations & Scenes" Which turns on in this example a WLED RGB light, as well as a single bi colored light. To add or change it you will need to find the light.XXX of the devices you want to include.

````
alias: WLED Alarm Smooth Morning Light Transition
variables:
  rgb_lights:
    - light.wled
  bi_color_lights:
    - light.left_key_light
  step_count: 60
  target_brightness_pct: 100
  offset_minutes: "{{ offset_minutes | default(0.01) }}"
  start_kelvin: 2900
  end_kelvin: 6000
  start_rgb_color:
    - 255
    - 137
    - 17
  end_rgb_color:
    - 255
    - 243
    - 225
sequence:
  - service: light.turn_on
    data:
      brightness: 0
      rgb_color: "{{ start_rgb_color }}"
    target:
      entity_id: "{{ rgb_lights }}"
  - service: light.turn_on
    data:
      brightness_pct: 0
    target:
      entity_id: "{{ bi_color_lights }}"
  - repeat:
      count: "{{ step_count }}"
      sequence:
        - service: light.turn_on
          data_template:
            kelvin: >-
              {{ ((end_kelvin - start_kelvin) / (step_count - 1) * repeat.index
              + start_kelvin) | int }}
            brightness_step: "{{ (target_brightness_pct / 100 * 255 / step_count) | round(0) }}"
          target:
            entity_id: "{{ bi_color_lights }}"
        - service: light.turn_on
          data_template:
            brightness: >-
              {{ (target_brightness_pct / 100 * 255 / step_count) * repeat.index
              | round(0) }}
            rgb_color:
              - >-
                {{ (start_rgb_color[0] + (end_rgb_color[0] - start_rgb_color[0])
                / (step_count - 1) * repeat.index) | round(0) }}
              - >-
                {{ (start_rgb_color[1] + (end_rgb_color[1] - start_rgb_color[1])
                / (step_count - 1) * repeat.index) | round(0) }}
              - >-
                {{ (start_rgb_color[2] + (end_rgb_color[2] - start_rgb_color[2])
                / (step_count - 1) * repeat.index) | round(0) }}
          target:
            entity_id: "{{ rgb_lights }}"
        - delay:
            minutes: "{{ offset_minutes | float }}"
mode: single
````

Bi-Color:  
![A001_11280005_C002.gif](A001_11280005_C002.gif)  
RGB lights Panel:  
![Recording 2023-11-27 235638_1_1.gif](Recording%202023-11-27%20235638_1_1.gif)

## Current Limitations

As of now, there is no check in place to verify if the user is at home. Therefore, if you go on a trip, you would need to disable the automation on HA because there are no restrictions preventing it from executing. Please take this into consideration.

## References and Acknowledgments

I'm incredibly grateful to DelusionalAI on Reddit. Thanks to their original shortcut, I no longer have to rely on my Google Home smart speaker for setting the alarm. I used to quietly call out across the room at 3am to adjust my morning alarm but now, I can simply change it on my phone.

[thread: r/homeassistant](https://www.reddit.com/r/homeassistant/comments/17fmyt8/its_now_very_easy_to_get_your_ios_wakeup_alarm/).
