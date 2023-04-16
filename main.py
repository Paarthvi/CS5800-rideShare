from navigation.navigation import Navigator
from position import Position

def main():
    snell         = Position(42.337952, -71.089872, name="snell")
    khoury        = Position(42.33886043446358  , -71.09209490721425, name="khoury")
    boylston      = Position(42.3459752960486   , -71.09445349072972, name="boylston")
    park_drive    = Position(42.34153516743033  , -71.0980578963843, name="park drive")
    marino        = Position(42.33999584960625  , -71.09052869353322, name="marino")
    top_left = Position(42.3627, -71.1201, name="top left point")
    bottom_right = Position(42.3212, -71.0693, name="bottom right point")
    nav = Navigator(top_left, bottom_right)
    returned_path = nav.service_order([khoury, boylston, park_drive, marino], snell)
    nav_list = nav.generate_route(returned_path)
    for i in returned_path:
        nav.set_node_color(nav.get_closest_point(i), 'y')
    nav.plot_path(nav_list)

main()