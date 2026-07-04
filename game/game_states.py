"""
Game State Management
Handles transitions between different game states.
"""

from .locations import ForestLocation, DesertLocation, CityLocation, FlowerfieldLocation, HomelandLocation, CrossroadsLocation

class StateManager:
    """
    Finite state machine for game flow control.

    Args:
        screen: Pygame display surface
    """

    def __init__(self, screen):
        self.screen = screen
        self.current_state = GameState.MAIN_MENU
        self.context = GameContext()
        self._init_states()

    def _init_states(self) -> None:
        """Initialize all state handlers"""
        self.states = {
            GameState.MAIN_MENU: self._main_menu_state,
            GameState.LOCATION_SELECT: self._location_select_state,
            GameState.PLAYING: self._playing_state
        }

        # Main menu configuration
        self.main_menu = MenuSystem(
            "Snake Game",
            [
                MenuItem("Start Game", MenuAction.START_GAME),
                MenuItem("Select Location", MenuAction.CHANGE_LOCATION),
                MenuItem("Settings", MenuAction.OPEN_SETTINGS),
                MenuItem("Quit", MenuAction.QUIT)
            ]
        )

        # Location selection menu
        self.location_menu = MenuSystem(
            "Select Location",
            [
                MenuItem("Forest", MenuAction.START_GAME, {"location": ForestLocation}),
                MenuItem("Desert", MenuAction.START_GAME, {"location": DesertLocation}),
                MenuItem("City", MenuAction.START_GAME, {"location": CityLocation}),
                MenuItem("Flowerfield", MenuAction.START_GAME, {"location": FlowerfieldLocation}),
                MenuItem("Homeland", MenuAction.START_GAME, {"location": HomelandLocation}),
                MenuItem("Crossroads", MenuAction.START_GAME, {"location": CrossroadsLocation}),
                MenuItem("Back", MenuAction.START_GAME)
            ]
        )

    def _main_menu_state(self, event: pygame.event.Event) -> None:
        """Handle main menu state"""
        selected_item = self.main_menu.handle_input(event)
        self.main_menu.draw(self.screen)

        if selected_item:
            if selected_item.action == MenuAction.START_GAME:
                self.current_state = GameState.PLAYING
            elif selected_item.action == MenuAction.CHANGE_LOCATION:
                self.current_state = GameState.LOCATION_SELECT

    def _location_select_state(self, event: pygame.event.Event) -> None:
        """Handle location selection state"""
        selected_item = self.location_menu.handle_input(event)
        self.location_menu.draw(self.screen)

        if selected_item:
            if selected_item.action == MenuAction.START_GAME:
                if selected_item.metadata and "location" in selected_item.metadata:
                    self.context.current_location = selected_item.metadata["location"]
                    self.current_state = GameState.PLAYING
                else:
                    self.current_state = GameState.MAIN_MENU