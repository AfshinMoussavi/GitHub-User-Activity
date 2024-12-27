import requests
from datetime import datetime

def fetch_github_activity(username):
    """
    Fetches the activity events of a GitHub user.

    Args:
    username (str): GitHub username to fetch events for.

    Returns:
    list: A list of activity events if the request is successful, None if there is an error.
    """
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            activities = response.json()
            return activities
        elif response.status_code == 404:
            print("Invalid username. Please check the username and try again.")
        else:
            print(f"Error: {response.status_code}. Unable to fetch data.")
    except requests.exceptions.RequestException as e:
        print(f"Network connection error: {e}")
        return None

def filter_activities(activities, event_type=None):
    """
    Filters a list of GitHub activity events by event type.

    Args:
    activities (list): A list of activity events to filter.
    event_type (str, optional): The event type to filter by (e.g., 'PushEvent'). 
                                If None, no filtering is applied.

    Returns:
    list: A list of filtered activity events.
    """
    if event_type:
        return [event for event in activities if event['type'] == event_type]
    return activities

def display_activity(activity):
    """
    Displays the filtered activity events in a colored box format.

    Args:
    activity (list): A list of activity events to display.
    """
    # Define the color for the box and text
    box_color = '\033[1;32m'  # Green box
    reset_color = '\033[0m'  # Reset color
    header_color = '\033[1;34m'  # Blue for header
    event_color = '\033[1;33m'  # Yellow for event type
    
    # Printing the colored box around the output
    print(f"{box_color}{'='*50}{reset_color}")
    print(f"{header_color}GitHub Activity Results:{reset_color}")
    print(f"{box_color}{'='*50}{reset_color}")
    
    # Display the filtered activities
    for event in activity[:5]:
        date_obj = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        created_at = date_obj.strftime("%d/%m/%Y")
        print(f"{event_color}- {event['type']} in {event['repo']['name']}{reset_color}")
        print(f"  created_at: {created_at}")
        print()
    
    print(f"{box_color}{'='*50}{reset_color}")

def main():
    """
    Main function to prompt user for a GitHub username, fetch and filter activity events, 
    and display them in a colored format.
    """
    username = input("Please input the GitHub username: ")
    activities = fetch_github_activity(username)

    if not activities:
        return

    print("\nFetched activities successfully.\n")

    event_type = input("Enter event type to filter by (CreateEvent-MemberEvent-PushEvent-DeleteEvent-WatchEvent)(leave blank for all events): ").strip()
    if event_type:
        activities = filter_activities(activities, event_type)

    if not activities:
        print("No activities found for the specified filter.")
    else:
        display_activity(activities)

if __name__ == "__main__":
    main()
