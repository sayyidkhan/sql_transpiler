import re


def get_curr_date_time_now(display_date=True, display_time=False, display_nanoseconds=False):
    """
    Get the current date/time now.
    :param display_date: if set to True will display date.
    :param display_time: if set to True will display time.
    :param display_nanoseconds: if set to True will include nanoseconds.

    If both display_date and display_time are set to True, it will display both date and time.
    """
    from datetime import datetime

    # Get current time with microseconds
    now = datetime.now()

    # Format date and time without microseconds first
    date_time_now = re.sub(r"\.\d+", "", str(now)).replace(":", "").replace("-", "").replace(" ", "_")

    date_now = date_time_now.split("_")[0]
    time_now = date_time_now.split("_")[1]

    if display_nanoseconds:
        nanoseconds = now.strftime('%f')  # Extract microseconds
        nanoseconds = nanoseconds + '000'  # Convert to nanoseconds (as a string)
        time_now = "".join([time_now, "_", nanoseconds])  # Append nanoseconds to time

    # Display both date and time
    if display_time and display_date:
        return date_time_now if not display_nanoseconds else f"{date_now}_{time_now}"
    elif display_date:
        return date_now
    elif display_time:
        return time_now
    else:
        return None