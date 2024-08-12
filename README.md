# Hashcat Output Monitor

## Overview

The **Hashcat Output Monitor** is a cross-platform Python application designed to monitor changes in a specified Hashcat output file. It provides real-time updates with both notification and alarm sounds to alert users when significant changes occur in the file. The application is built using `tkinter` for the GUI and `pygame` for sound alerts.

## Features

- **File Monitoring**: Continuously monitors a selected file for changes.
- **Sound Alerts**: Plays a notification sound for regular changes and a continuous alarm sound when the file is initially empty and then updated.
- **Log Tracking**: Records detailed logs of changes detected in the file.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Installation

```bash
git clone https://github.com/yourusername/hashcat-output-monitor.git
cd hashcat-output-monitor
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

---

**Created by [D.S](https://wpgsys.ca)**

*Contact: ds@wpgsys.ca*

---


