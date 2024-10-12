from datetime import timedelta, datetime

TOTAL_COURTS = {"OMAC CT1", "OMAC CT2", "OMAC CT3", "OMAC CT4"}

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
    full_day_slots = list(generate_time_range(day_start_time, day_end_time))
    free_slots = []
    for slot in full_day_slots:
        # Default available courts for this time slot
        available_courts = TOTAL_COURTS.copy()

        # Check if any event overlaps with this slot
        for event in events:
            event_start = event.start_time.time()
            event_end = event.end_time.time()
            if event_start <= slot < event_end:
                # Remove the courts occupied by this event from the available list
                occupied_courts = set(event.courts.split(", "))
                # print(occupied_courts)
                available_courts -= occupied_courts
                print(available_courts)

        # If there are any available courts left, include this slot with details of free courts
        if available_courts:
            free_slots.append({
                "time": slot,
                "available_courts": sorted(available_courts)  # Sorting for better display
            })

    return free_slots
