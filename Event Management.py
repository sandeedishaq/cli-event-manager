import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
FILES = {
    'events': r"C:\Users\Anas Khan\Downloads\events.csv",
    'participants': r"C:\Users\Anas Khan\Downloads\participants.csv",
    'payments': r"C:\Users\Anas Khan\Downloads\payments.csv",
    'venues': r"C:\Users\Anas Khan\Downloads\venues.csv",
    'services': r"C:\Users\Anas Khan\Downloads\event_type.csv",}
def load_data(file_type):
    """Load data from CSV file"""
    try:
        with open(FILES[file_type], mode='r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def save_data(file_type, data):
    """Save data to CSV file"""
    if not data:
        return
    with open(FILES[file_type], mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def show_events():
    """Display all events"""
    events = load_data('events')
    venues = load_data('venues')

    print("\nAll Events:")
    for event in events:
        venue = next((v for v in venues if v['venue_id'] == event['venue_id']), {})
        print(f"\nID: {event['event_id']} | {event['event_name']}")
        print(f"Type: {event['event_type']} | Venue: {venue.get('venue_name', 'Unknown')}")
        print(f"Date: {event['date']} | Time: {event['time']}")
        print(f"Total Price: Rs.{event['total_price']} | Services: {event['categories']}")
def add_event():
    """Add a new event to the system"""
    events = load_data('events')
    venues = load_data('venues')
    services = load_data('services')

    print("\n--- Add New Event ---")

    # Display available venues
    print("\nAvailable Venues:")
    for v in venues:
        print(f"{v['venue_id']} - {v['venue_name']} (Capacity: {v['capacity']}, Rs.{v['daily_rate']}/day)")

    venue_id = input("Enter Venue ID for the event: ")
    venue = next((v for v in venues if v['venue_id'] == venue_id), None)
    if not venue:
        print("Invalid venue ID.")
        return

    # Display event types/services
    print("\nAvailable Event Types:")
    for s in services:
        print(f"- {s['event_type']}")

    event_id = f"E{len(events)+1:03d}"
    event_name = input("Enter Event Name: ")
    event_type = input("Enter Event Type: ")
    date = input("Enter Event Date (MM/DD/YYYY): ")
    time = input("Enter Event Time (e.g., 5:00 PM): ")
    total_price = input("Enter Total Price: ")
    categories = input("Enter Services/Categories (comma-separated): ")

    new_event = {
        'event_id': event_id,
        'event_name': event_name,
        'event_type': event_type,
        'venue_id': venue_id,
        'date': date,
        'time': time,
        'total_price': total_price,
        'categories': categories
    }

    events.append(new_event)
    save_data('events', events)
    print(f"\nEvent '{event_name}' added successfully!")

def register_participant():
    """Register a new participant with capacity check"""
    events = load_data('events')
    participants = load_data('participants')
    venues = load_data('venues')

    show_events()
    event_id = input("\nEnter Event ID to register: ")
    event = next((e for e in events if e['event_id'] == event_id), None)

    if not event:
        print("Event not found!")
        return

    # Check capacity
    venue = next((v for v in venues if v['venue_id'] == event['venue_id']), None)
    if not venue:
        print("Venue not found!")
        return

    current_participants = sum(1 for p in participants if p['event_id'] == event_id)
    if current_participants >= int(venue['capacity']):
        print("Event is full! Cannot register more participants.")
        return

    # Get participant details
    participant_id = f"P{len(participants)+1:03d}"
    name = input("Enter participant name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")

    new_participant = {
        'participant_id': participant_id,
        'event_id': event_id,
        'name': name,
        'email': email,
        'phone': phone,
        'registration_date': datetime.now().strftime("%m/%d/%Y"),
        'payment_status': 'Pending'
    }

    participants.append(new_participant)
    save_data('participants', participants)

    # Create payment record
    payments = load_data('payments')
    payment_id = f"PY{len(payments)+1:03d}"
    new_payment = {
        'payment_id': payment_id,
        'event_id': event_id,
        'participant_id': participant_id,
        'amount': event['total_price'],
        'payment_date': 'Pending',
        'payment_method': 'Pending',
        'categories': event['categories']
    }

    payments.append(new_payment)
    save_data('payments', payments)
    print(f"\nRegistration successful! Payment due: Rs.{event['total_price']}")

def record_payment():
    """Record a payment for a participant"""
    payments = load_data('payments')
    participants = load_data('participants')

    pending_payments = [p for p in payments if p['payment_date'] == 'Pending']
    if not pending_payments:
        print("No pending payments!")
        return

    print("\nPending Payments:")
    for payment in pending_payments:
        participant = next((p for p in participants if p['participant_id'] == payment['participant_id']), {})
        print(f"ID: {payment['payment_id']} | Participant: {participant.get('name', 'Unknown')}")
        print(f"Event: {payment['event_id']} | Amount: Rs.{payment['amount']}")

    payment_id = input("\nEnter Payment ID to complete: ")
    payment = next((p for p in payments if p['payment_id'] == payment_id), None)

    if not payment:
        print("Payment not found!")
        return

    payment['payment_date'] = datetime.now().strftime("%m/%d/%Y")
    payment['payment_method'] = input("Enter payment method (Card/Bank Transfer/Cash): ")

    # Update participant status
    participant = next((p for p in participants if p['participant_id'] == payment['participant_id']), None)
    if participant:
        participant['payment_status'] = 'Paid'

    save_data('payments', payments)
    save_data('participants', participants)
    print("Payment recorded successfully!")

def venue_analysis():
    """Analyze venues by price and capacity"""
    venues = load_data('venues')
    if not venues:
        print("No venue data available!")
        return

    # Sort by daily rate
    venues_sorted = sorted(venues, key=lambda x: int(x['daily_rate']))

    print("\nVenue Analysis:")
    print("\nMost Expensive Venues:")
    for venue in venues_sorted[-3:][::-1]:
        print(f"{venue['venue_name']} - Rs.{venue['daily_rate']}/day")

    print("\nMost Affordable Venues:")
    for venue in venues_sorted[:3]:
        print(f"{venue['venue_name']} - Rs.{venue['daily_rate']}/day")

    # Search by amenity
    amenity = input("\nEnter amenity to search (e.g., WiFi, Stage): ")
    matching = [v for v in venues if amenity.lower() in v['amenities'].lower()]

    if matching:
        print(f"\nVenues with '{amenity}':")
        for venue in matching:
            print(f"{venue['venue_name']} - {venue['location']}")
    else:
        print(f"No venues found with '{amenity}'")

def generate_report():
    """Generate simple reports"""
    events = load_data('events')
    participants = load_data('participants')
    payments = load_data('payments')

    print("\n1. Event Participation")
    print("2. Financial Summary")
    choice = input("Select report type: ")

    if choice == '1':
        print("\nEvent Participation:")
        for event in events:
            count = sum(1 for p in participants if p['event_id'] == event['event_id'])
            print(f"{event['event_name']}: {count} participants")

    elif choice == '2':
        total = sum(int(p['amount']) for p in payments if p['payment_date'] != 'Pending')
        print(f"\nTotal Revenue: Rs.{total}")

        print("\nRevenue by Event Type:")
        event_types = {}
        for event in events:
            amount = sum(int(p['amount']) for p in payments
                        if p['event_id'] == event['event_id'] and p['payment_date'] != 'Pending')
            event_types[event['event_type']] = event_types.get(event['event_type'], 0) + amount

        for etype, revenue in event_types.items():
            print(f"{etype}: Rs.{revenue}")
def visualize_venues():
    """Create visualizations for venue data using pandas and matplotlib"""
    try:
        # Load venue data using pandas
        venues = pd.read_csv(FILES['venues'])

        # Set up the figure
        plt.figure(figsize=(12, 6))

        #Venue Capacity
        plt.subplot(1, 2, 1)
        venues_sorted = venues.sort_values('capacity', ascending=False)
        plt.bar(venues_sorted['venue_name'], venues_sorted['capacity'], color='skyblue')
        plt.title('Venue Capacities')
        plt.xlabel('Venue Name')
        plt.ylabel('Capacity')
        plt.xticks(rotation=45, ha='right')

        # Create subplot 2: Daily Rates
        plt.subplot(1, 2, 2)
        venues_sorted = venues.sort_values('daily_rate', ascending=False)
        plt.bar(venues_sorted['venue_name'], venues_sorted['daily_rate'], color='lightgreen')
        plt.title('Venue Daily Rates')
        plt.xlabel('Venue Name')
        plt.ylabel('Daily Rate (Rs.)')
        plt.xticks(rotation=45, ha='right')

        # Adjust layout and display
        plt.tight_layout()
        plt.show()

        # Create pie chart for amenities analysis
        amenities_count = venues['amenities'].str.get_dummies(',').sum()
        plt.figure(figsize=(8, 8))
        amenities_count.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Amenities Distribution Across Venues')
        plt.ylabel('')
        plt.show()

        # Print some statistics
        print("\nVenue Statistics:")
        print(f"Total venues: {len(venues)}")
        print(f"Average capacity: {venues['capacity'].mean():.0f} people")
        print(f"Average daily rate: Rs.{venues['daily_rate'].mean():.0f}")
        print(f"Most common amenity: {amenities_count.idxmax()}")

    except Exception as e:
        print(f"Error generating visualizations: {e}")

def main_menu():
    """Main menu for the system"""
    while True:
        print("\nEVENT MANAGEMENT SYSTEM")
        print("1. View All Events")
        print("2. Register Participant")
        print("3. Record Payment")
        print("4. Venue Analysis")
        print("5. Generate Report")
        print("6. Venue Visualizations")
        print("7. Add new Event")
        print("8. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            show_events()
        elif choice == '2':
            register_participant()
        elif choice == '3':
            record_payment()
        elif choice == '4':
            venue_analysis()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            visualize_venues()
        elif choice == '7':
            add_event()
        elif choice=='8':
            print("Exiting system. Goodbye!")
        else:
            print("Invalid choice. Please try again.")
main_menu()