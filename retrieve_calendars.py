from __future__ import print_function
import datetime







def retrieve_calendars(service):
    """Returns a list of the calendars accessible from the current service.
    """
    

    # Call the Calendar API
    
    calendar_ids = []
    while True:
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            
            calendar_ids.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return calendar_ids
    

