import pytest

from whitebox.exercises import (
    DocumentEditingSystem,
    ElevatorSystem,
    TrafficLight,
    UserAuthentication,
    VendingMachine,
)


def test_vending_machine_initial_state():
    machine = VendingMachine()

    assert machine.state == "Ready"


def test_vending_machine_insert_coin_success():
    machine = VendingMachine()

    assert machine.insert_coin() == "Coin Inserted. Select your drink."
    assert machine.state == "Dispensing"


def test_vending_machine_insert_coin_invalid_state():
    machine = VendingMachine()
    machine.state = "Dispensing"

    assert machine.insert_coin() == "Invalid operation in current state."
    assert machine.state == "Dispensing"


def test_vending_machine_select_drink_success():
    machine = VendingMachine()
    machine.state = "Dispensing"

    assert machine.select_drink() == "Drink Dispensed. Thank you!"
    assert machine.state == "Ready"


def test_vending_machine_select_drink_invalid_state():
    machine = VendingMachine()

    assert machine.select_drink() == "Invalid operation in current state."
    assert machine.state == "Ready"


def test_traffic_light_initial_state():
    traffic_light = TrafficLight()

    assert traffic_light.get_current_state() == "Red"


def test_traffic_light_state_cycle():
    traffic_light = TrafficLight()

    traffic_light.change_state()
    assert traffic_light.get_current_state() == "Green"

    traffic_light.change_state()
    assert traffic_light.get_current_state() == "Yellow"

    traffic_light.change_state()
    assert traffic_light.get_current_state() == "Red"


def test_user_authentication_initial_state():
    auth = UserAuthentication()

    assert auth.state == "Logged Out"


def test_user_authentication_login_success():
    auth = UserAuthentication()

    assert auth.login() == "Login successful"
    assert auth.state == "Logged In"


def test_user_authentication_login_invalid_state():
    auth = UserAuthentication()
    auth.state = "Logged In"

    assert auth.login() == "Invalid operation in current state"
    assert auth.state == "Logged In"


def test_user_authentication_logout_success():
    auth = UserAuthentication()
    auth.state = "Logged In"

    assert auth.logout() == "Logout successful"
    assert auth.state == "Logged Out"


def test_user_authentication_logout_invalid_state():
    auth = UserAuthentication()

    assert auth.logout() == "Invalid operation in current state"
    assert auth.state == "Logged Out"


def test_document_editing_system_initial_state():
    system = DocumentEditingSystem()

    assert system.state == "Editing"


def test_document_editing_system_save_success():
    system = DocumentEditingSystem()

    assert system.save_document() == "Document saved successfully"
    assert system.state == "Saved"


def test_document_editing_system_save_invalid_state():
    system = DocumentEditingSystem()
    system.state = "Saved"

    assert system.save_document() == "Invalid operation in current state"
    assert system.state == "Saved"


def test_document_editing_system_edit_success():
    system = DocumentEditingSystem()
    system.state = "Saved"

    assert system.edit_document() == "Editing resumed"
    assert system.state == "Editing"


def test_document_editing_system_edit_invalid_state():
    system = DocumentEditingSystem()

    assert system.edit_document() == "Invalid operation in current state"
    assert system.state == "Editing"


def test_elevator_system_initial_state():
    elevator = ElevatorSystem()

    assert elevator.state == "Idle"


def test_elevator_system_move_up_success():
    elevator = ElevatorSystem()

    assert elevator.move_up() == "Elevator moving up"
    assert elevator.state == "Moving Up"


def test_elevator_system_move_down_success():
    elevator = ElevatorSystem()

    assert elevator.move_down() == "Elevator moving down"
    assert elevator.state == "Moving Down"


@pytest.mark.parametrize("state", ["Moving Up", "Moving Down"])
def test_elevator_system_move_up_invalid_state(state):
    elevator = ElevatorSystem()
    elevator.state = state

    assert elevator.move_up() == "Invalid operation in current state"
    assert elevator.state == state


@pytest.mark.parametrize("state", ["Moving Up", "Moving Down"])
def test_elevator_system_move_down_invalid_state(state):
    elevator = ElevatorSystem()
    elevator.state = state

    assert elevator.move_down() == "Invalid operation in current state"
    assert elevator.state == state


@pytest.mark.parametrize("state", ["Moving Up", "Moving Down"])
def test_elevator_system_stop_success(state):
    elevator = ElevatorSystem()
    elevator.state = state

    assert elevator.stop() == "Elevator stopped"
    assert elevator.state == "Idle"


def test_elevator_system_stop_invalid_state():
    elevator = ElevatorSystem()

    assert elevator.stop() == "Invalid operation in current state"
    assert elevator.state == "Idle"
