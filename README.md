## YourPhone-MicrosoftLauncher-ForensicTool

YourPhone-MicrosoftLauncher-ForensicTool is Plaso Parser plugin
This tool can analyze digital forensic artifacts of Your Phone and Microsoft Launcher. 

### Your Phone plugin
sqlite/yourphone_calls
sqlite/yourphone_contacts
sqlite/yourphone_devicedata
sqlite/yourphone_message
sqlite/yourphone_notifications
sqlite/yourphone_photos
sqlite/yourphone_settingsdb
winreg/windows_yourphone_settingsdat

### Microsoft Launcher Plugin
sqlite/mslauncher_activitiescache
sqlite/mslauncher_arrowfrequency
sqlite/mslauncher_arrowreminderfolders
sqlite/mslauncher_arrowreminders
sqlite/mslauncher_bingsearchhistory
sqlite/mslauncher_cookies
sqlite/mslauncher_notes
mslauncher_accesstoken
mslauncher_familymemberscachekey

### Usage
log2timeline --parsers ?input parser plugins? ?plaso storage? ?evidence image?
psort -o 4n6time_sqlite --evidence ?evidence name? -w ?Result database? ?plaso storage?
