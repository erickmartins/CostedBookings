from parse_events import calculate_time
import iso8601

def cost_hours(events):

    """
    Calculates how many cost-hours are in each event.

    Applies all the arcane CAMDU rules to figure out how many cost-hours
    a certain booking is. Overnights are 4h, weekends are up to 4h, regular
    hours are just the amount of hours booked. Appends that value to each event.

    Parameters
    ----------
    events : list of lists
        A matrix-like object with details parsed from calendar events.
    
    Returns
    -------
    events : list of lists
        A matrix-like object with details parsed from calendar events.

    """

    for i in range(len(events)):
        event = events[i]
        time_start = iso8601.parse_date(event[2])
        time_end = iso8601.parse_date(event[3])
        hours = 0
        #overnight
        if time_start.day != time_end.day:
            #check that it is mon-thu
            if time_start.weekday() < 4:
                #at least 4h
                hours = min(4.0, calculate_time(event[2],event[3]).total_seconds()/3600.0)
                #calculate time before 18h
                startts = event[2][:10]+"T18:00:00Z"
                extra = max(0.0,calculate_time(event[2],startts).total_seconds()/3600.0)
                hours = hours + extra
                #calculate time after 9h
                endts = event[3][:10]+"T09:00:00Z"
                extra = max(0.0,calculate_time(endts,event[3]).total_seconds()/3600.0)
                hours = hours + extra
            #check for friday start
            elif time_start.weekday() == 4:
                hours = min(4.0, calculate_time(event[2],event[3]).total_seconds()/3600.0)
                #calculate time before 18h
                startts = event[2][:10]+"T18:00:00Z"
                extra = max(0.0,calculate_time(event[2],startts).total_seconds()/3600.0)
                hours = hours + extra
            #check for sunday start
            elif time_start.weekday() == 6:
                hours = 0
                #calculate time after 9h
                endts = event[3][:10]+"T09:00:00Z"
                extra = max(0.0,calculate_time(endts,event[3]).total_seconds()/3600.0)
                hours = hours + extra
        else:
            hours = calculate_time(event[2],event[3]).total_seconds()/3600.0
            if time_end.hour > 21:
                startts = event[2][:10]+"T18:00:00Z"
                extra = max(0.0,calculate_time(event[2],startts).total_seconds()/3600.0)
                hours = 4.0 + extra
            if time_start.hour < 5:
                endts = event[3][:10]+"T09:00:00Z"
                extra = max(0.0,calculate_time(endts,event[3]).total_seconds()/3600.0)
                hours = 4.0 + extra
            if time_start.weekday() > 4:
                hours = 0
        events[i].append(hours)
        events[i].append(time_start.weekday())
    return events