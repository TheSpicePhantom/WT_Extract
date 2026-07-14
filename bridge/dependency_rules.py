# Abhängigkeitsregeln — maschinenlesbar für spätere Lint-/Import-Checks.
#
# Erlaubte Kanten (source -> target):
#   wt_platform    -> (keine internen Engine-Module)
#   render_core    -> wt_platform
#   render_graphics -> render_core, render_scene
#   render_scene   -> (keine Abhängigkeiten zu render_core, game_core, bridge)
#   bridge         -> render_scene, game_core
#   game_core      -> (keine Abhängigkeiten zu render_*)
#
# Verboten:
#   render_core    -> render_graphics, bridge, game_core
#   render_scene   -> render_core, render_graphics, bridge, game_core
#   game_core      -> render_core, render_graphics, bridge
#   render_*       -> game_core (direkt)

ALLOWED_EDGES: dict[str, frozenset[str]] = {
    "wt_platform": frozenset(),
    "render_core": frozenset({"wt_platform"}),
    "render_graphics": frozenset({"render_core", "render_scene"}),
    "render_scene": frozenset(),
    "bridge": frozenset({"render_scene", "game_core"}),
    "game_core": frozenset(),
}

FORBIDDEN_EDGES: dict[str, frozenset[str]] = {
    "render_core": frozenset({"render_graphics", "bridge", "game_core"}),
    "render_scene": frozenset({"render_core", "render_graphics", "bridge", "game_core"}),
    "game_core": frozenset({"render_core", "render_graphics", "bridge"}),
}

DATA_FLOW = "game_core -> bridge -> render_scene -> render_graphics -> render_core -> wt_platform"
