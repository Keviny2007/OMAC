from datetime import timedelta, datetime

# Helper function to generate time ranges using datetime for arithmetic
def generate_time_range(start_time, end_time, slot_duration=timedelta(minutes=30)):
    '''
    Input: Start time, end time, duration
    Output: Time slots that are available
    '''

    # Convert start_time and end_time (time objects) to datetime objects for arithmetic
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)

    current_time = start_datetime
    while current_time < end_datetime:
        yield current_time.time()  # Return just the time part
        current_time += slot_duration


# Function to calculate free slots around events
def calculate_free_slots(events, day_start_time, day_end_time):
    # All times in the range from day start to end
    full_day_slots = list(generate_time_range(day_start_time, day_end_time))
    # print(f"Full day slots: {full_day_slots}")  # Debugging output


    # Sort events by start time to process them chronologically
    sorted_events = sorted(events, key=lambda event: event.start_time)
    # for event in sorted_events:
        # print(f"Event start: {event.start_time}, Event end: {event.end_time}")  # Debugging output

    # Remove the times that are occupied by events
    for event in sorted_events:
        event_start = event.start_time.time()
        event_end = event.end_time.time()
        full_day_slots = [slot for slot in full_day_slots if not (event_start <= slot < event_end)]

    # print(f"Free slots after event removal: {full_day_slots}")  # Debugging output
    return full_day_slots
